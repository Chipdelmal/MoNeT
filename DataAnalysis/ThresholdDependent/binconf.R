library(Hmisc)

totals <- c(1308, 1267, 1957, 1674, 949, 1412, 190, 22, 174)
wolb <- round(totals * c(.24,.7,.62,.38,.88,.76,.98,1,.95))
out = binconf(x = wolb, n = totals, alpha = 0.05, method = "exact")
write.csv(out, file="/Users/sanchez.hmsc/Desktop/CI.csv")
