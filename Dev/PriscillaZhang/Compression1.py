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

input_directory = r'C:\Users\prisc\Desktop\Marshall Lab Data\Marshall Lab Data'
output_directory = r'C:\Users\prisc\Desktop\Compressed Files + Analysis'
list_recorded_times = []
initial_filesize = []
compressed_filesize = []
filename2dict = {}

all_compression_algs = [gzip.compress, lzma.compress, bz2.compress]
compression_alg_map = { gzip.compress: "gzip", lzma.compress: "lzma", bz2.compress : "bz2"}

for i in all_compression_algs:
    print(i)
    print(type(i))

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


lzma_compression_time = []
lzma_compressed_filesize = []
lzma_compressedData_Time = []
"""LZMA Compression"""
for filename in filename2dict.keys():
    dict = filename2dict[filename]
    start_time = time.time()
    pickled_dict= pickle.dumps(dict)

    lzma_compressed_data = lzma.compress(pickled_dict)

    lzma_compressedData_Time.append(str(time.time() - start_time))

    with open(os.path.join(output_directory, filename+'.xz'), 'wb') as f:
        f.write(lzma_compressed_data)
        f.close()

    recorded_time = str(time.time() - start_time)
    lzma_compression_time.append(recorded_time)

for file in os.listdir(output_directory):
    if file.endswith('.xz'):
        lzma_compressed_filesize.append(os.path.getsize(output_directory + '\\' + file))

gzip_compresstion_time = []
gzip_compressed_filesize = []
gzip_compressedData_Time = []

"""GZIP Compression """
for filename in filename2dict.keys():
    dict = filename2dict[filename]
    start_time = time.time()
    pickled_dict= pickle.dumps(dict)

    gzip_compressed_data = gzip.compress(pickled_dict)
    gzip_compressedData_Time.append(str(time.time() - start_time))


    with open(os.path.join(output_directory, filename+'.gz'), 'wb') as f:
        f.write(gzip_compressed_data)

    recorded_time = str(time.time() - start_time)
    gzip_compresstion_time.append(recorded_time)
f.close()

for file in os.listdir(output_directory):
    if file.endswith('.gz'):
        gzip_compressed_filesize.append(os.path.getsize(output_directory + '\\' + file))


bz2_compressed_filesize = []
bz2_compression_time = []
bz2_compressedData_Time = []
"""bz2 Compression"""
for filename in filename2dict.keys():
    dict = filename2dict[filename]
    start_time = time.time()
    pickled_dict= pickle.dumps(dict)

    bz2_compressed_data = bz2.compress(pickled_dict)
    bz2_compressedData_Time.append(str(time.time() - start_time))

    with open(os.path.join(output_directory, filename+'.bz2'), 'wb') as f:
        f.write(bz2_compressed_data)

    recorded_time = str(time.time() - start_time)
    bz2_compression_time.append(recorded_time)

    f.close()

for file in os.listdir(output_directory):
    if file.endswith('.bz2'):
        bz2_compressed_filesize.append(os.path.getsize(output_directory + '\\' + file))


zip_compressed_filesize = []
zip_compression_time = []

"""ZIP FILE Compression"""
zf = zipfile.ZipFile(output_directory + "\Zip Compression file.zip", mode='w')
for filename in filename2dict.keys():
    dict = filename2dict[filename]
    pickled_dict= pickle.dumps(dict)
    start_time = time.time()
    zf.write(input_directory + '\\' + filename + '.csv', filename, compress_type = zipfile.ZIP_DEFLATED)
    recorded_time = str(time.time() - start_time)
    zip_compression_time.append(recorded_time)

zf.close()

for filename in filename2dict.keys():
    k = zf.getinfo(filename)
    zip_compressed_filesize.append(k.compress_size)

"""Create a dataframe, put data into it then
    convert to csv in output_directory file """

df = pd.DataFrame()

df['LZMA Compress Data (sec)'] = lzma_compressedData_Time
df['gzip Compress Data (sec)'] = gzip_compressedData_Time
df['bz2 Compress Data (sec)'] = bz2_compressedData_Time

df['LZMA Compression Time (sec)'] = lzma_compression_time
df['gzip Compression Time (sec)'] = gzip_compresstion_time
df['bz2 Compression Time (sec)'] = bz2_compression_time
df['zip Compression Time(sec)'] = zip_compression_time

df['Initial File Size (bytes)'] = initial_filesize

df['LZMA Compression File Size (bytes)'] = lzma_compressed_filesize
df['gzip Compression File Size (bytes)'] = gzip_compressed_filesize
df['bz2 Compression File Size (bytes)'] = bz2_compressed_filesize
df['zip Compression File Size (bytes)'] = zip_compressed_filesize


df['LZMA Ratio'] = np.array(initial_filesize) / np.array(lzma_compressed_filesize)
df['gzip Ratio'] = np.array(initial_filesize) / np.array(gzip_compressed_filesize)
df['bz2 Ratio'] = np.array(initial_filesize) / np.array(bz2_compressed_filesize)
df['zip Ratio'] = np.array(initial_filesize) / np.array(zip_compressed_filesize)

df.to_csv(output_directory+'\Analysis.csv')
