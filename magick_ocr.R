library(magick)
library(magrittr)
text <- image_read("6.jpeg") %>%
  image_resize("2000") %>%
  image_convert(colorspace = 'gray') %>%
  image_trim() %>%
  image_ocr()

new<-text
cat(text)
write.table(new,file = "new1.txt")

#data<-readLines("new.txt")
#data[1:20]
data<-read.table("new.txt")
View(data)
##text[g]

