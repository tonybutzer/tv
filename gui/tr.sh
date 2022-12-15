#! /bin/bash

# /data/miniconda3/envs/tv/bin/python

source /data/miniconda3/etc/profile.d/conda.sh \
	&& conda activate tv \
	&& conda env list \
	&& (cd /home/tony/opt/tv/gui; python3 titan_record.py $1)
