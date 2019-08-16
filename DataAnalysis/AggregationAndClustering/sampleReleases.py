#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import sample

coverage = .5
nodesIDPool = range(0, 1000)


sampledNumber = round(len(nodesIDPool) * coverage)
sample(nodesIDPool, sampledNumber)
