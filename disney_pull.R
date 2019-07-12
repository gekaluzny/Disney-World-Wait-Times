library(tidyverse)
library(rvest)
library(lubridate)

dateseq <- seq.Date(from = as_date('2019-06-01'), to = as_date('2019-06-02'), by = 'day')

waittimes <- function(x) {
  url <- paste0('https://touringplans.com/magic-kingdom/attractions/haunted-mansion/wait-times/date/', x)
  file <- read_html('https://touringplans.com/magic-kingdom/attractions/haunted-mansion/wait-times/date/2019-07-11')
  
  lines <- file %>%
    html_nodes('#center') %>%
    html_nodes('script') %>%
    html_text() %>%
    strsplit('\n') %>%
    unlist() %>%
    str_subset('\\[new Date\\(') %>%
    str_subset('\\),,,,,,,,\\d+,,,,,null,,null')
  
  dates <- lines %>%
    str_extract('Date\\(.*\\)') %>%
    str_extract('[0-9,]+') %>%
    as_datetime()
  
  waits <- lines %>%
    str_extract('\\).*') %>%
    str_extract('\\d+') %>%
    as.numeric()
  
  waits_tib <- tibble(dates, waits)
  return(waits_tib)
}

waittimes_all <- map(dateseq, waittimes)

