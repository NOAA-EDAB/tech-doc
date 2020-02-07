# rec div analysis


#```{r, eval = F, include = T, echo = T}
REC_DATA <- read.csv('X:/gdepiper/ESR2018/SOE/Data/Rec_Days_Fished_2018.csv', as.is=TRUE)

REC_DATA$P_Shore <- -(as.numeric(gsub("","",'""',REC_DATA$Shore)) /
                        as.numeric(gsub("","",'""',REC_DATA$All_Modes))) *
  log(as.numeric(gsub("","",'""',REC_DATA$Shore)) /
        as.numeric(gsub("","",'""',REC_DATA$All_Modes)))

REC_DATA$P_Private <- -(as.numeric(gsub("","",'""',REC_DATA$Private_Rental)) /
                          as.numeric(gsub("","",'""',REC_DATA$All_Modes))) *
  log(as.numeric(gsub("","",'""',REC_DATA$Private_Rental)) /
        as.numeric(gsub("","",'""',REC_DATA$All_Modes)))

REC_DATA$P_Party <- -(as.numeric(gsub("","",'""',REC_DATA$Party_Charter)) /
                        as.numeric(gsub("","",'""',REC_DATA$All_Modes))) *
  log(as.numeric(gsub("","",'""',REC_DATA$Party_Charter)) /
        as.numeric(gsub("","",'""',REC_DATA$All_Modes)))

REC_DATA$Value <- exp(REC_DATA$P_Shore+REC_DATA$P_Private+REC_DATA$P_Party)

REC_DATA$Region[REC_DATA$Region=='"MID-ATLANTIC"'] <- 'MA'
REC_DATA$Region[REC_DATA$Region=='"NORTH ATLANTIC"'] <- 'NE'

E_SHANNON <- subset(REC_DATA, select=c('Time','Region','Value'))
E_SHANNON$Units <- 'Effective Shannon'
E_SHANNON$Var <- 'Recreational fleet effort diversity across modes'
E_SHANNON$Source <- 'MRIP effort time series, processed to generate diversity measure.'
#```