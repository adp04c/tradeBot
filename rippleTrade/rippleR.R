library(quantmod)

Ripple <- read.csv(file="C:/Users/AustinPeel/Documents/python/rip.csv",head=TRUE,sep=",")

Ripple$rsi <- RSI(Ripple$close)
trend <- aroon( Ripple[,c("high", "low")], n=20 )
Ripple <- cbind(Ripple, trend)
macd <- MACD( Ripple[,"close"], 12, 26, 9, maType="EMA" )
Ripple <- cbind(Ripple, macd)
Ripple$obv <- OBV(Ripple[,"close"], Ripple[,"base_volume"])
stochOSC <- stoch(Ripple[,c("high","low","close")])
Ripple <- cbind(Ripple,stochOSC)
Ripple$stochWPR <- WPR(Ripple[,c("high","low","close")])
Ripple$ad <- chaikinAD(Ripple[,c("high","low","close")], Ripple[,"base_volume"])
Ripple$cmf <- CMF(Ripple[,c("high","low","close")], Ripple[,"base_volume"])
atr <- ATR(Ripple[,c("high","low","close")], n=14)
Ripple <- cbind(Ripple,atr)
bbands.HLC <- BBands( Ripple[,c("high","low","close")] )
####dn up mavg pactB#######
Ripple <- cbind(Ripple,bbands.HLC)
Ripple$cci <- CCI(Ripple[,c("high","low","close")])
dmi.adx <- ADX(Ripple[,c("high","low","close")])
######dIP DN DX ADX#####
Ripple <- cbind(Ripple,dmi.adx)
Ripple$roc <- ROC(Ripple[,"close"])


write.csv(Ripple,"rip.csv")