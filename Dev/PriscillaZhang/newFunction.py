import pickle
import time

output_directory = r'C:\Users\prisc\Desktop\Compressed Files + Analysis'

def newFunction(algorithm, dictionary, type_alg, all_data):
    start_time = time.time()
    pickled_dict = pickle.dumps(dict)
    compressed_data = algorithm(pickled_dict)
    all_data[type_alg + '_compressedData_Time'].append(str(time.time() - start_time))

    with open(os.path.join(output_directory, filename+end), 'wb') as f:
        f.write(compressed_data)
        f.close()

    recorded_time = str(time.time() - start_time)
    all_data[type_alg+'_compression_time'].append(recorded_time)
