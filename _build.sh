#!/bin/sh

Rscript -e "source('R/pull_functions.R')"
Rscript -e "source('R/write_processing_steps.R')"
Rscript -e "bookdown::render_book('index.Rmd', 'bookdown::gitbook')"
