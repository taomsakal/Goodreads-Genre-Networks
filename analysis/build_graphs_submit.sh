#!/bin/bash
#PBS -l nodes=1:ppn=12
#PBS -l walltime=2:00:00
#PBS -V

cd $PBS_O_WORKDIR

./run_all.py