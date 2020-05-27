'''
Usage:
    gut validate [options] <samplesfn> <fileinfofn>
    gut build [options] <samplesfn> <fileinfofn>
    gut upload [options] [-u URL] <outdir> <user> <pass> <geodir>

Options:
    -h, --help             the help
    -o DIR --outdir=DIR    directory to stage all files into [default: geo_submission]
    --addnl=FN             CSV file with additional section fields, see documentation
    --no-cache             do not use cached results from previous runs
    --copy                 copy files into staging directory instead of creating
                           symbolic links
    -r --ref-fa=FA         for paired end sequencing experiments, a path to a
                           fasta file to be used as reference when estimating
                           average insert size
    -u URL --url=URL       URL of NCBI's FTP server [default: ftp-private.ncbi.nlm.nih.gov]
    --cluster=ARG          Cluster command (e.g. qsub), passed to snakemake to
                           enable parallelism
    --jobs=N               Maximum number of concurrent jobs when submitting
                           with snakemake [default: 1]
    --cores=N              Tell snakemake to use N cores [default: 1]
    -v --verbose           verbose output
    -q --quiet             quiet output (overridden by --verbose)
'''

from collections import OrderedDict, defaultdict
import csv
from docopt import docopt
import hashlib
import ftplib
import logging
import os
import pandas
from pathlib import Path
from pprint import pformat, pprint
import shutil
from pkg_resources import resource_filename, resource_listdir
from snakemake import snakemake
from subprocess import Popen, PIPE
import sys

FILETYPES = (
    'solid_native_csfasta',
    'solid_native_qual',
    'Illumina_native_qseq',
    'fastq',
    '454_native_seq',
    '454_native_qual',
    'srf',
    'Helicos_native',
    'PacBio_HDF5'
)

REQUIRED_COLS = {
    'sample_info': ('Sample name','source name','organism','molecule'),
    'file_info': ('Sample name','rectype','file type','instrument model','path'),
}

RAW_RECTYPES = ('SE fastq','PE fastq')
RECTYPES = {_:'raw' for _ in RAW_RECTYPES}

#PROCESSED_RECTYPES = ('csv','txt')
#RECTYPES.update({_:'processed' for _ in PROCESSED_RECTYPES})

snakefile = resource_filename('geo_upload_tool','gut.snake')

def log_raise(msg) :
    logging.error(msg)
    raise ValidationError(msg)

# https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

def sanitize(s) :
    bad_chrs = '.-'
    tr = str.maketrans(bad_chrs,'_'*len(bad_chrs))
    return s.translate(tr)

class ValidationError(Exception) : pass

class GEODataset(object) :
    def __init__(self,
            outdir,
            sample_info,
            file_info,
            other_sections=None,
            use_cache=True,
            ref_fa=None,
            copy_on_stage=False,
            snakemake_opts={}
            ) :

        self.outdir = Path(outdir)
        self.outdir.mkdir(parents=True, exist_ok=True)

        self.cache_dir = self.outdir.joinpath('.cache')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.use_cache = use_cache

        self.sample_info = sample_info
        self.file_info = file_info
        self.other_sections = other_sections if other_sections is not None else {}

        # this is used for calculating inner mate distance on paired end reads
        self.ref_fa = ref_fa

        self.copy_on_stage = copy_on_stage

        # these are the defaults
        self.snakemake_opts = dict(
                printshellcmds=False,
                forceall=not self.use_cache,
                quiet=True,
                show_failed_logs=True,
                nocolor=True,
                keep_logger=True
        )

        self.snakemake_opts.update(snakemake_opts)

        self.metadata_csv = self.outdir.joinpath('metadata_TOFILL.csv')
        self.metadata_xlsx = self.outdir.joinpath('metadata_TOFILL.xlsx')

        # only generate file name if it doesn't already exist
        if 'file name' not in file_info.columns :
            file_info['file name'] = file_info.path.map(lambda p: os.path.split(p)[-1])

        self.validate()

    def get_staged_path(self,path) :
        path = Path(path).resolve()
        staged_path = Path(os.path.join(self.outdir,path.name))
        logging.debug('staged path: {}'.format(staged_path))
        return staged_path

    def stage_file(self,path,symlink=True) :

        path = Path(path).resolve()
        staged_path = self.get_staged_path(path)

        if self.copy_on_stage :
            logging.info('copying path: {} -> {}'.format(path,staged_path))
            shutil.copyfile(path, staged_path)
        else :
            logging.info('symlinking path: {} -> {}'.format(path,staged_path))
            if not staged_path.exists() :
                staged_path.symlink_to(path)
            else : # file already exists, make sure it points to the right file
                if not staged_path.samefile(path) :
                    log_raise(('Tried to create symlink to {}, but a file with '
                        'that name already exists and does not point to it. '
                        'Check that you don\'t have duplicated file names in '
                        'your file info.').format(staged_path))

    def md5(self,path) :
        staged_path = self.get_staged_path(path)
        md5_path = self.cache_dir.joinpath(staged_path.with_suffix('.md5').name)
        logging.info('using md5 checksum path: {}'.format(md5_path))

        checksum = None
        if self.use_cache and md5_path.exists() :
            with open(md5_path,'rt') as f :
                checksum = f.read().strip()
        else :
            hash_md5 = hashlib.md5()
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_md5.update(chunk)
            checksum = hash_md5.hexdigest()
            with open(md5_path,'wt') as f :
                f.write(checksum)
        return checksum

    @property
    def processed_files(self) :
        return self.file_info[~self.file_info.rectype.isin(RAW_RECTYPES)]

    @property
    def raw_files(self) :
        return self.file_info[self.file_info.rectype.isin(RAW_RECTYPES)]

    def validate_sample_info(self) :

        # user must supply at least some required cols
        missing = [_ for _ in REQUIRED_COLS['sample_info'] if _ not in self.sample_info.columns]
        if len(missing) > 0 :
            log_raise('Missing required sample info columns: {}'.format(missing))

        # can't have blank Sample name
        if (self.sample_info['Sample name']=='').any() :
            log_raise('Cannot have empty sample names in sample info')

        # can't have any duplicated Sample name rows in sample info
        duplicated = self.sample_info['Sample name'].duplicated(keep=False)
        if duplicated.any() :
            log_raise('Duplicated sample names in sample info: {}'.format(
                pformat(self.sample_info['duplicated'])
            ))

    def validate_file_info(self) :

        missing = [_ for _ in REQUIRED_COLS['file_info'] if _ not in self.file_info.columns]
        if len(missing) > 0 :
            log_raise('Missing required file info columns: {}'.format(missing))

        # user must supply at least some required cols
        if (self.file_info['Sample name']=='').any() :
            log_raise('Cannot have empty sample names file info')

        # make sure if there are any PE fastq records that both ends are included
        pe_recs = self.file_info[self.file_info.rectype == 'PE fastq']

        for name, recs in pe_recs.groupby('Sample name') :
            if recs.shape[0] != 2 :
                log_raise('Must be exactly two PE fastq file info records for sample {}'.format(name))

            if set(recs.end.apply(int)) != {1,2} :
                log_raise('There must be a PE fastq file info record for both end 1 and 2 for sample {}'.format(name))

        # make sure there is both raw and processed data for every sample
        for name, recs in self.file_info.groupby('Sample name') :
            missing_raw = not recs.rectype.isin(RAW_RECTYPES).any()
            missing_processed = not (~recs.rectype.isin(RAW_RECTYPES)).any()
            if missing_raw or missing_processed :
                log_raise('Must have both raw and processed file info records for sample {}'.format(name))

        # make sure all of the file types are valid
        invalid_filetypes = set(self.raw_files['file type']).difference(set(FILETYPES))
        if len(invalid_filetypes) > 0 :
            log_raise('Found invalid file type(s) in file info: {}, expected: {}'.format(invalid_filetypes, FILETYPES))

        # raw files must have instrument model defined
        if (self.raw_files['instrument model'].fillna('') == '').any() :
            log_raise('All raw files must have an instrument model specified')

        # the same processed file may be specified multiple times for different
        # samples, but the rest of the fields should have the same values
        processed = self.processed_files[['file name','file type','path']]
        processed = processed[~processed.duplicated()]
        if processed['file name'].duplicated().any() :
            log_raise('A processed file shared by more than one sample must '
                    'have identical file name and file type in every entry, '
                    'duplicated: {}'.format(
                        processed[processed['file name'].duplicated()]
                        )
                    )

    def validate(self) :

        self.validate_sample_info()
        self.validate_file_info()

        # make sure there is at least one file for each sample
        sample_info_names = set(self.sample_info['Sample name'])
        file_info_names = set(self.file_info['Sample name'])

        missing_file_info = sample_info_names.difference(file_info_names)
        if len(missing_file_info) != 0 :
            log_raise('Missing file info for sample names: {}'.format(
                missing_file_info
            ))

        missing_sample_info = file_info_names.difference(sample_info_names)
        if len(missing_sample_info) != 0 :
            log_raise('Missing sample info for sample names: {}'.format(
                missing_sample_info
            ))

    def _format_field_section(self,df,required) :

        if df is None :
            out = pandas.DataFrame([{'field':_,'value':''} for _ in required])
        else :
            missing_fields = set(required).difference(set(df.field))
            if len(missing_fields) != 0 :
                logging.warning('Provided section is missing required '
                    'fields: {}'.format(missing_fields)
                )
            addnl_fields = [_ for _ in df.field if _ not in required]

            out = []
            for field in required+addnl_fields :
                out.extend(df[df.field == field].values.tolist())

            out = pandas.DataFrame(out,columns=df.columns)
        return out

    @property
    def series_section(self) :
        logging.info('Processing SERIES section')
        return self._format_field_section(
            self.other_sections.get('SERIES'),
            ['title','summary','overall design','contributor']
        )

    @property
    def samples_section(self) :

        # collect info from the sample and file info to construct sample section
        base = ['Sample name', 'title', 'source name', 'organism']
        mol_desc = ['molecule','description']

        characteristics = [_ for _ in self.sample_info.columns if _ not in REQUIRED_COLS['sample_info']]

        max_processed_files = self.processed_files.groupby('Sample name').count().max().max()
        max_raw_files = self.raw_files.groupby('Sample name').count().max().max()

        recs = []
        for i, sample in self.sample_info.iterrows() :

            rec = sample.reindex(base+characteristics+['molecule']).tolist()
            rec += [sample.get('description','')]

            # identify processed files for this sample
            sample_processed = self.processed_files[self.processed_files['Sample name'] == sample['Sample name']]['file name']
            rec += sample_processed.tolist() + ['']*(max_processed_files - sample_processed.size)

            # identify raw files for this sample
            sample_raw = self.raw_files[self.raw_files['Sample name'] == sample['Sample name']]['file name']
            rec += sample_raw.tolist() + ['']*(max_raw_files - sample_raw.size)

            recs.append(rec)

        sample_cols = base + \
            ['characteristics: {}'.format(_) for _ in characteristics] + \
            mol_desc + \
            ['processed data file']*max_processed_files + \
            ['raw data file']*max_raw_files

        out = pandas.DataFrame(recs, columns=sample_cols)
        out.fillna('',inplace=True)
        for i, rec in out.iterrows() :
            if rec['title'] == '' :
                out.loc[i,'title'] = rec['Sample name']

        return out

    @property
    def protocols_section(self):
        logging.info('Processing PROTOCOLS section')
        return self._format_field_section(
            self.other_sections.get('PROTOCOLS'),
            ['growth protocol','treatment protocol','extract protocol',
             'library construction protocol','library strategy']
        )

    @property
    def data_processing_section(self):
        logging.info('Processing DATA PROCESSING PIPELINE section')
        return self._format_field_section(
            self.other_sections.get('DATA PROCESSING PIPELINE'),
            ['data processing step','genome build',
             'processed data files format and content']
        )

    @property
    def processed_files_section(self) :
        out = self.processed_files[['file name','file type','path']].copy()

        # should create only one record per file
        out = out[~out.duplicated()]

        #out['file checksum'] = self.processed_files['path'].apply(lambda fn: self.md5(fn))
        md5_files = OrderedDict()
        config = {}
        for i,rec in out.iterrows() :

            path = Path(rec.path).resolve()
            config[sanitize(path.name)] = str(path)

            md5_path = self.cache_dir.joinpath(Path(str(path)+'.md5').name).resolve()

            md5_files[i] = str(md5_path)

        if len(md5_files) > 0 :
            snake_success = snakemake(
                snakefile,
                allowed_rules=['md5sum'],
                config=config,
                targets=md5_files.values(),
                **self.snakemake_opts
            )

            if not snake_success :
                logging.warning('snakemake failed to complete pipeline '
                    'calculating md5 checksum. Output will be blank.'
                )
            else :
                for i, md5fn in md5_files.items() :
                    with open(md5fn,'rt') as f :
                        md5,rest = f.read().strip().split()
                        logging.info('File {} md5 checksum: {}'.format(
                            out.loc[i,'file name'],md5)
                        )
                        out.loc[i,'file checksum'] = md5

        return out.drop(columns=['path'])

    @property
    def raw_files_section(self) :

        out = self.raw_files[['file name','file type','instrument model','path']].copy()
        out['file checksum'] = '' # fill in later self.raw_files['path'].apply(lambda fn: self.md5(fn))
        out['single or paired-end'] = self.raw_files.rectype.apply(
                lambda t: 'paired-end' if t == 'PE fastq' else 'single'
        )

        config = {}
        md5_files = {}
        rlen_files = {}
        for i, rec in out.iterrows() :
            if rec['file type'] == 'fastq' :

                path = Path(rec.path).resolve()
                config[sanitize(path.name)] = str(path)

                md5_path = self.cache_dir.joinpath(Path(str(path)+'.md5').name).resolve()
                md5_files[i] = str(md5_path)

                rlen_path = self.cache_dir.joinpath(Path(str(path)+'.rlen').name).resolve()
                rlen_files[i] = str(rlen_path)

        if len(md5_files) > 0 :
            targets = list(md5_files.values())+list(rlen_files.values())
            snake_success = snakemake(
                snakefile,
                allowed_rules=['md5sum','readlen'],
                config=config,
                targets=targets,
                **self.snakemake_opts
            )

            if not snake_success :
                logging.warning('snakemake failed to complete pipeline '
                    'calculating md5 checksum. Output will be blank.'
                )
            else :
                for i, md5fn in md5_files.items() :
                    with open(md5fn,'rt') as f :
                        md5,rest = f.read().strip().split()
                        logging.info('File {} md5 checksum: {}'.format(
                            out.loc[i,'file name'],md5)
                        )
                        out.loc[i,'file checksum'] = md5
                    with open(rlen_files[i],'rt') as f :
                        rlen = f.read().strip()
                        logging.info('File {} read length: {}'.format(
                            out.loc[i,'file name'],rlen)
                        )
                        out.loc[i,'read length'] = rlen

        return out

    @property
    def paired_end_section(self) :

        pe_reads = self.raw_files[self.raw_files.rectype=='PE fastq']

        out = pandas.DataFrame(
            columns=['file name 1',
                'file name 2',
                'average insert size',
                'standard deviation'
            ],
            index=range(int(pe_reads.shape[0]/2))
        )

        if pe_reads.size > 0 :

            # construct the snakemake targets and config
            imd_files = OrderedDict()
            config = {'outdir': str(self.outdir) }
            for i, (sample, recs) in enumerate(pe_reads.groupby('Sample name')) :

                read1 = recs[recs.end==1]
                assert read1.shape[0] == 1
                read1 = read1.iloc[0]

                read2 = recs[recs.end==2]
                assert read2.shape[0] == 1
                read2 = read2.iloc[0]

                out.loc[i,'file name 1'] = read1['file name']
                out.loc[i,'file name 2'] = read2['file name']

                ref_fa = read1.get('ref_fa',read2.get('ref_fa',self.ref_fa))

                if ref_fa is None :
                    logging.warning(
                     'There are paired end fastq files but no reference fasta was '
                     'provided, not computing inner mate distance or standard '
                     'deviation. Be sure to compute these manually prior to '
                     'submission, or rerun with a fasta formatted sequence file '
                     'appropriate for your sample.'
                    )
                    continue

                imdfn = '{}_Aligned.out.bam_imdstats.csv'.format(sample)
                imd_files[sample] = str(self.cache_dir.joinpath(imdfn))

                # fasta file could end in .fa or .fasta, optionally with .gz
                # at the end
                ref_fa = Path(ref_fa).resolve()
                ref_star = str(ref_fa.name)+'__star'
                ref_star = self.cache_dir.joinpath(ref_star)

                config[sanitize(ref_fa.name)] = str(ref_fa)

                config.update({
                    sanitize(sample+'_read1'): read1.path,
                    sanitize(sample+'_read2'): read2.path,
                    sanitize(sample+'_index'): str(ref_star)
                })

            if len(imd_files) > 0 :
                snake_success = snakemake(
                    snakefile,
                    allowed_rules=['star_index','star','inner_mate'],
                    config=config,
                    targets=imd_files.values(),
                    **self.snakemake_opts
                )

                if not snake_success :
                    logging.warning('snakemake failed to complete pipeline '
                        'calculating inner mate distance. Output will be blank.'
                    )
                else :
                    for i, (sample, imdfn) in enumerate(imd_files.items()) :
                        with open(imdfn,'rt') as f :
                            n, mean, median, std = stats = f.read().strip().split(',')
                            logging.info((
                                'Sample {} inner mate distance stats: '
                                'num_reads={}, median={}, mean={}, std={}'
                                ).format(sample,*stats))
                            out.loc[i,'average insert size'] = float(mean)
                            out.loc[i,'standard deviation'] = float(std)

            return out.fillna('')

    def process(self) :

        # first stage all the files
        for path in self.file_info['path'] :
            self.stage_file(path)

        # load the template, only have sequencing template right now
        #template_fn = resource_filename('geo_upload_tool','templates/seq_template_v2.1.csv')

        metadata = []
        def add_section(name,info,colnames=True) :
            metadata.append([name])
            if colnames :
                metadata.append(info.columns.tolist())
            metadata.extend(info.values.tolist())
            metadata.append([])

        add_section('SERIES',self.series_section,colnames=False)
        add_section('SAMPLES',self.samples_section,colnames=True)
        add_section('PROTOCOLS',self.protocols_section,colnames=False)
        add_section('DATA PROCESSING PIPELINE',self.data_processing_section,colnames=False)
        add_section('PROCESSED DATA FILES',self.processed_files_section,colnames=True)
        add_section('RAW FILES',self.raw_files_section,colnames=True)
        add_section('PAIRED-END EXPERIMENTS',self.paired_end_section,colnames=True)

        metadata = pandas.DataFrame(metadata)
        metadata.to_csv(self.metadata_csv,index=False,header=False)
        metadata.to_excel(self.metadata_xlsx,index=False,header=False)

        return metadata

def main(argv=None) :

    opts = docopt(__doc__,argv=argv)

    log_level = logging.INFO
    if opts['--verbose'] :
        log_level = logging.DEBUG
    elif opts['--quiet'] :
        log_level = logging.WARN
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    )

    if opts['validate'] or opts['build'] :
        sample_info = pandas.read_csv(
                opts['<samplesfn>'],
                engine='python',
                sep=None
        )

        file_info = pandas.read_csv(
                opts['<fileinfofn>'],
                engine='python',
                sep=None
        )

        # load in additional sections if supplied
        other_sections = None
        other_section_names = ('SERIES','PROTOCOLS','DATA PROCESSING PIPELINE')
        if opts['--addnl'] :
            other_sections = defaultdict(list)
            with open(opts['--addnl'],'rt',encoding='ISO-8859-1') as f :
                curr_section = None
                for i,r in enumerate(csv.reader(f)) :
                    if len(r) > 2 :
                        logging.warning('Encountered other section row with more '
                                'than 2 columns, skipping: {}'.format(r))
                    elif len(r) == 0 or len(r[0].strip()) == 0 :
                        pass # blank line
                    elif r[0].strip() in other_section_names :
                        curr_section = r[0].strip()
                    elif curr_section is not None :
                        other_sections[curr_section].append([_.strip() for _ in r])
                    else :
                        logging.info('Skipping additional section row {}: {}'.format(i+1,r))

            other_sections = {
                k:pandas.DataFrame(v,columns=('field','value')).fillna('')
                for k,v in other_sections.items()
            }

        log_f = {
            'debug': logging.debug,
            'error': logging.error,
            'info': logging.info,
            'progress': None,
            'job_info': logging.debug
        }
        def snakemake_log(log) :
            l = log_f.get(log.get('level'))
            if l is not None :
                l(log.get('msg','no merserge?!'))

        d = GEODataset(
                opts['--outdir'],
                sample_info,
                file_info,
                other_sections=other_sections,
                use_cache=not opts['--no-cache'],
                ref_fa=opts['--ref-fa'],
                copy_on_stage=opts['--copy'],
                snakemake_opts={
                    'cluster': opts['--cluster'],
                    'cores': int(opts['--cores']),
                    'nodes': int(opts['--jobs']),
                    'log_handler': snakemake_log
                }
        )

        if opts['build'] :

            d.process()

    elif opts['upload'] :

        with ftplib.FTP(opts['--url']) as ftp :

            logging.info('connected to ftp server {}'.format(opts['--url']))

            try :
                ftp.login(opts['<user>'],opts['<pass>'])
            except ftplib.error_reply :
                logging.error('error loggin in, check your username and password')
                sys.exit(1)
            logging.info('successfully logged in')

            try :
                ftp.cwd(opts['<geodir>'])
            except ftplib.error_reply :
                logging.error('could not navigate to your GEO directory, check for typos')
                sys.exit(2)
            logging.info('successfully changed to upload directory')

            try :
                ftp.mlsd(opts['<outdir>'])
            except ftplib.error_perm as err :
                if 'No such file' in err.args[0] :
                    try :
                        ftp.mkd(opts['<outdir>'])
                    except ftplib.error_reply :
                        logging.error('could not create or navigate to submission directory')
                        sys.exit(3)
                    logging.info('successfully created submission directory')
                else : # some other error occurred, bail
                    raise err
            else :
                logging.info('upload directory already exists')

            ftp.cwd(opts['<outdir>'])

            outdir = Path(opts['<outdir>'])
            to_upload = os.listdir(opts['<outdir>'])
            to_upload.remove('.cache')
            to_upload = [outdir.joinpath(_) for _ in to_upload if 'TOFILL' not in _]
            logging.info('{} files to upload'.format(len(to_upload)))

            logging.info('beginning upload')

            # ftp uploads text and binary files differently, check each file
            for path in to_upload :

                logging.info('uploading {}'.format(path))

                # check if file is already there
                file_size = None
                if opts['--no-cache'] :
                    logging.info('--no-cache provided, skipping file size checks and forcing upload')
                else :
                    try :
                        ftp.sendcmd('TYPE I') # need this to get file sizes
                        file_size = ftp.size(str(path.name))
                    except ftplib.error_perm as err :
                        if 'No such file' in err.args[0] :
                            pass # file doesn't exist, it's fine
                        else : # some other error occurred, bail
                            raise err

                # check to see if file size is the same, if so skip
                if file_size :
                    local_size = path.stat().st_size

                    logging.info(
                        'remote file {} found with size {}, local size {}'.format(
                            path,file_size,local_size
                        )
                    )

                    if file_size == local_size :
                        logging.info('file sizes match, skipping upload')
                        continue
                    else :
                        logging.info('file sizes mismatch, deleting remote and reuploading')
                        ftp.delete(str(path.name))

                is_binary = False
                with open(path,'rb') as f :
                    is_binary = is_binary_string(f.read(1024))

                if is_binary :
                    with open(path,'rb') as f :
                        ftp.storbinary('STOR {}'.format(path.name),f, 1024)
                else :
                    with open(path,'rb') as f :
                        ftp.storlines('STOR {}'.format(path.name),f)

                logging.info('uploaded {}'.format(path))

            logging.info('done uploading')

if __name__ == '__main__' :
    main()
