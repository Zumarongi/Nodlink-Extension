#!/bin/bash

set -x

datasets=("cadets" "theia" "trace")

for dataset in "${datasets[@]}"; do
    mkdir -p "./exp_res/standard/$dataset"
    python eval.py --dataset "$dataset" | tee "./exp_res/standard/$dataset/output.txt"
done

set +x
