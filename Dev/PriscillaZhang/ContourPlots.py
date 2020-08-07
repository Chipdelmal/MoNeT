import glob
from joblib import Parallel, delayed
import ContourPlots_directories as directories
import ContourPlots_functions as functions

Parallel(n_jobs=4)(delayed(functions.read_generate)(pathname) for pathname in glob.glob(directories.path))
