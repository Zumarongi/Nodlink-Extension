#!/bin/bash

set -x

datasets=("streamspot" "wget" "cadets" "theia" "trace")

for dataset in "${datasets[@]}"; do
    mkdir -p "./exp_res/quick/$dataset"
    python eval.py --dataset "$dataset" | tee "./exp_res/quick/$dataset/output.txt"
done

set +x
