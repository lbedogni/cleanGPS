library(ggplot2)

colnames = c('DIST','TIME1','LON1','LAT1','TIME2','LON2','LAT2')

df <- data.frame()


df <- data.frame(DIST = rep(NA,550000),TIME1 = rep(NA,550000), LON1 = rep(NA,550000),LAT1 = rep(NA,550000), TIME2 = rep(NA,550000),LON2 = rep(NA,550000), LAT2 = rep(NA,550000), KIND = rep(NA,550000))



for (file in list.files(path='errors',pattern='our_*')) {
	print(file)
	path = paste('errors/',file,sep='')
	if (length(readLines(path) > 0)) {
		dftmp <- read.table(path, col.names=colnames)
		dftmp$KIND = "OUR"
		if (nrow(df) == 0) {
			df = dftmp
		} else {
			df = rbind(df, dftmp)
		}
	}
}

for (file in list.files(path='errors',pattern='their_*')) {
	print(file)
	path = paste('errors/',file,sep='')
	if (length(readLines(path) > 0)) {
		dftmp <- read.table(path, col.names=colnames)
		dftmp$KIND = "THEIR"
		if (nrow(df) == 0) {
			df = dftmp
		} else {
			df = rbind(df, dftmp)
		}
	}
}

g <- ggplot(data=df, aes(x=DIST, colour=factor(KIND)))
g <- g + stat_ecdf() + theme_classic()
#g <- ggplot(data=df, aes(x=KIND, y=DIST, colour=factor(KIND)))
#g <- g + geom_boxplot() + theme_classic()
g <- g + scale_x_continuous(expand=c(0,0))
g <- g + scale_y_continuous(expand=c(0,0), limits=c(0,1))

ggsave('errors.eps',g,width=7,height=5)
