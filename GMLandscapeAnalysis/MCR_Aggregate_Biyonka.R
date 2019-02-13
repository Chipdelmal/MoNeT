######################################################################################################
# ______  __________________       _____       __________
# ___   |/  /_  ____/__  __ \_________(_)__   ____  ____/
# __  /|_/ /_  / __ __  / / /_  ___/_  /__ | / /_  __/
# _  /  / / / /_/ / _  /_/ /_  /   _  / __ |/ /_  /___
# /_/  /_/  \____/  /_____/ /_/    /_/  _____/ /_____/
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# Confinable Drive System: MCR
######################################################################################################
### Setup packages ###################################################################################
######################################################################################################
rm(list=ls());gc()
#library(stringr)
library(MGDrivE)
library(MGDrivEv2)
library(parallel)
######################################################################################################
# Experimental Setup and PATHS Definition
######################################################################################################
# USER: {1: HMSC, 2: JB, 3: SLW, 4: Pusheen, 5: Valeri, 6: Gillian}
# GEOGRAPHY: TBD
# DRIVE_SYSTEM: {1: CRISPR (dummy), 2: MCR}
# NUM_CORES: Cores for the parallel threads
# TBD: {}
# TBD: {}
######################################################################################################
USER=8
#repetitions is number of times to run MGDRive on eeach patch
REPETITIONS=5
SIM_TIME=5*365
NUM_CORES=4
GEOGRAPHY=2
HDR_STEP= c(0.99) #c(0.65, 0.86, 0.99)
B_FITNESS= c(0.00) #c(0.4, 0.05)
H_FITNESS= c(0.00) #c(0.1)
DEPOSITION= c(0.00)  #c(0.75, 0.25)
######################################################################################################
# Select User ########################################################################################
######################################################################################################
if(USER==1){
  setwd("/Users/sanchez.hmsc/Documents/GitHub/MGDrivE/Main/AggregateLandscape/")
  BASE_OUTPUT_PATH="/Users/sanchez.hmsc/Desktop/AggregateLandscape/"
  BASE_GEO_PATH=paste0(getwd(),"/LineLocations/")
  BASE_DRIVE_PATH=paste0(getwd(),"/Drives/")
}else if(USER==2){
  setwd("~/Documents/MGDrivE/Main/AggregateLandscape/")
  BASE_OUTPUT_PATH="~/Desktop/HOLD/MGDrivE/"
  BASE_GEO_PATH=paste0(getwd(),"/LineLocations/")
  BASE_DRIVE_PATH=paste0(getwd(),"/Drives/")
}else if(USER==3){
  setwd("/Users/slwu89/Desktop/git/MGDrivE-V2/Main/AggregateLandscape/")
  BASE_OUTPUT_PATH="/Users/slwu89/Desktop/MGDrivEv2-Test/"
  BASE_GEO_PATH=paste0(getwd(),"/LineLocations/")
  BASE_DRIVE_PATH=paste0(getwd(),"/Drives/")
}else if(USER==4){
  setwd("/Users/sanchez.hmsc/Documents/GitHub/MGDrivE_v2/Main/AggregateLandscape/")
  BASE_OUTPUT_PATH="/Users/sanchez.hmsc/Desktop/AggregateLandscape/"
  BASE_GEO_PATH=paste0(getwd(),"/LineLocations/")
  BASE_DRIVE_PATH=paste0(getwd(),"/Drives/")
}else if(USER==5){
  setwd("/home/valeri/MGDrivE/Main/AggregateLandscape/")
  BASE_OUTPUT_PATH=  "/Tuatara/" #"/Kauri/"
  BASE_GEO_PATH=paste0(getwd(),"/LineLocations/")
  BASE_DRIVE_PATH=paste0(getwd(),"/Drives/")
}else if(USER==6){
  setwd("/Users/gillianchu/marshall/MGDrivE/Main/AggregateLandscape")
  BASE_OUTPUT_PATH="/Users/gillianchu/Desktop/MGDrive-Experiments/"
  BASE_GEO_PATH=paste0(getwd(),"/LineLocations/")
  BASE_DRIVE_PATH=paste0(getwd(),"/Drives/")
}else if(USER==7){
  setwd("/Users/mayashen/Desktop/MGDrivE/Main/GMLandscapeAnalysis")
  BASE_OUTPUT_PATH="/Users/mayashen/Desktop/Marshall_MCR_Agg/"
  #BASE_GEO_PATH=paste0(getwd(),"/LineLocations/")
  BASE_DRIVE_PATH=paste0(getwd(),"/Drives/")
}else if(USER==8){
  setwd("/Users/Biyonka/MGDrivE/Main/GMLandscapeAnalysis")
  BASE_OUTPUT_PATH="/Users/Biyonka/Desktop/Output"
  BASE_DRIVE_PATH=paste0(getwd(),"/Drives/")
  }else{
  warning("invalid user!")
}
source("./Auxiliary.R")
startTime=Sys.time()
######################################################################################################
# Experimental Setup #################################################################################
######################################################################################################
RELEASE_INTERVAL=7
RELEASES_START=150
RELEASES_NUMBER=1
RELEASES_RATIO=10
bioParameters=list(betaK=20,tEgg=5,tLarva=6,tPupa=4,popGrowth=1.175,muAd=0.09)
stayProbability=.72
######################################################################################################
### Landscape ########################################################################################
######################################################################################################
heterogFile=read.csv(paste0("/Users/Biyonka/Desktop/Output/spaHet/","output.csv"),sep=",",header=TRUE)
  #read.csv(paste0("/Users/Biyonka/Downloads/","0.csv"),sep=",",header=FALSE)
#geoFile=paste0(BASE_GEO_PATH,"halfAggregationCoord.csv")
#number of x coordinates manages number of patches
geo=heterogFile$x#V1
pop=heterogFile$n#V3
landscape=setupLandscapeMatrix(geo,pop,stayProbability,bioParameters$muAd)
siteIDMin=1
siteIDMax=1
######################################################################################################
### Gene Drive #######################################################################################
######################################################################################################

# need this for release function.
driveCube <- MGDrivE::Cube_HomingDrive()

# all releases the same
releasesParameters=list(
  releasesStart=RELEASES_START,releasesNumber=RELEASES_NUMBER,
  releasesInterval=RELEASE_INTERVAL,releaseProportion=RELEASES_RATIO
)
patchReleases=replicate(n=landscape$sitesNumber,expr={list(maleReleases=NULL,femaleReleases=NULL,eggReleases=NULL)},simplify=FALSE)
patchReleases[[1]]$maleReleases=generateReleaseVector(driveCube=driveCube,releasesParameters=releasesParameters,sex="M")
patchReleases[[1]]$femaleReleases=generateReleaseVector(driveCube=driveCube,releasesParameters=releasesParameters,sex="F")

# all netPars the same
netPar=Network.Parameters(
  runID=1,simTime=SIM_TIME,nPatch=landscape$sitesNumber,
  beta=bioParameters$betaK,muAd=bioParameters$muAd,popGrowth=bioParameters$popGrowth,
  tEgg=bioParameters$tEgg,tLarva=bioParameters$tLarva,tPupa=bioParameters$tPupa,
  AdPopEQ=landscape$patchPops
)

# create base directory
OUTPUT_DIRECTORY=BASE_OUTPUT_PATH
if(!dir.exists(OUTPUT_DIRECTORY)){ dir.create(OUTPUT_DIRECTORY) }

# create holding/deleting directories
SUB_DIRECTORES <- vector(mode = "character", length = 3)
extension <- c("RAW","ANALYZED","GARBAGE")
for(folder in 1:3){
  SUB_DIRECTORES[folder] <- file.path(OUTPUT_DIRECTORY,
                                      file.path(gsub(pattern = "-", replacement = "_", x = Sys.Date(), fixed = TRUE),
                                                extension[folder], fsep = "_")
  )

  if(!dir.exists(SUB_DIRECTORES[folder])){ dir.create(SUB_DIRECTORES[folder]) }
}
######################################################################################################
### Factorial setup ##################################################################################
######################################################################################################
Rep_names <- formatC(x = 1:REPETITIONS, width = 4, format = "d", flag = "0")
ExperimentList <- vector(mode = "list", length = length(HDR_STEP)*length(DEPOSITION)*length(H_FITNESS)*length(B_FITNESS))

listmarker=1
for(HDR_S in HDR_STEP){
  for(DEP in DEPOSITION){
    for(H_F in H_FITNESS){
      for(B_F in B_FITNESS){

        # three base file paths
        ExperimentList[[listmarker]]$folders <- file.path(SUB_DIRECTORES, file.path("E",
                                                                                    formatC(x = HDR_S*100, width = 3, format = "d", flag = "0"),
                                                                                    formatC(x = DEP*100, width = 3, format = "d", flag = "0"),
                                                                                    formatC(x = H_F*100, width = 3, format = "d", flag = "0"),
                                                                                    formatC(x = B_F*100, width = 3, format = "d", flag = "0"),
                                                                                    fsep = "_"))

        # random seed for each
        ExperimentList[[listmarker]]$randomSeed <- as.integer(sample(x = .Random.seed, size = 1, replace = FALSE) %% 2^31)

        # drive cube homing rates
        ExperimentList[[listmarker]]$e <- 1.0
        ExperimentList[[listmarker]]$r <- 1.0*(1-HDR_S)*0.15
        ExperimentList[[listmarker]]$b <- 1.0*(1-HDR_S)*(1-0.15)
        ExperimentList[[listmarker]]$eD <- DEP
        ExperimentList[[listmarker]]$rD <- DEP*0.05
        ExperimentList[[listmarker]]$bD <- DEP*(1-0.05)

        # drive cube costs
        ExperimentList[[listmarker]]$H <- 1-H_F
        ExperimentList[[listmarker]]$B <- 1-B_F

        listmarker = listmarker + 1
      }# end fitness loop
    }# end H fitness loop
  }# end female deposition loop
}# end homing loop


######################################################################################################
### Run Model ########################################################################################
######################################################################################################
cl=parallel::makePSOCKcluster(names=NUM_CORES)
parallel::clusterExport(
  cl=cl,
  varlist=c(
    "landscape","patchReleases","netPar","Rep_names"
  )
)
parallel::clusterEvalQ(cl=cl,expr={
  library(MGDrivE)
  library(MGDrivEv2)
})


# Change ExperimentList_A to ExperimentList_B for second set of runs, comment out the subsetting stuff (Sept 29, 2018)
parallel::clusterApplyLB(cl = cl, x = ExperimentList, fun = function(x){

  # make run folders
  for(i in x$folders){
    dir.create(path = i)
  }

  # make folders
  for(i in c(3,1)){
    repFolders <- file.path(x$folders[i], Rep_names)
    for(folder in repFolders){ dir.create(path = folder) }
  }

  driveCube <- MGDrivE::Cube_HomingDrive()#eM = x$e, eF = x$e, rM = x$r, bM = x$b,
                                         #rF = x$r, bF = x$b, eD = x$eD, rD = x$rD, bD = x$bD,
                                         #eta = c("WH"=x$H,"WB"=x$B,"HH"=x$H*x$H,"HR"=x$H,"HB"=x$H*x$B,"RB"=x$B,"BB"=x$B*x$B),
                                         #s = c("WH"=x$H,"WB"=x$B,"HH"=x$H*x$H,"HR"=x$H,"HB"=x$H*x$B,"RB"=x$B,"BB"=x$B*x$B))


  MGDrivEv2::stochastic_multiple(
    seed=x$randomSeed,
    cubeR=driveCube,
    parametersR=netPar,
    migrationFemaleR=landscape$movementKernel,
    migrationMaleR=landscape$movementKernel,
    migrationBatchR=landscape$batchMigration,
    releasesR=patchReleases,
    output=repFolders,
    verbose=FALSE
  )

  # split and aggregate, save originals
  MGDrivEv2::SplitAggregateCpp(readDir = x$folders[1], writeDir = x$folders[3],
                               simTime = netPar$simTime, numPatch = netPar$nPatch,
                               genotypes = driveCube$genotypesID, remFiles = FALSE)

  # mean and quantiles, remove split/agg files
  MGDrivEv2::AnalyzeQuantilesCpp(readDirectory = x$folders[3], writeDirectory = x$folders[2],
                                 doMean=TRUE, quantiles=NULL,
                                 simTime = netPar$simTime, numPatch = netPar$nPatch,
                                 genotypes = driveCube$genotypesID, remFiles = TRUE)

  # remove garbage folder
  unlink(x = x$folders[3], recursive = TRUE, force = TRUE)
  gc()

})

# stop cluster
parallel::stopCluster(cl)

# remove garbage directory
unlink(x = SUB_DIRECTORES[3], recursive = TRUE, force = TRUE)

endTime=Sys.time()
cat(paste0(startTime," - ",endTime,"\n"))
endTime - startTime

detach("package:MGDrivE", unload=TRUE)
detach("package:MGDrivEv2", unload=TRUE)

#output is a file for each habitat/patch, that tracks the number of mosquitos in each habitat 
#that have each genotype for each time in the gene drive
