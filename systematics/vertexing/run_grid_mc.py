import os
import time
import pathlib

### Small snippet for merging multiple output MC files
# import glob
# df = pd.concat([pd.read_pickle(path) for path in glob.glob('/data/hnl/KShort/ntuples/dijet_mc16e/JZ?_selected/*.pkl')])
# df.to_pickle('/data/hnl/KShort/ntuples/dijet_mc16e/JZ?/output.pkl')


jz_slice = 'JZ4'
mc_path = f'/data/hnl/KShort/ntuples/dijet_mc16e/{jz_slice}'
mc_files = [os.path.join(mc_path, f) for f in os.listdir(mc_path) if os.path.isfile(os.path.join(mc_path, f))]
subdir = '/home/newhouse/tmp/submit_grid/'

for mc_path in mc_files:
    mc_file = pathlib.Path(mc_path)
    i = mc_file.stem.split('.')[3]
    in_file = str(mc_file) 
    out_file = f'/data/hnl/KShort/ntuples/dijet_mc16e/{jz_slice}_selected/output{i}.pkl'
    os.makedirs(pathlib.Path(out_file).parent, exist_ok=True)

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
