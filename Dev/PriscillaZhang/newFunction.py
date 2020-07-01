import numpy as np
import pickle
import time
import os
import pandas as pd
import directories as directory
import Constants as constants


output_directory = r'C:\Users\prisc\Desktop\Compressed Files + Analysis'

"""
algorithm: function, compression function
dict:  dictionary, Key is the header (genotype) : Value is the counts stored in a np array
type_alg: String, type of algorithm
filenameend: filename + .algorithm_ending
all_data: dictionary, name of list: list

"""


#Perform Compression Experiment
def newFunction(algorithm, dict, type_alg, filename_end, all_data, output_directory):
    start_time = time.time()
    pickled_dict = pickle.dumps(dict)
    compressed_data = algorithm(pickled_dict)
    all_data[type_alg + '_compressedData_Time'].append(str(time.time() - start_time))

    with open(os.path.join(output_directory, filename_end), 'wb') as f:
        f.write(compressed_data)
        f.close()

    recorded_time = str(time.time() - start_time)
    return all_data[type_alg+'_compression_time'].append(recorded_time)


def data2dict():
    for filename in os.listdir(directory.input_directory):
        data = pd.read_csv(directory.input_directory + '\\' + filename)
        constants.initial_filesize.append(os.path.getsize(directory.input_directory + '\\' + filename))

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
        constants.filename2dict[filename[:-4]] = data_dict

    return constants.filename2dict
