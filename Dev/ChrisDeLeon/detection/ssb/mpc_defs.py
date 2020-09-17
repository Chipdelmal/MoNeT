import pandas as pd
import simulator
import detector

def kmeans_exp(name, kernel, location, c_num, tstep, state):
    return name, c_num, simulator.Simulator(kernel, 
                                            location,
                                            n_clusters=c_num,
                                            random_state=state).run(tstep)

def sao_tome_kmeans_exp(name, kernel, location, c_num, tstep, state):
    sao_tome_locs = pd.read_csv(location)
    sao_tome_tmtx = pd.read_csv(kernel, header=None).to_numpy()
    sao_tome_locs = sao_tome_locs[sao_tome_locs['lat'] < 0.50]
    sao_tome_indx = sao_tome_locs.index.to_numpy()
    sao_tome_tmtx = sao_tome_tmtx[sao_tome_indx[:, None], sao_tome_indx]
    return name, c_num, simulator.Simulator(sao_tome_tmtx, 
                                            sao_tome_locs.reset_index(drop=True),
                                            n_clusters=c_num,
                                            random_state=state).run(tstep)

# Each process calls this function feel free to replace the body
def main(*inputs):
    return sao_tome_kmeans_exp(*inputs)