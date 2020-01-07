# reads in shapefile then simplifies it and writes out to gis folder
simplify_coastline <- function(tol=100000) {
  
  coast <- sf::st_read(here::here("gis"),layer="us_medium_shoreline",quiet=T)
  xmin = -81
  xmax = -66
  ymin = 30
  ymax = 45
  coast <- sf::st_crop(coast,c(xmin=xmin, xmax=xmax,ymin=ymin,ymax=ymax))
  map.crs <- "+proj=longlat +lat_1=35 +lat_2=45 +lat_0=40 +lon_0=-77 +x_0=0
                +y_0=0 +datum=NAD83 +no_defs +ellps=GRS80 +towgs84=0,0,0"
  coast <- sf::st_transform(coast,map.crs)
  
  simplifiedCoast <- sf::st_as_sf(rgeos::gSimplify(sf::as_Spatial(sf::st_geometry(coast)),tol=tol))
#  return(simplifiedCoast)
  
   # plot(gSimplify(sf::as_Spatial(sf::st_geometry(coast)),tol=10000000));title("tol: 10000000")
  sf::st_write(simplifiedCoast,dsn=here::here("gis"),layer="NEUSCoast",driver="ESRI Shapefile",delete_layer=T,update=T)
}