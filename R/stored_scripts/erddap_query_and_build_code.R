# ERDDAP Query and build

#```{r query, echo = T, eval = F, message=F, warning=F}

build_latest <- FALSE

if (build_latest){
  
  # Relative working directories
  data.dir  <- here::here('data')
  r.dir <- here::here('R')
  
  #Source function for querying ERDDAP server
  source(file.path(r.dir,"get_erddap.R"))
  
  #Set URL for COMET (server where NEFSC ERDDAP lives)
  comet <- 'https://comet.nefsc.noaa.gov/erddap/'
  
  #List datasets on the NEFSC ERDDAP
  tab_list <- ed_datasets(url = comet)
  
  #Get updated data set IDs
  erddap_datasets <- tab_list %>% 
    filter(str_detect(Dataset.ID, "soe_v")) %>% 
    get_erddap(id = NULL)
  
  #Save and clean updated IDs for use in rest of report
  save(erddap_datasets, file = file.path(data.dir, "ERDDAP_datasets.Rdata"))
  
  # Exclude stock assessment status data, which have unique structure
  erddap_datasets <- erddap_datasets %>%
    dplyr::filter(!str_detect(Dataset.ID, "assess")) 
  
  #Create SOE parent data set, filter out NAs. This queries based on 
  #data set IDs that were collected above
  SOE.data.erd <- sprintf("http://comet.nefsc.noaa.gov/erddap/tabledap/%s.csv",
                          erddap_datasets$Dataset.ID) %>% 
    purrr::map(function(x) {
      readr::read_csv(url(x))
    }) %>% 
    do.call(rbind,.) %>% 
    mutate(Value = as.numeric(Value)) %>% 
    dplyr::filter(!is.na(Value))
  
  #Convert to data.table
  SOE.data <- as.data.table(SOE.data.erd)
  
  #Save data
  save(SOE.data, file = file.path(data.dir,"SOE_data_erddap.Rdata"))
}
#```