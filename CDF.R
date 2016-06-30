library(ggplot2)
print("BEGIN")

data <- read.table('bari_speeds.csv')
data$city = "Bari"
print("BARI")
data2 <- read.table('milano_speeds.csv')
data2$city = "Milano"
print("MILANO")
data3 <- read.table('roma_speeds.csv')
data4$city = "Roma"
print("ROMA")
data4 <- read.table('napoli_speeds.csv')
data4$city = "Napoli"
print("NAPOLI")
data5 <- read.table('torino_speeds.csv')
data5$city = "Torino"
print("TORINO")

print("READ EVERYTHING")

dftotal = rbind(data,data2)
dftotal = rbind(dftotal,data3)
dftotal = rbind(dftotal,data4)
dftotal = rbind(dftotal,data5)

print("Now we plot")

g <- ggplot(data = dftotal, aes(x = V1), group = factor(city)) + stat_ecdf()
ggsave('cdf.eps',g)
