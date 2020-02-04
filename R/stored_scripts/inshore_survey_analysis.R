# inshore survey analysis


#```{r, eval = F, include = T, echo = T}
#SOE Mass State data
##SML

#User parameters
if(Sys.info()['sysname'] == "Windows"){
  data.dir <- 'L:\\EcoAP\\Data\\survey'
  out.dir  <- 'L:\\EcoAP\\Data\\SOE'
  gis.dir  <- 'L:\\Rworkspace\\GIS_files'
}
if(Sys.info()['sysname'] == "Linux"){
  data.dir <- '/home/slucey/slucey/EcoAP/Data/survey'
  out.dir  <- '/home/slucey/slucey/EcoAP/Data/SOE'
  gis.dir  <- '/home/slucey/slucey/Rworkspace/GIS_files'
}

#-------------------------------------------------------------------------------
#Required packages
library(data.table); library(rgdal); library(Survdat)

#-------------------------------------------------------------------------------
#User created functions


#-------------------------------------------------------------------------------
load(file.path(data.dir, 'Survdat_Mass.RData'))
load(file.path(data.dir, 'SOE_species_list.RData'))

#Grab strata
strata <- readOGR(gis.dir, 'RA_STRATA_POLY_MC')

#Generate area table
strat.area <- getarea(strata, 'stratum')

#Fix strata code to match data
strat.area[, STRATUM := as.numeric(paste0(9, stratum, 0))]

#Subset by season/ strata set
fall   <- survdat.mass[SEASON == 'FALL',   ]
spring <- survdat.mass[SEASON == 'SPRING', ]

#Run stratification prep
fall.prep   <- stratprep(fall,   strat.area, strat.col = 'STRATUM', area.col = 'Area')
spring.prep <- stratprep(spring, strat.area, strat.col = 'STRATUM', area.col = 'Area')

#Calculate mean weight/tow by aggregate groups
#n tows
n.tows.fall  <- unique(fall.prep[,   list(YEAR, EPU, ntows)])
n.tow.spring <- unique(spring.prep[, list(YEAR, EPU, ntows)])

#drop length data
setkey(fall.prep, YEAR, EPU, STATION, STRATUM, SVSPP, CATCHSEX)
fall.prep <- unique(fall.prep, by = key(fall.prep))
fall.prep[, c('LENGTH', 'NUMLEN') := NULL]

setkey(spring.prep, YEAR, EPU, STATION, STRATUM, SVSPP, CATCHSEX)
spring.prep <- unique(spring.prep, by = key(spring.prep))
spring.prep[, c('LENGTH', 'NUMLEN') := NULL]

#Merge Sexed species
setkey(fall.prep, YEAR, EPU, STATION, STRATUM, SVSPP)
fall.prep <- fall.prep[, sum(BIOMASS, na.rm = T), by = key(fall.prep)]

setkey(spring.prep, YEAR, EPU, STATION, STRATUM, SVSPP)
spring.prep <- spring.prep[, sum(BIOMASS, na.rm = T), by = key(spring.prep)]

#Sum biomass within an EPU
fall.sum   <- fall.prep[,   sum(V1), by = c('YEAR', 'EPU', 'SVSPP')]
spring.sum <- spring.prep[, sum(V1), by = c('YEAR', 'EPU', 'SVSPP')]

#Merge sum with station count
fall.sum   <- merge(fall.sum,   n.tows.fall, by = c('YEAR', 'EPU'))
spring.sum <- merge(spring.sum, n.tows.fall, by = c('YEAR', 'EPU'))

#Calculate mean weight per tow
fall.sum[, kg.per.tow := V1 / ntows]
fall.mean <- fall.sum[, list(YEAR, EPU, SVSPP, kg.per.tow)]

spring.sum[, kg.per.tow := V1 / ntows]
spring.mean <- spring.sum[, list(YEAR, EPU, SVSPP, kg.per.tow)]

#Aggregate by EBFM codes
fall   <- merge(fall.mean,   unique(species[, list(SVSPP, SOE.18, Fed.Managed)]), 
                by = 'SVSPP', all.x = T)
spring <- merge(spring.mean, unique(species[, list(SVSPP, SOE.18, Fed.Managed)]), 
                by = 'SVSPP', all.x = T)

#Fix NA group to other
fall[  is.na(SOE.18), SOE.18 := 'Other']
spring[is.na(SOE.18), SOE.18 := 'Other']

#Sum by feeding guild and managed species
fall.agg   <- fall[,   sum(kg.per.tow), by = c('YEAR', 'EPU', 'SOE.18', 'Fed.Managed')]
spring.agg <- spring[, sum(kg.per.tow), by = c('YEAR', 'EPU', 'SOE.18', 'Fed.Managed')]

#Total
fall.agg[, Total := sum(V1), by = c('YEAR', 'EPU', 'SOE.18')]
fall.agg[, Prop.managed := V1 / Total]

spring.agg[, Total := sum(V1), by = c('YEAR', 'EPU', 'SOE.18')]
spring.agg[, Prop.managed := V1 / Total]

#Get in correct long format for SOE
#By feeding guild
fall.tot <- copy(fall.agg)
fall.tot[, Var := paste(SOE.18, 'Fall Biomass Index')]
setnames(fall.tot, c('YEAR', 'EPU', 'Total'), c('Time', 'Region', 'Value'))
fall.tot[, c('SOE.18', 'V1', 'Prop.managed', 'Fed.Managed') := NULL]
fall.tot[, Units  := 'kg tow^-1']
fall.tot[, Source := 'NEFSC bottom trawl survey (survdat)']
setcolorder(fall.tot, c('Time', 'Value', 'Var', 'Units', 'Region', 'Source'))
fall.tot <- unique(fall.tot)

spring.tot <- copy(spring.agg)
spring.tot[, Var := paste(SOE.18, 'Spring Biomass Index')]
setnames(spring.tot, c('YEAR', 'EPU', 'Total'), c('Time', 'Region', 'Value'))
spring.tot[, c('SOE.18', 'V1', 'Prop.managed', 'Fed.Managed') := NULL]
spring.tot[, Units  := 'kg tow^-1']
spring.tot[, Source := 'NEFSC bottom trawl survey (survdat)']
setcolorder(spring.tot, c('Time', 'Value', 'Var', 'Units', 'Region', 'Source'))
spring.tot <- unique(spring.tot)

#Proportion managed
fall.prop <- copy(fall.agg)
fall.prop[is.na(Fed.Managed), Fed.Managed := 'Non']
fall.prop[, Var := paste(SOE.18, Fed.Managed, 'managed species - Fall Biomass Index')]
setnames(fall.prop, c('YEAR', 'EPU', 'Prop.managed'), c('Time', 'Region', 'Value'))
fall.prop[, c('SOE.18', 'V1', 'Total', 'Fed.Managed') := NULL]
fall.prop[, Units  := 'proportion']
fall.prop[, Source := 'NEFSC bottom trawl survey (survdat)']
setcolorder(fall.prop, c('Time', 'Value', 'Var', 'Units', 'Region', 'Source'))

spring.prop <- copy(spring.agg)
spring.prop[is.na(Fed.Managed), Fed.Managed := 'Non']
spring.prop[, Var := paste(SOE.18, Fed.Managed, 'managed species - Spring Biomass Index')]
setnames(spring.prop, c('YEAR', 'EPU', 'Prop.managed'), c('Time', 'Region', 'Value'))
spring.prop[, c('SOE.18', 'V1', 'Total', 'Fed.Managed') := NULL]
spring.prop[, Units  := 'proportion']
spring.prop[, Source := 'NEFSC bottom trawl survey (survdat)']
setcolorder(spring.prop, c('Time', 'Value', 'Var', 'Units', 'Region', 'Source'))

#Merge into one data set
survey <- rbindlist(list(fall.tot, spring.tot, fall.prop, spring.prop))
save(survey, file = file.path(out.dir, 'Aggregate_Survey_biomass_19.RData'))
#```