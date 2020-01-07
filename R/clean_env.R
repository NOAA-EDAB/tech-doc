clean_env <- function(clean=FALSE) {
  if(clean) {
    file.remove(here::here("tech_doc.Rmd"))
  }
  bookdown::clean_book(clean)
}
