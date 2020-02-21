#```{r , fig.cap = " HMS landings from 2016-2018 broken out by group (sharks, tunas or swordfish.", fig.align="center", eval=T, echo=F}

apex<-ecodata::hms_landings_weight

apex$sp.group <- ifelse(grepl("Shark", apex$Var, ignore.case = T), "shark", 
                        ifelse(grepl("TUNA", apex$Var, ignore.case = T), "tuna", "swordfish"))

apex<-apex %>% 
  dplyr::group_by(sp.group, Region, Time) %>% 
  dplyr::summarise(Value = sum(Value)) %>% 
  dplyr::mutate(Units = c("metric tons"),
                feeding.guild = factor(c("Apex Predator")),
                Value = (Value/2024.6)) %>% 
  dplyr::rename(EPU = Region, 
                Var = sp.group) %>% 
  dplyr::mutate(grouping = factor(c("total")))


#Define constants for figure plot
series.col <- c("indianred","black")

##Plot
apex %>% 
  dplyr::filter(EPU == "MA") %>% 
  dplyr::group_by(Var) %>% 
  dplyr::mutate(hline = mean(Value)) %>% 
  ggplot(aes(x = Time, y = Value, color = Var)) +
  
  #Add time series
  geom_line(size = lwd) +
  geom_point(size = pcex) +
  stat_summary(fun.y = sum, color = "black", geom = "line")+
  #scale_color_manual(values = series.col, aesthetics = "color")+
  #guides(color = FALSE) +
  geom_hline(aes(yintercept = hline,
                 color = Var,
                 size = Var),
             size = hline.size,
             alpha = hline.alpha,
             linetype = hline.lty)+
  #Highlight last ten years
  annotate("rect", fill = shade.fill, alpha = shade.alpha,
           xmin = x.shade.min , xmax = x.shade.max,
           ymin = -Inf, ymax = Inf) +
  #Axis and theme
  scale_y_continuous(labels = function(l){trans = l / 1000})+
  scale_x_continuous(breaks = seq(1985, 2015, by = 5), limits = c(1985, 2018)) +
  theme_facet() +
  theme(strip.text=element_text(hjust=0), 
        legend.position = c(0.4, 0.7), 
        legend.direction = "horizontal", 
        legend.title = element_blank())+
  ylab("")

#```
