#!/bin/bash
#SBATCH -N 2
#SBATCH -c 4
#SBATCH -t 02:00:00

NODES=2
CPUS=4
MODE="ray"

#3.59376

module purge --force

module load release/2026
module load GCCcore/14.2.0
module load GCC/14.2.0
module load Python/3.13.1
module load OpenMPI/5.0.7
#module load mpi4py/4.1.0

# VENV
VENV="$(ws_allocate python_virtual_environment 1)"
python3 -m venv --system-site-package "${VENV}"
source "${VENV}"/bin/activate

# ALL
#pip install --no-binary :all: --compile mpi4py
pip install --force-reinstall -v "mpi4py==4.1.0"
pip install --force-reinstall -v "unidist[mpi]==0.7.2"
pip install "modin[all]"
export MODIN_CPUS=${CPUS}




if [ "$MODE" = "ray" ]; 
then
	export MODIN_ENGINE=ray
	export RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
fi

if [ "$MODE" = "dask" ]; 
then
	# code needs to be in __main__
	export MODIN_ENGINE=dask
fi

if [ "$MODE" = "mpi" ]; 
then
	export MODIN_ENGINE=unidist
	export UNIDIST_BACKEND=mpi
	#export OMPI_MCA_rmaps_default_mapping_policy=:oversubscribe
	export UNIDIST_CPUS=${CPUS+1}
	export UNIDIST_MPI_HOSTS=i7017,i7015
	#export MODIN_NPARTITIONS=${NODES}
	export UNIDIST_MPI_SPAWN=False
	#export MPI4PY_BUILD_MPICC=$(eval mpicc -show)
fi


####
pip install asv
#pip install numpy
#pip install pandas
#pip install odfpy
pip install matplotlib
pip install scipy



srun -N ${NODES} -c ${CPUS} asv machine --yes
srun -N ${NODES} -c ${CPUS} asv run -e -E existing
asv publish
#asv preview

#srun -N ${NODES} -c ${CPUS} python -u test.py
#srun --nodelist i[7014-7015] -c ${CPUS} python -u test.py




deactivate
