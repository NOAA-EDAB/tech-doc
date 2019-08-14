write_to_rmd <- function(script, rmd, hook = NULL, output_path){
  
  #Read in script
  source <-  readr::read_file(script)

  #Concatenate Rmd chunk yml
  source <- paste0("```{r, eval = F, echo = T}\n",source, "```\n")
  
  #Read in Rmd
  rmd = here::here("chapters","inshore_bottom_trawl_surveys.rmd")
  rmd <- readr::read_file(rmd)
  
  output <- stringr::str_replace(rmd,
                       regex(paste0("Process",hook,"Start\\}\\} -->.*\\<\\!-- \\{\\{Process",hook,"End"),dotall = T),
                       paste0("Process",hook,"Start}} -->\\\n",source,"<\\!-- \\{\\{Process",hook,"End"))
  
  
  #write output to file
  readr::write_file(output, path = output_path)

}

#Seasonal SST anomaly----------------------

write_to_rmd(script = here::here("source","get_seasonal_oisst_anom_gridded.r"),
             rmd = here::here("chapters","Seasonal_SST_anomaly_maps_indicator.rmd"),
             output_path = here::here("chapters",
                                      "Seasonal_SST_anomaly_maps_indicator.rmd"))

#Single species stock data----------------------

write_to_rmd(script = here::here("source","get_stocks.r"),
             rmd = here::here("chapters","singlespp_status_indicator.rmd"),
             output_path = here::here("chapters",
                                      "singlespp_status_indicator.rmd"))

#Inshore surveys----------------------

write_to_rmd(script = here::here("source","get_ne_inshore_survey.r"),
             rmd = here::here("chapters","inshore_bottom_trawl_surveys.rmd"),
             hook = "NESurvey",
             output_path = here::here("chapters",
                                      "inshore_bottom_trawl_surveys.rmd"))

write_to_rmd(script = here::here("source","get_mass_inshore_survey.r"),
             rmd = here::here("chapters","inshore_bottom_trawl_surveys.rmd"),
             hook = "MassSurvey",
             output_path = here::here("chapters",
                                      "inshore_bottom_trawl_surveys.rmd"))

write_to_rmd(script = here::here("source","get_mab_inshore_survey.r"),
             rmd = here::here("chapters","inshore_bottom_trawl_surveys.rmd"),
             hook = "NEAMAPSurvey",
             output_path = here::here("chapters",
                                      "inshore_bottom_trawl_surveys.rmd"))

#NEFSC Bottom Trawl Survey----------------------

write_to_rmd(script = here::here("source","get_nefsc_survey.r"),
             rmd = here::here("chapters","survey_data.rmd"),
             output_path = here::here("chapters",
                                      "survey_data.rmd"))
# CFDBS Landings Data----------------------

write_to_rmd(script = here::here("source","get_comdat.r"),
             rmd = here::here("chapters","landings_data.rmd"),
             output_path = here::here("chapters",
                                      "landings_data.rmd"))
# Gulf Stream Index----------------------

write_to_rmd(script = here::here("source","get_gsi.r"),
             rmd = here::here("chapters","gulf_stream_index.rmd"),
             output_path = here::here("chapters",
                                      "gulf_stream_index.rmd"))
# Recreational indicators----------------------

write_to_rmd(script = here::here("source","get_rec.r"),
             rmd = here::here("chapters","Recreational_Data.rmd"),
             output_path = here::here("chapters",
                                      "Recreational_Data.rmd"))

# Zooplankton indicators----------------------

# Abundance anomaly
write_to_rmd(script = here::here("source","get_zoo_anom_sli.r"),
             rmd = here::here("chapters","Zooplankton_indicators.rmd"),
             hook = "AbundAnom",
             output_path = here::here("chapters",
                                      "Zooplankton_indicators.rmd"))
#Seasonal abundance 1
write_to_rmd(script = here::here("source","process_oi.r"),
             rmd = here::here("chapters","Zooplankton_indicators.rmd"),
             hook = "SeasAbund1",
             output_path = here::here("chapters",
                                      "Zooplankton_indicators.rmd"))
#Seasonal abundance 2
write_to_rmd(script = here::here("source","get_zoo_oi.r"),
             rmd = here::here("chapters","Zooplankton_indicators.rmd"),
             hook = "SeasAbund2",
             output_path = here::here("chapters",
                                      "Zooplankton_indicators.rmd"))

# Common tern diet data------------------------

#Seasonal abundance 2
write_to_rmd(script = here::here("source","get_commontern.r"),
             rmd = here::here("chapters","seabird_diet_and_productivity.rmd"),
             output_path = here::here("chapters",
                                      "seabird_diet_and_productivity.rmd"))

# Ches bay water quality------------------------
write_to_rmd(script = here::here("source","get_ches_bay_wq.r"),
             rmd = here::here("chapters","ches_bay_water_quality.rmd"),
             output_path = here::here("chapters",
                                      "ches_bay_water_quality.rmd"))

# Species distribution indicators--------------
write_to_rmd(script = here::here("source","get_species_dist.r"),
             rmd = here::here("chapters","Species_dist_indicators.rmd"),
             output_path = here::here("chapters",
                                      "Species_dist_indicators.rmd"))
# NARW------------------------
write_to_rmd(script = here::here("source","get_narw.r"),
             rmd = here::here("chapters","RW_indicator.rmd"),
             output_path = here::here("chapters",
                                      "RW_indicator.rmd"))
# Productivity data------------------------
write_to_rmd(script = here::here("source","get_productivity_anomaly.r"),
             rmd = here::here("chapters","productivity_for_tech_memo.rmd"),
             output_path = here::here("chapters",
                                      "productivity_for_tech_memo.rmd"))

# Long-term SST time series------------------------
write_to_rmd(script = here::here("source","get_long_term_sst.r"),
             rmd = here::here("chapters","long_term_sst_indicator.rmd"),
             output_path = here::here("chapters",
                                      "long_term_sst_indicator.rmd"))

# Ichthyoplankton div indices------------------------
write_to_rmd(script = here::here("source","get_ichthyoplankton.r"),
             rmd = here::here("chapters","ich_div_indicator.rmd"),
             output_path = here::here("chapters",
                                      "ich_div_indicator.rmd"))

# CHL and PPD------------------------
write_to_rmd(script = here::here("source","get_chl_pp.r"),
             rmd = here::here("chapters","CHL_PPD_indicator.rmd"),
             output_path = here::here("chapters",
                                      "CHL_PPD_indicator.rmd"))

# Harbor porpoise------------------------
write_to_rmd(script = here::here("source","get_harborporpoise.r"),
             rmd = here::here("chapters","HP_indicator.rmd"),
             output_path = here::here("chapters",
                                      "HP_indicator.rmd"))
# Aquaculture------------------------
write_to_rmd(script = here::here("source","get_aquaculture.r"),
             rmd = here::here("chapters","Aquaculture_indicators.rmd"),
             output_path = here::here("chapters",
                                      "Aquaculture_indicators.rmd"))

# Bennet indicator------------------------
write_to_rmd(script = here::here("source","get_bennet.r"),
             rmd = here::here("chapters","Bennet_indicator.rmd"),
             output_path = here::here("chapters",
                                      "Bennet_indicator.rmd"))

# Commercial diversity------------------------
write_to_rmd(script = here::here("source","get_commercial_div.r"),
             rmd = here::here("chapters","Catch_and_Fleet_Diversity_indicators.rmd"),
             output_path = here::here("chapters",
                                      "Catch_and_Fleet_Diversity_indicators.rmd"))

# Commercial/recreational reliance and vulnerability
write_to_rmd(script = here::here("source","get_engagement_reliance.r"),
             rmd = here::here("chapters","Comm_rel_vuln_indicator.rmd"),
             output_path = here::here("chapters",
                                      "Comm_rel_vuln_indicator.rmd"))
# EPU sf objects
write_to_rmd(script = here::here("source","get_epu_sf.r"),
             rmd = here::here("chapters","EPU.rmd"),
             output_path = here::here("chapters",
                                      "EPU.rmd"))

