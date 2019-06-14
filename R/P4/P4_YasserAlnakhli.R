library(ggplot2)
library(ggmap)
library(maps)
library(mapdata)
library(gridExtra)
library(rworldmap)
library(tidyr)
library(ggplot2)
library(GGally)
library(scales)
library(memisc)
library(RColorBrewer)
library(dplyr)
library(plyr)

#=======================================#


# import the dataset
MissingMigrants <- read.csv("~/Udacity/P4/MissingMigrants2.csv")
#view the dataset
View(MissingMigrants)
# assign it to a simple variable
MM = MissingMigrants
#exploring
str(MissingMigrants)
str(MM)

#Dataset cleaning
#The dataset has missing values (NA) it will be treated directly on the variable..
#the following 4 variables have 
?is.na
MM$affected_missing[is.na(MM$affected_missing)] <- 0
MM$affected_dead[is.na(MM$affected_dead)] <- 0
MM$geo_lat[is.na(MM$geo_lat)] <- 0
MM$geo_lon[is.na(MM$geo_lon)] <- 0


#change the current date format to be suitable to R
MM$Year <- as.Date(MM$date_reported,format="%d/%m/%Y")

# Let's assign color values to some regions, of interest so we might use them to plot later
MM$color[MM$region_incident == "Mediterranean"] <- "red"
MM$color[MM$region_incident == "Middle East"] <- "yellow"
MM$color[MM$region_origin== "MENA"] <- "blu"
#MM$Year <- as.Date(MM$date_reported,format="%d/%m/%Y")

plot(MM$affected_dead~MM$affected_missing, data=MM)
plot(MM$Tdeath~MM$Year, data=MM)


# assume the missing migrants are dead and then sum the dead and the missings 
#this step to explore the total death by years/moths as following
MM$D <- as.numeric(MM$affected_dead)
MM$M <- as.numeric(MM$affected_missing)
MM$Tdeath <- MM$M + MM$D 
MissingMigDate <- ggplot( data = MM, aes( Year, MM$Tdeath )) + 
  geom_line()+ ylab("Number of deaths") +
  ggtitle("Number of total deaths over years")
  
MissingMigDate 


#check some statistics
sum(MM$affected_missing)
sum(MM$affected_dead)
sum(MM$Tdeath)

summary(which(MM$Tdeath>0))
summary.factor(na.exclude(MM$affected_nationality))
table(na.exclude(MM$affected_nationality))


#Exploring more variables:
### Review 1
plot(MM$affected_dead~MM$affected_missing, data=MM)
plot(MM$Tdeath~MM$Year, data=MM)


### Review 2
# For this I recommend adding a third categorical variable to the scatter plot, 
#or using 2 categorical variables and adding a third continuous variable 
#in a boxplot (affected missing vs cause type vs region, for example).

bb <- ggplot(MM, aes(MM$cause_type,MM$Tdeath))
bb + geom_boxplot()

#keep top levels only then do box plot
levels(MM$cause_type) 
table(MM$cause_type)
summary(CausT)

group_by(MM$cause_type) 
  top_n(n = 5)


ggplot(dat,aes(x = x,y = y)) + 
  facet_grid(grp1~grp2,drop = FALSE) + 
  geom_point()




#subseting for the most frequency in a some variables using dplyr
factor(MM$cause_type)
factor(MM$affected_nationality)
count(MM,"cause_type")
count(MM$affected_nationality)

MM %>% 
  group_by(MM$cause_type) %>% 
  mutate(N=n()) %>%
  ungroup() %>% 
  filter(N==max(N))


### Review 3
# Affected nationality:
summary(na.exclude(MM$affected_nationality))

Nationality <- as.data.frame.character(MM$affected_nationality)
summary(Nationality)

#from https://stackoverflow.com/questions/19731071/r-find-elements-in-a-character-array-that-contains-a-string

StatNa<- ggplot(MM,aes(x= factor(MM$affected_nationality,
      levels=names(sort(table(MM$affected_nationality),
                        increasing=TRUE)) ))
      ) +
  geom_bar() 

StatNa + xlim('Mexico', 'Syria', 'Honduras', 'Afghanistan', 'Guatemala',
              'El Salvador') + 
  ggtitle("Top 6 affected nationalities")+
  xlab("Nationalities")





###################################################
#Couse Type:
CausT <- as.data.frame.character(MM$cause_type)
summary(na.omit(CausT))

CT<- ggplot(MM,aes(x= factor(MM$cause_type,
          levels=names(sort(table(MM$cause_type),increasing=TRUE)) ))
            ) +
  geom_bar() 

CT + xlim('Drowning', 'Unknown (skeletal remains)','Presumed drowning',
          'Sickness_and_lack_of_access_to_medicines', 'Vehicle_Accident' ) + 
  ggtitle("Top 5 death causes among migrants")+
  xlab("Cause Types")

######################################################### NEED to be completed
#Subsetting Siryan Nati
summary(MM$affected_nationality == "Syria")
#not all syrian are includied in on category... 
#I will check another way to find out more

summary(grep('Syria', MM$affected_nationality, value=TRUE))

summary(grep("Syr", Nationality, value = T))

Syrians <- subset(MM , MM$affected_nationality== "Syria")

ggplot(data = Syrians, aes(Syrians$Year,Syrians$Tdeath),na.rm = T)+  
  geom_point(mapping = aes(x = Syrians$Year, y = Syrians$Tdeath))


##########################################################
# focus of the year with the higher death rate 2015
#http://stackoverflow.com/questions/34174799/r-get-subset-from-data-frame-filtering-by-year-date-value
years2015 <- subset(MM,format(as.Date(MM$Year),"%Y")==2015)
ggplot( data = years2015, aes( Year, years2015$Tdeath)) + 
  geom_line()+ ylab("Number of total deaths") +
  ggtitle("Number of deaths in 2015")+
  xlab("Months of 2015")


#subsetting by year2017
year2017 <- subset(MM, MM$Year > "2017-01-01")

#subsetting only Mediterranean
Mediterranean <- subset(MM, MM$region_incident == "Mediterranean")


#cause of death:
# I would like to invistigate in what is the common couse of death among all migrants 
# subset

ggplot(data = MM, aes(MM$cause_type,MM$Tdeath),na.rm = T)+  
  geom_point(mapping = aes(x = MM$cause_type, y = MM$Tdeath,color = MM$cause_type =="Drowning"))

#subset by regon of oregion
MENA <- subset(MM, MM$region_origin == "MENA")

#different informations (Deaths Vs Missing)
ggplot( data = year2017, aes( Year, year2017$Tdeath)) + 
  geom_line()+ ylab("Number of total deaths") +
  ggtitle("Number of deaths in 2017")+
  xlab("Months of 2017")

#total deaths of migrants over year
ggplot( data = MM, aes( Year, MM$Tdeath )) + 
  geom_line()+ 
  ylab("Number oftotal deaths")+
  ggtitle("Total dead migrants over years")



#different informations (Deaths Vs Missing)
# Combine into one
P1 = ggplot( data = MM, aes( Year, MM$affected_dead )) + geom_line()
P2 = P1 +geom_line( data = MM, aes( Year, MM$affected_missing), colour="red")
P2+ ggtitle(label = "Number of missing and dead migrants over years")+ 
  ylab("missing and dead number")+
  theme(plot.title = element_text(color="blue", face="bold", size=32, hjust=0.5)) +
  theme(axis.title = element_text(color="gray", face="bold", size=17)) 



summary.factor(MM$region_origin)
ggplot(data = MM,aes(x = MM$region_origin))+ geom_bar()+
  theme(axis.text.x =element_text(angle = 90, hjust = 1,size = 12,color = "black"))+
  ggtitle("Migrants Region of Origin")+ 
  xlab("Region of Origin")

##########################################################################
#subset by region of oregion  MENA
MENA <- subset(MM, MM$region_origin == "MENA")

MENAplot <- ggplot(MENA, aes(y=MENA$Tdeath, x = MENA$Year)) + 
  geom_line()+
  ggtitle("Incident in the MENA Region")+ 
  xlab("Years")+
  ylab("Total number of deaths")
MENAplot 


#subset by region of oregion  Mediterranean
Mediterranean <- subset(MM, MM$region_incident == "Mediterranean")

Meditplot <- ggplot(Mediterranean, aes(y=Mediterranean$Tdeath, x = Mediterranean$Year)) + 
  geom_line(colour="red")+
  ggtitle("Incident in the Mediterranean Region")+ 
  xlab("Years")+
  ylab("Total number of deaths")
Meditplot


# Comparission
MENAplot <- ggplot(MENA, aes(y=MENA$Tdeath, x = MENA$Year))+ 
  geom_line(size=2, colour = "blue")

Meditplot <- MENAplot + geom_line(data= Mediterranean, 
                aes(y=Mediterranean$Tdeath, x = Mediterranean$Year), 
                colour="red") + 
  ggtitle("Incident in the Mediterranean Vs MENA Regions")+ 
  xlab("Years")+
  ylab("Total number of deaths")

Meditplot
?geom_line


#####################################################################3
summary.factor(MM$region_incident)
#Region Inc Migr RIM
MM$RIM  <- factor(MM$region_incident, 
                  levels=c("North Africa", "Mediterranean", 
                           "U.S./Mexico Border", "NA" ,"Central America incl. Mexico",
                           "Horn of Africa", "Europe"))
ggplot(MM, aes(x=RIM, group = MM$RIM)) + 
  geom_bar(color="red", fill="yellow")+
  theme(axis.text.x =element_text(angle = 90, hjust = 0.5,size = 12,color = "black"))+
  ggtitle("Selected Incident Regions")+ 
  xlab("Region of incident")+
  theme(plot.title = element_text(color="blue", face="bold", size=20, hjust=0.5)) +
  theme(axis.text = element_text(color = "gray", face="bold", size=17)) +
  geom_hline(yintercept = 500, size = 1, linetype = 7)+
  coord_flip()

###########################################################

# Plotting coordinates into a map 

Nationality <- as.data.frame.character(MM$affected_nationality)
country <- as.data.frame.character(MM$region_incident)
lat <- as.data.frame.numeric(MM$geo_lat)
lon <- as.data.frame.numeric(MM$geo_lon)
Deaths <- as.data.frame.integer(MM$affected_dead)
Missings <- as.data.frame.integer(MM$affected_missing)
TotalDe <- as.data.frame.integer(MM$Tdeath)
DDate <- as.data.frame.Date(MM$Year)

###########################################################

#from http://sarahleejane.github.io/learning/r/2014/09/20/plotting-beautiful-clear-maps-with-r.html
world_map <- map_data("world")

#Add map to base plot
ma <- ggplot() + coord_fixed() +
  xlab("") + ylab("")

#Add map to base plot
base_world_messy <- ma + geom_polygon(data=world_map, aes(x=long, y=lat, group=group), 
                                     colour="light green", fill="light green")

base_world_messy

cleanup <- 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), 
        panel.background = element_rect(fill = 'white',
                                        colour = 'white'), 
        axis.line = element_line(colour = "white"), legend.position="none",
        axis.ticks=element_blank(), axis.text.x=element_blank(),
        axis.text.y=element_blank())

base_world <- base_world_messy + cleanup

base_world


#####################################
# plotting on maps         ##
#####################################
#region incident 
map_data <- 
  base_world_messy +
  geom_count(data= country, 
             aes(x=lon, y=lat), colour="Deep Pink", 
             fill="Pink",pch=21, size=3, alpha=I(0.5))+
  geom_text()

map_data


#plot both missing and deaths by size

# 1 Total Death
map_data_Deaths <- 
  base_world_messy +
  geom_point(data=TotalDe, 
             aes(x=lon, y=lat), colour="blue", 
             fill="yellow", alpha=0.5)

map_data_Deaths


# 2 missing
map_data_both <-
  map_data_Deaths +
  
    geom_count(data=Missings, 
               aes(x=lon, y=lat), colour="pink", 
               fill="red",pch=20, alpha=I(0.4)) 
map_data_both



#zoom in to the middle east and medeterrean 
ME <- map_data_both + coord_cartesian(xlim = c(-15,100), ylim = c(-40,55))
ME + coord_cartesian(xlim = c(10,40), ylim = c(20,45)) +
  scale_alpha(range = c(01,1))

####################################
lonMENA <- as.data.frame.numeric(MENA$geo_lon)
latMENA <- as.data.frame.numeric(MENA$geo_lat)
TD_MENA <- as.data.frame.integer(MENA$Tdeath)
MENA_Nati <- as.data.frame.character(MENA$affected_nationality)

#####  1

MENAdeaths <- 
  base_world_messy +
  geom_density2d(data = TD_MENA, aes(x = lonMENA, y=latMENA),
                 colour="black", bins=10,inherit.aes=FALSE, alpha=0.7)

MENAdeaths
MENAdeaths + coord_cartesian(xlim = c(-10,50), ylim = c(25,53))




#plot3
MMEEE <- 
  base_world_messy + 
  stat_density2d(data = TD_MENA, aes(x = lonMENA, y = latMENA,
alpha=..level.., fill=..level..,contour = T), 
                 size=4, 
                 bins=10, 
                 geom=c("polygon","contour"),
                 inherit.aes=FALSE) + 
  geom_density2d(data = TD_MENA, aes(x = lonMENA, y=latMENA),
                 colour="black", bins=2,inherit.aes=FALSE, alpha=I(0.5),
                 size=2)+
  scale_fill_gradient(low = "blue", high = "red") +
  geom_point(data = MENA_Nati, aes(x = lonMENA, y=latMENA),inherit.aes=FALSE)
 
MMEEE + coord_cartesian(xlim = c(-10,50), ylim = c(25,53))+
  ggtitle("Total Migrants Deaths in MENA Region")+ 
  xlab("Longitude")+
  ylab("Latitude")+
  theme(axis.title = element_text(color="black", face="bold", size=17)) +
  theme(plot.title = element_text( color="blue", face="bold", size=32, hjust=0.5))

summary(MENA$affected_nationality == "Syria")



MMEE22 <- 
  base_world + 
  stat_density2d(data = TotalDe, aes(x = lon, y = lat,
                alpha=..level.., fill=..level..,contour = T), 
                 size=4, bins=10, geom=c("polygon","contour"),
                 inherit.aes=FALSE) + 
  geom_density2d(data = TotalDe, aes(x = lon, y=lat),
                 colour="black", bins=2,inherit.aes=FALSE, alpha=I(0.5),
                 size=2)+
  scale_fill_gradient(low = "blue", high = "red") +
  geom_point(data = TotalDe, aes(x = lon, y=lat),inherit.aes=FALSE)

MMEE22 + coord_cartesian(xlim = c(-10,70), ylim = c(0,53))+
  ggtitle("Total Migrants Deaths")+ 
  xlab("Longitude")+
  ylab("Latitude")+
  theme(axis.title = element_text(color="black", face="bold", size=17)) +
  theme(plot.title = element_text( color="blue", face="bold", size=32, hjust=0.5))


