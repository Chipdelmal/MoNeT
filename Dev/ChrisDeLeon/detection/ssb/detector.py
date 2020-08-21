#!/usr/bin/env python
# coding: utf-8

# # Mosquito Sinks and Sources Detector

# # Setup

# In[1]:

import pandas as pd
import numpy as np

from sklearn.cluster import KMeans, AgglomerativeClustering
from collections import defaultdict

# # The Detector Class

# In[2]:


class Detector:
    def __init__(self, transitions, locations, method='kmeans', b_tol=0.25, b_heuristic=None, s_tol=0.05, ss_vals=100000, *args, **kwargs):
        """
        Inputs:
            transitions : A dataframe (or string to a csv file) with transition probabilities
            locations   : A dataframe (or string to a csv file) with an initial population column, 'pop'
            method      : The clustering method, which is either 'kmeans' | 'agglomerative'
            b_tol       : The tolerance for bridge detection (see `b_heuristic`)
            b_heuristic : A function that takes the dataframe returned by 
                          `proportions()` and the `b_tol` parameter as input and 
                          returns a new/modified dataframe with a column named 'type'
                          that consists of labels for each community. By default, a 
                          community is labeled as a bridge if it is the case that:
                          |prp_in - prp_out| <= b_tol * maximum_prp_out
            s_tol       : The tolerance for steady state detection
            ss_vals     : The number of possible steady-state steps to consider
            *args       : Extra arguments for sklearn's kmeans function
            **kwargs    : Extra key word arguments for the clustering method
        
        Notes:
            - Please use set_params instead of reassigning any of the parameters
              manually. If parameters are reassigned manually, results are undefined
            - Many functions do not perform error checking (yet) be careful!
        """
        if type(transitions) == str:
            self.tmtx = pd.read_csv(transitions, header=None)
        else:
            self.tmtx = transitions.copy()
        
        if type(locations) == str:
            self.n_data = pd.read_csv(locations)
        else:
            self.n_data = locations.copy()
            
        self.c_data      = pd.DataFrame()
        self.method      = method
        self.b_tol       = b_tol 
        self.b_heuristic = b_heuristic
        self.s_tol       = s_tol
        self.ss_vals     = ss_vals
        self.args        = args
        self.kwargs      = kwargs
        self.ss_step     = self.compute_sss(self.ss_vals)
        
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
        Assigns each node in `self.n_data` their corresponding 
        cluster number. These labels are stored in the `cid` 
        column of `self.n_data`. More clustering methods may 
        be added using the `self.method` class attribute.
        """
        cluster = None
        if self.method == 'kmeans':
            cluster = KMeans(*self.args, **self.kwargs).fit(self.n_data[['lon', 'lat']])
        elif self.method == 'agglomerative':
            cluster = AgglomerativeClustering(*self.args, **self.kwargs).fit(self.n_data[['lon', 'lat']])
        else:
            raise ValueError("Method '{}' is not supported".format(self.method))
        self.n_data['cid'] = cluster.labels_
        
    def proportions(self, start_step, final_step):
        """
        Returns a dataframe such that the index is the community
        ID and the columns are:
            1. num_in  -> number of mosquitos that migrated into 
                          this community since time step `start_step`
            2. num_out -> number of mosquitos that migrated out of 
                          this community since time step `start_step`
            3. prp_in  -> the proportion of mosquitos that entered 
                          the community since time step `start_step`
            4. prp_out -> the proportion of mosquitos that left the
                          community since time step `start_step`
        """
        start = self.migrate(start_step)
        final = self.migrate(final_step)
        total = np.sum(self.n_data['pop'])
        
        def compute_inum(community):
            s = start[community.index]
            f = final[community.index]
            return np.sum(f[f > s] - s[f > s])
        
        def compute_onum(community):
            s = start[community.index]
            f = final[community.index]
            return np.sum(s[f < s] - f[f < s])
        
        data = pd.DataFrame()
        grouped = self.n_data.groupby('cid')
        data['num_in']  = grouped.apply(compute_inum)
        data['num_out'] = grouped.apply(compute_onum)
        data['prp_in']  = data['num_in' ]  / (data['num_in'] + data['num_out'])
        data['prp_out'] = data['num_out']  / (data['num_in'] + data['num_out'])
        return data
        
    def classify(self, data):
        """
        Classifies each community as a sink/source/bridge.
        """
        if self.b_heuristic is not None:
            return self.b_heuristic(data, self.b_tol)
        
        diff = data['prp_in'] - data['prp_out']
        mask = np.abs(diff) <= self.b_tol * np.max(data['prp_out'])
        
        data['type'] = None
        data.loc[mask, 'type'] = 'bridge'
        data.loc[(diff < 0) & ~mask, 'type'] = 'source'
        data.loc[(diff > 0) & ~mask, 'type'] = 'sink'
        return data
    
    def pipeline(self, start, final):
        """
        Performs all steps of sink/source detection and append
        any additional data.
        """
        if self.recompute:
            self.communities()
            self.recompute = False
            
        if final == float('inf'):
            final = self.ss_step
        
        self.c_data = self.classify(self.proportions(start, final))
        self.n_data['ctype'] = self.n_data['cid'].apply(lambda cid: self.c_data.loc[cid, 'type'])
        return self
            
    ###################
    # Public Methods: #
    ###################
    
    def set_params(self, b_tol=None, b_heuristic=None, s_tol=None, ss_vals=None, method=None, *args, **kwargs):
        """
        Resets the parameters of this instance.
        """
        self.recompute = True
        if b_tol is not None:       self.b_tol = b_tol
        if b_heuristic is not None: self.b_heuristic = b_heuristic
        if s_tol is not None:       self.s_tol = s_tol        
        if ss_vals is not None:     self.ss_vals = ss_vals
        if method is not None:      self.method = method
        if   args:                  self.args = args
        if kwargs:                  self.kwargs = kwargs
            
    def run(self, start=0, final=float('inf')):
        """
        Runs sink source detection from time step `start` to time step
        `final`. By defualt, this runs from step 0 to steady-state.
        """
        return self.pipeline(start, final)
    
    def ndata(self):
        """
        Assuming `run()` has been called beforehand, returns a dataframe 
        containing the coordinates of each node, their cids, and their 
        ctypes. A node's 'ctype' is the label of the community it is in. 
        If this is called before `run()` then the original `locations` 
        dataframe will be returned.
        """
        return self.n_data.copy()
    
    def cdata(self):
        """
        Returns the in/out proportions for each community along with
        their labels (sink/source/bridge). If this is called before 
        `run()` then an empty dataframe will be returned.
        """
        return self.c_data.copy()
    
    def migrate(self, k):
        """
        Returns the populations at each location after `k` time steps.
        """
        return np.linalg.matrix_power(self.tmtx, k) @ self.n_data['pop']
