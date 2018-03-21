library(maptools)
library(shapefiles)
library(ggplot2)
library(viridis)
library(MGDrivE)
library(MGDrivEv2)
library(igraph)
library(rgdal)
################################################################################
setwd("~/Documents/GitHub/MGDrivE/Main")
shapeFile=read.shp("./GeoLandscapes/SHP/Buildings/Moroni/Moroni.shp")
################################################################################
latLongsVoid=vector("list",length(shapeFile$shp))#length(shapeFile$shp))
latLongs=for(i in 1:length(shapeFile$shp)){
  temp=shapeFile$shp[[i]]$points
  latLongsVoid[[i]]=c(mean(temp$X),mean(temp$Y))
}
matrixLatLongs=unname(Reduce(rbind,latLongsVoid))
colnames(matrixLatLongs)=c("Latitude","Longitude")
distancesMatrix=calc_haversine(matrixLatLongs)
sitesNumber=nrow(matrixLatLongs)
movementKernel=calc_HurdleExpKernel(distancesMatrix,MGDrivE::kernels$exp_rate,.5)
################################################################################
graphKernelInverse=graph_from_adjacency_matrix(distancesMatrix,weighted=TRUE)
graphKernelInverseWeights=E(graphKernelInverse)$weight
################################################################################
centrality_between=estimate_betweenness(graphKernelInverse,weights=graphKernelInverseWeights,cutoff=1500)
################################################################################
data=cbind(
  matrixLatLongs,
  betweenness=centrality_between#,
  #eigen=centrality_eigen$vector,
  #closeness=centrality_closeness
  #authority=centrality_authority$vector
)
names(data)[1:2]=c("Longitude","Latitude")
data_long=reshape2::melt(data=data,measure.vars=c("betweenness"))#,"closeness"))#"eigen","authority"))
################################################################################
ggplot(data=as.data.frame(data),aes(x=Latitude,y=Longitude)) +
  geom_point(aes(color=betweenness),size=8,shape=16,alpha=.65) +
  scale_color_viridis(
    name="Centrality",
    guide=guide_legend(keyheight=unit(3,units="mm"),keywidth=unit(12,units="mm"),label.position="bottom",title.position='top',nrow=10)
  ) + theme_light()
ggsave(paste0("./Centrality/","ComorosMain","_centralityScatter.pdf"),width=30,height=30)
################################################################################
ggplot(data=as.data.frame(data),aes(x=Latitude,y=Longitude))  +
    stat_summary_hex(aes(z=betweenness),size=25,alpha=.95,bins=375) +
    scale_fill_viridis(option="B") + theme_light()
ggsave(paste0("./Centrality/","ComorosMain","_centralityHex.pdf"),width=30,height=30)
sitesNumber/30
################################################################################
shape=readOGR("./GeoLandscapes/SHP/Buildings/Moroni/")
ggplot(data = shape, aes(x = long, y = lat, group = group)) + geom_path()
################################################################################
