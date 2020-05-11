#!/usr/bin/python
# -*- coding: utf-8 -*-

# Setting up node indices (from R and 0-index shifting)
STP = (
        [i-1 for i in range(29, 268)],  # Sao Tome
        [i-1 for i in range(1, 28)]     # Principe
    )

# Panmictic
PAN = ([0], )
