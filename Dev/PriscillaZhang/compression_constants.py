import lzma
import gzip
import bz2
import zipfile
import zlib
import compression_directories as directory


input_directory = directory.input_directory
output_directory = directory.output_directory
zipfolder = zipfile.ZipFile(directory.output_directory + "\Zip Compression file.zip", mode='w')

list_recorded_times = []
initial_filesize = []
filename2dict = {}

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
