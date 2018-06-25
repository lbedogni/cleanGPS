library(ggplot2)

colnames = c('DISTANCE','ERR')
df <- data.frame()
#DIST = rep(NA,550000),TIME1 = rep(NA,550000), LON1 = rep(NA,550000),LAT1 = rep(NA,550000), TIME2 = rep(NA,550000),LON2 = rep(NA,550000), LAT2 = rep(NA,550000), KIND = rep(NA,550000), SAMPLING = rep(NA,550000))
for (sampling in c(10,20,30,60,100,180,240,300)) {
#for (sampling in c(300)) {
#for (sampling in c(10)) {
	path = paste("total_errors_OU_",sampling,".csv",sep="")
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

	path = paste("total_errors_TH_",sampling,".csv",sep="")
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

	path = paste("total_errors_LI_",sampling,".csv",sep="")
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

df$ERR = as.numeric(df$ERR)
summary(df)

#df$ERR = log10(df$ERR)
summary(df)

df$y0 = min(df$ERR)
df$ylow = quantile(df$ERR, 0.1, na.rm=TRUE)
df$ymedian = median(df$ERR)
df$yupper = quantile(df$ERR, 0.9, na.rm=TRUE)
df$y100 = max(df$ERR)

print("----------")
#df$y0
#df$ylow
#df$ymedian
#df$yupper
#df$y100
print("----------")

f <- function(x) {
	r <- quantile(x, probs = c(0.2, 0.35, 0.5, 0.65, 0.8))
	#r <- quantile(x, probs = c(0.1, 0.3, 0.5, 0.7, 0.9))
  	names(r) <- c("ymin", "lower", "middle", "upper", "ymax")
  	r
}

df$KIND <- as.factor(df$KIND)
df$SAMPLING = as.factor(df$SAMPLING)

#g <- ggplot(data=df, aes(x=interaction(KIND,SAMPLING), y=ERR))
g <- ggplot(data=df, aes(x=SAMPLING, y=ERR, fill=KIND))
#g <- ggplot(data=df, aes(x=SAMPLING, y=DIST, fill=KIND))
g <- g + geom_boxplot(outlier.shape=NA) + theme_classic() + theme_classic()
#g <- g + geom_boxplot(outlier.shape=NA, aes(fill=factor(KIND)), position=position_dodge(10)) + theme_classic()
#g <- g + geom_boxplot(outlier.shape=NA, position=position_dodge(1)) + theme_classic()
#g <- g + geom_boxplot(outlier.shape=NA, aes(fill=factor(KIND)), position=position_dodge(.9), ymin=df$y0, lower=df$ylow, middle=df$ymedian, upper=df$yupper, ymax=df$y100) + theme_classic()
#g <- g + stat_summary(fun.data=f, geom="boxplot", aes(fill=factor(KIND), position=position_dodge(.9))) + theme_classic()
#g <- g + geom_point(outlier.shape=NA, aes(fill=factor(KIND)), position=position_dodge(.9)) + theme_classic()
#g <- ggplot(data=df, aes(x=KIND, y=DIST, colour=factor(KIND)))
#g <- g + geom_boxplot() + theme_classic()
#g <- g + scale_x_continuous(expand=c(0,0))
#g <- g + scale_y_continuous(expand=c(0,0), limits=c(0,420))

g <- g + scale_y_log10(breaks=c(1,10,100,1000))
g <- g + coord_cartesian(ylim=c(0.1,10000))
g <- g + theme(legend.position="bottom")
#, legend.justification=c(-0.1,0.8))
g <- g + xlab("Subsampling (s)") + ylab("Error (m)")
g <- g + guides(fill=guide_legend(title=""))
g <- g + theme(panel.grid.major = element_line(colour = "gray"), panel.grid = element_line(colour="gray"))
#g <- g + scale_fill_manual(values=c("OUR","THEIR"), labels=c("OURS","[30]"))
g <- g + theme(text = element_text(size=30), axis.text.x = element_text(hjust=-0.01))
#g <- g + theme(text = element_text(size=20))
#g <- g + theme(text = element_text(size=20))

colorder = c("INTERP.10","OUR.10","THEIR.10","INTERP.20","OUR.20","THEIR.20","INTERP.30","OUR.30","THEIR.30","INTERP.60","OUR.60","THEIR.60","INTERP.100","OUR.100","THEIR.100","INTERP.180","OUR.180","THEIR.180","INTERP.240","OUR.240","THEIR.240","INTERP.300","OUR.300","THEIR.300")

#g <- g + scale_x_discrete(limits=colorder,labels=c("10 s","","","20 s","","","30 s","","","60 s","","", "100 s","","", "180 s","","","240 s","","","300 s","",""))
g <- g + scale_fill_manual(breaks=c("INTERP","OUR","THEIR"),labels=c("LI","OURS","[13]"),values=c("#000000","#BBBBBB","#CB5A4E"))
g <- g + guides(fill = guide_legend(ncol = 6, nrow = 1,keyheight=1, title=""))

ggsave('errors_boxplot_with_LI.eps',g,width=10,height=5)

df <- na.omit(df)

df$DISTANCE = as.numeric(df$DISTANCE)
df$DISTANCE = df$DISTANCE/100
df$DISTANCE = as.integer(df$DISTANCE)
df$DISTANCE = df$DISTANCE*100
df$ERR = as.numeric(df$ERR)
df$SAMPLING = as.numeric(df$SAMPLING)
#finaldf <- aggregate(list(ERR=df$ERR),by=list(DISTANCE = df$DISTANCE, KIND=df$KIND, SAMPLING=df$SAMPLING), data=df, FUN=mean)
finaldf <- na.omit(df)
finaldf <- aggregate(list(ERR=df$ERR),by=list(DISTANCE = df$DISTANCE, KIND=df$KIND), data=df, FUN=mean)
#print(finaldf)
summary(finaldf)

g <- ggplot(data=finaldf, aes(x=DISTANCE, y=ERR))
#g <- ggplot(data=df, aes(x=SAMPLING, y=DIST, fill=KIND))
#g <- g + geom_boxplot(outlier.shape=NA) + theme_classic()
#g <- g + geom_point(aes(colour=factor(KIND))) + theme_classic()
g <- g + geom_point(aes(colour=factor(KIND))) + theme_classic()
#g <- ggplot(data=df, aes(x=KIND, y=DIST, colour=factor(KIND)))
#g <- g + geom_boxplot() + theme_classic()
#g <- g + scale_x_continuous(expand=c(0,0))
#g <- g + scale_y_continuous(expand=c(0,0), limits=c(0,420))
g <- g + theme(legend.position=c(0,1), legend.justification=c(-0.1,1))
g <- g + xlab("Subsampling") + ylab("Error (m)")
g <- g + guides(fill=guide_legend(title=""))
g <- g + guides(colour=guide_legend(title=""))
#g <- g + scale_fill_manual(values=c("OUR","THEIR"), labels=c("OURS","[30]"))
g <- g + theme(text = element_text(size=30), axis.text.x = element_text(hjust=-0.01))
#g <- g + theme(text = element_text(size=20))
#g <- g + theme(text = element_text(size=20))

#colorder = c("INTERP.10","OUR.10","THEIR.10","INTERP.20","OUR.20","THEIR.20","INTERP.30","OUR.30","THEIR.30","INTERP.60","OUR.60","THEIR.60","INTERP.100","OUR.100","THEIR.100","INTERP.180","OUR.180","THEIR.180","INTERP.240","OUR.240","THEIR.240","INTERP.300","OUR.300","THEIR.300")

#g <- g + scale_x_discrete(limits=colorder,labels=c("10 s","","20 s","","30 s","","60 s", "", "100 s", "", "180 s","","240 s","","300 s",""))
g <- g + scale_fill_manual(breaks=c("INTERP","OUR","THEIR"),labels=c("LI","OURS","[13]"),values=c("#000000","#BBBBBB","#CB5A4E"))
g <- g + scale_colour_manual(breaks=c("INTERP","OUR","THEIR"),labels=c("LI","OURS","[13]"),values=c("#000000","#BBBBBB","#CB5A4E"))
g <- g + guides(fill = guide_legend(nrow = 3,keyheight=3, title=""))
g <- g + scale_y_log10()


ggsave('errors_line_with_LI.png',g,width=10,height=5)
