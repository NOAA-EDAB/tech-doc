## ne hab plotting

#```{r NE-HAB, fig.cap="Regional HAB related shellfish bed closures in New England between 2007 and 2016.", fig.asp=1.1, fig.align='center', message=F, warning=F, echo = T}
#get map data and set constants

# Relative working directories
data.dir  <- here::here('data')
r.dir <- here::here('R')
gis.dir <- here::here('gis')

#Source GIS script
source(file.path(r.dir, "GIS_source.R"))

# Load data
load(file.path(data.dir,"SOE_data_erddap.Rdata"))


#projection
map.crs <- CRS("+proj=longlat +lat_1=35 +lat_2=45 +lat_0=40 +lon_0=-77 +x_0=0
               +y_0=0 +datum=NAD83 +no_defs +ellps=GRS80 +towgs84=0,0,0")

#coastline
coast <- readOGR(gis.dir, 'NES_LME_coast', verbose = F)
coast <- spTransform(coast,map.crs)

#define extents for cropping
e1  <- extent(-78.5, -64, 41, 45)

#crop
coast1 <- crop(coast, e1)

#Get data from SOE dataset
events <- SOE.data[grepl("SP occurrence",SOE.data$Var),]
lon <- SOE.data %>%
  dplyr::filter(Var == "NE HAB Regional center Lon") %>% pull(Value)
lat <- SOE.data %>%
  dplyr::filter(Var == "NE HAB Regional center Lat") %>% pull(Value)

events_df <- data.frame(lon = lon,
                        lat = lat,
                        val = events$Value,
                        var = events$Var)


g1 <- events_df %>% filter(val == 8)
#g2 <- events_df %>% filter(val == 3.5)
g3 <- events_df %>% filter(val == 1)

#data.frame to sp object
coordinates(g1) <- ~lon+lat
g1@proj4string <- map.crs
g1 <- spTransform(g1, map.crs)

coordinates(g3) <- ~lon+lat
g3@proj4string <- map.crs
g3 <- spTransform(g3, map.crs)


#plot map and dots of different size based on category
par(mar = c(0,2.8,0,0.2))
plot(coast1, xlim = c(-71.5,-64.5),ylim = c(41,45),col = "grey",yaxs="i")
plot(g1,  add = T,cex = 6, pch = 16, col = "darkorange")
#plot(g2,  add = T,cex = 4, pch = 16, col = "purple")
plot(g3,  add = T,cex = 2, pch = 16, col = c("purple","#56B4E9"))

axis(1, at = c(-71,-69,-67,-65), labels = paste( c(-71,-69,-67,-65) * -1, 'W')
     ,col = NA, col.ticks = 1, pos = 41)
axis(2, at = c(45, 44, 43, 42, 41.05), labels = paste(c(45, 44, 43, 42, 41), 'N')
     , las = T, pos = -71.78,col = NA, col.ticks = 1)
legend(-66.2,42.5, c("PSP", "ASP", "DSP"), col = c("darkorange","purple","#56B4E9"), pch = 16,
       cex = 1.1, bty = "n", pt.cex = 2)
text(-65.65,42.495, "Category")
arrows(-71.765,41,-71.765,45,angle = 90,lwd = 2)
arrows(-64.22,41,-64.22,45,angle = 90,lwd = 2)
abline(h = 41, lwd = 2)
abline(h = 45, lwd = 2)
abline(v = -64, lwd = 2)
legend(-67.9,42.5, c("6-10", "2-5", "1"), col = c("black"), pch = 16, cex = 1.1,
       pt.cex = c(6,4,2), x.intersp = 1.45, y.intersp = 1.75, bty = "n")
text(-67.7,42.525, "2007-2016 Detections")

#```