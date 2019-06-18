# Load the necessary packages
library(twitteR)
library(RCurl)
library(wordcloud)
library(RColorBrewer)
library(plyr)
library(ggplot2)

# OAuth settings:
library(httr)

# Register an application (API) at https://apps.twitter.com/
Consumer_Key<-"HiMQogoLdJPSMhIjf6vlImRR3"
Consumer_Secret<-"MLBFOwq4krIAEl4Rlm34O4CuDlpWguGjPmS3oEmOODo9F3CNxr"

Access_Token<-"2432328559-uPi1dkGokIUg074ri2WlH7eSbP3T6eBsNWTGd8q"
Access_Token_Secret<-"Nv2QaltJAnIjy8qAfJnMa7i2KZZnf2Zi56sfjSq3K78t2"
setup_twitter_oauth(Consumer_Key,Consumer_Secret,Access_Token,Access_Token_Secret)

#Extracting data on tweets-
tweets.list = searchTwitter("solarcoin", n=500,lang="en",since = '2018-01-01')
length(tweets.list)
tweets.df = twListToDF(tweets.list)
write.csv(x = tweets.df,file = "tweets.csv")
#Trends
trend <- availableTrendLocations()
head(trend)
trend
View(trend)

world <- getTrends(1)
View(world)
boston <- getTrends(2367105)
luckhnow <- getTrends(2295377)
head(boston)
tail(boston)
head(luckhnow)
tail(luckhnow)
