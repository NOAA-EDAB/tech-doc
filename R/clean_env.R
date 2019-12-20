clean_env <- function(clean=FALSE) {
  if(clean) {
    file.remove(here::here("_main.Rmd"))
  }
  bookdown::clean_book(clean)
}
