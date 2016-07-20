library(ggplot2)

dd <- read.table('allFactors.csv')
dd

g <- ggplot(data = dd, aes(x=V1)) + stat_density(aes(x=V1),position='identity',geom='line')
ggsave('allfactors.eps',g)
g <- g + scale_x_continuous(limits=c(0,5))
ggsave('allfactors_01.eps',g)
