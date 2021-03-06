###############################################################################################################
# ______  __________________       _____       __________
# ___   |/  /_  ____/__  __ \_________(_)__   ____  ____/
# __  /|_/ /_  / __ __  / / /_  ___/_  /__ | / /_  __/
# _  /  / / / /_/ / _  /_/ /_  /   _  / __ |/ /_  /___
# /_/  /_/  \____/  /_____/ /_/    /_/  _____/ /_____/
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# Kernels calculator: Works in tandem with SHPtoCSV.R
# Kernels parameters calculated by: Partow Imani
###############################################################################################################
######################### LOAD AND SETUP PACKAGES #############################################################
rm(list=ls());gc()
library(MGDrivE)
library(MGDrivEv2)
###############################################################################################################
######################### SETUP PATHS #########################################################################
user = system(command = "whoami",intern = TRUE)
if(user == "sanchez.hmsc"){
  setwd("/Users/sanchez.hmsc/Documents/GitHub/MoNeT/")
  outputPath="./OSMnx/"
}
outputFolderDistances="./DistancesAnalysis/"
outputFolderGeo="./OSMnx/"
###############################################################################################################
######################### SETUP LANDSCAPE AND BIOLOGY #########################################################
placeLabel="YorkeyTrinity"
bioParameters=list(betaK=2*10,tEgg=5,tLarva=6,tPupa=4,popGrowth=1.175,muAd=.09)
lifespanStayProbability=.90
###############################################################################################################
###############################################################################################################
rawGeoData=as.matrix(read.csv(paste0(outputFolderGeo,"POINTS/",placeLabel,"_LatLongs.csv"),sep=",",header=FALSE))
latLongs=as.matrix(rawGeoData)
distancesMatrix=calc_haversine(latLongs)
write.table(distancesMatrix,file=paste0(outputPath,"DISTANCES/",placeLabel,"_Distances.csv"),row.names=FALSE,col.names=FALSE,sep=",")
###############################################################################################################
pulseHeight=lifespanStayProbability^(bioParameters$muAd)
movementKernel=calc_HurdleExpKernel(distancesMatrix,MGDrivE::kernels$exp_rat,pulseHeight)
write.table(movementKernel,file=paste0(outputFolderGeo,"KERNELS/",placeLabel,"_Kernel.csv"),row.names=FALSE,col.names=FALSE,sep=",")
###############################################################################################################
######################### ANALYZE MINIMUM DISTANCES ###########################################################
diag(distancesMatrix)=100000000
minDistances=apply(distancesMatrix,1,min)
minDistancesDF=as.data.frame(minDistances)
meanDistance=median(minDistances)
base=ggplot(data=minDistancesDF,aes(x=minDistances)) + xlab("Minimum Distance") + ylab("Density") + ggtitle(placeLabel,subtitle=paste0("Median: ",meanDistance))
base + geom_density(alpha=.2, fill="#FF6666") + geom_vline(aes(xintercept=meanDistance),linetype="dashed",size=.5)
ggsave(paste0(outputFolderDistances,"images/",placeLabel,"_minDistances.pdf"),width=10,height=10)




###############################################################################################################
###############################################################################################################
# TESTS FOR ANOPHELES IN MADAGASCAR
###############################################################################################################
###############################################################################################################

######################### SETUP LANDSCAPE AND BIOLOGY #########################################################
placeLabel="Madagascar"
bioParameters=list(betaK=2*10,tEgg=5,tLarva=6,tPupa=4,popGrowth=1.175,muAd=.09)
lifespanStayProbability=.90
###############################################################################################################
###############################################################################################################
rawGeoData=as.matrix(read.csv(paste0(outputFolderGeo,"POINTS/",placeLabel,"_Coordinates.csv"),sep=",",header=FALSE))
latLongs=as.matrix(rawGeoData)
distancesMatrix=calc_haversine(latLongs)
#write.table(distancesMatrix,file=paste0(outputPath,"DISTANCES/",placeLabel,"_Distances.csv"),row.names=FALSE,col.names=FALSE,sep=",")
###############################################################################################################
pulseHeight=lifespanStayProbability^(bioParameters$muAd)
movementKernel=calc_HurdleExpKernel(distancesMatrix,MGDrivE::kernels$exp_rate/250,pulseHeight)
write.table(movementKernel,file=paste0(outputFolderGeo,"KERNELS/",placeLabel,"_Kernel.csv"),row.names=FALSE,col.names=FALSE,sep=",")
###############################################################################################################
######################### ANALYZE MINIMUM DISTANCES ###########################################################
diag(distancesMatrix)=100000000
minDistances=apply(distancesMatrix,1,min)
minDistancesDF=as.data.frame(minDistances)
meanDistance=median(minDistances)
base=ggplot(data=minDistancesDF,aes(x=minDistances)) + xlab("Minimum Distance") + ylab("Density") + ggtitle(placeLabel,subtitle=paste0("Median: ",meanDistance))
base + geom_density(alpha=.2, fill="#FF6666") + geom_vline(aes(xintercept=meanDistance),linetype="dashed",size=.5)
ggsave(paste0(outputFolderDistances,"images/",placeLabel,"_minDistances.pdf"),width=10,height=10)

diag(movementKernel)=0
apply(movementKernel,1,max)
