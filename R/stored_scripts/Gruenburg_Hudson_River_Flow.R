#Purpose: Create Plot of Mean Annual Hudson River Flowrate at Green Island, NY.
#Data: Hudson River Flow (Gruenburg_River_Flow.Rmd)
#Fit GAM and use year effect as indicator
#Created by Laura Gruenburg - Last edited DEC 01, 2021


#####load required functions
#  You will need to download the Deriv functions from here https://gist.github.com/gavinsimpson/e73f011fdaaab4bb5a30

setwd("~/Desktop/NYB Indicators/Deriv")
source("Deriv.R")
library(mgcv)
library(ggplot2)


#######Load the datasets
setwd("~/Desktop/NYB Indicators/Final_timeseries")
meanflow<-read.csv("Gruenburg_Riverflow2021.csv", header = TRUE)

# Hudson river mean flow data where one column is year and the other is flowrate in m3s-1

# Creat a GAM - adjust k and remember to check model
mod<- gam(flowrate ~ s(year, k=15), data = meanflow)
summary(mod) #check out model
gam.check(mod)

pdata <- with(meanflow, data.frame(year = year))
p2_mod <- predict(mod, newdata = pdata,  type = "terms", se.fit = TRUE)
intercept = 411.6686 # look at p2_mod and extract the intercept
pdata <- transform(pdata, p2_mod = p2_mod$fit[,1], se2 = p2_mod$se.fit[,1])

#  Now that we have the model prediction, the next step is to calculate the first derivative
#  Then determine which increases and decreases are significant
Term = "year"
mod.d <- Deriv(mod, n=70) # n is the number of years
mod.dci <- confint(mod.d, term = Term)
mod.dsig <- signifD(pdata$p2_mod, d = mod.d[[Term]]$deriv,
                    +                    mod.dci[[Term]]$upper, mod.dci[[Term]]$lower)

# Take a quick look to make sure it appears ok before final plotting
plot(flowrate ~ year, data = meanflow)
lines(flowrate ~ year, data = meanflow)
lines(p2_mod+intercept ~ year, data = pdata, type = "n")
lines(p2_mod+intercept ~ year, data = pdata)
lines(unlist(mod.dsig$incr)+intercept ~ year, data = pdata, col = "blue", lwd = 3)
lines(unlist(mod.dsig$decr)+intercept ~ year, data = pdata, col = "red", lwd = 3)

linearMod<- lm(flowrate ~ year, data=meanflow)
summary(linearMod)
mf = meanflow
ggplot() + 
  geom_line(data = meanflow, aes(x = year, y = flowrate), color = 'grey53') +
  geom_point(data = meanflow, aes(x = year, y = flowrate), color = 'gray53') + 
  geom_smooth(data = meanflow, aes(x = year, y = flowrate), method = lm, se = FALSE, color = 'black') + 
  geom_line(data=pdata, aes(x = year, y = p2_mod+intercept), se = FALSE, color = 'black', linetype = 'twodash', size = 1) + 
  geom_line(data = pdata, aes(y = unlist(mod.dsig$incr)+intercept, x = year), color = "blue", size = 1) + 
  geom_line(data = pdata, aes(y = unlist(mod.dsig$decr)+intercept, x = year), color = 'red', size = 1) + 
  theme_bw() +
  labs (y = bquote("Mean Flow "~m^3~"/s"), x = 'Year', title = 'Hudson Mean Flow at Green Island') + 
  theme(plot.title=element_text(size = 16,face = 'bold',hjust = 0.5), axis.title=element_text(size = 14, face = 'bold'), axis.text= element_text(color = 'black', size = 12))
