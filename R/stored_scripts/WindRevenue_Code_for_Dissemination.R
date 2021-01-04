#Geret DePiper
#Wind Energy Site revenue indicator
#November 24, 2020
require(data.table)
require(tidyr)
require(dplyr)
require(stringr)

setwd("Folder with confidential data sources")
file_list<- list.files("Folder with confidential data sources")

number_of_top_species = 5 #Setting number of species to display
REVENUE <- NULL

#Sppnames <- unique(REVENUEFILE[,c("NESPP3","SPPNM"),])

MAB <- c(23,51,754,769,11,12,352,121,801,335,446,802,
         329,212,444,215)

NE <- c(81,82,11,12,269,120,364:370,800,147,
        352,153,168,122,123,124,125,152,155,507:509,
        512,240,159,710,250,372,373,154)

#had to specify columns to get rid of the total column
for (i in 1:length(file_list)) {
  load(file=file_list[i]) #read in files using the fread function from the data.table
  REVENUEFILE <- REVENUEFILE[which(REVENUEFILE$BROADZONE!="Other"),]
  REVENUE <- rbind(REVENUE, REVENUEFILE) #for each iteration, bind the new data to the building dataset
}

Top_5_Managed <- NULL
Top_5_Unfiltered_Names <- NULL

for (x in c("MAB", "NE")) {

pii_all_yr_area_top_species <- subset(REVENUE, !is.na(SPPNM)) %>% 
  dplyr::select(SPPNM, NESPP3, InsideREV, InsideLANDED, PERMIT, DEALNUM) %>%
  filter(NESPP3%in%get(x)) %>%
  group_by(SPPNM) %>% 
  dplyr::summarize(
    InsideREV = sum(InsideREV, na.rm = T),
    InsideLANDED = sum(InsideLANDED, na.rm = T),
    npermits = length(unique(PERMIT)),
    ndealers = length(unique(DEALNUM))
  ) %>%
  #mutate(CONF =  npermits < 3 | ndealers < 3) %>%
  #mutate(SPPNM_CONF = ifelse(CONF == T, 'All Others', SPPNM)) %>%
  mutate(SPPNM_CONF=SPPNM) %>%
  ungroup() %>%
  group_by(SPPNM_CONF) %>%
  dplyr::summarize(
    yfa_rev = sum(InsideREV, na.rm = T),
    yfa_land = sum(InsideLANDED, na.rm = T),
    npermits = sum(npermits, na.rm = T),
    ndealers = sum(ndealers, na.rm = T)
  ) %>% 
  dplyr::rename("Species"= SPPNM_CONF) %>% 
  arrange(desc(yfa_rev)) %>% 
  top_n(n=number_of_top_species, wt=yfa_rev) %>% 
  pull(Species)

top_species_names <- str_to_title(pii_all_yr_area_top_species)
top_species_names <- paste0(paste0(!top_species_names %in% tail(top_species_names, n=1), collapse = ", ") , " and ", tail(top_species_names, n=1))


piispecies <- subset(REVENUE, !is.na(SPPNM)) %>%
  dplyr::select(SPPNM, NESPP3, Year, InsideREV, InsideLANDED, PERMIT, DEALNUM) %>%
  mutate(SPPNM = ifelse(SPPNM%in% pii_all_yr_area_top_species,SPPNM,'All Other')) %>%
  mutate(SPPNM = ifelse(SPPNM%in% "RED CRAB",'All Other',SPPNM)) %>%
  group_by(SPPNM, Year) %>%
  dplyr::summarize(
    InsideREV = sum(InsideREV, na.rm = T),
    InsideLANDED = sum(InsideLANDED, na.rm = T),
    npermits = length(unique(PERMIT)),
    ndealers = length(unique(DEALNUM))
  ) %>%
  mutate(CONF =  npermits < 3 | ndealers < 3) %>%
  mutate(SPPNM_CONF = ifelse(CONF == T, 'All Other', SPPNM)) %>%
  ungroup() %>%
  group_by(SPPNM_CONF, Year) %>%
  dplyr::summarize(
    Value = sum(InsideREV, na.rm = T),
    yfa_land = sum(InsideLANDED, na.rm = T),
    npermits = sum(npermits, na.rm = T),
    ndealers = sum(ndealers, na.rm = T)) %>% 
  dplyr::rename("Species"= SPPNM_CONF)

piispecies$EPU <- x
pii_all_yr_area_top_species <- cbind(pii_all_yr_area_top_species,x)

Top_5_Managed <- rbind(Top_5_Managed,piispecies)
Top_5_Unfiltered_Names <- rbind(Top_5_Unfiltered_Names,pii_all_yr_area_top_species)

}

Top_5_Managed$Species <-str_to_title(Top_5_Managed$Species)

Top_5_Managed <- Top_5_Managed[,c("Species","Year","Value","EPU")] %>%
  pivot_longer(Species, values_to="Var") %>%
  mutate(Var = paste0(Var," (Top 5 Species Revenue from Wind Development Areas)", sep="")) %>%
  mutate(Units = "2019 Constant Dollars") %>%
  mutate(Time=Year) %>%
  dplyr::select(Time,Var,Value,EPU,Units)

write.csv(Top_5_Managed,"X:/gdepiper/ESR2020/Data/FINAL/Wind_Energy_Revenue.csv")
