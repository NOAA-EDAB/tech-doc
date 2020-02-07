#mab hab extraction




#```{r r-extract,fig.align = "center", eval = T, fig.cap='(ref:r-extract)', echo = F, message=F, warning=F}
data.dir <- "data/CB_HAB"

#Function to process data - cpm specifies cells per ml filter
fixer <- function(cpm){
  hab_2007_2012 <- read_excel(file.path(data.dir,"Query_2007-2012.xlsx"))
  hab_2013_odu <- read_excel(file.path(data.dir,"2013 ODU Data.xlsx"),skip = 4)
  hab_2013_vims <- read_excel(file.path(data.dir,"vims_2013.xlsx"),skip = 6)
  hab_2014_odu <- read_excel(file.path(data.dir,"2014 ODU data.xlsx"))
  hab_2014_vims <- read_excel(file.path(data.dir,"FINALforVDH_22Dec14final.xlsx"))
  hab_2016 <- read_excel(file.path(data.dir,"HAB_MAP_Data_2016.xlsx"))
  hab_2017 <- read_excel(file.path(data.dir,"HAB_MAP_Data_2017.xlsx"),sheet=2)
  
  #2012---------------------------------------------------------
  HAB_2007_2012 <- hab_2007_2012 %>% filter(!is.na(cells_per_ml)) %>%
    filter(!is.na(date)) %>%
    mutate(year = format(as.POSIXct(date), "%Y")) %>% 
    filter(cells_per_ml >= cpm) %>%
    group_by(year, species) %>%
    dplyr::summarise(Events = n()) %>%
    as.data.frame()
  
  #2013---------------------------------------------------------
  #ODU
  odu_2013 <- gather(hab_2013_odu, species, cells_per_ml, 
                     `Pfiesteria like dinoflagellate`:`A. monilatum`) %>%
    filter(!is.na(cells_per_ml)) %>%
    filter(cells_per_ml >= cpm) %>%
    mutate(year = 2013) %>%
    group_by(year, species) %>%
    dplyr::summarise(Events = n()) %>%
    as.data.frame()
  
  #VIMS
  vims_2013 <- hab_2013_vims %>% filter(!is.na(cells_per_ml)) %>%
    mutate(year = "2013") %>%
    filter(cells_per_ml >= cpm) %>%
    group_by(year, species) %>%
    dplyr::summarise(Events = n()) %>%
    as.data.frame()
  
  HAB_2013 <- rbind(vims_2013, odu_2013)
  
  #2014--------------------------------------------------------
  #ODU
  long <- gather(hab_2014_odu, species, cells_per_ml, 
                 `Karlodinium veneficum`:`Cyanobacteria bloom`, factor_key = TRUE)
  hab_2014_odu <- long %>% filter(cells_per_ml != 0)
  hab_2014_odu$species <- sub("[.]"," ", hab_2014_odu$species)
  hab_2014_odu$cells_per_ml <- gsub("[A-Za-z+//]",'',hab_2014_odu$cells_per_ml)
  hab_2014_odu$cells_per_ml <- as.numeric(hab_2014_odu$cells_per_ml)
  
  hab_2014_odu <- hab_2014_odu %>% mutate(year = "2014") %>%
    filter(cells_per_ml >= cpm) %>%
    group_by(year,species) %>%
    dplyr::summarise(Events = n()) %>%
    as.data.frame()
  
  #VIMS
  long <- gather(hab_2014_vims, species, cells_per_ml, `A. monilatum`:`C. subsalsa`)
  hab_2014_vims <- long %>% mutate(year = "2014") %>% filter(!is.na(cells_per_ml)) %>%
    mutate(cells_per_ml = as.numeric(cells_per_ml)) %>% 
    filter(cells_per_ml >= cpm) %>%
    group_by(year,species) %>%
    dplyr::summarise(Events = n()) %>%
    as.data.frame()
  HAB_2014 <- rbind(hab_2014_odu, hab_2014_vims)
  
  #2015----------------------------------------------------------
  #No data
  
  #2016---------------------------------------------------------
  HAB_2016 <- hab_2016 %>% mutate(species= plyr::mapvalues(species, 
                                                           from = c("Eugelna sanguinea",
                                                                    "Microcystin aeruginosa",
                                                                    "Microcystis aeruginosa",
                                                                    "Alexandrium monilatum-likely",
                                                                    "Alexandrium monilatum"),
                                                           to = c("Eugelena spp.", 
                                                                  "Microcystis spp.",
                                                                  "Microcystis spp.",
                                                                  "Alexandrium spp.",
                                                                  "Alexandrium spp.")))
  HAB_2016$cells_per_ml <- gsub('[a-zA-Z+<>]','',HAB_2016$cells_per_ml)
  HAB_2016 <- HAB_2016 %>%
    filter(!is.na(cells_per_ml)) %>%
    mutate(year = 2016, cells_per_ml = as.numeric(cells_per_ml)) %>%
    filter(cells_per_ml >= cpm) %>%
    group_by(year, species) %>%
    dplyr::summarise(Events = n()) %>%
    as.data.frame()
  
  #2017------------------------------------------------------------
  hab_2017$species = str_trim(hab_2017$species)
  HAB_2017 <- hab_2017 %>% 
    mutate(species = plyr::mapvalues(species, c("A. monilatum","Anabaena sp",
                                                "Anabaena sp.","Anabaena spp",
                                                "none","NO HABs",
                                                "C. polykrikoides",
                                                "Microcystis aeurignosa",
                                                "Cylindrospermopsis sp"),
                                     c("Alexandrium monilatum", "Anabaena spp.",
                                       "Anabaena spp.","Anabaena spp.",
                                       "NA","NA","Cochlodinium polykrikoides",
                                       "Microcystis aeruginosa",
                                       "Cylindrospermopsis sp.")))
  HAB_2017$cells_per_ml <- gsub("[a-zA-Z+/]",'',HAB_2017$cells_per_ml)
  HAB_2017$cells_per_ml <- str_trim(HAB_2017$cells_per_ml)
  HAB_2017$cells_per_ml <- as.numeric(HAB_2017$cells_per_ml)
  HAB_2017 <- HAB_2017 %>% 
    filter(!is.na(cells_per_ml)) %>%
    mutate(year = "2017") %>%
    filter(cells_per_ml >= cpm) %>%
    group_by(year, species) %>%
    dplyr::summarise(Events = n()) %>%
    as.data.frame()
  
  #Aggregate--------------------------------------------------------
  ts <- rbind(HAB_2007_2012, HAB_2013, HAB_2014, HAB_2016, HAB_2017)
  
  return(ts)
}

#All blooms > 5000 cells ml^-1
full <- fixer(cpm = 5000)
full <- full %>% group_by(year) %>% dplyr::summarise(total = sum(Events))
plot(full$year, full$total, type = "o", ylim = c(0,90),
     pch = 20, ylab = "Bloom Events", las = 1, xlab = "Time", lwd = 2)

#cochlodinum > 300 cells ml^-1
cochlo <- fixer(cpm = 300)
cochlo[cochlo$species == "C. polykrikoides" |
         cochlo$species == "C.polykrikoides" ,]$species <- "Cochlodinium polykrikoides"
cochlo <- cochlo[cochlo$species == "Cochlodinium polykrikoides",]
cochlo <- cochlo %>% group_by(year) %>% dplyr::summarise(total = sum(Events))
points(cochlo$year, cochlo$total, type = "o", pch = 20, col = "indianred", lwd = 2)
legend(x = 2007, y = 80, legend = c(expression(paste("All reports >5000 cells ml"^"-1")),
                                    expression(paste(italic("C. polykrikoides "),
                                                     "reports >300 cells ml"^"-1"))),
       col = c("black","indianred"),
       lwd = 2,
       bty = "n")
#```