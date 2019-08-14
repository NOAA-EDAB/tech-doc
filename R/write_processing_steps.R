library(tidyverse)

write_to_rmd <- function(script, rmd, hook = NULL, output_path){
  
  #Read in script
  source <-  readr::read_file(script)

  #Concatenate Rmd chunk yml
  source <- paste0("```{r, eval = F, echo = T}\n",source, "```\n")
  
  #Read in Rmd
  rmd <- readr::read_file(rmd)
  
  output <- stringr::str_replace(rmd,
                       regex(paste0("Process",hook,"Start\\}\\} -->.*\\<\\!-- \\{\\{Process",hook,"End"),dotall = T),
                       paste0("Process",hook,"Start}} -->\\\n",source,"<\\!-- \\{\\{Process",hook,"End"))
  
  
  #write output to file
  readr::write_file(output, path = output_path)

}

#Seasonal SST anomaly----------------------

write_to_rmd(script = here::here("source","get_seasonal_oisst_anom_gridded.R"),
             rmd = here::here("chapters","Seasonal_SST_anomaly_maps_indicator.Rmd"),
             output_path = here::here("chapters",
                                      "Seasonal_SST_anomaly_maps_indicator.Rmd"))

#Single species stock data----------------------

write_to_rmd(script = here::here("source","get_stocks.R"),
             rmd = here::here("chapters","singlespp_status_indicator.Rmd"),
             output_path = here::here("chapters",
                                      "singlespp_status_indicator.Rmd"))

#Inshore surveys----------------------

write_to_rmd(script = here::here("source","get_ne_inshore_survey.R"),
             rmd = here::here("chapters","inshore_bottom_trawl_surveys.Rmd"),
             hook = "NESurvey",
             output_path = here::here("chapters",
                                      "inshore_bottom_trawl_surveys.Rmd"))

write_to_rmd(script = here::here("source","get_mass_inshore_survey.R"),
             rmd = here::here("chapters","inshore_bottom_trawl_surveys.Rmd"),
             hook = "MassSurvey",
             output_path = here::here("chapters",
                                      "inshore_bottom_trawl_surveys.Rmd"))

write_to_rmd(script = here::here("source","get_mab_inshore_survey.R"),
             rmd = here::here("chapters","inshore_bottom_trawl_surveys.Rmd"),
             hook = "NEAMAPSurvey",
             output_path = here::here("chapters",
                                      "inshore_bottom_trawl_surveys.Rmd"))

#NEFSC Bottom Trawl Survey----------------------

write_to_rmd(script = here::here("source","get_nefsc_survey.R"),
             rmd = here::here("chapters","survey_data.rmd"),
             output_path = here::here("chapters",
                                      "survey_data.rmd"))
# CFDBS Landings Data----------------------

write_to_rmd(script = here::here("source","get_comdat.R"),
             rmd = here::here("chapters","landings_data.Rmd"),
             output_path = here::here("chapters",
                                      "landings_data.Rmd"))
# Gulf Stream Index----------------------

write_to_rmd(script = here::here("source","get_gsi.R"),
             rmd = here::here("chapters","gulf_stream_index.Rmd"),
             output_path = here::here("chapters",
                                      "gulf_stream_index.Rmd"))
# Recreational indicators----------------------

write_to_rmd(script = here::here("source","get_rec.R"),
             rmd = here::here("chapters","Recreational_Data.Rmd"),
             output_path = here::here("chapters",
                                      "Recreational_Data.Rmd"))

# Zooplankton indicators----------------------

# Abundance anomaly
write_to_rmd(script = here::here("source","get_zoo_anom_sli.R"),
             rmd = here::here("chapters","Zooplankton_indicators.Rmd"),
             hook = "AbundAnom",
             output_path = here::here("chapters",
                                      "Zooplankton_indicators.Rmd"))
#Seasonal abundance 1
write_to_rmd(script = here::here("source","process_oi.R"),
             rmd = here::here("chapters","Zooplankton_indicators.Rmd"),
             hook = "SeasAbund1",
             output_path = here::here("chapters",
                                      "Zooplankton_indicators.Rmd"))
#Seasonal abundance 2
write_to_rmd(script = here::here("source","get_zoo_oi.R"),
             rmd = here::here("chapters","Zooplankton_indicators.Rmd"),
             hook = "SeasAbund2",
             output_path = here::here("chapters",
                                      "Zooplankton_indicators.Rmd"))

# Common tern diet data------------------------

#Seasonal abundance 2
write_to_rmd(script = here::here("source","get_commontern.R"),
             rmd = here::here("chapters","seabird_diet_and_productivity.Rmd"),
             output_path = here::here("chapters",
                                      "seabird_diet_and_productivity.Rmd"))

# Ches bay water quality------------------------
write_to_rmd(script = here::here("source","get_ches_bay_wq.R"),
             rmd = here::here("chapters","ches_bay_water_quality.Rmd"),
             output_path = here::here("chapters",
                                      "ches_bay_water_quality.Rmd"))

# Species distribution indicators--------------
write_to_rmd(script = here::here("source","get_species_dist.R"),
             rmd = here::here("chapters","Species_dist_indicators.Rmd"),
             output_path = here::here("chapters",
                                      "Species_dist_indicators.Rmd"))
# NARW------------------------
write_to_rmd(script = here::here("source","get_narw.R"),
             rmd = here::here("chapters","RW_indicator.Rmd"),
             output_path = here::here("chapters",
                                      "RW_indicator.Rmd"))
# Productivity data------------------------
write_to_rmd(script = here::here("source","get_productivity_anomaly.R"),
             rmd = here::here("chapters","productivity_for_tech_memo.Rmd"),
             output_path = here::here("chapters",
                                      "productivity_for_tech_memo.Rmd"))

# Long-term SST time series------------------------
write_to_rmd(script = here::here("source","get_long_term_sst.R"),
             rmd = here::here("chapters","long_term_sst_indicator.Rmd"),
             output_path = here::here("chapters",
                                      "long_term_sst_indicator.Rmd"))

# Ichthyoplankton div indices------------------------
write_to_rmd(script = here::here("source","get_ichthyoplankton.R"),
             rmd = here::here("chapters","ich_div_indicator.Rmd"),
             output_path = here::here("chapters",
                                      "ich_div_indicator.Rmd"))

# CHL and PPD------------------------
write_to_rmd(script = here::here("source","get_chl_pp.R"),
             rmd = here::here("chapters","CHL_PPD_indicator.Rmd"),
             output_path = here::here("chapters",
                                      "CHL_PPD_indicator.Rmd"))

# Harbor porpoise------------------------
write_to_rmd(script = here::here("source","get_harborporpoise.R"),
             rmd = here::here("chapters","HP_indicator.Rmd"),
             output_path = here::here("chapters",
                                      "HP_indicator.Rmd"))
# Aquaculture------------------------
write_to_rmd(script = here::here("source","get_aquaculture.R"),
             rmd = here::here("chapters","Aquaculture_indicators.Rmd"),
             output_path = here::here("chapters",
                                      "Aquaculture_indicators.Rmd"))

# Bennet indicator------------------------
write_to_rmd(script = here::here("source","get_bennet.R"),
             rmd = here::here("chapters","Bennet_indicator.Rmd"),
             output_path = here::here("chapters",
                                      "Bennet_indicator.Rmd"))

# Commercial diversity------------------------
write_to_rmd(script = here::here("source","get_commercial_div.R"),
             rmd = here::here("chapters","Catch_and_Fleet_Diversity_indicators.Rmd"),
             output_path = here::here("chapters",
                                      "Catch_and_Fleet_Diversity_indicators.Rmd"))

# Commercial/recreational reliance and vulnerability
write_to_rmd(script = here::here("source","get_engagement_reliance.R"),
             rmd = here::here("chapters","Comm_rel_vuln_indicator.Rmd"),
             output_path = here::here("chapters",
                                      "Comm_rel_vuln_indicator.Rmd"))
# EPU sf objects
write_to_rmd(script = here::here("source","get_epu_sf.R"),
             rmd = here::here("chapters","EPU.Rmd"),
             output_path = here::here("chapters",
                                      "EPU.Rmd"))