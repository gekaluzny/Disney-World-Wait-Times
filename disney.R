library(tidyverse)
library(lubridate)
library(hms)
library(combinat)

data <- read_csv("/Users/grahamkaluzny/Documents/disney.csv")

avg_waits <- data %>%
  mutate(datetime_round = round_date(datetime, unit = "15 minutes")) %>%
  mutate(time = strftime(datetime_round, "%H:%M")) %>%
  filter(time <= "22:00") %>%
  select(-starts_with("datetime")) %>%
  mutate_at(vars(-time), str_extract, "\\d+") %>%
  mutate_at(vars(-time), as.numeric) %>%
  group_by(time) %>%
  summarise_all(mean, na.rm = TRUE)

long <- avg_waits %>%
  gather(key = "ride", value = "wait", -time) %>%
  filter(!is.na(wait))

write_csv(long, "/Users/grahamkaluzny/Documents/magic_kingdom.csv")

