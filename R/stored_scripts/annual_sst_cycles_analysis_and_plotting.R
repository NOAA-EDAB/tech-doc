#### annual sst cycles data analysis and plotting

### Analysis 
#----------------------Load results--------------------------#
load("dir1_sst.Rdata")
load("dir2_sst.Rdata")
load("dir3_sst.Rdata")
load("sst_2017.Rdata")

#Get long term mean and standard deviation
d <- rbind(data1, data2, data3)

ltm <- d %>% group_by(EPU, day) %>% dplyr::summarise(mean  = mean(Value),
                                                     sd = sd(Value)) 


### Plotting
# ```{r plotting, echo = T, eval = T, fig.cap = "Long-term mean SSTs for the Mid-Atlantic Bight (A),
# Georges Bank (B), and Gulf of Maine (C). Orange and cyan shading show where the 2017 daily SST 
# values were above or below the long-term mean respectively; red and dark blue shades indicate days 
# when the 2017 mean exceeded +/- 1 standard deviation from the long-term mean.", fig.width=8, 
# fig.height=3.25, fig.align='center'}

# Load data
load(file.path(data.dir,"SOE_data_erddap.Rdata"))

##---------------------------------MAB-----------------------------------------#
par(mfrow = c(1,3))
doy <- as.numeric(SOE.data[SOE.data$Var == "sst mean 2017 MAB",]$Time)
val_2017 <- SOE.data[SOE.data$Var == "sst mean 2017 MAB",]$Value
val_LT <- SOE.data[SOE.data$Var == "sst mean long term MAB",]$Value
val_LT_sd <- SOE.data[SOE.data$Var == "sst sd long term MAB",]$Value


# val_2017 <- approx(doy,val_2017, xout = seq(doy[1],doy[length(doy)],length.out = 365*1))$y
# val_LT <- approx(doy,val_LT, xout = seq(doy[1],doy[length(doy)],length.out = 365*1))$y
# val_LT_sd <- approx(doy,val_LT_sd, xout = seq(doy[1],doy[length(doy)],length.out = 365*1))$y
doy <- seq(doy[1],doy[length(doy)],length.out = 365*1)


above_mean <- NULL
for (i in 1:length(val_2017)){
  if (val_2017[i] >= val_LT[i]){
    above_mean[i] <- val_2017[i]
  } else if (val_2017[i] < val_LT [i]){
    above_mean[i] <- NA
  }
}

below_mean <- NULL
for (i in 1:length(val_2017)){
  if (val_2017[i] <= val_LT[i]){
    below_mean[i] <- val_2017[i]
  } else if (val_2017[i] > val_LT [i]){
    below_mean[i] <- NA
  }
}

above_sd <- NULL
for (i in 1:length(val_2017)){
  if (val_2017[i] >= val_LT_sd[i] + val_LT[i]){
    above_sd[i] <- val_2017[i]
  } else if (val_2017[i] < val_LT_sd [i] + val_LT[i]){
    above_sd[i] <- NA
  }
}

below_sd <- NULL
for (i in 1:length(val_2017)){
  if (val_2017[i] <= val_LT[i] - val_LT_sd[i]){
    below_sd[i] <- val_2017[i]
  } else if (val_2017[i] > val_LT[i] - val_LT_sd [i]){
    below_sd[i] <- NA
  }
}

#Lines for polygons
above_sd[is.na(above_sd)] <- val_LT_sd[which(is.na(above_sd))] + val_LT[which(is.na(above_sd))]
below_sd[is.na(above_sd)] <- val_LT[which(is.na(below_sd))] - val_LT_sd[which(is.na(below_sd))] 
above_mean[is.na(above_mean)] <- val_LT[which(is.na(above_mean))]
below_mean[is.na(below_mean)] <- val_LT[which(is.na(below_mean))]

upper <- val_LT_sd + val_LT
lower <- val_LT - val_LT_sd

#Null figure
plot(NULL, xlim = c(doy[1],doy[(length(doy))]), ylim = c(4,25), las = 1, 
     ylab = "", yaxt = "n", xaxt = "n", xlab = "")
axis(2, cex.axis = 1.25, las = 1)
axis(1,  labels = c("Jan","Mar","May","July","Sep","Nov","Jan"), 
     at = c(1,61,122,183,245,306,365), cex.axis= 1.25)
mtext(2, line = 2.3, text = expression(paste("Mean SST (",degree,"C)")), cex = 1.1)
mtext(1, line = 2.5, text = "Time", cex = 1.1)
text(15,25*.95,"A",cex = 1.5)
# +/- 1 sd
polygon(c(doy, rev(doy)),
        c(upper, rev(lower)),
        col = "grey85", border = NA)

#Fills plot
polygon(c(doy, rev(doy)),
        c(below_mean + (val_LT-below_mean), rev(below_mean)),
        col = "lightblue", border = NA)
polygon(c(doy, rev(doy)),
        c(above_mean - (above_mean-val_LT), rev(above_mean)),
        col = "orange", border = NA)
polygon(c(doy, rev(doy)),
        c(above_sd - (above_sd-(val_LT + val_LT_sd)), rev(above_sd)),
        col = "red", border = NA)
polygon(c(doy, rev(doy)),
        c(below_sd + (below_sd-(val_LT - val_LT_sd)), rev(below_sd)),
        col = "blue", border = NA)
points(doy,val_LT, type = "l", lwd = 1, "grey90")


##-------------------------------------GB-------------------------------------#

doy <- as.numeric(SOE.data[SOE.data$Var == "sst mean 2017 GB",]$Time)
val_2017 <- SOE.data[SOE.data$Var == "sst mean 2017 GB",]$Value
val_LT <- SOE.data[SOE.data$Var == "sst mean long term GB",]$Value
val_LT_sd <- SOE.data[SOE.data$Var == "sst sd long term GB",]$Value


# val_2017 <- approx(doy,val_2017, xout = seq(doy[1],doy[length(doy)],length.out = 365*1))$y
# val_LT <- approx(doy,val_LT, xout = seq(doy[1],doy[length(doy)],length.out = 365*1))$y
# val_LT_sd <- approx(doy,val_LT_sd, xout = seq(doy[1],doy[length(doy)],length.out = 365*1))$y
doy <- seq(doy[1],doy[length(doy)],length.out = 365*1)


above_mean <- NULL
for (i in 1:length(val_2017)){
  if (val_2017[i] >= val_LT[i]){
    above_mean[i] <- val_2017[i]
  } else if (val_2017[i] < val_LT [i]){
    above_mean[i] <- NA
  }
}

below_mean <- NULL
for (i in 1:length(val_2017)){
  if (val_2017[i] <= val_LT[i]){
    below_mean[i] <- val_2017[i]
  } else if (val_2017[i] > val_LT [i]){
    below_mean[i] <- NA
  }
}

above_sd <- NULL
for (i in 1:length(val_2017)){
  if (val_2017[i] >= val_LT_sd[i] + val_LT[i]){
    above_sd[i] <- val_2017[i]
  } else if (val_2017[i] < val_LT_sd [i] + val_LT[i]){
    above_sd[i] <- NA
  }
}

below_sd <- NULL
for (i in 1:length(val_2017)){
  if (val_2017[i] <= val_LT[i] - val_LT_sd[i]){
    below_sd[i] <- val_2017[i]
  } else if (val_2017[i] > val_LT[i] - val_LT_sd [i]){
    below_sd[i] <- NA
  }
}

#Lines for polygons
above_sd[is.na(above_sd)] <- val_LT_sd[which(is.na(above_sd))] + val_LT[which(is.na(above_sd))]
below_sd[is.na(above_sd)] <- val_LT[which(is.na(below_sd))] - val_LT_sd[which(is.na(below_sd))] 
above_mean[is.na(above_mean)] <- val_LT[which(is.na(above_mean))]
below_mean[is.na(below_mean)] <- val_LT[which(is.na(below_mean))]

upper <- val_LT_sd + val_LT
lower <- val_LT - val_LT_sd

#Null figure
plot(NULL, xlim = c(doy[1],doy[(length(doy))]), ylim = c(4,21), las = 1, 
     ylab = "", yaxt = "n", xaxt = "n", xlab = "")
axis(2, cex.axis = 1.25, las = 1)
axis(1,  labels = c("Jan","Mar","May","July","Sep","Nov","Jan"), 
     at = c(1,61,122,183,245,306,365), cex.axis= 1.25)
#mtext(2, line = 2.5, text = expression(paste("Mean SST (",degree,"C)")), cex = 1.1)
mtext(1, line = 2.5, text = "Time", cex = 1.1)
text(15,21*.95,"B",cex = 1.5)
# +/- 1 sd
polygon(c(doy, rev(doy)),
        c(upper, rev(lower)),
        col = "grey85", border = NA)

#Fills plot
polygon(c(doy, rev(doy)),
        c(below_mean + (val_LT-below_mean), rev(below_mean)),
        col = "lightblue", border = NA)
polygon(c(doy, rev(doy)),
        c(above_mean - (above_mean-val_LT), rev(above_mean)),
        col = "orange", border = NA)
polygon(c(doy, rev(doy)),
        c(above_sd - (above_sd-(val_LT + val_LT_sd)), rev(above_sd)),
        col = "red", border = NA)
polygon(c(doy, rev(doy)),
        c(below_sd + (below_sd-(val_LT - val_LT_sd)), rev(below_sd)),
        col = "blue", border = NA)
points(doy,val_LT, type = "l", lwd = 1, "grey90")

#----------------------------------------------------------------------------#

## SST GOM

doy <- as.numeric(SOE.data[SOE.data$Var == "sst mean 2017 GOM",]$Time)
val_2017 <- SOE.data[SOE.data$Var == "sst mean 2017 GOM",]$Value
val_LT <- SOE.data[SOE.data$Var == "sst mean long term GOM",]$Value
val_LT_sd <- SOE.data[SOE.data$Var == "sst sd long term GOM",]$Value


# val_2017 <- approx(doy,val_2017, xout = seq(doy[1],doy[length(doy)],length.out = 365*1))$y
# val_LT <- approx(doy,val_LT, xout = seq(doy[1],doy[length(doy)],length.out = 365*1))$y
# val_LT_sd <- approx(doy,val_LT_sd, xout = seq(doy[1],doy[length(doy)],length.out = 365*1))$y
doy <- seq(doy[1],doy[length(doy)],length.out = 365*1)


above_mean <- NULL
for (i in 1:length(val_2017)){
  if (val_2017[i] >= val_LT[i]){
    above_mean[i] <- val_2017[i]
  } else if (val_2017[i] < val_LT [i]){
    above_mean[i] <- NA
  }
}

below_mean <- NULL
for (i in 1:length(val_2017)){
  if (val_2017[i] <= val_LT[i]){
    below_mean[i] <- val_2017[i]
  } else if (val_2017[i] > val_LT [i]){
    below_mean[i] <- NA
  }
}

above_sd <- NULL
for (i in 1:length(val_2017)){
  if (val_2017[i] >= val_LT_sd[i] + val_LT[i]){
    above_sd[i] <- val_2017[i]
  } else if (val_2017[i] < val_LT_sd [i] + val_LT[i]){
    above_sd[i] <- NA
  }
}

below_sd <- NULL
for (i in 1:length(val_2017)){
  if (val_2017[i] <= val_LT[i] - val_LT_sd[i]){
    below_sd[i] <- val_2017[i]
  } else if (val_2017[i] > val_LT[i] - val_LT_sd [i]){
    below_sd[i] <- NA
  }
}

#Lines for polygons
above_sd[is.na(above_sd)] <- val_LT_sd[which(is.na(above_sd))] + val_LT[which(is.na(above_sd))]
below_sd[is.na(above_sd)] <- val_LT[which(is.na(below_sd))] - val_LT_sd[which(is.na(below_sd))] 
above_mean[is.na(above_mean)] <- val_LT[which(is.na(above_mean))]
below_mean[is.na(below_mean)] <- val_LT[which(is.na(below_mean))]

upper <- val_LT_sd + val_LT
lower <- val_LT - val_LT_sd

#Null figure
plot(NULL, xlim = c(doy[1],doy[(length(doy))]), ylim = c(4,21), las = 1, 
     ylab = "", yaxt = "n", xaxt = "n", xlab = "")
axis(2, cex.axis = 1.25, las = 1)
axis(1,  labels = c("Jan","Mar","May","July","Sep","Nov","Jan"), 
     at = c(1,61,122,183,245,306,365), cex.axis= 1.25)
#(2, line = 2.5, text = expression(paste("Mean SST (",degree,"C)")), cex = 1.1)
mtext(1, line = 2.5, text = "Time", cex = 1.1)
text(15,21*.95,"C",cex = 1.5)
# +/- 1 sd
polygon(c(doy, rev(doy)),
        c(upper, rev(lower)),
        col = "grey85", border = NA)

#Fills plot
polygon(c(doy, rev(doy)),
        c(below_mean + (val_LT-below_mean), rev(below_mean)),
        col = "lightblue", border = NA)
polygon(c(doy, rev(doy)),
        c(above_mean - (above_mean-val_LT), rev(above_mean)),
        col = "orange", border = NA)
polygon(c(doy, rev(doy)),
        c(above_sd - (above_sd-(val_LT + val_LT_sd)), rev(above_sd)),
        col = "red", border = NA)
polygon(c(doy, rev(doy)),
        c(below_sd + (below_sd-(val_LT - val_LT_sd)), rev(below_sd)),
        col = "blue", border = NA)
points(doy,val_LT, type = "l", lwd = 1, "grey90")
box()




