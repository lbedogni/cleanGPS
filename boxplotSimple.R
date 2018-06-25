library(ggplot2)

colnames = c('DIST')
df <- data.frame()
#DIST = rep(NA,550000),TIME1 = rep(NA,550000), LON1 = rep(NA,550000),LAT1 = rep(NA,550000), TIME2 = rep(NA,550000),LON2 = rep(NA,550000), LAT2 = rep(NA,550000), KIND = rep(NA,550000), SAMPLING = rep(NA,550000))
#for (sampling in c(10,20)) {
for (sampling in c(10,20,30,60,100,180,240,300)) {
	path = paste("errors_our_",sampling,".csv",sep="")
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

	path = paste("errors_their_",sampling,".csv",sep="")
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

	path = paste("errors_interp_",sampling,".csv",sep="")
	print(path)
	if (length(readLines(path) > 0)) {
		dftmp <- read.table(path, col.names=colnames)
		dftmp$KIND = "INTERP"
		dftmp$SAMPLING = sampling
		if (nrow(df) == 0) {
			df = dftmp
		} else {
			df = rbind(df, dftmp)
		}
	}
}

summary(df)

g <- ggplot(data=df, aes(x=interaction(KIND,SAMPLING), y=DIST))
#g <- ggplot(data=df, aes(x=SAMPLING, y=DIST, fill=KIND))
#g <- g + geom_boxplot(outlier.shape=NA) + theme_classic()
g <- g + geom_boxplot(outlier.shape=NA, aes(fill=factor(KIND)), position=position_dodge(.9)) + theme_classic()
#g <- ggplot(data=df, aes(x=KIND, y=DIST, colour=factor(KIND)))
#g <- g + geom_boxplot() + theme_classic()
#g <- g + scale_x_continuous(expand=c(0,0))
g <- g + scale_y_continuous(expand=c(0,0), limits=c(0,420))
g <- g + theme(legend.position=c(0,1), legend.justification=c(-0.1,1))
g <- g + xlab("Subsampling") + ylab("Error (m)")
g <- g + guides(fill=guide_legend(title=""))
#g <- g + scale_fill_manual(values=c("OUR","THEIR"), labels=c("OURS","[30]"))
g <- g + theme(text = element_text(size=30), axis.text.x = element_text(hjust=-0.01))
#g <- g + theme(text = element_text(size=20))
#g <- g + theme(text = element_text(size=20))

colorder = c("INTERP.10","OUR.10","THEIR.10","INTERP.20","OUR.20","THEIR.20","INTERP.30","OUR.30","THEIR.30","INTERP.60","OUR.60","THEIR.60","INTERP.100","OUR.100","THEIR.100","INTERP.180","OUR.180","THEIR.180","INTERP.240","OUR.240","THEIR.240","INTERP.300","OUR.300","THEIR.300")

g <- g + scale_x_discrete(limits=colorder,labels=c("10 s","","20 s","","30 s","","60 s", "", "100 s", "", "180 s","","240 s","","300 s",""))
g <- g + scale_fill_manual(breaks=c("INTERP","OUR","THEIR"),labels=c("LI","OURS","[13]"),values=c("#000000","#BBBBBB","#CB5A4E"))
g <- g + guides(fill = guide_legend(nrow = 3,keyheight=3, title=""))

ggsave('errors_boxplot.eps',g,width=10,height=5)
