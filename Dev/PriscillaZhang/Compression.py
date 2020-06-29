import pandas as pd
import numpy as np
import pickle
import os
import sys
import time
import csv
import lzma
import gzip
import bz2
import zipfile
import zlib
import newFunction as newfunc

input_directory = r'C:\Users\prisc\Desktop\Marshall Lab Data\Marshall Lab Data'
output_directory = r'C:\Users\prisc\Desktop\Compressed Files + Analysis'
list_recorded_times = []
initial_filesize = []
compressed_filesize = []
filename2dict = {}

all_compression_algs = [lzma.compress, gzip.compress , bz2.compress]

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

for filename in os.listdir(input_directory):
    data = pd.read_csv(input_directory + '\\' + filename)
    initial_filesize.append(os.path.getsize(input_directory + '\\' + filename))

    headers = []
    for col in data.columns:
        headers.append(col)

    headers_list = list(data.columns)[1:]

    """Create a Dictionary
       First element is the header (genotype)
       Second element are the counts stored in a np array
    """

    data_dict = {}
    for header in headers_list:
        dic_val = np.array(data[header])
        data_dict[header] = dic_val
    filename2dict[filename[:-4]] = data_dict


all_data = {
'lzma_compressedData_Time':[],
'gzip_compressedData_Time': [],
'bz2_compressedData_Time': [],

'lzma_compression_time': [],
'gzip_compression_time' : [],
'bz2_compression_time': [],

'zip_compression_time': [],

'initial_filesizes': [],

'lzma_compressed_filesize' : [],
'gzip_compressed_filesize': [],
'bz2_compressed_filesize': [],
'zip_compressed_filesize': [],
}

alg2name = {
    lzma.compress: "lzma",
    gzip.compress: "gzip",
    bz2.compress : "bz2"
}

alg2end = {
    "lzma": ".xz",
    "gzip": ".gz",
    "bz2": ".bz2"
}

end2alg = {
".xz": 'lzma',
".gz": 'gzip',
".bz2": 'bz2'
}



for alg in all_compression_algs:
    type_alg = alg2name[alg]
    end = alg2end[alg2name[alg]]
    for filename in filename2dict.keys():
        dict = filename2dict[filename]

        newfunc.newFunction(alg, dict, type_alg, filename+end, all_data, output_directory)


        # start_time = time.time()
        # pickled_dict = pickle.dumps(dict)
        #
        # compressed_data = alg(pickled_dict)
        #
        # input = filename+end
        #
        # all_data[type_alg + '_compressedData_Time'].append(str(time.time() - start_time))
        #
        # with open(os.path.join(output_directory, filename+end), 'wb') as f:
        #     f.write(compressed_data)
        #     f.close()
        #
        # recorded_time = str(time.time() - start_time)
        # all_data[type_alg+'_compression_time'].append(recorded_time)


# Get the compressed file sizes to calculate compression ratio later
for file in os.listdir(output_directory):
    if file.endswith("bz2"):
        all_data['bz2_compressed_filesize'].append(os.path.getsize(output_directory + '\\' + file))
    if file.endswith(".gz"):
        all_data['gzip_compressed_filesize'].append(os.path.getsize(output_directory + '\\' + file))
    if file.endswith(".xz"):
        all_data['lzma_compressed_filesize'].append(os.path.getsize(output_directory + '\\' + file ))


""" ZIP Compression"""
zf = zipfile.ZipFile(output_directory + "\Zip Compression file.zip", mode='w')
for filename in filename2dict.keys():
    dict = filename2dict[filename]
    pickled_dict= pickle.dumps(dict)
    start_time = time.time()
    zf.write(input_directory + '\\' + filename + '.csv', filename, compress_type = zipfile.ZIP_DEFLATED)
    recorded_time = str(time.time() - start_time)
    all_data['zip_compression_time'].append(recorded_time)
zf.close()

for filename in filename2dict.keys():
    k = zf.getinfo(filename)
    all_data['zip_compressed_filesize'].append(k.compress_size)


"""Get initial file sizes """
for filename in os.listdir(input_directory):
    all_data['initial_filesizes'] = os.path.getsize(input_directory + '\\' + filename)

"""Create a dataframe, put data into it then
    convert to csv in output_directory file """
df = pd.DataFrame.from_dict(all_data)

df['LZMA Compression Ratio'] = np.array(all_data['initial_filesizes']) / np.array(all_data['lzma_compressed_filesize'])
df['gzip Compression Ratio'] = np.array(all_data['initial_filesizes']) / np.array(all_data['gzip_compressed_filesize'])
df['bz2 Compression Ratio'] = np.array(all_data['initial_filesizes']) / np.array(all_data['bz2_compressed_filesize'])
df['zip Compression Ratio'] = np.array(all_data['initial_filesizes']) / np.array(all_data['zip_compressed_filesize'])

df.to_csv(output_directory+'\Analysis.csv')
