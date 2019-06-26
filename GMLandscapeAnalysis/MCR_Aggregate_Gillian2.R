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
#library(MGDrivE)
#library(MGDrivEv2)
#library(parallel)
library(markovchain)
###############################################################################
### Experimental Setup and PATHS Definition
###############################################################################
# USER: {1: JB, 2: Maya, 3: Gillian}
# NUM_CORES: Cores for the parallel threads
USER=4
REPETITIONS=50 # number of repetitions of each experiment
REPITER=1 # number of groups of repetitions to perform, for analysis purposes ONLY BIYONKA SHOULD NEED THIS,
SIM_TIME=365*3
NUM_CORES=4

###############################################################################
if(USER==1){
  LANDSCAPE_PATH='~/Desktop/Output/1clustering_analysis'
  BASE_OUTPUT_PATH="~/Desktop/Output/1clustering_analysis/drive_output"
}else if(USER==2){
  LANDSCAPE_PATH='~/Desktop/popHeterog_csv/test'
  BASE_OUTPUT_PATH="~/Desktop/Marshall_Simulations"
}else if(USER==3){
  LANDSCAPE_PATH='/Users/gillian/Desktop/marshall/MoNeT/GMLandscapeAnalysis/2d_outputs'
  BASE_OUTPUT_PATH="/Users/gillian/Desktop/MGDrive-Experiments"
}else if(USER==4){
  LANDSCAPE_PATH="~/Desktop/OUTPUT/LANDSCAPES/"
  BASE_OUTPUT_PATH="~/Desktop/OUTPUT/GILLIAN/"
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
# biological parameters
bioParameters=list(betaK=20,tEgg=5,tLarva=6,tPupa=4,popGrowth=1.175,muAd=0.09)
# daily probs for staying in one patch
stayProbability=.72
# gene drive is the same for all simulations
driveCube <-MGDrivE::cubeHomingDrive(cM=1, cF=1, chM=.95, chF=.95, crM=.95, crF=.95)
# release parameters
releasesParameters=list(releasesStart=50, releasesNumber=1,
                        eachreleasesInterval=7, releaseProportion=5)

###############################################################################
### Clustering Movement Kernel Update
###############################################################################

update_movement_kernel <- function(movement, lFile) {

  # get labels, store num for later
  #  These are zero indexed, and R is 1 indexed, but that isn't a problem
  labels = sort.int(x = unique(lFile$label), method = "radix")
  numLab <- length(x = labels)

  # setup return matrix
  ending_matrix = matrix(data = 0, nrow=numLab, ncol=numLab) # default to zero, no need to fill

  # get all patches that fall under each label
  index <- lapply(X = labels, FUN = function(x){which(lFile$label == x)})

  # get the number of patches in each label for normalization later
  normVal <- vapply(X = index, FUN = 'length', FUN.VALUE = 1)

  # loop over rows
  # loop runs for number of groups in labels
  for(i in 1:numLab){
    # store row index
    rowIndex <- index[[i]]

    # loop over columns
    for(j in 1:numLab){
      # perform subset and sum in one stet
      ending_matrix[i,j] <- sum(movement[rowIndex, index[[j]]])
    }

    # normalize, vectorized over row
    ending_matrix[i, ] <- ending_matrix[i, ] / normVal[i]

  } # end loop over rows

  return(ending_matrix)
}

###############################################################################
### Clustering Population Update
###############################################################################
update_population <- function(patchPops, lFile) {
  newPops <- numeric(length = length(unique(lFile$label)) )
  
  for (ii in 1:nrow(lFile)){
    curr_label <- lFile$label[ii] + 1L
    newPops[curr_label] <- newPops[curr_label] + lFile$n[ii]
  }
  
  # This is effectively what is happening
  #  we are aggregating lFile$n by values in lFile$label
  #newPops <-aggregate(lFile$n ~ lFile$label, FUN = sum)
  
  return(newPops)
}


###############################################################################
### Compare Transition Matrices
###############################################################################
compare_matrices <- function(movementKernel, new_moves) {
  statesNamesA <- as.character(seq(1, length(movementKernel[1,]), by=1))
  statesNamesB <- as.character(seq(1, length(new_moves[1,]), by=1))
  markovA <- new("markovchain", states = statesNamesA, transitionMatrix =movementKernel,
                 name = "Old MC to Check")
  markovB <- new("markovchain", states = statesNamesB, transitionMatrix =new_moves,
                 name = "New MC to Check")
  stationary_old <- steadyStates(markovA)
  stationary_new <- steadyStates(markovB)

  comparable <- vector("numeric", length(stationary_new))
  for (k in 1:length(comparable))
  {
    comparable[k] = 0
  }
  for (j in 1:length(stationary_old))
  {
    label = lFile[j, "label"] + 1
    comparable[label] = comparable[label] + stationary_old[j]
  }
  print(stationary_new)
  print(comparable)
}

###############################################################################
### Check All Rows in the Movement Kernel Sum to 1
###############################################################################
kernel_check_sum_one <- function(movement) {
  a = rowSums(movement)
  not_all_sum_one = 0
  for (j in 1:length(a)) {
    if (a[j] != 1){
      print("Row does not sum to 1.")
      not_all_sum_one = 1
    }
  }
  if (not_all_sum_one == 1) {
    print("One of the rows does not sum to 1.")
  } else {
    print("All rows sum to 1.")
  }
}


# kernel_check_sum_one2 <- function(movement) {
#   a = rowSums(movement)
#   
#   if(sum(a) != dim(movement)[1]){
#     cat("Rows", which(a != 1), "do not sum to 1.\n")
#   } else {
#     cat("All rows sum to 1.\n")
#   }
# 
# }


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






# lscape <- landscapes[3]
# # read in and setup landscape
# lFile <- read.csv(file = lscape, header = TRUE, sep = ",")
# # population from each patch
# patchPops <- lFile$n
# # movement, calculate distances, weight with an exponential kernal, pulse of pi
# movementKernel <- MGDrivE::calcHurdleExpKernel(distMat = outer(X = lFile$x, Y = lFile$x,
#                                                        FUN = function(x,y){abs(x-y)}),
#                                        r = MGDrivE::kernels$exp_rate,
#                                        pi = stayProbability^(bioParameters$muAd))
# 
# write.csv(movementKernel, 'movementKernel.csv')
# new_moves <- update_movement_kernel(movementKernel, lFile)
# #new_moves <- new_moves/rowSums(new_moves)
# compare_matrices(movementKernel, new_moves)
# 
# patchPops









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
  movementKernel <- MGDrivE::calcHurdleExpKernel(distMat = outer(X = lFile$x, Y = lFile$x,
                                                         FUN = function(x,y){abs(x-y)}),
                                         r = MGDrivE::kernels$exp_rate,
                                         pi = stayProbability^(bioParameters$muAd))
  # lumped transition matrix
  movementKernel <- update_movement_kernel(movementKernel, lFile)

  # lumped populations
  #typeof(patchPops) # don't need?
  patchPops <- update_population(patchPops, lFile)

  # batch migration, just zero
  batchMigration <- MGDrivE::basicBatchMigration(batchProbs=0,sexProbs=c(.5,.5),
                                        numPatches=NROW(movementKernel))

  ####################
  # things that depend on landscape info
  ####################
  # all netPars the same
  netPar <- MGDrivE::parameterizeMGDrivE(runID=1,simTime=SIM_TIME,
                               nPatch=NROW(movementKernel),
                               beta=bioParameters$betaK, muAd=bioParameters$muAd,
                               popGrowth=bioParameters$popGrowth,tEgg=bioParameters$tEgg,
                               tLarva=bioParameters$tLarva, tPupa=bioParameters$tPupa,
                               AdPopEQ=patchPops)

  # all releases the same
  patchReleases <- replicate(n=NROW(movementKernel),
                             expr={list(maleReleases=NULL,femaleReleases=NULL,eggReleases=NULL)},
                             simplify=FALSE)

  # replace with label of the cluster at 0, 0 + 1
  release_node <- as.numeric(lFile$label[1] + 1)
  patchReleases[[release_node]]$maleReleases <- MGDrivE::generateReleaseVector(driveCube=driveCube,releasesParameters=releasesParameters,sex="M")
  patchReleases[[release_node]]$femaleReleases <- MGDrivE::generateReleaseVector(driveCube=driveCube,releasesParameters=releasesParameters,sex="F")


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


for(i in ExperimentList)
{
  print(dim(i$movementKernel))
}
# Change ExperimentList_A to ExperimentList_B for second set of runs, comment out the subsetting stuff (Sept 29, 2018)
parallel::clusterApplyLB(cl = cl, x = ExperimentList, fun = function(x){

  # make folders
  for(i in c(3,1)){
    repFolders <- file.path(x$folders[i], Rep_names)
    for(folder in repFolders){ dir.create(path = folder) }
  }

#  print(dim(x$movementKernel))

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
  MGDrivEv2::calcQuantilesCpp(readDirectory = x$folders[3], writeDirectory = x$folders[2],
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
#detach("package:MGDrivE", unload=TRUE)
#detach("package:MGDrivEv2", unload=TRUE)




