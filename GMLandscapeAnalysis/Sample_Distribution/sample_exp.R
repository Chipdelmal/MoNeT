# zero-inflated truncated exponential (ZITE)

args <- commandArgs()
.libPaths( c( .libPaths(), "/Library/Frameworks/R.framework/Versions/3.5/Resources/library"))
library(truncdist)

# expectation of truncated exp; from Mathematica
texp_mean <- function(lambda,b){
  (-b/(exp(b*lambda)-1)) + (1/lambda)
}

# use this function if using uniroot
texp_f <- function(lambda,b,mean){
  ((-b/(exp(b*lambda)-1)) + (1/lambda)) - mean
}

main <- function(filepath, n, popnode, p, b) {
  totpop <- n*popnode
  # sample the populations n_samp times
  pops <- replicate(n = 1,expr = {
    # bernoulli draws for 0 adults
    x <- rbinom(n = n,size = 1,prob = p)
    x <- as.integer(!x)
    # the rate parameter we would need to hit the same mean overall with untruncated
    adpop_star <- totpop/sum(x!=0)
    # solve for the truncated lambda (trancendental equation, need numerical soln)
    lambda_trunc <- uniroot(f = texp_f,interval = c(1e-6,b),b = b,mean = adpop_star)$root
    # draw from the distribution
    x[x!=0] <- truncdist::rtrunc(n = sum(x!=0),spec = "exp",a = 0,b = b,rate = lambda_trunc)
    if(any(x[x!=0] > b)){
      stop("something has gone horribly awry")
    }
    x <- as.integer(round(x))
    write.csv(x, file = paste(filepath,".csv", sep=""),row.names=FALSE)
    return(x)
  },simplify = FALSE)
}
main(args[7], as.numeric(args[8]), as.numeric(args[9]), as.numeric(args[10]), as.numeric(args[11]))
