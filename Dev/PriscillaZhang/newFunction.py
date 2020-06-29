import pickle
import time
import os


output_directory = r'C:\Users\prisc\Desktop\Compressed Files + Analysis'

"""
algorithm: function, compression function
dict:  dictionary, Key is the header (genotype) : Value is the counts stored in a np array
type_alg: String, type of algorithm
filenameend: filename + .algorithm_ending
all_data: dictionary, name of list: list

"""

def newFunction(algorithm, dict, type_alg, filename_end, all_data, output_directory):

    start_time = time.time()
    pickled_dict = pickle.dumps(dict)
    compressed_data = algorithm(pickled_dict)
    all_data[type_alg + '_compressedData_Time'].append(str(time.time() - start_time))

    with open(os.path.join(output_directory, filename_end), 'wb') as f:
        f.write(compressed_data)
        f.close()

    recorded_time = str(time.time() - start_time)
    all_data[type_alg+'_compression_time'].append(recorded_time)
