library(Hmisc)

totals <- c(1308, 1267, 1957, 1674, 949, 1412, 190, 22, 174)
wolb <- round(totals * c(.24,.7,.62,.38,.88,.76,.98,1,.95))
out = binconf(x = wolb, n = totals, alpha = 0.05, method = "exact")
write.csv(out, file="/Users/sanchez.hmsc/Desktop/CI_Y.csv")


gv_totals <- c(1495, 1105, 1843, 1865, 1776, 237, 174, 101)
gv_wolb <- round(gv_totals * c(.17,.44,.49,.66,.68,.79,.90,.81))
out = binconf(x = gv_wolb, n = gv_totals, alpha = 0.05, method = "exact")
write.csv(out, file="/Users/sanchez.hmsc/Desktop/CI_G.csv")



n <- c(1308,1267,1957,1674,949,1412,190,22,174)
p <- c(.24,.7,.62,.38,.88,.76,.98,1,.95)
ci <- Hmisc::binconf(x = round(n*p),n = n,alpha = 0.05,method = "exact")
li <- (n*p) - (ci[,2]*n) # lower CI
ui <- (n*p) + (ci[,3]*n) # upper CI

# for da visuals
plot(n*p,type="l",ylim = c(0,max(ui)))
lines(li,lty=2)
lines(ui,lty=2)
