#' Find snippets of text in the Tech doc
#'
#' Scans all chapter Rmd for text snippet
#'
#'@param textSnippet Character string. A snippet of text
#'
#' @return Character vector. Unique names of contributors to the current tech doc
#'

find_text <- function(textSnippet){
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

  options(warn=-1)
  # loop over each rmd file
  for (afile in filenames) {
    # read in rmd
    chapterContent <- readLines(here::here("chapters",paste0(afile,".Rmd")))
    # pick out contributor line 
    
    lineContrib <- chapterContent[grepl(textSnippet,chapterContent)]
    if (length(lineContrib) == 0) next
    
    print(afile)
    #print(lineContrib)
    
    

  }

}
