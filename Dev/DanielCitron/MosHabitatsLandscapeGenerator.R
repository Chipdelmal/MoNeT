################################################################################
# From: Sean L Wu
################################################################################
library(spatstat)
library(mvtnorm)
library(tidyverse)
library(viridis)
library(RandomFields)
library(RandomFieldsUtils)
library(stringr)
install.packages("")
################################################################################
# simulate pointset
# we first simulate a deterministic intensity function
# for houses this is the superposition of 2 bivariate gaussians
# for mosquito habitats this is the superposition of 2 bivariate student t's
# then simulate a GP with gaussian covariance function and those means
# to get the stochastic random field that gives the first order 
# terms
# 
###############################################################################
# spatially varying intensity function for houses (houses cluster together like gaussians)
win <- square(2)
sigma1 <- diag(2)*0.05
sigma2 <- diag(2)*0.05
sigma3 <- diag(2)*0.05
sigma4 <- diag(2)*0.05
mean1 <- c(0.75,0.75)*2
mean2 <- c(0.25,0.25)*2
mean3 <- c(0.33,0.67)*2
mean4 <- c(0.67,0.33)*2
w = 2/3
fun_house <- function(x,y,mean1,mean2,sigma1,sigma2,w){
  (w*dmvnorm(x =c(x,y),mean =mean1,sigma = sigma1,log = FALSE)) + 
    ((1-w)*dmvnorm(x = c(x,y),mean = mean2,sigma = sigma2,log = FALSE))
}

#fun_house <- function(x,y,mean1,mean2,mean3,mean4,sigma1,sigma2,sigma3,sigma4,w){
#  (w*dmvnorm(x =c(x,y),mean =mean1,sigma = sigma1,log = FALSE)) + 
#  (w*dmvnorm(x =c(x,y),mean =mean3,sigma = sigma3,log = FALSE)) + 
#  ((1-w)*dmvnorm(x = c(x,y),mean = mean2,sigma = sigma2,log = FALSE)) +
#  ((1-w)*dmvnorm(x = c(x,y),mean = mean4,sigma = sigma4,log = FALSE)) 
#}

fun_house <- Vectorize(FUN = fun_house,vectorize.args = c("x","y"))
mu_house <- as.im(fun_house,W = win,mean1=mean1,mean2=mean2,sigma1=sigma1,sigma2=sigma2,w=w)
#mu_house <- as.im(fun_house,W = win,mean1=mean1,mean2=mean2,mean3=mean3,mean4=mean4,
#                  sigma1=sigma1,sigma2=sigma2,sigma3=sigma3,sigma4=sigma4,w=w)

## Breeding Sites
# spatially varying intensity function for breeding sites (they are more dispersed, like a t-distribution)
# when simulating from a t-distribution, keep df>2 otherwise it approaches Cauchy and is hard to parameterize
# (no finite second moment)
mean3 <- c(0.25,0.8)*2
mean4 <- c(0.8,0.2)*2
df1 <- 5.5 # as df->0 get Cauchy, as df->Inf get Gaussian
df2 <- 5
df3 <- 4.5
df4 <- 4.5
scale1 <- sigma1 * (df1-2)/df1
scale2 <- sigma2 * (df2-2)/df2
scale3 <- sigma2 * (df3-2)/df3
scale4 <- sigma2 * (df3-2)/df3
ww <- rep(1/4,4)

fun_breeding <- function(x,y,mean1,mean2,mean3,mean4,scale1,scale2,scale3,scale4,df1,df2,df3,df4,ww){
  (ww[1]*dmvt(x = c(x,y),sigma = scale1,delta = mean1,df = df1,log = FALSE)) +
  (ww[2]*dmvt(x = c(x,y),sigma = scale2,delta = mean2,df = df2,log = FALSE)) +
  (ww[3]*dmvt(x = c(x,y),sigma = scale3,delta = mean3,df = df3,log = FALSE)) +
  (ww[4]*dmvt(x = c(x,y),sigma = scale4,delta = mean4,df = df4,log = FALSE))
}

#fun_breeding <- function(x,y,mean1,mean2,mean3,scale1,scale2,scale3,df1,df2,df3,ww){
#  (ww[1]*dmvt(x = c(x,y),sigma = scale1,delta = mean1,df = df1,log = FALSE)) +
#    (ww[2]*dmvt(x = c(x,y),sigma = scale2,delta = mean2,df = df2,log = FALSE)) +
#    (ww[3]*dmvt(x = c(x,y),sigma = scale3,delta = mean3,df = df3,log = FALSE)) 
#}


fun_breeding <- Vectorize(FUN = fun_breeding,vectorize.args = c("x","y"))
mu_breeding <- as.im(fun_breeding,W = win,
                     mean1=mean1,mean2=mean2,mean3=mean3,mean4=mean4,
                     scale1=scale1,scale2=scale2,scale3=scale3,scale4=scale4,
                     df1=df1,df2=df2,df3=df3,df4=df4,ww=ww)
mu_breeding_xy <- mu_breeding %>% 
  as.matrix %>% 
  as.tibble %>% 
  rename_all(funs(str_extract(.,"[0-9]+"))) %>% 
  mutate(x=1:nrow(mu_breeding))  %>%
  gather(y,value,-x) %>%
  mutate(y = as.integer(y)) %>%
  arrange(x) %>%
  rename(intensity=value)
mu_house_xy  <- mu_house %>% 
  as.matrix %>% 
  as.tibble %>% 
  rename_all(funs(str_extract(.,"[0-9]+"))) %>% 
  mutate(x=1:nrow(mu_house))  %>%
  gather(y,value,-x) %>%
  mutate(y = as.integer(y)) %>%
  arrange(x) %>%
  rename(intensity=value)
mu_intensity <- bind_rows(houses=mu_house_xy,habitats=mu_breeding_xy,.id = "type")
mu_intensity %>% ggplot(mapping = aes(x = x,y = y,fill = intensity)) +
  geom_raster() +
  scale_fill_viridis() +
  facet_wrap(~ type) +
  theme_bw()
# we can choose to simluate how houses and habitats arise as a doubly stochastic process
# in this case the underlying intensity is a random field, here modeled as
# log(intensity) ~ GP(.)
rf_intensity_h <- rLGCP(model = "gauss",mu = log(mu_house),var = 0.15,scale = 0.1,win = win)
rf_intensity_h <- attr(rf_intensity_h, "Lambda")
rf_house <- rf_intensity_h %>% 
  as.matrix %>% 
  as.tibble %>% 
  rename_all(~ as.character(rf_intensity_h$yrow)) %>%
  # rename_all(funs(str_extract(.,"[0-9]+"))) %>% 
  mutate(x = rf_intensity_h$xcol) %>%
  # mutate(x=1:nrow(rf_intensity_b))  %>%
  gather(y,value,-x) %>%
  mutate(y = as.numeric(y)) %>%
  arrange(x) %>%
  rename(intensity=value)
rf_intensity_b <- rLGCP(model = "gauss",mu = log(mu_breeding),var = 0.2,scale = 0.125,win = win)
rf_intensity_b <- attr(rf_intensity_b, "Lambda")
rf_habitats <- rf_intensity_b %>% 
  as.matrix %>% 
  as.tibble %>% 
  rename_all(~ as.character(rf_intensity_b$yrow)) %>%
  # rename_all(funs(str_extract(.,"[0-9]+"))) %>% 
  mutate(x = rf_intensity_b$xcol) %>%
  # mutate(x=1:nrow(rf_intensity_b))  %>%
  gather(y,value,-x) %>%
  mutate(y = as.numeric(y)) %>%
  arrange(x) %>%
  rename(intensity=value)
rf_sample <- bind_rows(houses=rf_house,habitats=rf_habitats,.id = "type")
rf_sample %>% ggplot(mapping = aes(x = x,y = y,fill = intensity)) +
  geom_raster() +
  scale_fill_viridis() +
  facet_wrap(~ type) +
  theme_bw()
# simulate houses - number of houses
n_house <- 100
# use Metropolis-Hastings simulation for point process because we need to condition on number
# of houses in the inhomogeneous  point process
# house_sim <- list(cif="poisson",par=list(beta=1),w=win,trend=rf_intensity_h)
house_sim <- list(cif="hardcore",par=list(beta=1,hc=0.1),w=win,trend=rf_intensity_h)
rmh_control <- list(p=1)
rmh_start <- list(n.start=n_house)
xy_h <- rmh(model = house_sim,control = rmh_control,start = rmh_start)
## simulate breeding sites, assume breeding sites cluster around houses
# on average, have this many mosquito habitats/house
n_habitat_house <- 1.5
# number of habitats, poisson-generated
n_habitat <- rpois(n = 1,lambda = n_habitat_house*n_house)
## use Metropolis-Hastings simulation for point process because we need to condition on number 
# of mosquito habitats in the Thomas process
sigma <- 0.1
h <- density(xy_h,sigma,edge=FALSE)
Lambda <- h * rf_intensity_b
habitat_sim <- list(cif="poisson",par=list(beta=1),w=win,trend=rf_intensity_b)
rmh_control <- list(p=1)
rmh_start <- list(n.start=n_habitat)
xy_hh <- rmh(model = habitat_sim,control = rmh_control,start = rmh_start)
xy_pts <- tibble(type=c(rep("houses",xy_h$n),rep("habitats",xy_hh$n)),
                 x=c(xy_h$x,xy_hh$x),
                 y=c(xy_h$y,xy_hh$y))
ggplot() +
  geom_raster(data = rf_sample,mapping = aes(x = x,y = y,fill = intensity)) +
  geom_point(data = xy_pts,aes(x=x,y=y),color=grey(0.8,0.25)) +
  scale_fill_viridis() +
  facet_wrap(~ type) +
  theme_bw()

## xy_pts is a tibble that combines locations of both houses and habitats

## Export data, for reading into mathematica

library(data.table)
xy.out.data = data.table(xy_pts)

write.table(x = xy.out.data, 
            file = "/Users/dtcitron/Documents/MosPopDyn/MoNeT/MoNeT/Dev/DanielCitron/MosHabitats_3.csv",
            sep = ",")

#write.table(x = xy.out.data, 
#           file = "/Users/dtcitron/Documents/MosPopDyn/MoNeT/MoNeT/Dev/DanielCitron/MosHabitats.csv",
#           sep = ",")
