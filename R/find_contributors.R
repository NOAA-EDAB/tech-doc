#' Find all contributors to Tech doc
#'
#' Scans all chapter Rmd for contributors
#'
#' @return Character vector. Unique names of contributors to the current tech doc
#'

find_contributors <- function(){
  # read yml file
  yml <- readLines(here::here("_bookdown.yml"))
  # find reference to rmd files but not ones commented out
  indRmd <- grepl("\\.[rR]md",yml)
  indHash <- grepl("\\#",yml)
  ind <- as.logical(indRmd * !indHash)
  lines <- yml[ind]
  # split by .rmd extension
  fList <-  strsplit(lines,"\\.[rR]md")
  fList <- simplify2array(lapply(fList,'[[',1))[-1] # omit first line, (index file)
  nfList <- lapply(fList,strsplit,"chapters/")
  filenames <-  head(simplify2array(lapply(simplify2array(nfList),'[[',2)),-1)

  # read in each file and pick out contributors
  options(warn=-1)
  tdContributors <- vector(mode="character")
  # loop over each rmd file
  for (afile in filenames) {
    # read in rmd
    chapterContent <- readLines(here::here("chapters",paste0(afile,".Rmd")))
    # pick out contributor line 
    lineContrib <- chapterContent[grepl("Contributor",chapterContent)]
    
    if (length(lineContrib) == 0) next #no contributors for this chapter
    # Now clean up vector of names
    contribs <- strsplit(lineContrib,":")[[1]][2]
    contribs <- strsplit(contribs,",")[[1]] 
    contribs <- sub(pattern="\\s+and\\s+",replacement="",contribs) # remove and if present
    contribs <- sub(pattern="\\.",replacement="",contribs) # remove period if present
    contribs <- sub(pattern="^\\s+",replacement="",contribs) # remove whitespace before
    contribs <- sub(pattern="\\s+$",replacement="",contribs) #and after name
    tdContributors <- c(tdContributors,contribs)
    
  }
  return(unique(sort(tdContributors)))
     
}
