#A script to pull processing functions from the data-raw directory of the ecodata github repo
library(rvest)
library(xml2)
library(stringr)
library(dplyr)
library(RCurl)

#A regex pattern to remove html
pattern <- "<!--?\\w+((\\s+\\w+(\\s*=\\s*(?:\".*?\"|'.*?'|[^'\"-->\\s]+))?)+\\s*|\\s*)/?>"

# A function to get raw processing code from ecodata repo-----------------------------------------------
get_raw_funcs <- function(script){
  print(script)
  #Find raw text and parse it to R
  fraw <- getURL(paste0("https://raw.githubusercontent.com/NOAA-EDAB/ecodata/master/data-raw/",script),
                 ssl.verifypeer = FALSE)
  
  fparsed <- gsub(pattern, "\\1", fraw)
  #save it as a source file
  
  fcon <- file.path(here::here("source",script))
  writeLines(fparsed, con = fcon)
  
}


#Scrape list of processing functions from ecodata repo--------------------------------------------------
page <- xml2::read_html("https://github.com/NOAA-EDAB/ecodata/tree/master/data-raw")

data_raw <- page %>% 
  html_nodes('.js-navigation-open') %>% 
  html_text() %>% 
  as.data.frame() %>% 
  dplyr::select(files = ".") %>%
  mutate(files = as.character(files)) %>% 
  filter(str_detect(.$files, pattern = "R$")) #Note that this pulls any files ending in ".R" in ecodata/data-raw
  
#Write files to tech-doc/source
lapply(data_raw$files, FUN = get_raw_funcs)

