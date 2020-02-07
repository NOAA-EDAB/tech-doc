# summer flounder occupancy model plot

#```{r occupancy-MAB, fig.cap="Summer flounder spring (A) and fall (B) occupancy habitat area in the Northeast Large Marine Ecosystem. ", echo = T, fig.show='hold', warning = F, message = F,fig.pos='H'}

# Relative working directories
data.dir  <- here::here('data')
r.dir <- here::here('R')

# Load data
load(file.path(data.dir,"SOE_data_erddap.Rdata"))

# Source plotting functions
source(file.path(r.dir,"BasePlot_source.R"))


opar <- par(mfrow = c(2, 1), mar = c(0, 0, 0, 0), oma = c(3.5, 5, 2, 4))

soe.plot(SOE.data, "Time", "sumflo spring habitat occupancy", stacked = "A",
         rel.y.num = 1.1, scale.axis = 10^3, end.start = 2007, full.trend = F,
         cex.stacked = 1.5)
soe.plot(SOE.data, "Time", "sumflo fall habitat occupancy", stacked = "B",
         rel.y.num = 1.1, scale.axis = 10^3, end.start = 2007, full.trend = F,
         cex.stacked = 1.5)

soe.stacked.axis("Year", expression("Habitat Area, 10"^3*" km"^2), y.line = 2.5)

#```