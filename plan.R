# A script to read in processing functions from the ecodata package. 
# These will be used to create a drake workflow, and are strictly for detecting changes to the master
# branch of ecodata. These functions are not sourced because they will break.
library(drake)
library(dplyr)

source_dir <- file.path(here::here("source"))
source_names <- list.files(source_dir)

ind_dir <- file.path(here::here("chapters"))
ind_names <- list.files(ind_dir)


test_files <- c("index.Rmd",
                "erddap_query_and_build.Rmd",
"aggregate_groups.Rmd",
"Annual_SST_cycle_indicator.Rmd",
"Aquaculture_indicators.Rmd",
"Bennet_indicator.Rmd",
"Catch_and_Fleet_Diversity_indicators.Rmd",
"CHL_PPD_indicator.Rmd",
"Comm_climate_vuln_indicator.Rmd",
"conceptualmodels.Rmd",
"Condition_indicator.Rmd",
"EPU.Rmd")

test <- drake_plan(
  
  #Create targets for processing functions
  proc = target(

     readLines(con = file.path(source_dir, fcon)),
     transform = map(fcon = !!source_names)

  ),
  
  book = target(
    bookdown::render_book(input = "index.Rmd",
                          config_file = "_bookdown.yml")
  )
  # Create targets for indicator sections (the .Rmd files)
)

make(test)

out <- drake_config(test)
vis_drake_graph(out)

