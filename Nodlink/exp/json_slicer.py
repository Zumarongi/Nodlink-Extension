import json
import os
import glob
from argparse import ArgumentParser

def slice(dir_name, file_name):
    print(f'Slicing file "{file_name}" in directory "{dir_name}"...')
    
    fileID = 1
    with open(os.path.join(dir_name, file_name), 'r') as filefrom:
        lineCount = 0
        fileto = open(os.path.join(dir_name, file_name[:-4] + f'{fileID}.json'), 'w')
        for line in filefrom:
            lineCount += 1
            if lineCount >= lengthPerFile:
                lineCount = 0
                fileID += 1
                fileto.close()
                fileto = open(os.path.join(dir_name, file_name[:-4] + f'{fileID}.json'), 'w')
            if (lineCount + 1) % reportPerLines == 0:
                print(f'Line {lineCount + 1} done.')
            data = json.loads(line)
            fileto.write(json.dumps(data) + '\n')
    
    fileto.close()
    
    print(f'File "{file_name}" sliced into {fileID} files.')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('data', type=str, help='The directory of the data.')
    parser.add_argument('-f', '--file', type=str, help='The file to process', default=None)
    parser.add_argument('-l', '--length', type=int, help='The length of each slice', default=1000000)
    parser.add_argument('-r', '--report', type=int, help='The number of lines to report', default=100000)
    args = parser.parse_args()

    lengthPerFile, reportPerLines = args.length, args.report

    fileList = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if args.file is None:
        fileList = glob.glob(os.path.join(script_dir, args.data, '*.json'))
    else:
        fileList.append(os.path.join(script_dir, args.data, args.file))
    
    for file in fileList:
        slice(os.path.dirname(file), os.path.basename(file))

    print('Finished.')