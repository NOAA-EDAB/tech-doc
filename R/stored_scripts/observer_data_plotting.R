# observer data plotting

#```{r, echo = T, eval = F}

#For map and plot. Latitude and longitude data for this figure are not publicly available. 
sk.dat <- SOE.data[grepl("Lat",SOE.data$Units) &
                     grepl("Southern Kingfish",SOE.data$Var),]
lon <- sk.dat[as.numeric(sk.dat$Value) < 0,]$Value
lat <- sk.dat[as.numeric(sk.dat$Value) > 0,]$Value

#create data.frame
df <- data.frame(year = sk.dat$Time,
                 lon = lon,
                 lat = lat)

#set color palette
colors1 <- adjustcolor(matlab.like2(8),.5)
colors2 <- adjustcolor(matlab.like2(8),.5)
colors3 <- adjustcolor(matlab.like2(8),.5)
colors4 <- adjustcolor(matlab.like2(8),1)
colors <- c(colors1[1:2], colors2[3:4], colors3[5:6],colors4[7:8])

#map values to colors
df <- df %>% arrange(year) %>%
  mutate(colors = plyr::mapvalues(year, from = c("2010","2011","2012","2013",
                                                 "2014","2015","2016","2017"),
                                  to = c(colors)))
colors <- df$colors

#projection
map.crs <- CRS("+proj=longlat +lat_1=35 +lat_2=45 +lat_0=40 +lon_0=-77 +x_0=0
               +y_0=0 +datum=NAD83 +no_defs +ellps=GRS80 +towgs84=0,0,0")

#data.frame to sp object
coordinates(df) <- ~lon+lat
df@proj4string <- map.crs
df <- spTransform(df, map.crs)

#plot
par(fig = c(0,1,0,1))
plot(coast, xlim = c(-76,-73), ylim = c(35,40.5),col = "grey")
plot(df, pch = 16, col = colors, add = T, cex = 2.5)


occur <- SOE.data[SOE.data$Var == "Southern Kingfish observer sightings",]$Value
time <- SOE.data[SOE.data$Var == "Southern Kingfish observer sightings",]$Time

ts <- zoo(occur,time)
par(fig = c(0.5,1, 0.1, .5), new = T, bty = "l",mar = c(5,6,3,1)) 
barplot(occur,time, col = matlab.like2(8), xlab = c("Time"),ylab = "S. Kingfish Occurrence, n",
        cex.lab = 1, las = 1, cex.axis = 1)
axis(1,at = seq(1250,18500,length.out = 8),labels = c("2010","2011","2012","2013",
                                                      "2014","2015","2016","2017"), cex.axis=1)
#```