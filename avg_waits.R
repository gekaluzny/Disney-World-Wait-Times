library(tidyverse)
library(lubridate)
library(hms)
setwd("/Users/grahamkaluzny/Documents/magic_kingdom/")

files <- list.files()

ride_names <- files %>%
  str_extract(".*(?=_)") %>%
  discard(~ .x=="hours") %>%
  unique()

data <- ride_names %>%
  map(~ str_subset(string = files, pattern = .x)) %>%
  set_names(ride_names) %>%
  map(map_dfr, read_csv, col_types = "cd") %>%
  map(mutate_at, "datetime", as_datetime)

hours_files <- list.files(pattern = "hours")

dates <- hours_files %>%
  str_extract("(?<=hours_).{10}") %>%
  ymd()

hours <- hours_files %>%
  map_dfr(read_csv, col_types = "tt") %>%
  mutate(date = dates)

dates_9_11 <- hours %>%
  filter(opening==as.hms("09:00:00") & closing==as.hms("23:00:00")) %>%
  pull(date)
  
avg_waits_9_11 <- data %>%
  map(mutate, datetime_round = round_date(datetime, "10 minutes")) %>%
  map(group_by, datetime_round) %>%
  map(summarize_at, "wait", mean, na.rm = TRUE) %>%
  map(mutate, "date" = date(datetime_round), "time" = strftime(datetime_round, "%H:%M:%S"), 
      "wday" = wday(datetime_round)) %>%
  map(select, -datetime_round) %>%
  map(filter, date %in% dates_9_11) %>%
  map(filter, wday!=6) %>%
  map(spread, key = "time", value = "wait") %>%
  map(summarize_at, vars(-date), mean, na.rm = TRUE) %>%
  map(gather, key = "time", value = "wait") %>%
  map(mutate_at, "time", as.hms) %>%
  reduce(full_join, by = "time") %>%
  setNames(c("time", ride_names)) %>%
  filter(time >= as.hms("09:00:00") & time <= as.hms("23:00:00"))
  
write_csv(avg_waits_9_11, "/Users/grahamkaluzny/Documents/avg_waits_9_11.csv")
  
long <- avg_waits_9_11 %>%
  gather(key = "ride", value = "wait", -time) %>%
  write_csv("/Users/grahamkaluzny/Documents/magic_kingdom.csv")
  

      
