#### Annual SST cycles Extraction and Processing

#libraries
library(ncdf4);library(dplyr)
library(readr);library(tidyr)
library(sp);library(rgdal)
library(raster);library(stringr)

#get spatial polygons for Ecological Production Units (EPUs) that are used to clip SST data.
EPU <- readOGR('Extended_EPU')

map.crs <- CRS("+proj=longlat +lat_1=35 +lat_2=45 +lat_0=40 +lon_0=-77 +x_0=0
               +y_0=0 +datum=NAD83 +no_defs +ellps=GRS80 +towgs84=0,0,0")

#find long term daily mean SSTs and 2017 SST anomaly
MAB_sst_daily_mean <- NULL
GB_sst_daily_mean <- NULL
GOM_sst_daily_mean <- NULL

#I split the data into three directories to loop through in separate R sessions concurrently. 


for (dir. in 1:3){
  
  #Loop through directories
  setwd(paste0('c:/users/sean.hardison/documents/sst_data/',dir.))
  print(getwd())
  
  for (f in 1:length(list.files())){
    
    if (!str_detect(list.files()[f],".nc")){
      print(paste(list.files()[f],"is not a raster")) #Based on file type
      next
    }
    
    for (j in c("MAB","GB","GOM")){
      
      sub_region <- EPU[EPU@data$EPU == j,]
      y <- as.numeric(str_extract(list.files()[f],"[0-9]+")) #get year
      
      for (i in 1:365){
        print(paste(j,y,i))
        daily_mean <- raster(paste0(list.files()[f]), band = i) #get band
        
        #set crs
        daily_mean@crs <- sub_region@proj4string 
        
        
        #rotate to lon scale from 0-360 to -180-180
        daily_mean <- rotate(daily_mean)
        
        #mask raster with spatialpolygon
        daily_mean_clipped <- mask(daily_mean, sub_region)
        
        
        #add mean value to data.frame
        assign(paste0(j,"_sst_daily_mean"),
               rbind(get(paste0(j,"_sst_daily_mean")),
                     c(mean(daily_mean_clipped@data@values, na.rm = T),y,i)))
        
      }
    }
    
    
  }
}

#Put results into data.frames
mab <- data.frame(EPU = "MAB",
                  year = MAB_sst_daily_mean[,2],
                  day = MAB_sst_daily_mean[,3],
                  Value = MAB_sst_daily_mean[,1])

gb <- data.frame(EPU = "GB",
                 year = GB_sst_daily_mean[,2],
                 day = GB_sst_daily_mean[,3],
                 Value = GB_sst_daily_mean[,1])

gom <- data.frame(EPU = "GOM",
                  year = GOM_sst_daily_mean[,2],
                  day = GOM_sst_daily_mean[,3],
                  Value = GOM_sst_daily_mean[,1])


data3 <- rbind(mab, gb, gom)

#Save as 1 of 3 files (one for each directory containing daily mean data)
save(data3, file = "dir3_sst.Rdata")

#--------------------------2017 SSTs----------------------------#
MAB_2017 <- NULL
GB_2017 <- NULL
GOM_2017 <- NULL

for (j in c("MAB","GB","GOM")){
  
  sub_region <- EPU[EPU@data$EPU == j,]
  
  for (i in 1:365){
    print(paste(j,i))
    daily_mean <- raster("sst.day.mean.2017.nc", band = i) #get band
    
    
    #set crs
    daily_mean@crs <- sub_region@proj4string 
    
    
    #rotate to lon scale from 0-360 to -180-180
    daily_mean <- rotate(daily_mean)
    
    #mask raster with spatialpolygon
    daily_mean_clipped <- mask(daily_mean, sub_region)
    
    
    #add mean value to data.frame
    assign(paste0(j,"_2017"),
           rbind(get(paste0(j,"_2017")),
                 c(mean(daily_mean_clipped@data@values, na.rm = T),"2017",i)))
    
  }
}
#Put results into data.frames
mab_2017 <- data.frame(EPU = "MAB",
                       year = MAB_2017[,2],
                       day = MAB_2017[,3],
                       Value = MAB_2017[,1])

gb_2017 <- data.frame(EPU = "GB",
                      year = GB_2017[,2],
                      day = GB_2017[,3],
                      Value = GB_2017[,1])

gom_2017 <- data.frame(EPU = "GOM",
                       year = GOM_2017[,2],
                       day = GOM_2017[,3],
                       Value = GOM_2017[,1])


#Final 2017 daily mean data
sst_2017 <- rbind(mab_2017, gb_2017, gom_2017)
#save(sst_2017, file = "sst_2017.Rdata")

