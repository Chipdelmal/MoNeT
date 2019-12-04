# zero-inflated truncated Gamma (ZITG)

args <- commandArgs()
.libPaths( c( .libPaths(), "/Library/Frameworks/R.framework/Versions/3.5/Resources/library"))

library(pracma)
library(truncdist)

# 1st moment (aka Mean) of upper-truncated Gamma
tgamma_m1 <- function(alpha,beta,b){
  pracma::gammainc(x = beta*b,a = alpha + 1)[[1]] / (beta * pracma::gammainc(x = beta*b,a = alpha)[[1]])
}

# 2st moment of upper-truncated Gamma
tgamma_m2 <- function(alpha,beta,b){
  pracma::gammainc(x = beta*b,a = alpha + 2)[[1]] / ((beta^2) * pracma::gammainc(x = beta*b,a = alpha)[[1]])
}

# Variance of upper-truncated Gamma
tgamma_var <- function(alpha,beta,b){
  tgamma_m2(alpha,beta,b) - (tgamma_m1(alpha,beta,b)^2)
}

# system of equations to solve: we want to find alpha,beta st. we get the mean/variance we asked for
tgamma_sys <- function(x,b,mean,var){
  alpha <- exp(x[[1]])
  beta <- exp(x[[2]])
  m <- tgamma_m1(alpha = alpha,beta = beta,b = b) - mean
  if(is.nan(m)){
    m <- 2e16
  }
  v <- tgamma_var(alpha = alpha,beta = beta,b = b) - var
  if(is.nan(v)){
    v <- 2e16
  }
  c(m,v)
}

# starting points for optimization, these are the parameters of the untruncated gamma
tgamma_start <- function(mean,var){
  c(
    alpha=(mean^2)/var,
    beta=mean/var
  )
}

main <- function(filepath, n, popnode, cv, p, b) {
  totpop <- n*popnode

  # resample
  pops <- replicate(n = 1,expr = {

    # bernoulli draws for 0 adults
    x <- rbinom(n = n,size = 1,prob = p)
    x <- as.integer(!x)

    # the mean and variance we would need to hit the same mean overall with untruncated
    mean_star <- (popnode*n)/sum(x!=0)
    var_star <- (mean_star*cv)^2

    # get some starting points, perturb them
    x0_pts <- tgamma_start(mean = mean_star,var = var_star)

    # try Newton's method
    soln <- try(pracma::newtonsys(Ffun = tgamma_sys,x0 = log(x0_pts),Jfun = NULL,
                                  b = b,mean = mean_star,var = var_star))
    if(inherits(soln,"try-error")){
      stop("warning: Newton's method did not converge; try reducing CV and re-sample")
    }

    # draw from the distribution
    x[x!=0] <- rtrunc(n = sum(x!=0),spec = "gamma",a = 0,b = b,shape = exp(soln$zero)[[1]],rate = exp(soln$zero)[[2]])
    if(any(x[x!=0] > b)) {
      stop("something has gone horribly awry")
    }
    x <- as.integer(round(x))
    write.csv(x, file = filepath, col.names = c("n"), row.names=FALSE)
    return(x)
  })
}
main(args[7], as.numeric(args[8]), as.numeric(args[9]), as.numeric(args[10]), as.numeric(args[11]), as.numeric(args[12]))
