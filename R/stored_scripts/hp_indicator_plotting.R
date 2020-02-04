### Harbor Porpoise Plotting

#```{r harbor-porpoise, fig.cap="Harbor porpoise bycatch estimated shown with 
#Potential Biological Removal (red) and confidence intervals (orange).", 
#echo = T, message=F, warning=F, fig.pos='H', fig.height=4}

# Relative working directories
data.dir  <- here::here('data')
r.dir <- here::here('R')

# Load data
load(file.path(data.dir,"SOE_data_erddap.Rdata"))

# Source plotting functions
source(file.path(r.dir,"BasePlot_source.R"))


opar <- par(mar = c(4, 6, 2, 6))

soe.plot(SOE.data, 'Time', "Harbor porpoise bycatch estimates",            
         rel.y.num = 1.2, end.start = 2007, full.trend = F, point.cex = 1,
         ymax = F, y.upper = 2500, mean_line = F, x.label = 'Year',
         y.label = 'Bycatch, n', rel.y.text = 1)

legend(2000, 2250, legend = "Potential Biological Removal",
       col = adjustcolor("red", .5), lwd = 3,
       bty = "n", cex = 0.9)

#credible intervals and PBI
lw_CI <- SOE.data[Var == 'Harbor porpoise bycatch 2.5 CI',
                  list(Time, Value)]
up_CI <- SOE.data[Var == 'Harbor porpoise bycatch 97.5 CI',
                  list(Time, Value)]
pbi   <- SOE.data[Var == 'Harbor porpoise potential biological removal',
                  list(Time, Value)]

points(pbi,   type  = "l", lty = 1, col = adjustcolor("red", .5), lwd = 3)
points(lw_CI, type  = "l", lty = 2, col = adjustcolor("darkorange", .9), lwd = 2.5)
points(up_CI, type  = "l", lty = 2, col = adjustcolor("darkorange", .9), lwd = 2.5)
#```