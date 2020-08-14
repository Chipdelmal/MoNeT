#!/usr/bin/env python
# coding: utf-8

# # Mosquito Sinks and Sources Detector

# # Setup

# In[1]:


from sklearn.cluster import KMeans, AgglomerativeClustering
from collections import defaultdict
import pandas as pd
import numpy as np


# # The Detector Class

# In[2]:


class Detector:
    def __init__(self, transitions, locations, method='kmeans', b_tol=0.25, b_heuristic=None, s_tol=0.05, ss_vals=100000, as_df=False, *args, **kwargs):
        """
        Inputs:
            transitions : A dataframe with transition probabilities
            locations   : A dataframe with an initial population column, 'pop'
            method      : The clustering method, which is either 'kmeans' | 'agglomerative'
            b_tol       : The tolerance for bridge detection (see `b_heuristic`)
            b_heuristic : A function that takes the nested dictionary returned by 
                          `proportions()` and the `b_tol` parameter as input and 
                          returns a new/modified nested dictionary where each second 
                          level dictionary has a 'type' key that indicates its label.                        
                          By default, a community is labeled as a bridge if it is the 
                          case that: |prp_in - prp_out| <= b_tol * maximum_prp_out
            s_tol       : The tolerance for steady state detection
            ss_vals     : The number of possible steady-state steps to consider
            as_df       : Whether or not to return the output as a dataframe
            *args       : Extra arguments for sklearn's kmeans function
            **kwargs    : Extra key word arguments for the clustering method
        
        Notes:
            - Please use set_params instead of reassigning any of the parameters
              manually. If parameters are reassigned manually, results are undefined
              
            - Many functions do not perform error checking (yet) be careful!
        """
        self.tmtx        = transitions
        self.locs        = locations
        self.method      = method
        self.b_tol       = b_tol 
        self.b_heuristic = b_heuristic
        self.s_tol       = s_tol
        self.ss_vals     = ss_vals
        self.as_df       = as_df
        self.args        = args
        self.kwargs      = kwargs
        self.ss_step     = self.compute_sss(self.ss_vals)
        self.coms        = None
        
        # This variable is used to check if we need to recompute the
        # communities. It is set to True on each call to `set_params()`
        self.recompute   = True

    ####################
    # Private Methods: #
    ####################
    def compute_sss(self, vals):
        """
        Computes the steady state step using binary search from the 
        list of possible steps passed in.
        """
        lo = 0
        hi = vals - 1
        while lo <= hi:
            m = (hi + lo) // 2
            prev = self.migrate(m)
            curr = self.migrate(m + 1)
            
            if np.all(np.abs(curr - prev) <= self.s_tol):
                hi = m - 1
            else:
                lo = m + 1
        return lo
        
    def communities(self):
        """
        Returns a dictionary where the key is the community id and
        the value is a list of locations grouped together using the
        kmeans algorithm. More clustering methods may be added using
        the `self.method` class attribute.
        """
        cluster = None
        if self.method == 'kmeans':
            cluster = KMeans(*self.args, **self.kwargs).fit(self.locs[['lon', 'lat']])
        elif self.method == 'agglomerative':
            cluster = AgglomerativeClustering(*self.args, **self.kwargs).fit(self.locs[['lon', 'lat']])
        else:
            raise ValueError("Method '{}' is not supported".format(self.method))
        self.coms = defaultdict(list)
        for loc, cid in enumerate(cluster.labels_):
            self.coms[cid].append(loc)
        return self.coms
    
    def proportions(self, communities, start_step, final_step):
        """
        Returns a dictionary such that each key is a community ID 
        and each value is a dictionary. In the second-level 
        dictionary, there are 5 keys which are explained in depth 
        below:
            1. num_in  -> number of mosquitos that migrated into 
                          this community since time step `start_step`
            2. num_out -> number of mosquitos that migrated out of 
                          this community since time step `start_step`
            3. prp_in  -> the proportion of mosquitos that entered 
                          the community since time step `start_step`
            4. prp_out -> the proportion of mosquitos that left the
                          community since time step `start_step`
            5. com     -> a list of the locations within this 
                          community
        """
        data = defaultdict(dict)
        for cid, community in communities.items():
            start = self.migrate(start_step)[community]
            final = self.migrate(final_step)[community]
            data[cid]['num_in']  = np.sum(final[final > start] - start[final > start])
            data[cid]['num_out'] = np.sum(start[final < start] - final[final < start])
            data[cid]['prp_in']  = data[cid]['num_in']  / (data[cid]['num_in'] + data[cid]['num_out'])
            data[cid]['prp_out'] = data[cid]['num_out'] / (data[cid]['num_in'] + data[cid]['num_out'])
            data[cid]['com']     = community    
        return data
        
    def classify(self, data):
        """
        Classifies each community as a sink/source/bridge.
        """
        if self.b_heuristic is not None:
            return self.b_heuristic(data, self.b_tol)
        
        max_prp = max(map(lambda d: d['prp_out'], data.values()))
        for d in data.values():
            diff = d['prp_in'] - d['prp_out']
            if abs(diff) <= self.b_tol * max_prp:
                d['type'] = 'bridge'
            elif diff < 0:
                d['type'] = 'source'
            else:
                d['type'] = 'sink'
        return data
    
    def pipeline(self, start, final):
        """
        Performs all steps of sink/source detection.
        """
        if self.recompute:
            self.recompute = False
            self.coms = self.communities()
        if final == float('inf'):
            final = self.ss_step    
        result = self.classify(self.proportions(self.coms, start, final))
        if self.as_df:
            return pd.DataFrame(result).transpose().sort_index()
        return result
        
    def get_cids(self):
        """
        Maps each location to its community ID.
        """
        if self.recompute:
            self.recompute = False
            self.coms = self.communities()
        if self.as_df:
            self.cids = self.locs.copy()
            self.cids['cid'] = self.locs.index
            for cid in self.coms:
                self.cids.loc[self.coms[cid], 'cid'] = cid
            return self.cids.copy()
        else: 
            return { loc : k for k, v in coms.items() for loc in v  }
            
    ###################
    # Public Methods: #
    ###################
    
    def set_params(self, b_tol=None, b_heuristic=None, s_tol=None, ss_vals=None, method=None, as_df=None, *args, **kwargs):
        """
        Resets the parameters of this instance.
        """
        self.recompute = True
        if b_tol is not None:       self.b_tol = b_tol
        if b_heuristic is not None: self.b_heuristic = b_heuristic
        if s_tol is not None:       self.s_tol = s_tol        
        if ss_vals is not None:     self.ss_vals = ss_vals
        if method is not None:      self.method = method
        if  as_df  is not None:     self.as_df = as_df
        if   args:                  self.args = args
        if kwargs:                  self.kwargs = kwargs
            
    def run(self, start=0, final=float('inf')):
        """
        Runs sink source detection from time step `start` to time step
        `final`. By defualt, this runs from step 0 to steady-state.
        """
        self.data = self.pipeline(start, final)
        self.cids = self.get_cids()
        return self
    
    def clabels(self):
        """
        Returns each location and its corresponding community id/label.
        """
        return self.cids.copy()
    
    def results(self):
        """
        Returns the in/out proportions of each community along with
        its class (sink/source/bridge).
        """
        return self.data.copy()
    
    def migrate(self, k):
        """
        Returns the populations at each location after `k` time steps.
        """
        return np.linalg.matrix_power(self.tmtx, k) @ self.locs['pop']

