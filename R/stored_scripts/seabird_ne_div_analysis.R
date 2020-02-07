#common tern diversity analysis



#```{r diet-div, eval = T, echo = T}
#Calculating time series of diversity indices using the vegan package. 
diet_div <- ecodata::common_tern %>% 
  filter(str_detect(Var, "Diet"),
         !str_detect(Var, "Sum")) %>% 
  mutate(Island = word(Var, 1),
         Var = word(Var, 4)) %>% 
  group_by(Island, Time) %>%
  dplyr::summarise(evenness = diversity(Value)/log(specnumber(Value)),
                   shannon = diversity(Value),
                   simpson = diversity(Value, index = "simpson")) %>% 
  gather(.,Var,Value,-Island, -Time) %>% 
  group_by(Var, Time) %>%
  dplyr::summarize(Value = mean(Value, na.rm = T),
                   sd = sd(Value, na.rm = T),
                   n = n()) %>%
  group_by(Var) %>% 
  mutate(hline = mean(Value, na.rm = T))
#```