#!/usr/bin/env python
# coding: utf-8

from sklearn.cluster import KMeans, AgglomerativeClustering
from collections import defaultdict
from scipy import sparse
import threading, queue
import pandas as pd
import numpy as np

class Detector:
    def __init__(self, transitions, locations, method='kmeans', b_tol=0.25, b_heuristic=None, s_tol=0.05, ss_vals=100000, *args, **kwargs):
        """
        Creates a detector object for sink/source/bridge detection.
        
        Parameters:
        -----------
        
            transitions : A dataframe, string to CSV file, or ndarray
                Should have the following properties:
                    1. columns should sum to 1
                    2. must be a square matrix
                            
            locations : A dataframe or string to CSV file
                Should have the following properties:
                    1. must have the columns: 'pop', 'lat', 'lon'
                    2. len(locations) is equal to transitions.shape[1]
                            
            method : string or list or ndarray
                The clustering method to use. If a string, then it must be either 'kmeans' | 'agglomerative'.
                A custom clustering may be specified by passing in a list, L, such that L[i] = CID of node i.
            
            b_tol : float or int
                The tolerance for bridge detection (see `b_heuristic`).
            
            b_heuristic : function
                A function that takes the dataframe returned by `_proportions()` and 
                the `_btol` parameter as input and returns a dataframe with a column 
                named 'type' that consists of labels for each community. By default, 
                a community is labeled as a bridge if it satisfies the following:
                |prp_in - prp_out| <= _btol * max_prp_out. If an invalid function is 
                passed in or 'type' is not found, the default heuristic is used.
                          
            s_tol : float or int
                The tolerance for steady state detection. If the absolute difference 
                in population between two consecutive time steps is less than this 
                value for all nodes, the detector will consider the earlier time step
                as steady state.
                          
            ss_vals : int
                The number of possible steady-state steps to consider.
            
            *args : tuple
                Extra arguments for the clustering method.
            
            **kwargs : dict
                Extra key word arguments for the clustering method.
        
        Returns:
        --------
            
            A detector object.
        
        Notes:
        ------
        
            - Please use set_params instead of reassigning any of the parameters
              manually. If parameters are reassigned manually, results are undefined.
        """
        if isinstance(transitions, str):
            self.tmtx = pd.read_csv(transitions, header=None).to_numpy().T
        elif isinstance(transitions, (pd.Series, pd.DataFrame)):
            self.tmtx = transitions.to_numpy().T
        elif isinstance(transitions, np.ndarray):
            self.tmtx = transitions.T
        else:
            raise TypeError('Received unexpected type for transitions: {}'.format(type(transitions)))
            
        if isinstance(locations, str):
            self._ndata = pd.read_csv(locations)
        elif isinstance(locations, pd.DataFrame):
            self._ndata = locations.copy()
        else:
            raise TypeError('Received unexpected type for locations: {}'.format(type(locations)))
          
        self._cdata      = pd.DataFrame()
        self.method      = method
        self._btol       = b_tol 
        self._bheuristic = b_heuristic
        self._stol       = s_tol
        self._ssvals     = ss_vals
        self.args        = args
        self.kwargs      = kwargs
        self.ss_step     = self._compute_sss(self._ssvals)
        
        # If our matrix is sparse, we can speed up population computations
        self._sparse_mtx = self.tmtx
        if 1 - (np.count_nonzero(self.tmtx) / self.tmtx.size) > 0.5:
            self._sparse_mtx = sparse.csr_matrix(self.tmtx)
        
        # This variable is used to check if we need to recompute the
        # communities. It is set to True on each call to `set_params()`
        self._recompute   = True

    ####################
    # Private Methods: #
    ####################
    
    def _compute_sss(self, vals):
        """
        Uses binary search over the range [0, vals) to find the step at
        which steady state occurs.
        
        Parameters:
        -----------
        
            vals : int
                A positive integer that marks the end of the range to search.
        
        Returns:
        --------
        
            ss_step : int
                The step at which steady state occurs.  
        """
        lo = 0
        hi = vals - 1
        while lo <= hi:
            m = (hi + lo) // 2
            prev = self.migrate(m)
            curr = self.migrate(m + 1)
            if np.all(np.abs(curr - prev) <= self._stol):
                hi = m - 1
            else:
                lo = m + 1
        return lo
        
    def _communities(self):
        """
        
        Assigns each node in `self._ndata` their corresponding cluster
        number. These labels are stored in the `cid` column of 
        `self._ndata`. More clustering methods may be added using the
        `self.method` class attribute.
        
        Parameters:
        -----------
        
            None
        
        Returns:
        --------
        
            None
        """
        cluster = None
        if isinstance(self.method, list) or isinstance(self.method, np.ndarray):
            self._ndata['cid'] = self.method
        elif self.method == 'kmeans':
            cluster = KMeans(*self.args, **self.kwargs)
            self._ndata['cid'] = cluster.fit_predict(self._ndata[['lon', 'lat']])
        elif self.method == 'agglomerative':
            cluster = AgglomerativeClustering(*self.args, **self.kwargs)
            self._ndata['cid'] = cluster.fit_predict(self._ndata[['lon', 'lat']])
        else:
            raise NotImplementedError("Method '{}' is not supported".format(self.method))

    def _flows(self, community, t):
        """
        Computes the in/out flows for the given `community` at time step `t`.
        
        Parameters:
        -----------
            
            community : pandas DataFrame
                A DataFrame such that each row is a member of the same community.
                
            t : int
                A nonnegative integer representing the time step to compute the flow.
                
        Returns:
        --------
            
            flows : pandas Series
                A new Series object with two columns:
                    "num_in"  : the number of objects that flow into this community
                    "num_out" : the number of objects that flow out of this community
        
        """        
        # Get the ids of the nodes that are in `community`
        cids = community.index
        
        # Get the ids of the nodes that are not in `community`
        aliens = ~self._ndata.index.isin(cids)
        aliens = self._ndata.loc[aliens].index.to_numpy()
        
        # Get the population at the given time step
        pops = self.migrate(t)
        
        # To find the flow into this community take the rows of kernel.T that
        # correspond to `cids` and the columns that correspond to `aliens`. 
        # Then, multiply this submatrix by the population vector that only 
        # consists of alien populations
        iflow = np.sum(self._sparse_mtx[np.ix_(cids, aliens)] @ pops[aliens])
        
        # To find the flow out of this community take the rows of kernel.T that
        # correspond to `aliens` and the columns that correspond to `cids`. 
        # Then, multiply this submatrix by the population vector that only 
        # consists of the populations from this community
        oflow = np.sum(self._sparse_mtx[np.ix_(aliens, cids)] @ pops[cids])
        
        # Attach the flows and return
        return pd.Series({ 'num_in' : iflow, 'num_out' : oflow })
    
    def _proportions(self, t):
        """
        Returns a pandas DataFrame with 4 new columns: 'num_in', 'num_out', 
        'prp_in', 'prp_out'. Each community will have its own row in the 
        resulting DataFrame.
        
        Parameters:
        -----------
        
            t : int
                A nonnegative integer representing the time step to compute the flow.
                
        Returns:
        --------
        
            result : pandas DataFrame
                `result` will contain the following columns:
                    num_in  : the number of objects expected to enter the given community at time step `t`
                    num_out : the number of objects expected to exit the given community at time step `t`                    
                    prp_in  : `num_in` / (`num_in + num_out`)
                    prp_out : `num_out` / (`num_in + num_out`)
        """
        result = self._ndata.groupby('cid').apply(lambda c: self._flows(c, t))
        totals = result['num_in'] + result['num_out']        
        z_mask = (totals != 0)
        result['prp_in' ] = 0
        result['prp_out'] = 0
        result.loc[z_mask, 'prp_in' ] = result.loc[z_mask, 'num_in' ] / totals[z_mask]
        result.loc[z_mask, 'prp_out'] = result.loc[z_mask, 'num_out'] / totals[z_mask]
        return result
        
    def _classify(self, data):
        """
        Classifies each community as a sink/source/bridge.
        
        Parameters:
        -----------
        
            data : pandas DataFrame
                The DataFrame returned by `self._proportions`.
                
        Returns:
        --------
        
            data : pandas DataFrame
                The original DataFrame with a new column, 'type', which indicates whether
                a community is a sink/source/bridge.
        """
        if self._bheuristic is not None:
            try:
                user = self._bheuristic(data.copy(), self._btol)
                if 'type' not in user.columns:
                    self._bheuristic = None
                else:
                    return user
            except TypeError as e:
                self._bheuristic = None
        
        diff = data['prp_in'] - data['prp_out']
        mask = np.abs(diff) <= self._btol * np.max(data['prp_out'])
        data['type'] = None
        data.loc[mask, 'type'] = 'bridge'
        data.loc[(diff < 0) & ~mask, 'type'] = 'source'
        data.loc[(diff > 0) & ~mask, 'type'] = 'sink'
        return data
    
    def _pipeline(self, t):
        """
        Performs all steps of sink/source detection and appends
        ctypes to nodes.
        
        Parameters:
        -----------
        
            t : int
                A nonnegative integer representing the time step to compute the flow.
                
        Returns:
        --------
        
            self : Detector object
                The result of performing SSB detection on this instance.
        """
        if t == float('inf'):
            t = self.ss_step
        
        if self._recompute:
            self._communities()
            self._recompute = False
            
        self._cdata = self._classify(self._proportions(t))
        self._ndata['ctype'] = self._ndata['cid'].apply(lambda cid: self._cdata.loc[cid, 'type'])
        return self
    
    ###################
    # Public Methods: #
    ###################
    
    def set_params(self, b_tol=None, b_heuristic=None, s_tol=None, ss_vals=None, method=None, *args, **kwargs):
        """    
        Resets the parameters of this instance.
        
        Parameters:
        -----------
        b_tol : float or int 
            The tolerance for bridge detection (see `_bheuristic`).
            
        b_heuristic : function
            A function of two args: DataFrame( 'num_in', 'num_out', 'prp_in', 'prp_out' ) and _btol 
            Should return a dataframe with a 'type' column.
        
        s_tol : float or int
            The tolerance for steady state detection.
            
        ss_vals : int
            The number of steady state values to consider.
            
        method : string
            The clustering method to use.
        
        args : tuple
            Extra arguments for the clustering method.
        
        kwargs : dict
            Extra keyword arguments for the clustering method.
            
        
        Returns:
        --------
        
            None
        
        Notes:
        ------
        
            If a variable is reassigned to the same value, then communities
            will be recomputed.
        """
        self._recompute = True
        if _btol       is not None : self._btol       = b_tol
        if _bheuristic is not None : self._bheuristic = b_heuristic
        if _stol       is not None : self._stol       = s_tol        
        if _ssvals     is not None : self._ssvals     = ss_vals
        if method      is not None : self.method      = method
        if   args                  : self.args        = args
        if kwargs                  : self.kwargs      = kwargs
    
    def run(self, t=float('inf')):
        """
        Runs sink/source/bridge detection at time step `t`. This call
        will compute ndata and cdata at the same time to avoid performing
        any unecessary work.
        
        Parameters:
        -----------
        
            t : int
                The time step to perform SSB detection. The default
                time step is steady state.
        
        Returns:
        --------
        
            ndata : pandas DataFrame
                A copy of the DataFrame described above.
                
        Notes:
        ------
            
            If it is expected that `ndata()` and `cdata()` will both be
            called, it is recommended to call this function first. Calling 
            `ndata()` or `cdata()` with a parameter will trigger SSB detection.
            For instance:
                        
            This will trigger SSB detection once:
            
                >>> d = detector.Detector(...).run()
                >>> n = d.ndata()
                >>> c = d.cdata()
            
            This will trigger SSB detection 3 times:
            
                >>> d = detector.Detector(...).run(1)
                >>> n = d.ndata(2)
                >>> c = d.cdata(3)
        """
        return self._pipeline(t)
    
    def ndata(self, t=None):
        """
        Returns a DataFrame containing the coordinates of each node, 
        their cids, and their ctypes. A node's 'ctype' is the label of
        the community it is in. If this is called before `run()` the 
        original locations DataFrame is returned.
        
        Parameters:
        -----------
        
            t : int
                The time step to perform SSB detection. For steady state
                pass in float('inf').
        
        Returns:
        --------
        
            ndata : pandas DataFrame
                A copy of the DataFrame described above.
        
        Notes:
        ------
        
            If `t` is specified, SSB detection will be performed. 
        """
        if t is None:
            return self._ndata.copy()
        else:
            return self._pipeline(t)._ndata.copy()
    
    def cdata(self, t=None):
        """
        Returns the in/out proportions for each community along with
        their labels (sink/source/bridge). If this is called before 
        `run()` then an empty DataFrame will be returned.
        
        Parameters:
        -----------
            
            t : int
                The time step to perform SSB detection. For steady state
                pass in float('inf').
        
        Returns:
        --------
        
            cdata : pandas DataFrame
                A copy of the DataFrame described above.
                
        Notes:
        ------

            If `t` is specified, then SSB detection will be performed. 
        """
        if t is None:
            return self._cdata.copy()
        else:
            return self._pipeline(t)._cdata.copy()
    
    def migrate(self, k):
        """
        Returns the populations at each location after `k` time steps.
        
        Parameters:
        
            k : int
                The time step to compute the populations.
            
        Returns:
        
            mtx : ndarray
                The population vector at time step `k`.
        """
        return np.linalg.matrix_power(self.tmtx, k) @ self._ndata['pop']