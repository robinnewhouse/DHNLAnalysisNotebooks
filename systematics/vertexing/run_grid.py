import os
import time
import pathlib

data_path = '/data/hnl/KShort/ntuples/data18/'
data_files = [os.path.join(data_path, f) for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]
subdir = '/home/newhouse/tmp/submit_grid/'

for data_path in data_files:
    data_file = pathlib.Path(data_path)
    i = data_file.stem.split('.')[3]
    in_file = str(data_file) 
    out_file = f'/data/hnl/KShort/ntuples/data18_selected/output{i}.pkl'

    command = f"""
#PBS -N dijet_ntuple{i}
#PBS -l walltime=48:00:00
#PBS -l nodes=1:ppn=1
#PBS -e /home/newhouse/tmp/grid_logs/kshort_sel{i}.err
#PBS -o /home/newhouse/tmp/grid_logs/kshort_sel{i}.log

source /home/newhouse/setup/pbs_setup.sh
source  ~/miniconda3/etc/profile.d/conda.sh
conda activate

cd /home/newhouse/public/Analysis/HNL/VertexingEfficiency

python kshort_selection.py {in_file} {out_file}
"""

    subfile = f'{subdir}{i}_submit.pbs'
    with open(subfile, 'w') as f:  
        print(command, file=f)

    print(f"Submitting {subfile}")
    # print(command)
    os.system(f'qsub {subfile}')
    print("Finished")
    time.sleep(0.5)

    max_job_count=250
    def run_count(): return int(os.popen('qstat -r|  wc -l').read().strip())
    def idle_count(): return int(os.popen('qstat -i|  wc -l').read().strip())
    while run_count() + idle_count() > max_job_count:
        time.sleep(10)
