import pandas as pd
import numpy as np
import sys
import os
import csv
import newFunction as newfunc
import Constants as constants
import directories as directory
import Compression_Algorithms as all_algs

# If an output directory doesn't exist, make one
if not os.path.exists(directory.output_directory):
    os.mkdir(directory.output_directory)

#Get the initial file sizes to later calculate compression ratio
for filename in os.listdir(directory.input_directory):
    data = pd.read_csv(directory.input_directory + '\\' + filename)
    constants.initial_filesize.append(os.path.getsize(directory.input_directory + '\\' + filename))
    headers = []
    for col in data.columns:
        headers.append(col)
    headers_list = list(data.columns)[1:]

    """Create a Dictionary for each csv file
       First element is the header (genotype)
       Second element are the counts stored in a np array
    """
    data_dict = {}
    for header in headers_list:
        dic_val = np.array(data[header])
        data_dict[header] = dic_val
    constants.filename2dict[filename[:-4]] = data_dict

"""Begin Compression Experiment"""
for alg in all_algs.all_compression_algs:
    type_alg = constants.alg2name[alg]
    end = constants.alg2end[constants.alg2name[alg]]
    for filename in constants.filename2dict.keys():
        dict = constants.filename2dict[filename]
        times = newfunc.getCompressionTimes(alg, dict, type_alg, filename+end, constants.all_data, directory.output_directory)
        constants.all_data[type_alg + '_compressedData_Time'].append(times[0])
        constants.all_data[type_alg + '_compression_time'].append(times[1])

# Get the compressed file sizes to calculate compression ratio later
for file in os.listdir(directory.output_directory):
    if file.endswith("bz2"):
        constants.all_data['bz2_compressed_filesize'].append(os.path.getsize(directory.output_directory + '\\' + file))
    if file.endswith(".gz"):
        constants.all_data['gzip_compressed_filesize'].append(os.path.getsize(directory.output_directory + '\\' + file))
    if file.endswith(".xz"):
        constants.all_data['lzma_compressed_filesize'].append(os.path.getsize(directory.output_directory + '\\' + file ))

""" ZIP Compression"""
for filename in constants.filename2dict.keys():
    recorded_time = newfunc.getZipCompressionTime(filename)
    constants.all_data['zip_compression_time'].append(recorded_time)
constants.zipfolder.close()

"""Get the file compressed zip file sizes """
for filename in constants.filename2dict.keys():
    k = constants.zipfolder.getinfo(filename)
    constants.all_data['zip_compressed_filesize'].append(k.compress_size)

"""Get initial file sizes """
for filename in os.listdir(directory.input_directory):
    constants.all_data['initial_filesizes'] = os.path.getsize(directory.input_directory + '\\' + filename)

"""Create a dataframe, put data into it then
    convert to csv in output_directory file """
df = pd.DataFrame.from_dict(constants.all_data)
df.to_csv(directory.output_directory+'\Analysis.csv')
