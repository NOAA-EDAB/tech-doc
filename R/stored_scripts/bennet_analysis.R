### Bennet indicator analysis


#```{r, echo = T, eval = F}
#R code to construct Bennet Indicator for Ecosystem Project
#Author: John Walden
#Date: October 4, 2017
#
#Revised January 18, 2018 to calculate the indicator relative to average conditions
#during each time period. Set EPU in extraction/processing code chunk above.


#filter by specific EPU
epu = "GB"
value <- subset(landsum, EPU == epu)

#Calculate price
value$PRICE=value$SPPVALUE/value$SPPLIVMT
value[is.na(value)]<-0


#Next two lines are to calculate mean values for landings
#and value for the time series by feeding guild

meanval<-as.data.frame(value[,j=list(mean(SPPVALUE,na.rm=TRUE), 
                                     mean(SPPLIVMT,na.rm=TRUE)), by=Feeding.guild])
meanval<-rename(meanval, c("V1"="BASEV", "V2"="BASEQ"))
meanval$BASEP=meanval$BASEV/meanval$BASEQ;

#order by feeding guild

value<-value[order(value$Feeding.guild),]
meanval<-meanval[order(meanval$Feeding.guild),]

#Merge Value data frame with Base Year Value Data Frame
value<-merge(value, meanval, by="Feeding.guild")

#Construct price and Volume Indicators
#NOTE: ALL values are normalized to $1,000,000

value$VI=((0.5*(value$BASEP+value$PRICE))*(value$SPPLIVMT-value$BASEQ))/1000000
value$PI=((0.5*(value$BASEQ+value$SPPLIVMT))*(value$PRICE-value$BASEP))/1000000

value<-value[order(value$YEAR),]

#The next Data table sets up the yearly aggregate Bennet PI and VI

biyear<-data.table(value)
setkey(biyear, "YEAR")
biyear<-biyear[,lapply(.SD, sum), by=key(biyear), .SDcols=c("VI","PI","BASEV","SPPVALUE")]
biyear$revchange<-(biyear$VI+biyear$PI)
biyear$BI<-(biyear$VI + biyear$PI)

#The Next Steps restructure the year data frame so the yearly
#Bennet Indicator can be plotted. Negative values are difficult in GGPLOT.
#Since the Bennet indicator can have a negative value, separate data frames
#need to be created. First, the data needs to be restructured to use the 
#stacked bar function in ggplot. GGPLOT is used because it can graph different
# data layers on the same graph.

y1<-biyear[,c(1,2)]
y1$indicator='VI'
y2<-biyear[,c(1,3)]
y2$indicator='PI'

colnames(y1)[2]<-"value"
colnames(y2)[2]<-"value"
ytotal<-rbind(y1,y2)
```