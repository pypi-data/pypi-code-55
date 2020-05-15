__version__ = '0.0.3'
import os
import re

version_pattern = re.compile(r'\d+$')
def update_run(run_file):
    '''run file is like src/scripts/run-vm.sh
       return bumped quay url
    '''
    with open(run_file) as f, open(run_file + '.tmp', 'w') as fout:
        for line in f:
            if 'quay' in line:
                version, *rest = line.strip().split(':')[1].split()
                # gcp-wtf2-snap23
                # match number at end
                print(version.strip())
                match = list( version_pattern.finditer(version) )[0]
                print(match)
                version_bump = int(version[match.start():match.end()])+1
                new_line = line.split(':')[0] + ':' + version[0:match.start()] + str(version_bump) + ' ' + ' '.join(rest)
                print(new_line, file=fout)
                for _ in new_line.strip().split():
                    if 'quay' in _:
                        quay_url = _
            else:
                print(line.strip(), file=fout)
    os.system(f'mv {run_file}.tmp {run_file}')
    return quay_url


def update_image(quay_url, dockerfile):
    '''dockerfile is like src/containers/Dockerfile_gcp
       quay_url is like quay.research.chop.edu/evansj/warehouse-var-table:gcp-wtf2-snap23
    '''
    cmd = f'docker build -t {quay_url} -f {dockerfile} .; docker push {quay_url}'
    print(cmd)
    os.system(cmd)

def run():
    with open('configs/.bump') as f:
        for line in f:
            run, dockerfile = line.strip().split()
            quay_img = update_run(run)
            update_image(quay_img, dockerfile)



