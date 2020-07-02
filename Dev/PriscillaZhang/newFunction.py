import numpy as np
import pickle
import time
import os
import pandas as pd
import directories as directory
import Constants as constants
import zipfile
import zlib

'''Perform Compression Experiment
    Returns a list of string:
    list[0] Time to compress data
    list[1] Time to compress data and write it into the file
'''
def getCompressionTimes(algorithm, dict, type_alg, filename_end, all_data, output_directory):
    times = []
    start_time = time.time()
    pickled_dict = pickle.dumps(dict)
    compressed_data = algorithm(pickled_dict)
    compressData_time = str(time.time() - start_time)
    times.append(compressData_time)
    with open(os.path.join(output_directory, filename_end), 'wb') as f:
        f.write(compressed_data)
        f.close()

    compressNwrite_time = str(time.time() - start_time)
    times.append(compressNwrite_time)
    return times

""" Perform Compression Experiment for Zip Comprssion algorithm
    Returns a string:
    time it takes to compress and write the file into a zip folder
"""
def getZipCompressionTime(filename):
    dict = constants.filename2dict[filename]
    pickled_dict= pickle.dumps(dict)
    start_time = time.time()
    constants.zipfolder.write(directory.input_directory + '\\' + filename + '.csv', filename, compress_type = zipfile.ZIP_DEFLATED)
    recorded_time = str(time.time() - start_time)
    return recorded_time
