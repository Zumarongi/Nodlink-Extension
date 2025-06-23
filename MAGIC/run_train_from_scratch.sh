#!/bin/bash

set -x

datasets=("streamspot" "wget" "cadets" "theia" "trace")

for dataset in "${datasets[@]}"; do
    mkdir -p "./exp_res/train-from-scratch/$dataset"
    python train.py --dataset "$dataset" | tee "./exp_res/train-from-scratch/$dataset/train.out"
    python eval.py --dataset "$dataset" | tee "./exp_res/train-from-scratch/$dataset/eval.out"
done

set +x
