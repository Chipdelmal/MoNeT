###############################################################################
# ______  __________________       _____       __________
# ___   |/  /_  ____/__  __ \_________(_)__   ____  ____/
# __  /|_/ /_  / __ __  / / /_  ___/_  /__ | / /_  __/
# _  /  / / / /_/ / _  /_/ /_  /   _  / __ |/ /_  /___
# /_/  /_/  \____/  /_____/ /_/    /_/  _____/ /_____/
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# Hector landscape exploration script
###############################################################################
### Setup packages
###############################################################################
rm(list=ls());gc()
library(MGDrivE)
library(MGDrivEv2)
library(parallel)
###############################################################################
### Experimental Setup and PATHS Definition
###############################################################################
# USER: {1: JB, 2: Maya, 3: Gillian}
# NUM_CORES: Cores for the parallel threads
USER=3
REPETITIONS=8 # number of repetitions of each experiment
REPITER=1 # number of groups of repetitions to perform, for analysis purposes ONLY BIYONKA SHOULD NEED THIS,
SIM_TIME=365*4
NUM_CORES=8

###############################################################################
if(USER==1){
  LANDSCAPE_PATH='~/Desktop/Output/1clustering_analysis'
  BASE_OUTPUT_PATH="~/Desktop/Output/1clustering_analysis/drive_output"
}else if(USER==2){
  LANDSCAPE_PATH='~/Desktop/popHeterog_csv/test'
  BASE_OUTPUT_PATH="~/Desktop/Marshall_Simulations"
}else if(USER==3){
  LANDSCAPE_PATH='/Users/gillian/Desktop/marshall/MoNeT/GMLandscapeAnalysis/New_Format_Outputs'
  BASE_OUTPUT_PATH="/Users/gillian/Desktop/MGDrive-Experiments"
}else if(USER==4){
  LANDSCAPE_PATH=''
  BASE_OUTPUT_PATH=""
}else if(USER==5){
  LANDSCAPE_PATH=''
  BASE_OUTPUT_PATH= ""
}else{
  warning("invalid user!")
}

startTime=Sys.time()


###############################################################################
### Setup drive, release parameters, and biological parameters
###############################################################################
# bioligcal parameters
bioParameters=list(betaK=20,tEgg=5,tLarva=6,tPupa=4,popGrowth=1.175,muAd=0.09)
# daily probs for staying in one patch
stayProbability=.72
# gene drive is the same for all simulations
driveCube <-MGDrivE::Cube_HomingDrive(cM=1, cF=1, chM=.95, chF=.95, crM=.95, crF=.95)
# release parameters
releasesParameters=list(releasesStart=50, releasesNumber=1,
                        eachreleasesInterval=7, releaseProportion=5)

###############################################################################
### Clustering Movement Kernel Update
###############################################################################
update_movement_kernel <- function(movement, lFile) {
  labels = unique(lFile$label)+1
  ending_matrix = matrix(nrow=length(labels), ncol=length(labels))
  for (ii in 1:nrow(ending_matrix)) 
  {
    ending_matrix[ii, ] <- 0
  }
  for (i in 1:nrow(movement)) 
  {
    for (j in 1:ncol(movement))
    {
      from_label = lFile[i, "label"]
      to_label = lFile[j, "label"]
      ending_matrix[from_label, to_label] = ending_matrix[from_label, to_label] + movement[i, j]
    }
  }
  for (i in 1:nrow(ending_matrix)) 
  {
    for (j in i:ncol(ending_matrix))
    {
      ending_matrix[i, j] = ending_matrix[i, j] / length(which(lFile$label == i))
    }
  }
}


###############################################################################
### Factorial setup
###############################################################################
# we are testing multiple landscapes, so we will loop over the landscapes in a folder
# The initial lines setup the experiment list, then the loop builds everything related
#  to each experiment.
landscapes <- list.files(path = LANDSCAPE_PATH, pattern = "*.csv", full.names = TRUE)

Rep_names <- formatC(x = 1:REPETITIONS, width = 4, format = "d", flag = "0")
Iter_names <- formatC(x = 1:REPITER, width = 4, format = "d", flag = "0")
ExperimentList <- vector(mode = "list", length = length(landscapes)*REPITER)
listmarker=1

lscape <- landscapes[1]
# read in and setup landscape
lFile <- read.csv(file = lscape, header = TRUE, sep = ",")
# population from each patch
patchPops <- lFile$n
# movement, calculate distances, weight with an exponential kernal, pulse of pi
movementKernel <- calc_HurdleExpKernel(distMat = outer(X = lFile$x, Y = lFile$x,
FUN = function(x,y){abs(x-y)}),
r = MGDrivE::kernels$exp_rate,
pi = stayProbability^(bioParameters$muAd))
movementKernel <- update_movement_kernel(movementKernel, lFile)
for(lscape in landscapes){

  ####################
  # setup output folders
  ####################
  # create base directory
  lscapeName <- tail(x = strsplit(x = lscape, split = "[/,.]")[[1]], n = 2)[1]
  OUTPUT_DIRECTORY=file.path(BASE_OUTPUT_PATH, lscapeName)
  if(!dir.exists(OUTPUT_DIRECTORY)){ dir.create(OUTPUT_DIRECTORY) }

  # create holding/deleting directories
  SUB_DIRECTORES <- file.path(OUTPUT_DIRECTORY,c("RAW","ANALYZED","GARBAGE"))

  # build output directories
  for(folder in SUB_DIRECTORES){if(!dir.exists(folder)){ dir.create(folder) }}

  # create iteration folders
  SUB_DIRECTORES <- outer(X = SUB_DIRECTORES, Y = Iter_names, FUN = "file.path")

  # build output directories
  for(folder in SUB_DIRECTORES){if(!dir.exists(folder)){ dir.create(folder) }}

  ####################
  # setup landscape
  ####################
  # read in and setup landscape
  lFile <- read.csv(file = lscape, header = TRUE, sep = ",")
  # population from each patch
  patchPops <- lFile$n
  # movement, calculate distances, weight with an exponential kernal, pulse of pi
  movementKernel <- calc_HurdleExpKernel(distMat = outer(X = lFile$x, Y = lFile$x,
                                         FUN = function(x,y){abs(x-y)}),
                                         r = MGDrivE::kernels$exp_rate,
                                         pi = stayProbability^(bioParameters$muAd))
  # batch migration, just zero
  batchMigration <- basicBatchMigration(batchProbs=0,sexProbs=c(.5,.5),
                                        numPatches=NROW(movementKernel))


  ####################
  # things that depend on landscape info
  ####################
  # all netPars the same
  netPar <- Network.Parameters(runID=1,simTime=SIM_TIME,
                                                         nPatch=NROW(movementKernel),
                                                         beta=bioParameters$betaK, muAd=bioParameters$muAd,
                                                         popGrowth=bioParameters$popGrowth,tEgg=bioParameters$tEgg,
                                                         tLarva=bioParameters$tLarva, tPupa=bioParameters$tPupa,
                                                         AdPopEQ=patchPops)

  # all releases the same
  patchReleases <- replicate(n=NROW(movementKernel),
                             expr={list(maleReleases=NULL,femaleReleases=NULL,eggReleases=NULL)},
                             simplify=FALSE)
  patchReleases[[1]]$maleReleases <- generateReleaseVector(driveCube=driveCube,releasesParameters=releasesParameters,sex="M")
  patchReleases[[1]]$femaleReleases <- generateReleaseVector(driveCube=driveCube,releasesParameters=releasesParameters,sex="F")


  ####################
  # loop over repetition groups
  ####################
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
### Run Model
###############################################################################
cl=parallel::makePSOCKcluster(names=NUM_CORES)
parallel::clusterExport(
  cl=cl,
  varlist=c("Rep_names","driveCube"
  )
)
parallel::clusterEvalQ(cl=cl,expr={
  library(MGDrivE)
  library(MGDrivEv2)
})


# Change ExperimentList_A to ExperimentList_B for second set of runs, comment out the subsetting stuff (Sept 29, 2018)
parallel::clusterApplyLB(cl = cl, x = ExperimentList, fun = function(x){

  # make folders
  for(i in c(3,1)){
    repFolders <- file.path(x$folders[i], Rep_names)
    for(folder in repFolders){ dir.create(path = folder) }
  }

  # run experiments
  MGDrivEv2::stochastic_multiple(
    seed=x$randomSeed,
    cubeR=driveCube,
    parametersR=x$netPar,
    migrationFemaleR=x$movementKernel,
    migrationMaleR=x$movementKernel,
    migrationBatchR=x$batchMigration,
    releasesR=x$patchReleases,
    output=repFolders,
    verbose=FALSE
  )

  # split and aggregate, save originals
  MGDrivEv2::SplitAggregateCpp(readDir = x$folders[1], writeDir = x$folders[3],
                               simTime = x$netPar$simTime, numPatch = x$netPar$nPatch,
                               genotypes = driveCube$genotypesID, remFiles = FALSE)

  # mean and quantiles, remove split/agg files
  MGDrivEv2::AnalyzeQuantilesCpp(readDirectory = x$folders[3], writeDirectory = x$folders[2],
                                 doMean=TRUE, quantiles=NULL,
                                 simTime = x$netPar$simTime, numPatch = x$netPar$nPatch,
                                 genotypes = driveCube$genotypesID, remFiles = FALSE)

  # remove raw/garbage folders
  #unlink(x = x$folders[c(1,3)], recursive = TRUE, force = TRUE)
  gc()

})

# stop cluster
parallel::stopCluster(cl)

# print time it took
print(difftime(time1 = Sys.time(), time2 = startTime))

# unload packages to be done
detach("package:MGDrivE", unload=TRUE)
detach("package:MGDrivEv2", unload=TRUE)




