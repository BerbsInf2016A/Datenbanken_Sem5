install.packages("ggplot2")
install.packages("dplyr")
install.packages("tidyr")
install.packages("maps")
install.packages("devtools")
library(devtools)
install_github("dkahle/ggmap")
library(ggmap)
library(ggplot2)
library(dplyr)
library(tidyr)
library(maps)
library(ggmap)
setwd("C:/Users/Andre/Downloads/Chicago-mvt-data-master")

register_google(key = "")

## Get Chicago map
chicago <- get_map(location = 'chicago', zoom = 11)
png(filename = "Chicago.png", width = 800, height = 600, units = "px")
ggmap(chicago)
dev.off()


tempData <- read.csv('dropoff.csv', stringsAsFactors = FALSE)

tempData$Longitude <- round(as.numeric(tempData$longitude), 2)
tempData$Latitude <- round(as.numeric(tempData$latitude), 2)

## Get locations
locations <- as.data.frame(table(tempData$Longitude, tempData$Latitude))
names(locations) <- c('long', 'lat', 'Frequency')
locations$long <- as.numeric(as.character(locations$long))
locations$lat <- as.numeric(as.character(locations$lat))
locations <- subset(locations, Frequency > 0)

## Plotting the location heatmap

png(filename = "Chicagomap_dropoff_tile.png", width = 800, height = 600, units = "px")
ggmap(chicago) + geom_tile(data = locations, aes(x = long, y = lat, alpha = Frequency),
                           fill = "red") + theme(axis.title.y = element_blank(), axis.title.x = element_blank())
dev.off()

png(filename = "Chicagomap_dropoff_point.png", width = 800, height = 600, units = "px")
ggmap(chicago) + geom_point(data = locations, aes(x = long, y = lat, alpha = Frequency),
                           fill = "red") + theme(axis.title.y = element_blank(), axis.title.x = element_blank())
dev.off()

