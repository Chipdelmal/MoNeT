###############################################################################
# ______  __________________       _____       __________
# ___   |/  /_  ____/__  __ \_________(_)__   ____  ____/
# __  /|_/ /_  / __ __  / / /_  ___/_  /__ | / /_  __/
# _  /  / / / /_/ / _  /_/ /_  /   _  / __ |/ /_  /___
# /_/  /_/  \____/  /_____/ /_/    /_/  _____/ /_____/
###############################################################################
# Original file:
#     https://github.com/Chipdelmal/MoNeT/blob/master/GMLandscapeAnalysis/MCR_Aggregate_Gillian2.R
###############################################################################

###############################################################################
# Setup Sim ###################################################################
###############################################################################

###############################################################################
# Setup packages
###############################################################################
rm(list=ls());gc()
library(MGDrivE); library(MGDrivEv2); library(parallel);
NUM_CORES = 4
###############################################################################
# Experimental Setup and PATHS Definition
###############################################################################
# USER: {1: HS, 2: YJ}
USER = 1
SIM_TIME = 365 * 3
REPETITIONS = 4 * 2   # number of repetitions of each experiment
REPITER = 1           # number of groups of repetitions to perform
###############################################################################
if(USER==1){
  LANDSCAPE_PATH='/Volumes/marshallShare/Heterogeneity/Yunwen/Landscapes/'
  BASE_OUTPUT_PATH='/Volumes/marshallShare/Heterogeneity/Yunwen/Output/'
}else if(USER==2){
  LANDSCAPE_PATH='/Volumes/marshallShare/Heterogeneity/Yunwen/Landscapes/'
  BASE_OUTPUT_PATH='/Volumes/marshallShare/Heterogeneity/Yunwen/Output/'
}else{
  warning("invalid user!")
}
startTime = Sys.time()
###############################################################################
# Setup drive, release parameters, and biological parameters
###############################################################################
# constant population sizes
popSize = 20
RELEASE_NODE = 1
# biological parameters
bioParameters=list(
    tEgg=5, tLarva=6, tPupa=4, popGrowth=1.175, muAd=0.09, betaK=20
)
# gene drive is the same for all simulations
driveCube <-MGDrivE::cubeHomingDrive(
  cM=1, cF=1, chM=.95, chF=.95, crM=.95, crF=.95
)
# release parameters
releasesParameters=list(
  releasesStart=50, releasesNumber=1,
  eachreleasesInterval=7, releaseProportion=popSize
)
###############################################################################
# Factorial setup #############################################################
###############################################################################
# we are testing multiple landscapes, so we will loop over the landscapes in a folder
# The initial lines setup the experiment list, then the loop builds everything related
#  to each experiment.
landscapes <- list.files(path=LANDSCAPE_PATH, pattern="*.csv", full.names=TRUE)
Rep_names <- formatC(x=1:REPETITIONS, width=4, format="d", flag="0")
Iter_names <- formatC(x=1:REPITER, width=4, format="d", flag="0")
ExperimentList <- vector(mode="list", length=length(landscapes)*REPITER)
listmarker = 1
for(lscape in landscapes){
  ############################################################################
  # Setup output folders
  ############################################################################
  # create base directory
  lscapeName <- tail(x = strsplit(x = lscape, split = "[/,.]")[[1]], n = 2)[1]
  OUTPUT_DIRECTORY=file.path(BASE_OUTPUT_PATH, lscapeName)
  if(!dir.exists(OUTPUT_DIRECTORY)){ dir.create(OUTPUT_DIRECTORY) }
  # create holding/deleting directories
  SUB_DIRECTORES <- file.path(OUTPUT_DIRECTORY, c("RAW","ANALYZED","GARBAGE"))
  # build output directories
  for(folder in SUB_DIRECTORES){if(!dir.exists(folder)){dir.create(folder)}}
  # create iteration folders
  SUB_DIRECTORES <- outer(X = SUB_DIRECTORES, Y = Iter_names, FUN = "file.path")
  # build output directories
  for(folder in SUB_DIRECTORES){if(!dir.exists(folder)){ dir.create(folder) }}
  ############################################################################
  # Setup landscape
  ############################################################################
  # read in and setup landscape
  lFile <- as.matrix(read.csv(file=lscape, header=FALSE, sep=","))
  movementKernel = lFile
  # population from each patch
  popsNum = NROW(movementKernel)
  patchPops = rep(popSize, popsNum)
  # batch migration, just zero
  batchMigration <- MGDrivE::basicBatchMigration(
    batchProbs=0, sexProbs=c(.5,.5), numPatches=NROW(movementKernel)
  )
  ############################################################################
  # Things that depend on landscape info
  ############################################################################
  # all netPars the same
  netPar <- MGDrivE::parameterizeMGDrivE(
    runID=1, simTime=SIM_TIME,
    nPatch=NROW(movementKernel),
    beta=bioParameters$betaK, muAd=bioParameters$muAd,
    popGrowth=bioParameters$popGrowth, tEgg=bioParameters$tEgg,
    tLarva=bioParameters$tLarva, tPupa=bioParameters$tPupa,
    AdPopEQ=patchPops
  )
  # all releases the same
  patchReleases <- replicate(
    n=NROW(movementKernel),
    expr={list(maleReleases=NULL,femaleReleases=NULL,eggReleases=NULL)},
    simplify=FALSE
  )
  # replace with label of the cluster at 0, 0 + 1
  release_node <- RELEASE_NODE
  patchReleases[[release_node]]$maleReleases <- MGDrivE::generateReleaseVector(
    driveCube=driveCube, releasesParameters=releasesParameters, sex="M"
  )
  patchReleases[[release_node]]$femaleReleases <- MGDrivE::generateReleaseVector(
    driveCube=driveCube, releasesParameters=releasesParameters, sex="F"
  )
  ############################################################################
  # Loop over repetition groups
  ############################################################################
  for(iter in 1:REPITER){
    # Experiment Paths
    ExperimentList[[listmarker]]$folders <- SUB_DIRECTORES[ ,iter]
    # Seed for each experiment
    ExperimentList[[listmarker]]$randomSeed <- as.integer(sample(x = .Random.seed, size = 1, replace = FALSE) %% 2^31)
    # landscape
    ExperimentList[[listmarker]]$patchPops <- patchPops
    ExperimentList[[listmarker]]$movementKernel <- movementKernel
    ExperimentList[[listmarker]]$batchMigration <- batchMigration
    # things that depend on landscape info
    ExperimentList[[listmarker]]$netPar <- netPar
    ExperimentList[[listmarker]]$patchReleases <- patchReleases
    # increment list counter
    listmarker = listmarker + 1
  } # end loop over RepIterations
} # end loop over landscapes
###############################################################################
# Run Model ###################################################################
###############################################################################
cl=parallel::makePSOCKcluster(names=NUM_CORES)
parallel::clusterExport(cl=cl, varlist=c("Rep_names","driveCube"))
parallel::clusterEvalQ(cl=cl,expr={library(MGDrivE); library(MGDrivEv2)})
# Change ExperimentList_A to ExperimentList_B for second set of runs, comment out the subsetting stuff (Sept 29, 2018)
parallel::clusterApplyLB(cl = cl, x = ExperimentList, fun = function(x){
  # make folders
  for(i in c(3,1)){
    repFolders <- file.path(x$folders[i], Rep_names)
    for(folder in repFolders){ dir.create(path = folder) }
  }
  # run experiments
  MGDrivEv2::stochastic_multiple(
    seed=x$randomSeed, cubeR=driveCube, parametersR=x$netPar,
    migrationFemaleR=x$movementKernel, migrationMaleR=x$movementKernel,
    migrationBatchR=x$batchMigration, releasesR=x$patchReleases,
    output=repFolders, verbose=FALSE
  )
  # split and aggregate, save originals
  MGDrivEv2::SplitAggregateCpp(
    readDir = x$folders[1], writeDir = x$folders[3],
    simTime = x$netPar$simTime, numPatch = x$netPar$nPatch,
    genotypes = driveCube$genotypesID, remFiles = FALSE
  )
  # mean and quantiles, remove split/agg files
  MGDrivEv2::calcQuantilesCpp(
    readDirectory = x$folders[3], writeDirectory = x$folders[2],
    doMean=TRUE, quantiles=NULL,
    simTime = x$netPar$simTime, numPatch = x$netPar$nPatch,
    genotypes = driveCube$genotypesID, remFiles = FALSE
  )
  # remove raw folder
  unlink(x = x$folders[c(1)], recursive = TRUE, force = TRUE)
  gc()
})
###############################################################################
# Cleanup #####################################################################
###############################################################################
# stop cluster
parallel::stopCluster(cl)
# print time it took
print(difftime(time1 = Sys.time(), time2 = startTime))
# unload packages to be done
detach("package:MGDrivE", unload=TRUE)
detach("package:MGDrivEv2", unload=TRUE)
