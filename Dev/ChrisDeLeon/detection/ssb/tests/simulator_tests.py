#!/usr/bin/env python
# coding: utf-8

from threading import active_count
import pandas as pd
import numpy as np
import unittest
import sys

sys.path.insert(0, '../')
import simulator

transitions = pd.read_csv('test_kernel.csv', header=None)
locations   = pd.read_csv('test_locations.csv')

class SimulatorTests(unittest.TestCase):
    
    def test_consecutive(self):
        
        s = simulator.Simulator(transitions, locations, random_state=42)
        start = 1; final = 100
        time_steps = np.arange(start, final)
        
        init_threads = active_count()
        p = s.get_sizes(time_steps) 
        curr_threads = active_count()
        
        # Any threads created by the function should have exited
        self.assertTrue(curr_threads == init_threads)
        
        # Check shapes
        self.assertTrue(p.shape[0] == len(locations))
        self.assertTrue(p.shape[1] == len(time_steps))
        
        # Any optimization tricks used in the code should still produce accurate results
        p = p.T
        for i in range(start, final):
            self.assertTrue(np.all(np.isclose(p[i - start], s.migrate(i))))
    
    def test_nonconsecutive(self):
        
        s = simulator.Simulator(transitions, locations, random_state=42)
        start = 1; final = 100
        time_steps = np.arange(start, final, 2)
        
        p = s.get_sizes(time_steps)

        # Check shapes
        self.assertTrue(p.shape[0] == len(locations))
        self.assertTrue(p.shape[1] == len(time_steps))

        # Any optimization tricks used in the code should still produce accurate results
        p = p.T
        for i, t in enumerate(time_steps):
            self.assertTrue(np.all(np.isclose(p[i], s.migrate(t))))


if __name__ == '__main__':
    unittest.main()
