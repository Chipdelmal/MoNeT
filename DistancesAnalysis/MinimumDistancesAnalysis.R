################################################################################
# ╔╦╗┌─┐╔╗╔┌─┐╔╦╗
# ║║║│ │║║║├┤  ║
# ╩ ╩└─┘╝╚╝└─┘ ╩
# Mosquito Networks Taskforce
# Minimum distances calculator to scale maps
################################################################################
rm(list=ls());gc()
library(maptools)
library(shapefiles)
library(ggplot2)
library(viridis)
library(MGDrivE)
library(MGDrivEv2)
library(igraph)
library(rgdal)
################################################################################
# Select the name tag of the location (same as the one used in the OSMnx parser)
# Setup your MoNeT base directory
placeNameTag="YorkeysKnob"
setwd("~/Documents/GitHub/MoNeT/")
outputFolder="./Dev/HectorSanchez/DistancesAnalysis/"
################################################################################
# Read shapefile
shapeFile=read.shp(paste0("./OSMnx/RoadsAndBuildingsParser/SHP/Buildings/",placeNameTag,"/",placeNameTag,".shp"))
################################################################################
# Calculate the centroids of the buildings polygons and store as matrix
latLongsVoid=vector("list",length(shapeFile$shp))
latLongs=for(i in 1:length(shapeFile$shp)){
  temp=shapeFile$shp[[i]]$points
  latLongsVoid[[i]]=c(median(temp$X),median(temp$Y))
}
matrixLatLongs=unname(Reduce(rbind,latLongsVoid))
colnames(matrixLatLongs)=c("Latitude","Longitude")
################################################################################
# Calculate the distances matrix and the movement kernel
distancesMatrix=calc_haversine(matrixLatLongs)
#movementKernel=calc_HurdleExpKernel(distancesMatrix,MGDrivE::kernels$exp_rate,.5)
################################################################################
diag(distancesMatrix)=100000
minDistances=apply(distancesMatrix,1,min)
minDistancesDF=as.data.frame(minDistances)
meanDistance=median(minDistances)
base=ggplot(data=minDistancesDF,aes(x=minDistances)) + xlab("Minimum Distance") + ylab("Density") + ggtitle(placeNameTag,subtitle=paste0("Median: ",meanDistance))
base + geom_density(alpha=.2, fill="#FF6666") + geom_vline(aes(xintercept=meanDistance),linetype="dashed",size=.5)
ggsave(paste0(outputFolder,"/images/",placeNameTag,"_minDistances.pdf"),width=10,height=10)
