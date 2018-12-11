#get latest data sets from ERDDAP

get_erddap <- function(df, id = NULL){
  
  `%>%` <- magrittr::`%>%`
  
  df$Dataset.ID
  
  if (!is.null(id)){
    df <- df %>% dplyr::filter(stringr::str_detect(Dataset.ID, id))
  }
  
  
  versions <- stringr::str_split_fixed(df$Dataset.ID, "(?=\\d+)",2)
  versions <- data.frame(Dataset.ID = versions[,1],
                         v  = as.numeric(versions[,2]))
  
  newest <- versions %>%
    dplyr::group_by(Dataset.ID) %>%
    dplyr::filter(v == max(v)) %>% 
    tidyr::unite(., Dataset.ID, c("Dataset.ID","v"), sep = "") %>% 
    dplyr::inner_join(df,.)
  
  if (is.null(id)){
    
    return(newest)
    
  } else {
    
    single_out <- sprintf("http://comet.nefsc.noaa.gov/erddap/tabledap/%s.csv",
                          newest$Dataset.ID) %>% 
      purrr::map(function(x) {
        readr::read_csv(url(x))
      }) 
    
    single_out <- single_out[[1]]
    if (all(is.na(single_out[1,]))){
      single_out <- dplyr::slice(single_out, -1)
    }

    return(single_out)
  }
  
  
}
