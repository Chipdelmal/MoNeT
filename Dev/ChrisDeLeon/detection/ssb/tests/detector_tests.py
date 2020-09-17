#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import unittest
import sys

sys.path.insert(0, '../')
import detector

transitions = pd.read_csv('test_kernel.csv', header=None)
locations   = pd.read_csv('test_locations.csv')

class DetectorTests(unittest.TestCase):
    
    def test_constructor(self):
        # Error should be raised if given a bad clustering method
        with self.assertRaises(NotImplementedError):
            d = detector.Detector(transitions, locations, method='oof', n_clusters=2, random_state=42)
            d._communities()
        
        # Error should be raised if locations is a bad type
        with self.assertRaises(TypeError):
            dummy_locs = 1.3423
            dummy_tmtx = np.array([])
            d = detector.Detector(dummy_tmtx, dummy_locs, n_clusters=2, random_state=42)
            
        # Error should be raised if transitions is a bad type
        with self.assertRaises(TypeError):
            dummy_locs = pd.DataFrame({'lat' : [0, 1], 'lon' : [0, 0], 'pop' : [1, 1]})
            dummy_tmtx = 0.1234
            d = detector.Detector(dummy_tmtx, dummy_locs, n_clusters=2, random_state=42)
                
        # No errors should be raised for a valid call
        d = detector.Detector(transitions, locations, method='agglomerative', n_clusters=2)

    def test_compute_sss(self):
        d = detector.Detector(transitions, locations, n_clusters=3, random_state=42)
        s = d.ss_step
        
        # Before steady state, some communities should still be outside the default threshold
        self.assertFalse(np.all(np.abs(d.migrate(d.ss_step - 1) - d.migrate(d.ss_step)) <= 0.05))
        
        # At steady state, no community should be outside the default threshold
        self.assertTrue(np.all(np.abs(d.migrate(d.ss_step) - d.migrate(d.ss_step + 1)) <= 0.05))
    
    def test_communities(self):
        d1 = detector.Detector(transitions, locations, n_clusters=3, random_state=42)
        d1._communities()
        n1 = d1.ndata()
        
        # Number of unique labels must match the number of clusters
        self.assertEqual(len(n1['cid'].unique()), 3)
        
        # Number of sinks, sources, and bridges should sum to the number of nodes
        self.assertTrue(np.sum(n1.groupby('cid').size()) == len(locations))
        
        # Should result in the same clusters when a random_state is used
        d2 = detector.Detector(np.zeros(transitions.shape), locations, n_clusters=3, random_state=42)
        d2._communities()
        self.assertTrue(np.all(n1['cid'] == d2.ndata()['cid']))
    
    def test_bridge_heuristic(self):
        
        def bad_func0(x):
            return x
        
        def bad_func1(data, b_tol):
            data['this is a bad name'] = 'bridge'
            return data
        
        def valid_func(data, b_tol):
            data['type'] = 'bridge'
            return data
            
        # Should use defualt heuristic instead
        d0 = detector.Detector(transitions, locations, b_heuristic=bad_func0, n_clusters=2, random_state=42).run()
        d1 = detector.Detector(transitions, locations, b_heuristic=bad_func1, n_clusters=2, random_state=42).run()
        
        # Get another instance for comparisons
        d2 = detector.Detector(transitions, locations, n_clusters=2, random_state=42).run()
        
        # Should be the same
        self.assertTrue(np.all(d0.cdata()['type'] == d2.cdata()['type']))
        self.assertTrue(np.all(d1.cdata()['type'] == d2.cdata()['type']))
        
        # Should pass if a valid function is used
        d3 = detector.Detector(transitions, locations, b_heuristic=valid_func, n_clusters=2, random_state=42).run()
        self.assertTrue(np.all(d3.ndata()['ctype'] == 'bridge'))
    
    def test_migrate(self):
        d = detector.Detector(transitions, locations, n_clusters=268, random_state=42).run()
        
        # Total initial population should be approximately equal to total final population
        initial = np.sum(locations['pop'])
        final   = np.sum(d.migrate(d.ss_step))
        self.assertTrue(np.isclose(initial, final), '{} != {}'.format(initial, final))
    
    def get_dummy_detector(self, K, p, labels=None, t=1):
        
        # If no custom labels are specified, assign each node to its own cluster
        if labels is None:
            labels = np.arange(len(K))
            
        # Create dummy locations so that all we need to worry about is population sizes
        if not isinstance(p, pd.DataFrame):
            p = pd.DataFrame({
                'lat' : np.arange(len(p)),
                'lon' : np.arange(len(p)),
                'pop' : np.array(p)
            })
        
        def strict_heuristic(data, btol):
            diff = data['prp_in'] - data['prp_out']
            mask = (diff == 0)
            data['type'] = None
            data.loc[mask, 'type'] = 'bridge'
            data.loc[(diff < 0) & ~mask, 'type'] = 'source'
            data.loc[(diff > 0) & ~mask, 'type'] = 'sink'
            return data
        
        # Run and return
        d = detector.Detector(K, p, b_heuristic=strict_heuristic, method=labels).run(t)
        return d
    
    def get_uniformly_random_kernel(self, rng, shape):
        K = rng.random((shape, shape))
        sums = np.sum(K, axis=1)
        K = K / sums[:, None]
        return K
        
    def flow_testing_helper(self, expected, K, p, labels=None, t=1, testid=None):

        d = self.get_dummy_detector(K, p, labels, t)
        n = d.ndata()
        c = d.cdata()
        
        debug = """
            
            testid    : {}
            expected  : {}
            got       : {}
            time step : {}
            labels    : {}
            num_in    : {}
            num_out   : {}
        
        """.format(testid, 
                   expected, 
                   n['ctype'].values, t,
                   n['cid'].values,
                   c['num_in'].values, 
                   c['num_out'].values)

        self.assertTrue(np.all(n['ctype'] == expected), debug)
    
    def test_flow_edge_cases(self):
        # All nodes have self loops
        K = np.array([[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]])
        
        # { 0 } => bridge, { 1 } => bridge, { 2 } => bridge
        expected = np.array(['bridge'] * 3)
        self.flow_testing_helper(expected, K, [100] * 3, testid='flow-edge-1')
        
        # { 0, 1 } => sink, { 2 } => sink 
        expected = np.array(['bridge'] * 3)
        self.flow_testing_helper(expected, K, [100] * 3, labels=[0, 0, 1], testid='flow-edge-2')
    
    def test_flow01(self):
        # 0 -> 1 -> 2
        K = np.array([[0, 1, 0],
                      [0, 0, 1],
                      [0, 0, 1]])

        # 100 flow out of {0}, 100 flow in AND out of {1}, and 100 flow into {2}
        expected = np.array(['source', 'bridge', 'sink'])
        self.flow_testing_helper(expected, K, [100] * 3, t=0, testid='flow01-1')
        
        # Nothing happens to {0}, 100 flow out of {1}, and 100 flow into {2}
        expected = np.array(['bridge', 'source', 'sink'])
        self.flow_testing_helper(expected, K, [100] * 3, t=1, testid='flow01-2')
        
        # 100 flow out of { 0, 1 } and 100 flow into {2}
        expected = np.array(['source', 'source', 'sink'])
        self.flow_testing_helper(expected, K, [100] * 3, labels=[0, 0, 1], t=0, testid='flow01-3')
        
        # 100 flow out of { 0, 1 } and 100 flow into {2}
        expected = np.array(['source', 'source', 'sink'])
        self.flow_testing_helper(expected, K, [100] * 3, labels=[0, 0, 1], t=1, testid='flow01-4')
        
        # No flows should occur
        expected = np.array(['bridge'] * 3)
        self.flow_testing_helper(expected, K, [100] * 3, labels=[0, 0, 1], t=2, testid='flow01-5')

    def test_flow02(self):
        # 0 -> 1 -> 2 -> 3 -> 0
        K = np.array([[0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1],
                      [1, 0, 0, 0]])
        
        # 100 units of flow circulate throughout the entire chain
        expected = np.array(['bridge'] * 4)
        self.flow_testing_helper(expected, K, [100] * 4, t=0, testid='flow02-1')
        
        # 100 units of flow re-circulate throughout the entire chain
        expected = np.array(['bridge'] * 4)
        self.flow_testing_helper(expected, K, [100] * 4, t=1, testid='flow02-2')
        
        # 100 units of flow circulate from {0, 1} to {2, 3} AND 
        # 100 units of flow circulate from {2, 3} to {0, 1}
        expected = np.array(['bridge'] * 4)
        self.flow_testing_helper(expected, K, [100] * 4, labels=[0, 0, 1, 1], t=0, testid='flow02-3')
        
        # 100 units of flow circulate from {0, 1} to {2, 3} AND 
        # 100 units of flow circulate from {2, 3} to {0, 1}
        expected = np.array(['bridge'] * 4)
        self.flow_testing_helper(expected, K, [100] * 4, labels=[0, 0, 1, 1], t=1, testid='flow02-3')
        
    def test_flow03(self):
        K = np.array([[0.5, 0.5, 0  , 0],
                      [0  , 0.5, 0.5, 0],
                      [0  , 0  , 0.5, 0.5],
                      [0  , 0  , 0  , 1]])
        
        expected = np.array(['source', 'bridge', 'bridge', 'sink'])
        self.flow_testing_helper(expected, K, [100] * 4, t=0, testid='flow03-1')
        
        expected = np.array(['source', 'source', 'bridge', 'sink'])
        self.flow_testing_helper(expected, K, [100] * 4, t=1, testid='flow03-2')
        
        expected = np.array(['source', 'source', 'source', 'sink'])
        self.flow_testing_helper(expected, K, [100] * 4, t=2, testid='flow03-3')
        
        # With the default steady state tolerance, we stop short of the 
        # state ['bridge', 'bridge', 'bridge', 'bridge']
        expected = np.array(['source', 'source', 'source', 'sink'])
        self.flow_testing_helper(expected, K, [100] * 4, t=float('inf'), testid='flow03-4')
    
    def basic_run_checks(self, d, t):
        n = d.ndata()
        c = d.cdata()
        
        # No labels should be None
        self.assertTrue(n['ctype'].isna().sum() == 0)
        
        # Proportions should be no greater than 1 (some may be zero)
        self.assertTrue(np.all(x == 0 or x == 1 for x in c['prp_in'] + c['prp_out']))
        
        # Total initial population should be approximately equal to total final population   
        p0 = d.migrate(0)
        pf = d.migrate(t)
        self.assertTrue(np.all(np.isclose(np.sum(p0), np.sum(pf))))
        
        # Ensure that all necessary columns exist
        self.assertTrue(set(['lon', 'lat', 'pop', 'cid', 'ctype']) == set(n.columns))
        self.assertTrue(set(['num_in', 'num_out', 'prp_in', 'prp_out', 'type']) == set(c.columns), set(c.columns))
        
    def run_loop(self, times, clusters):
        for c in clusters:
            for t in times:
                d = detector.Detector(transitions, locations, n_clusters=c, random_state=42).run(t)
                if t is None:
                    t = d.ss_step
                self.basic_run_checks(d, t)
        
    def test_short_run(self):
        self.run_loop([10, 100, 1000], [2, 100, 268])

    def test_medium_run(self):
        self.run_loop([10, 50, 100, 500, 1000], [3, 200, 268])

    def test_long_run(self):
        self.run_loop([10, 25, 50, 75, 100, 250, 500, 750, 1000], [268])


if __name__ == '__main__':
    unittest.main()
