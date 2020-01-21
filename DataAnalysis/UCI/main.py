#!/usr/bin/python
# -*- coding: utf-8 -*-

# import sys
# import aux
import fun
import datetime
import argparse
# import MoNeT_MGDrivE as monet


###############################################################################
# Code for terminal-call: python main.py
# -----------------------------------------------------------------------------
#   --dev:  {0: Desktop, 1: Server  }
#   --land:  {0: Comoros, 1: STP     }
###############################################################################
parser = argparse.ArgumentParser(description='Main UCI Analysis routine!')
parser.add_argument("--dev", default=0, type=int, help="Device")
parser.add_argument("--land", default=0, type=int, help="Landscape")
(ROOT, LAND) = fun.experimentSelector(parser.parse_args())
# Full path -------------------------------------------------------------------
PATH_ROOT = '{}/marshallShare/UCI/{}/'.format(ROOT, LAND)
PATH_IMG = PATH_ROOT + 'img/'
###############################################################################
# Print experiment info to terminal
###############################################################################
time = str(datetime.datetime.now())
fun.printExperimentHead(PATH_ROOT, PATH_IMG, time)
