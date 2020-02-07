# rec catch div analysis



#```{r, eval = F, include = T, echo = T}
REC_CATCH <- read.csv('X:/gdepiper/ESR2018/SOE/Data/Rec_Species_Quantity_2018.csv', as.is=TRUE)

REC_CATCH$Value <-  as.numeric(gsub(",","",REC_CATCH$Value))
TOT_REC_CATCH <- aggregate(Value~Time+Region, data=REC_CATCH, FUN=sum)
names(TOT_REC_CATCH) <- c('Time','Region','Tot_Catch')
REC_CATCH <- merge(REC_CATCH,TOT_REC_CATCH, by=c('Time','Region'))
REC_CATCH$P_Catch <- -(REC_CATCH$Value/REC_CATCH$Tot_Catch*
                         log(REC_CATCH$Value/REC_CATCH$Tot_Catch))
REC_CATCH <- aggregate(P_Catch~Time+Region, data=REC_CATCH, FUN=sum)
REC_CATCH$Value <- exp(REC_CATCH$P_Catch)
REC_CATCH <- subset(REC_CATCH, select=c('Time','Region','Value'))
REC_CATCH$Region[REC_CATCH$Region=="MID-ATLANTIC"] <- 'MA'
REC_CATCH$Region[REC_CATCH$Region=="NORTH ATLANTIC"] <- 'NE'
REC_CATCH$Units <- 'Effective Shannon'
REC_CATCH$Var <- 'Recreational Diversity of Catch' 

##Species include: American Eel, Atlantic Cod, Atlantic Mackerel, 
##Atlantic Sturgeon, Black Drum, Black Sea Bass, Bluefish, 
##Cobia, Haddock, Pollock, Red Drum, Scup, Spanish Mackerel,
##Spiny Dogfish, Spot, Spotted Seatrout, Striped Bass, 
##Summer Flounder, Tautog, Tilefish, Weakfish, Winter Flounder,   
#and All Other Species.

REC_CATCH$Source <- 'MRIP catch time series.'
#```