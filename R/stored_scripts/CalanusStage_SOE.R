## R Morse 20210226 ryan.morse@noaa.gov
## script to load zooplankton stage data and process seasonal means for Calanus
## email harvey.walsh@noaa.gov for data access
library(stats)
library(reshape2)
library(readxl)
library(lubridate)
library(dplyr)
library(sp)
library(maptools)
library(marmap)
library(maps)
library(mapdata)
library(raster)

## function to standardize highly skewed data - log normalize data and compute mean, return exponent
log_mean1 = function(x, na.rm=TRUE){
  x2=log10(x+1)
  x3=mean(x2, na.rm=na.rm)
  x4=10^x3
  return(x4)
}

### load data file, format date
### Stage codes in MARMAP/EcoMon:
# 020                       COPEPODITE I                                                                                            
# 021                       COPEPODITE II                                                                                           
# 022                       COPEPODITE III                                                                                          
# 023                       COPEPODITE IV                                                                                           
# 024                       COPEPODITE V                                                                                            
# 000                       ADULT                                                                                                   
# 999                       UNKNOWN  
ZPD=read.csv('/home/ryan/Desktop/Z/SOE_2021_PlanktonData/Ryan_Morse_2021_01_14.csv', stringsAsFactors = F) # 2021 from Harvey
ZPD$date=as.Date(ZPD$FORMATED_EVENT_DATE, format="%m/%d/%y %R")
ZPD$year=year(ZPD$date)
ZPD$month=month(ZPD$date)
ZPD$DOY=yday(ZPD$date)

## bin bimonthly date for EcoMon cruises
cruises=unique(ZPD$CRUISE_NAME)
ZPD$medmonth=NA
for (i in 1:length(cruises)){
  ZPD$medmonth[ZPD$CRUISE_NAME == cruises[i]]=median(ZPD$DOY[ZPD$CRUISE_NAME == cruises[i]])
}
ZPD$bmm=NA
ZPD$bmm[which(as.integer(ZPD$medmonth) %in% seq(0,59))]=1
ZPD$bmm[which(as.integer(ZPD$medmonth) %in% seq(60,120))]=3
ZPD$bmm[which(as.integer(ZPD$medmonth) %in% seq(121,181))]=5
ZPD$bmm[which(as.integer(ZPD$medmonth) %in% seq(182,243))]=7
ZPD$bmm[which(as.integer(ZPD$medmonth) %in% seq(244,304))]=9
ZPD$bmm[which(as.integer(ZPD$medmonth) %in% seq(305,366))]=11

### Assign locations to EPUs
# EPU=ecodata::epu_sf # not sure how to make this work with my methods using spatialpolygonsdataframe
gbk=rgdal::readOGR("EPU_GBKPoly.shp")
gom=rgdal::readOGR("EPU_GOMPoly.shp")
mab=rgdal::readOGR("EPU_MABPoly.shp")
scs=rgdal::readOGR("EPU_SCSPoly.shp")
#extract just lat/lons for lines
gbk.lonlat =as.data.frame(lapply(slot(gbk, "polygons"), function(x) lapply(slot(x, "Polygons"), function(y) slot(y, "coords"))))
gom.lonlat =as.data.frame(lapply(slot(gom, "polygons"), function(x) lapply(slot(x, "Polygons"), function(y) slot(y, "coords"))))
mab.lonlat =as.data.frame(lapply(slot(mab, "polygons"), function(x) lapply(slot(x, "Polygons"), function(y) slot(y, "coords"))))
scs.lonlat =as.data.frame(lapply(slot(scs, "polygons"), function(x) lapply(slot(x, "Polygons"), function(y) slot(y, "coords"))))
# create matrix to use in in.out function from package 'mgcv'
gom.mat=as.matrix(gom.lonlat)
gbk.mat=as.matrix(gbk.lonlat)
mab.mat=as.matrix(mab.lonlat)
scs.mat=as.matrix(scs.lonlat)
m4=as.matrix(ZPD[,c('LONGITUDE','LATITUDE')]) #lon,lat from ZPD
ZPD$epu=NA
ZPD$epu[which(in.out(gbk.mat, m4))]='GB'
ZPD$epu[which(in.out(gom.mat, m4))]='GOM'
ZPD$epu[which(in.out(scs.mat, m4))]='SS'
ZPD$epu[which(in.out(mab.mat, m4))]='MAB'
test=ZPD[is.na(ZPD$epu),] #unassigned

# sum all counts across stage categories, necessary for calculations below
ZPD$zooplankton_count=apply(ZPD[,c(12:18)], 1, sum)

## convert from counts to units of # per 100m^-3 following MARMAP protocol
ZPD$c1_100m3=(ZPD$ZOO_STAGE_020+(ZPD$zooplankton_count/(ZPD$zooplankton_count-ZPD$ZOO_STAGE_999)*ZPD$ZOO_STAGE_999))*ZPD$ZOO_ALIQUOT*(100/ZPD$GEAR_VOLUME_FILTERED)
ZPD$c2_100m3=(ZPD$ZOO_STAGE_021+(ZPD$zooplankton_count/(ZPD$zooplankton_count-ZPD$ZOO_STAGE_999)*ZPD$ZOO_STAGE_999))*ZPD$ZOO_ALIQUOT*(100/ZPD$GEAR_VOLUME_FILTERED)
ZPD$c3_100m3=(ZPD$ZOO_STAGE_022+(ZPD$zooplankton_count/(ZPD$zooplankton_count-ZPD$ZOO_STAGE_999)*ZPD$ZOO_STAGE_999))*ZPD$ZOO_ALIQUOT*(100/ZPD$GEAR_VOLUME_FILTERED)
ZPD$c4_100m3=(ZPD$ZOO_STAGE_023+(ZPD$zooplankton_count/(ZPD$zooplankton_count-ZPD$ZOO_STAGE_999)*ZPD$ZOO_STAGE_999))*ZPD$ZOO_ALIQUOT*(100/ZPD$GEAR_VOLUME_FILTERED)
ZPD$c5_100m3=(ZPD$ZOO_STAGE_024+(ZPD$zooplankton_count/(ZPD$zooplankton_count-ZPD$ZOO_STAGE_999)*ZPD$ZOO_STAGE_999))*ZPD$ZOO_ALIQUOT*(100/ZPD$GEAR_VOLUME_FILTERED)
ZPD$adult_100m3=(ZPD$ZOO_STAGE_000+(ZPD$zooplankton_count/(ZPD$zooplankton_count-ZPD$ZOO_STAGE_999)*ZPD$ZOO_STAGE_999))*ZPD$ZOO_ALIQUOT*(100/ZPD$GEAR_VOLUME_FILTERED)
ZPD$unstaged_100m3=(ZPD$ZOO_STAGE_999+(ZPD$zooplankton_count/(ZPD$zooplankton_count-ZPD$ZOO_STAGE_999)*ZPD$ZOO_STAGE_999))*ZPD$ZOO_ALIQUOT*(100/ZPD$GEAR_VOLUME_FILTERED)
ZPD$total_100m3=ZPD$zooplankton_count*ZPD$ZOO_ALIQUOT*(100/ZPD$GEAR_VOLUME_FILTERED)
## deal with instances of bad values
ZPD$c1_100m3[ZPD$c1_100m3==Inf]=NA
ZPD$c2_100m3[ZPD$c2_100m3==Inf]=NA
ZPD$c3_100m3[ZPD$c3_100m3==Inf]=NA
ZPD$c4_100m3[ZPD$c4_100m3==Inf]=NA
ZPD$c5_100m3[ZPD$c5_100m3==Inf]=NA
ZPD$adult_100m3[ZPD$adult_100m3==Inf]=NA

## subset to just Calanus finmarchicus
Cfin=ZPD[ZPD$TAXA_004==101,]

### Aggregate samples to EPU, season, year
## Early spring months (bimonth means in 1 or 3)
biseas=Cfin[which((Cfin$bmm==1) | (Cfin$bmm==3)),]; SEASON='Spring'
s.yr.c3=aggregate(biseas$c3_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
s.yr.c4=aggregate(biseas$c4_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
s.yr.c5=aggregate(biseas$c5_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
s.yr.adt=aggregate(biseas$adult_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
s.yr.tot=aggregate(biseas$total_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
Calfin=s.yr.c3
Calfin=left_join(Calfin, s.yr.c4, by=c("Group.1", "Group.2"))
Calfin=left_join(Calfin, s.yr.c5, by=c("Group.1", "Group.2"))
Calfin=left_join(Calfin, s.yr.adt, by=c("Group.1", "Group.2"))
Calfin=left_join(Calfin, s.yr.tot, by=c("Group.1", "Group.2"))
meanday=aggregate(biseas$DOY, by=list(biseas$year, biseas$epu), FUN=mean, na.rm=T)
nday=aggregate(biseas$DOY, by=list(biseas$year, biseas$epu), FUN=length)
Calfin=left_join(Calfin, meanday, by=c("Group.1", "Group.2"))
Calfin=left_join(Calfin, nday, by=c("Group.1", "Group.2"))
colnames(Calfin)=c('Year', 'epu', 'c3', 'c4', 'c5', 'adt', 'tot', 'meanday', 'ndays')
Calfin$season=SEASON
Calfin$C3pct=Calfin$c3/Calfin$tot
Calfin$C4pct=Calfin$c4/Calfin$tot
Calfin$C5pct=Calfin$c5/Calfin$tot
Calfin$Adtpct=Calfin$adt/Calfin$tot
Cfspr=Calfin
## Summer months (bimonth means in 5 or 7)
biseas=Cfin[which((Cfin$bmm==5) | (Cfin$bmm==7)),]; SEASON='Summer'
s.yr.c3=aggregate(biseas$c3_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
s.yr.c4=aggregate(biseas$c4_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
s.yr.c5=aggregate(biseas$c5_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
s.yr.adt=aggregate(biseas$adult_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
s.yr.tot=aggregate(biseas$total_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
Calfin=s.yr.c3
Calfin=left_join(Calfin, s.yr.c4, by=c("Group.1", "Group.2"))
Calfin=left_join(Calfin, s.yr.c5, by=c("Group.1", "Group.2"))
Calfin=left_join(Calfin, s.yr.adt, by=c("Group.1", "Group.2"))
Calfin=left_join(Calfin, s.yr.tot, by=c("Group.1", "Group.2"))
meanday=aggregate(biseas$DOY, by=list(biseas$year, biseas$epu), FUN=mean, na.rm=T)
nday=aggregate(biseas$DOY, by=list(biseas$year, biseas$epu), FUN=length)
Calfin=left_join(Calfin, meanday, by=c("Group.1", "Group.2"))
Calfin=left_join(Calfin, nday, by=c("Group.1", "Group.2"))
colnames(Calfin)=c('Year', 'epu', 'c3', 'c4', 'c5', 'adt', 'tot', 'meanday', 'ndays')
Calfin$season=SEASON
Calfin$C3pct=Calfin$c3/Calfin$tot
Calfin$C4pct=Calfin$c4/Calfin$tot
Calfin$C5pct=Calfin$c5/Calfin$tot
Calfin$Adtpct=Calfin$adt/Calfin$tot
Cfsum=Calfin
## Fall months (bimonth means in 9 or 11)
biseas=Cfin[which((Cfin$bmm==9) | (Cfin$bmm==11)),]; SEASON='Fall'
s.yr.c3=aggregate(biseas$c3_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
s.yr.c4=aggregate(biseas$c4_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
s.yr.c5=aggregate(biseas$c5_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
s.yr.adt=aggregate(biseas$adult_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
s.yr.tot=aggregate(biseas$total_100m3, by=list(biseas$year, biseas$epu), FUN=log_mean1, na.rm=T)
Calfin=s.yr.c3
Calfin=left_join(Calfin, s.yr.c4, by=c("Group.1", "Group.2"))
Calfin=left_join(Calfin, s.yr.c5, by=c("Group.1", "Group.2"))
Calfin=left_join(Calfin, s.yr.adt, by=c("Group.1", "Group.2"))
Calfin=left_join(Calfin, s.yr.tot, by=c("Group.1", "Group.2"))
meanday=aggregate(biseas$DOY, by=list(biseas$year, biseas$epu), FUN=mean, na.rm=T)
nday=aggregate(biseas$DOY, by=list(biseas$year, biseas$epu), FUN=length)
Calfin=left_join(Calfin, meanday, by=c("Group.1", "Group.2"))
Calfin=left_join(Calfin, nday, by=c("Group.1", "Group.2"))
colnames(Calfin)=c('Year', 'epu', 'c3', 'c4', 'c5', 'adt', 'tot', 'meanday', 'ndays')
Calfin$season=SEASON
Calfin$C3pct=Calfin$c3/Calfin$tot
Calfin$C4pct=Calfin$c4/Calfin$tot
Calfin$C5pct=Calfin$c5/Calfin$tot
Calfin$Adtpct=Calfin$adt/Calfin$tot
Cffal=Calfin

# Format data wide to long and save data for SOE report 2021
t1=rbind(Cfspr, Cfsum)
wide=rbind(t1, Cffal)
long=melt(wide, id.vars = 1:2, variable.name = "year")
long=wide %>% 
  tidyr::pivot_longer(cols = c(c3, c4, c5, adt, C3pct, C4pct, C5pct, Adtpct), 
                      names_to = "Var", values_to = "Value") %>%  dplyr::mutate(Units=c("No. per 100m^-3"))
long$Units[which(long$Var== "C3pct")]=c("percent abundance")
long$Units[which(long$Var== "C4pct")]=c("percent abundance")
long$Units[which(long$Var== "C5pct")]=c("percent abundance")
long$Units[which(long$Var== "Adtpct")]=c("percent abundance")
CalanusStage=long

## Subset to just adults and c5 copepodites; substitute NA when less than 10 days are available for a crusie (poor sample coverage for year-season)
# add scaled biomass based on day of year (experimental - not for use until validated)
CS2=CalanusStage %>% filter(Var==c('c5', 'adt')) %>% 
  mutate(newval=ifelse(ndays<10, NA, Value)) %>% 
  mutate(newday= (meanday/ 365)) %>% 
  mutate(scaledval=newval*newday)

CalanusStage2=CS2 %>% select(Year, epu, season, Var, newval, Units)
colnames(CalanusStage2)[5]='Value'
save(CalanusStage2, file='/home/ryan/Desktop/Z/RM_20210205_CalanusStage.Rda')