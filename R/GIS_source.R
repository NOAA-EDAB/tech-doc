#Tech-memo GIS sourcing

#Libraries
library(raster)
library(ncdf4)
library(rgdal)

#Colors for SST anomalies
colors <- colorRampPalette(c("darkblue",'blue', 'white', 'firebrick1',"firebrick4"))  
color_levels=100   

#GIS Directory
gis.dir <- "gis"

#Projection
map.crs <- CRS("+proj=longlat +lat_1=35 +lat_2=45 +lat_0=40 +lon_0=-77 +x_0=0
               +y_0=0 +datum=NAD83 +no_defs +ellps=GRS80 +towgs84=0,0,0")

#Bathymetry
bathy <- raster(paste0(gis.dir,"/NES_bathymetry.tif"))
e  <- extent(-78.5, -64, 33, 45)
bathy <- crop(bathy, e)

#Coastline
coast <- readOGR(gis.dir, 'NES_LME_coast', verbose = F)
coast <- spTransform(coast,map.crs)

#Extent for SST anomaly function
e  <- extent(-77.2, -64.2, 35, 48)
