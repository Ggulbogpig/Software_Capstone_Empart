#!/bin/bash

source ~/miniconda3/etc/profile.d/conda.sh
export PATH=$PATH:/home/min/blender-4.5.1-linux-x64

conda activate empart

cd /mnt/d/Software_Capstone/EmpartACD/empart

python -m intrinsic.empart decompose \
office_chair.glb \
10 \
--boxes_csv outputs/auto_regions_office_chair_bbox.csv \
--method vhacd \
> outputs/total_result_office_chair.json



# source ~/miniconda3/etc/profile.d/conda.sh
# export PATH=$PATH:/home/min/blender-4.5.1-linux-x64

# conda activate empart

# cd /mnt/d/Software_Capstone/EmpartACD/empart

# python -m intrinsic.empart decompose \
# knife5.glb \
# 408 \
# --boxes_csv outputs/auto_regions_knife5_bbox_grasp.csv \
# --method vhacd \
# > outputs/total_result_knife5.json