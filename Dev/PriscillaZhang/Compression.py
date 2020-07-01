import pandas as pd
import numpy as np
import sys
import time
import os
import pickle
import csv
import zipfile
import zlib
import newFunction as newfunc
import Constants as constants
import directories as directory
import Compression_Algorithms as all_algs

if not os.path.exists(directory.output_directory):
    os.mkdir(directory.output_directory)

filename2dict = newfunc.data2dict()

"""Begin Compression Experiment"""
for alg in all_algs.all_compression_algs:
    type_alg = constants.alg2name[alg]
    end = constants.alg2end[constants.alg2name[alg]]
    for filename in filename2dict.keys():
        dict = filename2dict[filename]
        newfunc.newFunction(alg, dict, type_alg, filename+end, constants.all_data, directory.output_directory)

# Get the compressed file sizes to calculate compression ratio later
for file in os.listdir(directory.output_directory):
    if file.endswith("bz2"):
        constants.all_data['bz2_compressed_filesize'].append(os.path.getsize(directory.output_directory + '\\' + file))
    if file.endswith(".gz"):
        constants.all_data['gzip_compressed_filesize'].append(os.path.getsize(directory.output_directory + '\\' + file))
    if file.endswith(".xz"):
        constants.all_data['lzma_compressed_filesize'].append(os.path.getsize(directory.output_directory + '\\' + file ))


""" ZIP Compression"""
zf = zipfile.ZipFile(directory.output_directory + "\Zip Compression file.zip", mode='w')
for filename in filename2dict.keys():
    dict = filename2dict[filename]
    pickled_dict= pickle.dumps(dict)
    start_time = time.time()
    zf.write(directory.input_directory + '\\' + filename + '.csv', filename, compress_type = zipfile.ZIP_DEFLATED)
    recorded_time = str(time.time() - start_time)
    constants.all_data['zip_compression_time'].append(recorded_time)
zf.close()

for filename in filename2dict.keys():
    k = zf.getinfo(filename)
    constants.all_data['zip_compressed_filesize'].append(k.compress_size)


"""Get initial file sizes """
for filename in os.listdir(directory.input_directory):
    constants.all_data['initial_filesizes'] = os.path.getsize(directory.input_directory + '\\' + filename)

"""Create a dataframe, put data into it then
    convert to csv in output_directory file """
df = pd.DataFrame.from_dict(constants.all_data)
df.to_csv(directory.output_directory+'\Analysis.csv')
