library(spatstat)
library(fields)
library(plyr)

if(interactive()) {
  nr   <- 1e5
  nv  <- 5000
  ns <- 50
} else {
  nr  <- 20
  nv <- 5
  ns <- 20
  oldopt <- spatstat.options()
  spatstat.options(expand=1.05)
}
set.seed(961018)

eta_small = seq(1e-5, 1, 0.01)#c(5e-4, 1e-4, 5e-3, 1e-3,  5e-2, 1e-2, 5e-1,1e-1) #seq(1e-5, 1, 0.01)
eta_big = seq(1, 1000000, 10000)
iterations = 100

generateModel_repulsive <- function(eta,hc=10) {
  for (i in 1:iterations) {
    mod <- rmhmodel(cif=c("areaint","hardcore"),par=list(
      list(beta=2,eta=eta,r=10),
      list(beta=2,hc=hc)
    ),
    w=c(0,1000,0,1000))
    X.area <- rmh(model=mod,start=list(n.start=ns),
                  control=list(nrep=nr,nverb=nv, p=1))
    if(interactive()) plot(X.area)
    d = data.frame(x = X.area[['x']], y = X.area[['y']], n = ns)
    #if we want to start writing files to csv, uncomment this code
    if (eta < 1){
      string = formatC(eta, format = "e", digits = 0)
      filename = sprintf("~/Desktop/Output/1clustering_analysis/eta%s_iter%s.csv", string, i)
      write.csv(d, file = filename)
    }
    else{
      filename = sprintf("~/Desktop/Output/1clustering_analysis/eta%s_iter%s.csv", eta, i)
      write.csv(d, file = filename)
    }
  }
}

generateModel = function(eta) {
  for (i in 1:iterations) {
    mod <- rmhmodel(cif="areaint",par=list(beta=2,eta=eta,r=10),
                    w=c(0,1000,0,1000))
    X.area <- rmh(model=mod,start=list(n.start=ns),
                  control=list(nrep=nr,nverb=nv, p=1))
    if(interactive()) plot(X.area)
    d = data.frame(x = X.area[['x']], y = X.area[['y']], n = ns)
    
    #if (eta < 1){
    #string = formatC(eta, format = "e", digits = 0)
    #filename = sprintf("~/Desktop/Output/1clustering_analysis/eta%s_iter%s.csv", string, i)
    #write.csv(d, file = filename)
    #}
    #else{
    filename = sprintf("~/Desktop/Output/1clustering_analysis/eta%s_iter%s.csv", eta, i)
    write.csv(d, file = filename)
    #}
  }
}

master = lapply(eta_big, generateModel)
master = lapply(eta_small, generateModel_repulsive)
base_case = generateModel_repulsive(1e-6, 100)
