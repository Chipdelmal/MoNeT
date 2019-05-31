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
# USER: {1: JB}
# NUM_CORES: Cores for the parallel threads
USER=2
REPETITIONS=10 # number of repetitions of each experiment
SIM_TIME=365*5
NUM_CORES=1


###############################################################################
if(USER==1){
  LANDSCAPE_PATH='~/Desktop/LANDSCAPES'
  BASE_OUTPUT_PATH="~/Desktop/HOLD/MGDrivE"
}else if(USER==2){
  LANDSCAPE_PATH='/Users/gillian/Desktop/marshall/MoNeT/GMLandscapeAnalysis/New_Format_Outputs'
  BASE_OUTPUT_PATH="/Users/gillian/Desktop/MGDrive-Experiments"
}else if(USER==3){
  LANDSCAPE_PATH=''
  BASE_OUTPUT_PATH=""
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
                        eachreleasesInterval=7, releaseProportion=10)


###############################################################################
### Factorial setup
###############################################################################
# we are testing multiple landscapes, so we will loop over the landscapes in a folder
# The initial lines setup the experiment list, then the loop builds everything related
#  to each experiment.
landscapes <- list.files(path = LANDSCAPE_PATH, pattern = "*.csv", full.names = TRUE)

Rep_names <- formatC(x = 1:REPETITIONS, width = 4, format = "d", flag = "0")
ExperimentList <- vector(mode = "list", length = length(landscapes))
listmarker=1

lscape = landscapes[3]

# read in and setup landscape
lFile <- read.csv(file = lscape, header = TRUE, sep = ",")
# population from each patch
ExperimentList[[listmarker]]$patchPops <- lFile$n
# movement, calculate distances, weight with an exponential kernal, pulse of pi
ExperimentList[[listmarker]]$movementKernel <- calc_HurdleExpKernel(distMat = outer(X = lFile$x, Y = lFile$x,
                                                                                    FUN = function(x,y){abs(x-y)}),
                                                                    r = MGDrivE::kernels$exp_rate,
                                                                    pi = stayProbability^(bioParameters$muAd))



#trial run
# trial_run = matrix(1:16, nrow = 4)
#another_one
#labels

# labels = matrix(nrow=4)
# labels[1,] = 1
# labels[2,] = 1
# labels[3,] = 2
# labels[4,] = 2
# tmp_matrix = matrix(nrow=length(unique(labels)), ncol=length(unique(labels)))
# counter = matrix(nrow=length(unique(labels)), ncol=length(unique(labels)))
# for (ii in 1:nrow(tmp_matrix)) 
# {
#   tmp_matrix[ii, ] <- 0
#   counter[ii, ] <- 0
# }
# 
# groupings = lFile$label[!duplicated(lFile$label)]
# for (i in 1:nrow(another_one)) 
# {
#   for (j in 1:ncol(another_one))
#   {
#     to_label = labels[i]
#     from_label = labels[j]
#     counter[to_label, from_label] = counter[to_label, from_label] + 1
#     tmp_matrix[to_label, from_label] = tmp_matrix[to_label, from_label] + another_one[i, j]
#   }
# }
# 
# for (i in 1:nrow(tmp_matrix)) 
# {
#   for (j in 1:ncol(tmp_matrix))
#   {
#     #number of nodes in the cluster
#     tmp_matrix[i, j] = tmp_matrix[i, j] / length(which(labels == i))
#   }
# }
# 

movement = ExperimentList[[1]]$movementKernel

update_movement_kernel <- function(movement, lFile) {
  
  labels = unique(lFile$label)
  ending_matrix = matrix(nrow=length(labels), ncol=length(labels))
  
  for (ii in 1:nrow(ending_matrix)) 
  {
    ending_matrix[ii, ] <- 0
  }
  
  labels = labels + 1
  
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


# May 1, 2019: 


# load a different population graph so I have more than just one node 
# ok so for every population I need to calculate the probability 
# 