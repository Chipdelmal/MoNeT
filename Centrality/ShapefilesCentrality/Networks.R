rm(list=ls());gc()
library(stringr)
library(MGDrivE)
library(MGDrivEv2)
library(viridis)
library(igraph)
library(ggplot2)
setwd("/Users/sanchez.hmsc/Documents/GitHub/MGDrivE/Main/")
####################################################################################
rangeScaling=function(x){(x-min(x))/(max(x)-min(x))}
plotGraphCentrality=function(centralityVector,rawGeoData,scalingConstant){
  ggplot(data=cbind(rawGeoData,centrality), aes(x=V1,y=V2)) +
    geom_point(aes(color=rangeScaling(centrality)),size=scalingConstant*rangeScaling(centrality),shape=1) +
    xlab("Longitude") + ylab("Latitude")
}
standardizeCentrality=function(centralityVector){
  (centralityVector-mean(centralityVector))/sd(centralityVector)
}
####################################################################################
location="YorkeysKnob"
rawGeoData=read.csv(paste0("./GeoLandscapes/",location,"_Coordinates.csv"),sep=",",header=FALSE)
latLongs=as.matrix(rawGeoData)
sitesNumber=nrow(latLongs)
distancesMatrix=calc_haversine(latLongs)
####################################################################################
movementKernel=calc_HurdleExpKernel(distancesMatrix,MGDrivE::kernels$exp_rate,.5)
movementKernelInverse=1/movementKernel
####################################################################################
graphKernel=graph_from_adjacency_matrix(movementKernel,weighted=TRUE)
graphKernelWeights=1000*E(graphKernel)$weight
####################################################################################
graphKernelInverse=graph_from_adjacency_matrix(distancesMatrix,weighted=TRUE)
graphKernelInverseWeights=E(graphKernelInverse)$weight
####################################################################################
graphDistance=graph_from_adjacency_matrix(distancesMatrix,weighted=TRUE)
graphDistanceWeights=E(graphDistance)$weight
####################################################################################
####################################################################################
####################################################################################
centrality_between=betweenness(graphKernelInverse,weights=graphKernelInverseWeights)
centrality_between=standardizeCentrality(centrality_between)
#####
#centrality_eigen=eigen_centrality(graphKernel,weights=graphKernelWeights)
#centrality_eigen$vector=standardizeCentrality(centrality_eigen$vector)
#####
centrality_closeness=closeness(graphKernelInverse,weights=graphKernelInverseWeights)
centrality_closeness=standardizeCentrality(centrality_closeness)
#####
#centrality_authority=authority_score(graphKernel,weights=graphKernelWeights)
#centrality_authority$vector=standardizeCentrality(centrality_authority$vector)
####################################################################################
data=cbind(
  rawGeoData,
  betweenness=centrality_between#,
  #eigen=centrality_eigen$vector,
  #closeness=centrality_closeness
  #authority=centrality_authority$vector
)
names(data)[1:2]=c("Longitude","Latitude")
data_long=reshape2::melt(data=data,measure.vars=c("betweenness"))#,"closeness"))#"eigen","authority"))
####################################################################################
ggplot(data=data_long,aes(x=Longitude,y=Latitude)) +
  geom_point(aes(color=value),size=3,shape=16,alpha=.9) +
  scale_color_viridis(
    name="Centrality",
    guide=guide_legend(keyheight=unit(3,units="mm"),keywidth=unit(12,units="mm"),label.position="bottom",title.position='top',nrow=10)
  ) +
  facet_wrap(~variable,ncol=2,scales="free")
ggsave(paste0("./Centrality/",location,"_centralityScatter.pdf"),width=30,height=15)
####################################################################################
ggplot(data=data_long,aes(x=Longitude,y=Latitude)) +
  stat_summary_hex(aes(z = value),size=3,alpha=.9,bins=round(sitesNumber/30)) +
  scale_fill_viridis(option="B") +
  #geom_hex(aes(color=value),size=3,alpha=.9,bins=50)  +
  facet_wrap(~variable,ncol=2,scales="free")
ggsave(paste0("./Centrality/",location,"_centralityHex.pdf"),width=30,height=15)
####################################################################################

#cluster_edge_betweenness(graphKernelInverse,weights=graphKernelInverseWeights)
