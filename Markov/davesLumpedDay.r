
# Adult Dynamics with Emergence
P = list(p=.9, f=0.3, Q=0.95, n=16, lambda=10)

makeInit = function(P){
  with(P,list(M=1, Y=rep(0, n), Z=0))
}

MOS = makeInit(P)

dMdt = function(kappa,t,MOS,P){with(c(MOS,P),{
  tt = t%%n+1
  M = lambda + p*M
  Z = p*(Z + Y[tt])
  Y[tt] = (1-(1-kappa)^(f*Q))*(M-sum(Y)-Z)*p^n
  list(M=M,Y=Y,Z=Z)
})}

MM=c(MOS$M, MOS$Z)
for(t in 1:100){
  MOS = dMdt(0.1,t,MOS,P)
  MM = rbind(MM, c(MOS$M, MOS$Z))
}

plot(0:100, MM[,1], type = "l", ylim = range(0,MM))
lines(0:100, MM[,2])
MM1 <- MM


MOSd = list(M=1, Y1=0, Y2=0, Y3=0, Z=0)

makeEIPp = function(n,d){
}

makePd = function(d, P){with(P,{
 P$D = (1-p^d)/(1-p)
 P$N = (1-p^n)/(1-p)
 P$pd = p^d
 P$d = d
 if(n <= d){
   P$pD = p^P$D
   P$EIP1 = P$D/P$N
   P$EIP2 = 0
   P$EIP3 = 0
 }
 if(n>d & n <= 2*d){
   P$pD = p^P$N
   P$EIP1 = P$D/P$N
   P$EIP2 = 1-P$D/P$N
   P$EIP3 = 0
 }
 if(n > 2*d){
   P$pD = p^P$N
   P$EIP1 = 0
   P$EIP2 = P$D/P$N
   P$EIP3 = 1-P$D/P$N
 }
 P
})}

Pd = makePd(10, P)

deltaM = function(kappa,MOS,Pd){with(c(MOS,Pd),{
  Z = pd*Z+ pD*(EIP1*Y1 + EIP2*Y2 + EIP3*Y3)
  Y3 = (1-EIP2)*Y2*pd + (1-EIP3)*Y3*pd
  Y2 = (1-EIP1)*Y1*pd
  Y1 = (1-(1-f*Q*kappa)^d)*(M-Y1-Y2-Y3-Z)*pD
  M = pd*M + lambda*D

  list(M=M,Y1=Y1,Y2=Y2,Y3=Y3,Z=Z)
})}

MM=c(MOSd$M, MOSd$Z)
for(t in 1:10){
  MOSd = deltaM(0.1,MOSd,Pd)
  MM = rbind(MM, c(MOSd$M, MOSd$Z))
}

plot(0:10, MM[,1], type = "l", ylim = range(0,MM))
lines(0:10, MM[,2])

lines(0:100/10, MM1[,1], col = "blue")
lines(0:100/10, MM1[,2], col = "blue")
