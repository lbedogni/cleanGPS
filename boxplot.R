library(ggplot2)

colnames = c('DIST','TIME1','LON1','LAT1','TIME2','LON2','LAT2')
df <- data.frame(DIST = rep(NA,550000),TIME1 = rep(NA,550000), LON1 = rep(NA,550000),LAT1 = rep(NA,550000), TIME2 = rep(NA,550000),LON2 = rep(NA,550000), LAT2 = rep(NA,550000), KIND = rep(NA,550000), SAMPLING = rep(NA,550000))
#for (sampling in c(10,20)) {
for (sampling in c(10,20,30,60,100,180,240,300)) {
	basepath = paste("errors_",sampling,"/",sep="")

	for (file in list.files(path=basepath, pattern='our_*')) {
		path = paste(basepath,file,sep='')
		print(path)
		if (length(readLines(path) > 0)) {
			dftmp <- read.table(path, col.names=colnames)
			dftmp$KIND = "OUR"
			dftmp$SAMPLING = sampling
			if (nrow(df) == 0) {
				df = dftmp
			} else {
				df = rbind(df, dftmp)
			}
		}
	}

	for (file in list.files(path=basepath, pattern='their_*')) {
		path = paste(basepath,file,sep='')
		print(path)
		if (length(readLines(path) > 0)) {
			dftmp <- read.table(path, col.names=colnames)
			dftmp$KIND = "THEIR"
			dftmp$SAMPLING = sampling
			if (nrow(df) == 0) {
				df = dftmp
			} else {
				df = rbind(df, dftmp)
			}
		}
	}
}

summary(df)

g <- ggplot(data=df, aes(x=interaction(KIND,SAMPLING), y=DIST))
g <- g + geom_boxplot(outlier.shape=NA, aes(fill=factor(KIND))) + theme_classic()
#g <- ggplot(data=df, aes(x=KIND, y=DIST, colour=factor(KIND)))
#g <- g + geom_boxplot() + theme_classic()
#g <- g + scale_x_continuous(expand=c(0,0))
g <- g + scale_y_continuous(expand=c(0,0), limits=c(0,150))

ggsave('errors_boxplot.eps',g,width=7,height=5)
