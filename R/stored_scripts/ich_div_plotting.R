## Ich Div Plotting

#```{r larval-diversity, fig.cap="Ichthyoplankton Shannon diversity in the spring (A) and fall (B) in the Northeast Large Marine Ecosystem.",echo = T, fig.show='hold', fig.align='default', warning = F, message = F,fig.pos='H'}
# Relative working directories
data.dir  <- here::here('data')
r.dir <- here::here('R')

# Load data
load(file.path(data.dir,"SOE_data_erddap.Rdata"))

# Source plotting functions
source(file.path(r.dir,"BasePlot_source.R"))


opar <- par(mfrow = c(2, 1), mar = c(0, 0, 0, 0), oma = c(3.5, 5, 2, 4))

soe.plot(SOE.data, "Time", "Spring_Ich_Shannon Diversity Index", stacked = "A",
         rel.y.num = 1.1, end.start = 2007, full.trend = F,
         cex.stacked = 1.5)
soe.plot(SOE.data, "Time", "Fall_Ich_Shannon Diversity Index", stacked = "B",
         rel.y.num = 1.1, end.start = 2007, full.trend = F,
         cex.stacked = 1.5)

soe.stacked.axis("Year", "Shannon Index", y.line = 2.5)

#```