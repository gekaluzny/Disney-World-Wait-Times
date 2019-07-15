library(tidyverse)
library(lubridate)
library(hms)
setwd("/Users/grahamkaluzny/Documents/magic_kingdom/")

files <- list.files()

ride_names <- files %>%
  str_replace("_.*", "") %>%
  unique()

data <- ride_names %>%
  map(~ str_subset(string = files, pattern = .x)) %>%
  set_names(ride_names) %>%
  map(map_dfr, read_csv, col_types = "cd") %>%
  map(mutate_at, "time", as_datetime)

avg_waits <- data %>%
  map(mutate_at, "time", round_date, "10 minutes") %>%
  map(group_by, time) %>%
  map(summarize_all, mean) %>%
  map(mutate, "date" = date(time), "time" = strftime(time, "%H:%M:%S")) %>%
  map(spread, key = "time", value = "wait") %>%
  map(summarize_at, vars(-date), mean, na.rm = TRUE) %>%
  map(gather, key = "time", value = "wait") %>%
  map(mutate_at, "time", as.hms) %>%
  reduce(full_join, by = "time") %>%
  setNames(c("time", ride_names)) %>%
  filter(time >= as.hms("09:00:00") & time <= as.hms("22:00:00"))
  
  

  

      