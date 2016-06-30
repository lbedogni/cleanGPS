library(ggplot2)

dd = read.table("beijing_speeds_5.csv.final")
dd$city = "Beijing"
dd2 = read.table("napoli_speeds_5.csv.final")
dd2$city = "Napoli"
dd3 = read.table("milano_speeds_5.csv.final")
dd3$city = "Milano"
dd4 = read.table("roma_speeds_5.csv.final")
dd4$city = "Roma"
dd5 = read.table("torino_speeds_5.csv.final")
dd5$city = "Torino"
dd6 = read.table("bari_speeds_5.csv.final")
dd6$city = "Bari"
dd7 = read.table("shanghai_speeds_5.csv.final")
dd7$city = "Shanghai"
dd8 = read.table("nyc_speeds_5.csv.final")
dd8$city = "NYC"
dd9 = read.table("sf_speeds_5.csv.final")
dd9$city = "SF"

df = rbind(dd,dd2)
df = rbind(df,dd3)
df = rbind(df,dd4)
df = rbind(df,dd5)
df = rbind(df,dd6)
df = rbind(df,dd7)
df = rbind(df,dd8)
df = rbind(df,dd9)
gp <- ggplot(data = df, aes(x = V1, y = V2, group = city, color = city)) + geom_line()
gp <- gp + theme_bw() + scale_y_continuous(expand=c(0,0)) + scale_x_continuous(expand=c(0,0), limits=c(0,50))
gp <- gp + xlab("Speed (m/s)") + ylab("CDF")
ggsave('cdf_red.eps', gp)
