#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import numpy as np


def maxAlleleInLandscape(geneLandscape):
    genesMaxes = map(np.amax, geneLandscape)
    landscapeMax = max(genesMaxes)
    return landscapeMax


def autoGenerateGenotypesDictionary(genes, genotypes):
    '''
    Description:
        * This function takes the genes and genotypes lists, and auto-generates
            the dictionary for the aggregation of genes.
    In:
        * genes: list of the genes to aggregate
        * genotypes: list of strings containing the genotypes
    Out:
        * Aggregation dictionary
    Notes:
        * This is the most general case of the aggregation. For specific
            applications, other functions will need to be created.
    '''
    tempList = []
    for gene in genes:
        tempList.append(findGeneInGenotypesList(gene, genotypes))
    returnDict = {
        "genotypes": genes,
        "indices": tempList
    }
    return returnDict


def findGeneInGenotypesList(gene, genotypes):
    '''
    Description:
        * Returns a list of the repetitions of the allele in a list of
            genotypes strings
    In:
        * gene: character of the allele we are looking for
        * genotypes: list of the genotypes present in the experiment
    Out:
        * List containing the counts of the appearances of the gene in
            the genotypes list
    Notes:
        * This function is mostly designed to be used in a wrapper
            (autoGenerateGenotypesDictionary)
    '''
    repsList = []
    for i in range(0, len(genotypes)):
        count = genotypes[i].count(gene)
        if count > 0:
            repsList.append([i] * count)
    return flatten(repsList)


def flatten(lst):
    '''
    Description:
        * Recursive function to flatten a list to a level 1
    In:
        * Any list
    Out:
        * Flattened list
    Notes:
        * Not coded by me
    '''
    return sum(([x] if not isinstance(x, list) else flatten(x)
                for x in lst), [])


def generateAggregationDictionary(genotypesList, indicesList):
    '''
    Description:
        * Creates a dictionary to be used in the aggregation functions.
    In:
        * List of genotypes strings (ordered)
        * List of the indices to aggregate
            (ordered and with duplicate instances)
    Out:
        * Dictionary containing:
            genotypesList
            indices
    Notes:
        * Probably unnecessary, but here so that I don't forget the names
            of the dictionary labels.
    '''
    aggregationDictionary = {
        "genotypes": genotypesList,
        "indices": indicesList
    }
    return aggregationDictionary


def listDirectoriesInPath(path):
    """
    Description:
        * This auxiliary function returns the names of all the folders within
            a given path.
    In:
        * path: Directory address
    Out:
        * List of folder names
    Notes:
        * NA
    """
    file = os.listdir(path)
    folderNames = [
        name for name in file if os.path.isdir(os.path.join(path, name))
    ]
    return folderNames


def listDirectoriesWithPathWithinAPath(pathFilename):
    '''
    Description:
        * Returns a list of folder paths within a given path.
    In:
        * pathFilename: Path to search directories in
    Out:
        * List of folder paths
    Notes:
        * NA
    '''
    folders = listDirectoriesInPath(pathFilename)
    for i, folder in enumerate(folders):
        folders[i] = pathFilename + folder
    return folders


def getUniqueGenesFromGenotypes(
    genotypes
):
    """
    Description:
        * From a list of genotypes, returns the list of unique genes.
    In:
        * genotypes: List of genotypes present in the experiment.
    Out:
        * genesList: List of unique genes present.
    Notes:
        * Use in tandem with: readGenotypes
    """
    genesList = list({l for word in genotypes for l in word})
    return genesList


def readGenotypes(filename, skipColumns=1):
    '''
    Description:
        * Returns the genotypes header from an run file.
    In:
        * filename: Path to the run file
        * skipColumns: Optional argument for compatibility in the cases where
            the patch number is still present in the data.
    Out:
        * List of genotypes strings
    Notes:
        * NA
    '''
    reader = csv.reader(open(filename))
    return next(reader)[skipColumns:]


def splitExperimentString(experimentString):
    """
    Description:
        * Ad hoc auxiliary function to retrieve releases number and coverage
            from the folder name.
    In:
        * Experiment folder name.
    Out:
        * Dictionary containing:
            releasesNumber
            coverage
    Notes:
        * Not to be used in different experiments
    """
    split = experimentString.split("_")
    releasesNumber = int(split[3])
    coverage = int(split[4])
    return {"releasesNumber": releasesNumber, "coverage": coverage}


def calculateMaxPopInLandscapeReps(landscapeReps):
    """
    Description:
        * Returns the max population from a set of experiments in garbage
            folder.
    In:
        * landscapeReps: Dictionary with the info for the traces (garbage)
    Out:
        * maxPop: Maximum population found in the experiments.
    Notes:
        * Mainly developed to set the "y" axis range in traces plots.
    """
    landscapes = landscapeReps["landscapes"]
    list = [None] * len(landscapeReps["landscapes"][0])
    for i in range(len(landscapeReps["landscapes"][0])):
        list[i] = sum(landscapes[0][i][0])
    return max(list)


def getGenotypesWithPositions(genotypes, allelePositions):
    """
    Description:
        * Returns a list of indices corresponding to genotypes with a
            desired allelePosition
    In:
        * genotypes: List of genotype strings
        * allelePositions: List of (char, int) tuples (allele, index in
            genotype string)
    Out:
        * indices: Indices of strings in genotypes that have an allele in a
            specified position
    Notes:
        * Indices are repeated if they have multiple alleles in specified
            positions
    """
    indices = []
    for i in range(len(genotypes)):
        s = genotypes[i]
        for allele, index in allelePositions:
            if s[index] == allele:
                indices.append(i)
    return indices


def quickSaveTraceAggData(
    aggData,
    filename,
    fmt="%.10d"
):
    np.savetxt(
        filename,
        aggData["population"],
        header=(",".join(aggData["genotypes"])),
        delimiter=",",
        fmt=fmt,
        comments=''
    )


def quickSaveRepsAggData(
    landscapeReps,
    foldername,
    fmt="%.10d",
    padNumb=5
):
    if not os.path.exists(foldername):
        try:
            os.mkdir(foldername)
        except:
            raise OSError("Can't create destination directory (%s)!" %
                          (foldername))

    repsNumber = len(landscapeReps["landscapes"])
    for i in range(0, repsNumber):
        nodesNumber = len(landscapeReps["landscapes"][0])
        for j in range(0, nodesNumber):
            aggData = {
                "genotypes": landscapeReps["genotypes"],
                "population": (landscapeReps["landscapes"][i][j])
            }
            quickSaveTraceAggData(
                aggData,
                foldername + "/N" + str(j).rjust(padNumb, "0") +
                "_R" + str(i).rjust(padNumb, "0") + ".csv",
                fmt=fmt
            )
