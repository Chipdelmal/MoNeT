#!/usr/bin/env python
# coding: utf-8

from joblib import Parallel, delayed
import multiprocessing
import pandas as pd
import numpy as np
import threading
import detector
import queue
import sys
import os

class Simulator(detector.Detector):
    def __init__(self, *d_args, **d_kwargs):
        """
        A class for parallelized network simulations.
        """
        super(Simulator, self).__init__(*d_args, **d_kwargs)
    
    ####################
    # Private Methods: #
    ####################
    
    def _run_parallel(self, func, inputs):
        """
        Runs `func()` with each input in `inputs` using multiprocessing.
        
        Parameters:
        -----------
        
            func : function
                A nonnegative integer for the beginning of the interval.
        
            inputs : iterable
                An iterable that contains the arguments for `func`.
        
        Returns:
        --------
        
            result : ndarray
                A list containing the results of calling `func()` on each input in `inputs`.
        """
        return Parallel(n_jobs=multiprocessing.cpu_count())(delayed(func)(inp) for inp in inputs)
    
    def _get_populations(self, start_step, final_step):
        """
        For each time step in [start_step, final_step] computes the
        population vector and returns a matrix of the results. The 
        ith column corresponds to the populations at time step i.
        
        Parameters:
        -----------
        
            start_step : int
                A nonnegative integer for the beginning of the interval.
        
            final_step : int
                A nonnegative integer for the end of the interval.
        
        Returns:
        --------
        
            mtx : ndarray
                An ndarray of shape (# of nodes) x (final_step - start_step + 1) such that
                arr[:, i] = the population vector at time step i
        """
        mtx = np.c_[self.migrate(start_step)]
        for i in range(start_step + 1, final_step + 1):
            mtx = np.c_[mtx, self._sparse_mtx @ mtx[:, -1]]
        return mtx
    
    def _get_populations_wrapper(self, q, lock, stop_event, output, offset):
        """
        Helper method for `get_sizes()`.
        
        Parameters:
        -----------
        
            q : queue.Queue object
                The work queue with jobs for the threads to perform.
            
            lock : threading.Lock object
                A lock for the output array.
                
            stop_event : threading.Event object
                Used to indicate if the thread should exit or continue.
                
            output : ndarray
                An ndarray of shape (# of nodes) x (final_step - start_step + 1) to
                store the results of the computation.
                
            offset : int
                Allows the program to compute populations from a `start_step` other than 0.
        
        Returns:
        --------
        
            None
        """
        while not stop_event.is_set():
            try:
                i, j = q.get(timeout=0.5)
                lock.acquire()
                output[:, i:j+1] = self._get_populations(i + offset, j + offset)
                lock.release()
            except queue.Empty:
                continue
            q.task_done()

    ###################
    # Public Methods: #
    ###################
            
    def get_sizes(self, time_steps, nthreads=10):
        """
        Retrieves the population sizes over a a specified range of 
        time steps. Passing an array of consecutive integers is 
        typically faster than passing an array of nonconsecutive
        integers.
        
        Parameters:
        -----------
        
            time_steps : ndarray
                A sorted array of unique integers. These integers represent the
                time steps to use when computing populations.
                
            nthreads : int
                The number of threads to use. This will be used if 
                `time_steps` is a consecutive range of integers.
        
        Returns:
        --------
        
            output_mtx : ndarray
                An ndarray of shape (# of nodes) x len(time_steps) such that
                arr[:, i] = the population vector at time step i.
        """
        if not np.all(np.diff(time_steps) == 1):
            return np.array(self._run_parallel(self.migrate, time_steps)).T
         
        thread_lst = []
        stop_event = threading.Event()
        outpt_lock = threading.Lock()
        work_queue = queue.Queue()
        input_size = len(time_steps)
        output_mtx = np.zeros((len(self._ndata), input_size))
        
        # Handles the case when the input is smaller than the number of threads available
        threads_to_use = min(input_size, nthreads)

        for inputs in np.array_split(np.arange(input_size), threads_to_use):
            work_queue.put((inputs[0], inputs[-1]))

        for i in range(threads_to_use):
            target_fun = self._get_populations_wrapper
            argmnt_lst = (work_queue, outpt_lock, stop_event, output_mtx, np.min(time_steps))
            thread_lst.append(threading.Thread(target=target_fun, name=f'thread {i}', args=argmnt_lst))
            thread_lst[i].start()

        work_queue.join()
        stop_event.set()
        for t in thread_lst:
            t.join()
        return output_mtx