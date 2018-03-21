################################################################################
# ╔╦╗┌─┐╔╗╔┌─┐╔╦╗
# ║║║│ │║║║├┤  ║
# ╩ ╩└─┘╝╚╝└─┘ ╩
# Mosquito Networks Taskforce
# Centrality parser for shapefiles in R
################################################################################
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
outputFolder="./Centrality/ShapefilesCentrality/"
################################################################################
# Read shapefile
shapeFile=read.shp(paste0("./OSMnx/RoadsAndBuildingsParser/SHP/Buildings/",placeNameTag,"/",placeNameTag,".shp"))
################################################################################
# Plot shapefile's polygons
#shape=readOGR("./GeoLandscapes/SHP/Buildings/Moroni/")
#ggplot(data = shape, aes(x = long, y = lat, group = group)) + geom_path()
################################################################################
# Calculate the centroids of the buildings polygons and store as matrix
latLongsVoid=vector("list",length(shapeFile$shp))
latLongs=for(i in 1:length(shapeFile$shp)){
  temp=shapeFile$shp[[i]]$points
  latLongsVoid[[i]]=c(mean(temp$X),mean(temp$Y))
}
matrixLatLongs=unname(Reduce(rbind,latLongsVoid))
colnames(matrixLatLongs)=c("Latitude","Longitude")
################################################################################
# Calculate the distances matrix and the movement kernel
distancesMatrix=calc_haversine(matrixLatLongs)
movementKernel=calc_HurdleExpKernel(distancesMatrix,MGDrivE::kernels$exp_rate,.5)
################################################################################
# Generate the network to analyse
graph=graph_from_adjacency_matrix(distancesMatrix,weighted=TRUE)
graphWeights=E(graph)$weight
################################################################################
# Calculate centrality
centrality=estimate_betweenness(graph,weights=graphWeights,cutoff=1500)
write.table(centrality,paste0(outputFolder,"/cache/",placeNameTag,"_centralityVector.csv"))
#centrality=read.table(paste0(outputFolder,"cache/",placeNameTag,"_centralityVector.csv"),header=FALSE)
################################################################################
# Reshape centrality matrix
data=cbind(matrixLatLongs,centrality=centrality)
names(data)[1:2]=c("Longitude","Latitude")
data_long=reshape2::melt(data=data,measure.vars=c("centrality"))
################################################################################
# Generate and export scatter plot
ggplot(data=as.data.frame(data),aes(x=Latitude,y=Longitude)) +
  geom_point(aes(color=centrality),size=8,shape=16,alpha=.65) +
  scale_color_viridis(
    name="Centrality",
    guide=guide_legend(keyheight=unit(3,units="mm"),keywidth=unit(12,units="mm"),label.position="bottom",title.position='top',nrow=10)
  ) + theme_light()
ggsave(paste0(outputFolder,"/images/",placeNameTag,"_centralityScatter.pdf"),width=30,height=30)
################################################################################
# Generate and export hex plot
ggplot(data=as.data.frame(data),aes(x=Latitude,y=Longitude))  +
    stat_summary_hex(aes(z=centrality),size=25,alpha=.95,bins=nrow(matrixLatLongs)/25) +
    scale_fill_viridis(option="B") + theme_light()
ggsave(paste0(outputFolder,"/images/",placeNameTag,"_centralityHex.pdf"),width=30,height=30)
################################################################################
