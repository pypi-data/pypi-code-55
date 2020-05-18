#!/bin/usr/env python

from adpred import ADpred
import sys

HELP = '''
        list of arguments
        -----------------

        -h  | --help 
        -id | --uniprot-id 
        -s  | --sequence 
        -l  | --local-psipred <path_to_"run_psipred">
        -sm | --saturated-mutagenesis (list of start positions separated by comma. Ends are starts+30)
        -o  | --output-prefix (if empty will use protein.id. if prot_id not provided it will be empty)
'''

# help is printed by default
if len(sys.argv)==1 or sys.argv[1] in ["-h","--help"] :
    print(HELP)
    exit(1)

# defaults
start = []
seq_or_id = None
out_prefix = None

# user set parameters
for n,arg in enumerate(sys.argv):
    if arg in ["-ID","-id","--uniprot-id","uniprot-ID"]:
        seq_or_id = sys.argv[n+1]

    elif arg in ["-s","seq","-Seq","--sequence","--Sequence"]:
        seq_or_id = sys.argv[n+1]

    elif arg in ["-l", "--local-psipred"]:
        local_psipred = sys.argv[n+1]

    elif arg in ["-sm", '--saturated-mutagenesis']:
        start = [int(i) for i in sys.argv[n+1].split(",")]
    
    elif arg in ["-o","--output-prefix"]:
        out_prefix = sys.argv[n+1]

# main
if __name__ == '__main__':

    # open file to output results
    if out_prefix==None:
        out_prefix = seq_or_id if len(seq_or_id)<=10 else ''
    
    # open output files
    predictions_f = open(out_prefix + '.predictions.csv','w')
    
    if len(start)>0:
        saturated_f = open(out_prefix + '.saturated_mutagenesis.csv','w') 

    # iniitialize protein 
    p = ADpred.protein(seq_or_id)
    sys.stderr.write('retrieving sequence...')

    # predict adpred probabilities
    p.predict()
    sys.stderr.write('calculating secondary structure and adpred...')
    
    predictions_f.write(','.join(list(p.predictions.astype(str))))
    
    # compute saturated mutagenesis
    if len(start)>0:
        for i in start:
            p.saturated_mutagenesis(i)

            string = [','.join(list(k.astype(str))) for k in p.heatmaps[i]]
            saturated_f.write('>' + str(i) + '\n' + '\n'.join(string) + '\n')
                
    # close written files
    predictions_f.close()

    try:
        saturated_f.close()
    except Exception:
        pass

