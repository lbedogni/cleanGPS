library(ggplot2)

columns <- c('LI','THEIR','OUR')
df <- read.table('total_errors.csv',col.names=columns)
#df2 <- df
#print("AA")
#df2$ERROR = df$THEIR
#print("AA")
#df2$KIND = "THEIR"

#df3 <- df
#df3$ERROR = df$OUR
#df3$KIND = "OUR"

#df <- df[c("ERROR")]
#df$KIND = "LI"

#df <- rbind(df,df2)
#df <- rbind(df,df3)

df$SAMPLING = 10
summary(df)

g <- ggplot(data = df, aes(x=SAMPLING, y=THEIR)) + geom_line() + geom_line(aes(x=SAMPLING,y=LI)) + geom_line(aes(x=SAMPLING,y=OUR))

ggsave('distance_erros.eps',g,width=7,height=5)
