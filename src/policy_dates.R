library(dplyr)
library(lubridate)


# ACAPS -----------
national <- read.csv("../data/policy_data/acaps/acaps_covid.csv", stringsAsFactors = FALSE)
names(national) <- tolower(names(national))
us <- national %>% 
  filter(iso == "USA") %>%
  select(country, category, measure, comments,
            date_implemented, source)

# coerce dates
us$date_implemented <- dmy(us$date_implemented)

write.csv(us, "../data/policy_data/acaps/acaps_nationa.csv", row.names = FALSE)