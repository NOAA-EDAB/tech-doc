## Catch and Fleet Diversity plotting

#```{r fleet-diversity, fig.cap="Fleet diversity (A) and fleet count (B) in the Mid Atlantic Bight.", echo=T, message=FALSE, warning=FALSE, fig.align="center", eval = T}

# Relative working directories
data.dir  <- here::here("data")
r.dir <- here::here("R")

# Load data
load(file.path(data.dir,"SOE_data_erddap.Rdata"))

# Source plotting functions
source(file.path(r.dir,"BasePlot_source.R"))

opar <- par(mfrow = c(2, 1), mar = c(0, 0, 0, 0), oma = c(4, 6, 2, 6))

soe.plot(SOE.data, "Time", "Mid-Atlantic average fleet diversity", stacked = "A",
         rel.y.num = 0.9, end.start = 2008, tol = 0.15, full.trend = F, cex.stacked = 1.5)
soe.stacked.axis("Year", "Fleet diversity", y.line = 2.5, outer = F,
                 rel.x.text = 1, rel.y.text = 1)
soe.plot(SOE.data,"Time", "Mid-Atlantic fleet count", stacked = "B",
         rel.y.num = 0.9, end.start = 2008, full.trend = F, cex.stacked = 1.5)

soe.stacked.axis("Year", "Fleet count", y.line = 2.5, outer = F,
                 rel.x.text = 1, rel.y.text = 0.95)

#```