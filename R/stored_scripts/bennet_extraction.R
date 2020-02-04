### bennet_extraction

# ```{r, echo = T, eval = F, warning=F, message=F}
#This code is used to load and process comland data. 
#See comland methods for source data (CFDBS) processing methods. 

drake::readd(proc_get_mass_inshore_survey.R)

#Packages
PKG <- c("data.table","plyr","RColorBrewer", "ggplot2","cowplot","gridExtra","grid")
for (p in PKG) {
  if(!require(p,character.only = TRUE)) {  
    install.packages(p)
    require(p,character.only = TRUE)}
}
# #Setting Save path


#load "comland" data - These data are unavailble due to PII concerns. 
#See aggregated data load below
ecosys2<-subset(comland, US=='TRUE' & YEAR>=1964 & SPPVALUE >=0)

#Load species and PDT codes
load(file.path(data.dir, "Species_codes.RData"))

#Set EPU
epu <- "GB"

#processing
spp<-subset(spp, NESPP3>0)
spp2<-unique(spp[,c(3,12)], by='NESPP3')
spp2<-spp2[which(!duplicated(spp2$NESPP3)),]
sp_combine<-merge(ecosys2, spp2, by="NESPP3", all.x=TRUE)
add.apex <- data.table(NESPP3 = 000, YEAR = 1971, QY = 1, GEAR = 'other',
                       SIZE = 'small', EPU = epu, UTILCD = 0, SPPLIVMT = 0,
                       SPPVALUE = 0, US = TRUE, Feeding.guild = 'Apex Predator')
sp_combine <- rbindlist(list(sp_combine, add.apex))

#Subset data into Georges Bank group
LANDINGS<-subset(sp_combine)
LANDINGS<-LANDINGS[which(!is.na(LANDINGS$Feeding.guild)),]

#Set Up data Table
landsum<-data.table(LANDINGS)
# setkey(landsum,  "EPU", "YEAR","Feeding.guild")
setkey(landsum,"EPU","YEAR","Feeding.guild")


#Sum by feeding guild
landsum[,lapply(.SD, sum, na.rm=TRUE), by=key(landsum), .SDcols=c("SPPLIVMT","SPPVALUE")]

# ```