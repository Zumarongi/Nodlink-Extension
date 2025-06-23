import numpy as np
import pickle as pkl
import utils

def load_pkl_file(file_path):
    with open(file_path, 'rb') as f:
        data = pkl.load(f)
    return data

if __name__ == '__main__':
    file_path = 'data/streamspot/graphs.pkl'
    data = load_pkl_file(file_path)
    print(data.keys())
