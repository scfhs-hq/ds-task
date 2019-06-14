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
library(reshape2)
library(Hmisc)
library(corrgram)
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
table(MM$cause_type)
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


# assume the missing migrants are dead and then sum the dead and the missings 
#this step to explore the total death by years/moths as following
MM$D <- as.numeric(MM$affected_dead)
MM$M <- as.numeric(MM$affected_missing)
MM$Tdeath <- MM$M + MM$D 
MissingMigDate <- ggplot( data = MM, aes( Year, MM$Tdeath )) + 
  geom_line()+ ylab("Number of deaths") +
  ggtitle("Number of total deaths over years")
  
MissingMigDate 



# Reviwer 3 Comment:
# Affected dead. 
grid.arrange( ggplot(aes(x=affected_dead), 
                     data = MissingMigrants) +
                scale_x_log10()+
                geom_histogram( bins = 30) ,
              ggplot(aes(x=1, y=affected_dead), 
                     data = MissingMigrants) +
                scale_y_log10()+
                geom_boxplot( )  , nrow =1)


# Affected Missing
grid.arrange( ggplot(aes(x=affected_missing), 
                     data = MissingMigrants) +
                scale_x_log10()+
                geom_histogram( bins = 30) ,
              ggplot(aes(x=1, y=affected_missing), 
                     data = MissingMigrants) +
                scale_y_log10()+
                geom_boxplot( )  , nrow =1)



#check some statistics
sum(MM$affected_missing)
sum(MM$affected_dead)
sum(MM$Tdeath)

summary.factor(na.exclude(MM$affected_nationality))
table(na.exclude(MM$affected_nationality))

### Based on the 1st Review 
#UniVariables Plots
#####
# 1 #
#####
# Affected nationality:
summary(na.exclude(MM$affected_nationality))

Nationality <- as.data.frame.character(MM$affected_nationality)
summary(Nationality)
StatNa<- ggplot(MM,aes(x= MM$affected_nationality)) +
  geom_bar() 

StatNa + 
  xlim('Mexico', 'Syria', 'Honduras', 'Afghanistan', 'Guatemala', 'El Salvador') +
  ggtitle("Top 6 affected nationalities")+
  xlab("Nationalities")+
  coord_flip()

#####
# 2#
#####
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

#####
# 3 #
#####
# Variable region_incident
summary.factor(MM$region_incident)
#CHanged based on the reviewer requiest 

ggplot(data = MM,aes(x = 
                       reorder(region_incident, region_incident, function(x) length(x))))+ 
  geom_bar()+
  theme(axis.text.x =element_text(angle = 90, hjust = 0.5,size = 12,color = "black"))+
  ggtitle("Region of incident")+ 
  xlab("Region of incident")+
  coord_flip()



#####
# 4 #
#####
#going deeper in univeriant plots analysis:
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




#Exploring more variables:
#BiVariables Plots
#####
# 1 #
#####
plot(MM$affected_missing)
plot(MM$affected_dead)
# exploring the affeted dead vs missing
plot(MM$affected_dead~MM$affected_missing, data=MM)
# adjestments in doing some transformation
# using ggplot this time 
#http://www.sthda.com/english/wiki/ggplot2-axis-scales-and-transformations
sp <- ggplot(MM, aes(x = MM$affected_dead, y = MM$affected_missing)) + geom_point()
sp
# Log transformation
# possible values for trans : 'log2', 'log10','sqrt'
sp + scale_x_continuous(trans='log2') +
  scale_y_continuous(trans='log2')
# Sqrt transformation
sp + scale_y_sqrt()+
  coord_flip()
#Correlation between Mising and dead migrants
rcorr(MM$affected_missing,MM$affected_dead,type = "pearson")
#ggpairs(data=MM, # data.frame with variables
 #       columns=c(5,6), # columns to plot, default to all.
  #      title="----------------")


#BiVariables Plots
#####
# 2 #
#####
#Mena area
MMEEE + coord_cartesian(xlim = c(-10,50), ylim = c(25,53))+
  ggtitle("Total Migrants Deaths in MENA Region")+ 
  xlab("Longitude")+
  ylab("Latitude")+
  theme(axis.title = element_text(color="black", face="bold", size=17)) +
  theme(plot.title = element_text( color="blue", face="bold", size=20, hjust=0.5))


#BiVariables Plots
#####
# 3 #
#####

# exploring  the Tatal (death and Missing) Vs Years
plot(MM$Tdeath~MM$Year, data=MM)
# adjestments in doing some transformation
# using ggplot this time l
#http://www.sthda.com/english/wiki/ggplot2-axis-scales-and-transformations

sct <- ggplot(MM, aes(x = MM$Tdeath, y = MM$Year)) + geom_point()
sct

# Log transformation
# possible values for trans : 'log2', 'log10','sqrt'
sct + scale_x_continuous(trans='log2')+
  coord_flip() 
# Sqrt transformation
sct + scale_x_sqrt()+
  coord_flip() 

sct +  geom_point(aes(colour = factor(MM$cause_type == "Drowning")))+
  coord_flip() 


#BiVariables Plots
#####
# 4 #
#####
### Review 2
# using 2 categorical variables and adding a third continuous variable 
#in a boxplot (affected missing vs cause type vs region, for example).
bb <- ggplot(MM, aes(MM$cause_type,MM$Tdeath))
bb + geom_boxplot(inherit.aes = TRUE)
# Becaouse there are so many couse types, the figure is not clear.
# I will narrow down to the top 20 causes.
#subseting for the most frequency in a some variables using dplyr
table(MM$cause_type)
#Convert the column to a table to get the frequency of each values 
freq <- table(MM$cause_type)
freq
top_cause <- sort(freq,decreasing=TRUE)[1:20]
top_cause
#Convert to data frame to extract the values 
top_cause_df <- as.data.frame(top_cause)
top_cause_df
#It shows that the variables become as a raws name. Insead, I need them as a value variable 
#column, so I will use this library to use it as a column
library(data.table)
setDT(top_cause_df, keep.rownames = TRUE)[]
#Convert the column to list as we will subset on the list 
cause_list <- lapply(top_cause_df$rn , as.character)
#Subset the original based on above list
MM_top_20 <- subset(MM, MM$cause_type %in% cause_list)
bo = ggplot(data= MM_top_20, aes(x= cause_type,y= MM_top_20$affected_dead))+
  geom_boxplot()+ theme(axis.text.x = element_text(angle = 90, hjust = 1, size = 10))
bo 

#Review 3... suggestion to change the above box blot to the following

ggplot(aes(factor(cause_type), 
           affected_dead), 
       data = MissingMigrants) +
  geom_jitter( alpha = .3)  + 
  geom_boxplot( alpha = .5,color = 'blue')+
  scale_y_log10()+ 
  stat_summary(fun.y = "mean", 
               geom = "point", 
               color = "red", 
               shape = 8, 
               size = 4)  + xlim('Drowning', 'Unknown (skeletal remains)','Presumed drowning',
                           'Sickness_and_lack_of_access_to_medicines', 'Vehicle_Accident' )+
  ggtitle("Affected dead number vs cause type")+ 
  xlab("Cause Type")+
  ylab("Affected deaths")

### Review 2b
freq <- table(MM_clean$cause_type)
top5_cause <- sort(freq,decreasing=TRUE)[1:5]

#Convert to data frame to extract the values 
top5_cause_df <- as.data.frame(top5_cause)
top5_cause_df
setDT(top5_cause_df, keep.rownames = TRUE)[]
#Convert the column to list as we will subset on the list 
cause5_list <- lapply(top5_cause_df$rn , as.character)
#Subset the original based on above list
MM_top_5 <- subset(MM, MM$cause_type %in% cause5_list)
ggplot(MM_top_5,aes(x = MM_top_5$Year, fill = MM_top_5$cause_type)) + 
  # as the 2nd reviewer requiested
  scale_fill_discrete(guide = guide_legend(title = "Cause Types"))+
  geom_histogram()


########################################################
#Subsetting Siryan Nati
summary(MM$affected_nationality == "Syria")
#not all syrian are includied in on category... 
#I will check another way to find out more

summary(grep('Syria', MM$affected_nationality, value=TRUE))

summary(grep("Syr", Nationality, value = T))

Syrians <- subset(MM , MM$affected_nationality== "Syria")

ggplot(data = Syrians, aes(Syrians$Year,Syrians$Tdeath),na.rm = T)+  
  geom_point(mapping = aes(x = Syrians$Year, y = Syrians$Tdeath))
#$$$$$$$$$$$$$$$$$$$$$$$#
ggpairs(data=Syrians, # data.frame with variables
        columns=5:6, # columns to plot, default to all.
        title="Missings amd Deaths Syrians During Years")

## 2nd Reviewer suggestion to also make a scatter plot and see the rlationship
ggplot(Syrians, aes(x=Syrians$affected_missing, y=Syrians$affected_dead)) +
  geom_point(size=5)      







##########################################################


#different informations (Deaths Vs Missing)
# Combine into one
P1 = ggplot( data = MM, aes( Year, MM$affected_dead,colour="darkblue")) + 
  geom_line()
P2 = P1 +geom_line( data = MM, aes( Year, MM$affected_missing, colour="red"))
P2+scale_color_discrete(name = " Color Code", labels = c("Missings", "Dead"))+
  ggtitle(label = "Number of missing and dead migrants over years")+ 
  ylab("missing and dead number")+
  theme(plot.title = element_text(color="blue", face="bold", size=20, hjust=0.5)) +
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
MENAplot <- ggplot(MENA, aes(y=MENA$Tdeath, x = MENA$Year,colour="blue"))+ geom_line(size=2)

Meditplot <- MENAplot + geom_line(data= Mediterranean, 
                aes(y=Mediterranean$Tdeath, x = Mediterranean$Year,colour="red")) + 
  ggtitle("Incident in the Mediterranean Vs MENA Regions")+ 
  scale_color_discrete(name = "Color Code", labels = c("MENA","Mediterranean"))+
  xlab("Years")+
  ylab("Total number of deaths")

Meditplot





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
                                     colour="blue", fill="light blue")

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
#check the source reliability for reporting the missing and the deaths 
ggpairs(data=MM, # data.frame with variables
        columns=c(5,6,10 ), # columns to plot, default to all.
        title="Missings and Deaths Migrents Relability")



#region incident 
map_data <- 
  base_world_messy +
  geom_count(data= country, 
             aes(x=lon, y=lat), colour="Deep Pink", 
             fill="Pink",pch=21, size=2, alpha=I(0.5))

map_data+ ggtitle("Total Migrants Deaths in World")+ 
  xlab("Longitude")+
  ylab("Latitude")+
  theme(axis.title = element_text(color="black", face="bold", size=17)) +
  theme(plot.title = element_text( color="blue", face="bold", size=20, hjust=0.5))



#plot both missing and deaths by size

# 1 Total Death
map_data_Deaths <- 
  base_world_messy +
  geom_count(data=TotalDe, aes(x=lon, y=lat), colour="red", alpha=0.5)

map_data_Deaths

####


# 2 missing
map_data_both <-
  map_data_Deaths +
  
    geom_count(data=Missings, 
               aes(x=lon, y=lat), colour="yellow", 
               fill="red",pch=20, alpha=I(0.5)) 
map_data_both+ggtitle("Missings Vs Deaths Migrants in The World")+ 
  xlab("Longitude")+
  ylab("Latitude")+
  theme(axis.title = element_text(color="black", face="bold", size=17)) +
  theme(plot.title = element_text( color="blue", face="bold", size=20, hjust=0.5))




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



#Final Plot 1

StatNa<- ggplot(MM,aes(x= factor(MM$affected_nationality,
                                 levels=names(sort(table(MM$affected_nationality),
                                                   increasing=TRUE)) ))) +
  geom_bar(color="red", fill="yellow") 

StatNa + xlim('Mexico', 'Syria', 'Honduras', 'Afghanistan', 'Guatemala',
              'El Salvador') + 
  ggtitle("Top 6 affected nationalities")+
  xlab("Nationalities")+
  theme(text = element_text(size=20),
        axis.text.x = element_text(angle=90, hjust=1))  +
  geom_hline(yintercept = 80, size = 1, linetype = 7)+
  coord_flip()



#final plot 2
### Reviewer suggestion
### Reviewer suggestion
MM_clean <- subset(MM, !(cause_type %in% c("")))
freq <- table(MM_clean$cause_type)
top5_cause <- sort(freq,decreasing=TRUE)[1:5]
MM_clean <- subset(MM, !(cause_type %in% c("")))
freq <- table(MM_clean$cause_type)
top5_cause <- sort(freq,decreasing=TRUE)[1:5]
#Convert to data frame to extract the values 
top5_cause_df <- as.data.frame(top5_cause)
setDT(top5_cause_df, keep.rownames = TRUE)[]
#Convert the column to list as we will subset on the list 
cause5_list <- lapply(top5_cause_df$rn , as.character)
#Subset the original based on above list
MM_top_5 <- subset(MM, MM$cause_type %in% cause5_list)
ggplot(MM_top_5,aes(x = MM_top_5$Year, fill = MM_top_5$cause_type)) + 
  geom_histogram()+
  #scale_fill_gradient(guide = guide_legend(title = "Cause Types"))+
  ggtitle("Top 5 Causes of Migrants Death")+ 
  xlab("Years")+
  ylab("Count")+
  theme(axis.title = element_text(color="black", face="bold", size=17)) +
  theme(plot.title = element_text( color="blue", face="bold", size=20, hjust=0.5))+
  scale_fill_discrete(guide = guide_legend(title = "Cause Types"))


# final plot3
MMEEE <- 
  base_world_messy + 
  stat_density2d(data = TD_MENA, aes(x = lonMENA, y = latMENA, fill=..level..), 
                 size=4, 
                 bins=10, 
                 geom=c("polygon"),
                 inherit.aes=FALSE) + 
  geom_density2d(data = TD_MENA, aes(x = lonMENA, y=latMENA),
                 colour="red", bins=2,inherit.aes=FALSE, alpha=I(0.5),
                 size=2)+
  scale_fill_gradientn(colours = terrain.colors(10),
                       guide = guide_legend(title = "Number")) +
  geom_point(data = MENA_Nati, aes(x = lonMENA, y=latMENA),inherit.aes=FALSE)

MMEEE + coord_cartesian(xlim = c(-10,50), ylim = c(25,53))+
  ggtitle("Total Migrants Deaths in MENA Region")+ 
  xlab("Longitude")+
  ylab("Latitude")+
  theme(axis.title = element_text(color="black", face="bold", size=17)) +
  theme(plot.title = element_text( color="blue", face="bold", size=20, hjust=0.5))

summary(MENA$affected_nationality == "Syria")

MMEE22 <- 
  base_world + 
  stat_density2d(data = TotalDe,aes(x = lon, y = lat,
                                    alpha=..level..,fill=..level..), 
                 size=2, bins=10, geom=c("polygon","contour"),
                 inherit.aes=FALSE) + 
  geom_density2d(data = TotalDe, aes(x = lon, y=lat),
                 colour="black", bins=2,inherit.aes=FALSE, alpha=I(0.5),
                 size=2)+
  scale_fill_gradient(low = "blue", high = "red") +
  geom_point(data = TotalDe, aes(x = lon, y=lat),inherit.aes=FALSE)
MMEE22+ ggtitle("Total Migrants Deaths")+ 
  xlab("Longitude")+
  ylab("Latitude")+
  theme(axis.title = element_text(color="black", face="bold", size=17)) +
  theme(plot.title = element_text( color="blue", face="bold", size=22, hjust=0.5))


#Zooming
MMEE22 + coord_cartesian(xlim = c(-10,70), ylim = c(0,53))+
  ggtitle("Total Migrants Deaths in MENA Area")+ 
  xlab("Longitude")+
  ylab("Latitude")+
  theme(axis.title = element_text(color="black", face="bold", size=17)) +
  theme(plot.title = element_text( color="blue", face="bold", size=22, hjust=0.5))


