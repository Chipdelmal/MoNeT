#!/usr/bin/python
# -*- coding: utf-8 -*-

# import sys
# import aux
import fun
import datetime
import argparse
import drive as drv
import MoNeT_MGDrivE as monet


driveID = 'CRISPR'
###############################################################################
# Setting up the experiment analyses
# -----------------------------------------------------------------------------
#   python main.py
#       --dev:  {0: Desktop, 1: Server  }
#       --land:  {0: Comoros, 1: STP     }
###############################################################################
# parser = argparse.ArgumentParser(description='Main UCI Analysis routine!')
# parser.add_argument("--dev", default=0, type=int, help="Device")
# parser.add_argument("--land", default=0, type=int, help="Landscape")
# (ROOT, LAND) = fun.experimentSelector(parser.parse_args())
(ROOT, LAND) = ('/Volumes', 'Comoros')
# Full path ###################################################################
PATH_ROOT = '{}/marshallShare/UCI/{}/'.format(ROOT, LAND)
(PATH_IMG, PATH_DATA) = (
        PATH_ROOT + 'img/',
        PATH_ROOT + 'out/'
    )
# Print experiment info to terminal ###########################################
time = str(datetime.datetime.now())
fun.printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, time)

###############################################################################
# Selecting drive and get exp dirs
# -----------------------------------------------------------------------------
###############################################################################
drvPars = drv.driveSelector(driveID)
expSetsDirs = monet.listDirectoriesWithPathWithinAPath(PATH_DATA)
# Kernel Selector #############################################################
dir = expSetsDirs[0]
# for loop here
fldrName = dir.split('/')[-1]
(pathTraces, pathMean) = (dir + '/GARBAGE/', dir + '/ANALYZED/')
(dirsTraces, dirsMean) = (
        monet.listDirectoriesWithPathWithinAPath(pathTraces),
        monet.listDirectoriesWithPathWithinAPath(pathMean)
    )
# Experiment Selector #########################################################
