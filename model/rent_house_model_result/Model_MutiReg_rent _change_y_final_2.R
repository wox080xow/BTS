library(dplyr)
library(Hmisc)
# library(AppliedPredictiveModeling)
# 1. Read data ####
# house <- read.csv("renting_house_merge_4.csv", row.names = 1L)
# house <- read.csv("C:/Shared/BDSE15_R/大數據分析與應用實戰程式碼/codes_R/renting_house_merge_2temp.csv", 
#                  sep=",",stringsAsFactors=FALSE,header=T)

house <- readxl::read_excel("renting_house_merge_5.xlsx")

# 2. Check data ####
str(house)

# 2.1 Check na ####
house %>% is.na() %>% sum()

# [1] 9116

# 2.2 Descrive Statistic ####
# 2.2.1 Fliter Vars ####
HouseRe <- house[house$主要用途 %in% c("住家用", "國民住宅"), ] 

HouseRe  <- HouseRe[HouseRe$建物類型 %in% c("住宅大樓", "公寓","套房","華廈"), ]

HouseRe <- HouseRe %>% filter(
  建物總坪數 < 90 & 建物總坪數 > 4 & 總額元 > 5000 &
    總額元 < 50000 & 單價元坪 < 2500 &
    單價元坪 > 400 & Year > 101)

# # 建物總坪數 < 150 & 建物總坪數 > 3 parking_lot <5
# 2.2.2 Plot ####
# par(mfrow=c(1,1))
# plot(HouseRe$Area,main="Area",family="黑體-繁 中黑")
# hist(HouseRe$總價元, main="總價",family="黑體-繁 中黑")
# plot(HouseRe$建物型態, main="建物型態",family="黑體-繁 中黑")
# hist(HouseRe$建物現況格局.廳,main="廳數量",family="黑體-繁 中黑")
# hist(HouseRe$建物現況格局.房,main="房數量",family="黑體-繁 中黑")
# hist(HouseRe$建物現況格局.衛,main="衛數量",family="黑體-繁 中黑")
# plot(HouseRe$建物現況格局.隔間,main="隔間",family="黑體-繁 中黑")
# plot(HouseRe$有無管理組織,main="管理組織",family="黑體-繁 中黑")
# hist(HouseRe$總坪數,main="總坪數",family="黑體-繁 中黑")
# hist(HouseRe$單價元坪,main="單價元坪",family="黑體-繁 中黑")
# hist(HouseRe$車位數,main="車位數",family="黑體-繁 中黑")
# hist(HouseRe$floor,main="樓層",family="黑體-繁 中黑")

# 2.2.3 Select Continuous vars ####

HouseRe$男女比 <- HouseRe$女性人數/HouseRe$男性人數

# original data(多)
HouseRe2 <- HouseRe[c("Area", "Address","St","建物現況格局-廳",
                      "建物現況格局-房","建物現況格局-衛","建物總坪數","主要用途",
                      "建物現況格局-隔間","有無管理組織","有無附傢俱",
                      "EightCount","FuneralCount","PoliceCount","busCount","CrimeCount",
                      "parking_lot","F", "ParkCount","GasCount","subwayCount",
                      "govCount", "hospitalCount", "martCount","clinicCount","pharmacyCount",
                      "fireareaCount","mallCount","firewayCount","總人口數","人口密度","儲蓄",
                      "所得收入總計","消費支出","可支配所得","Year",
                      "每戶成年人數","每戶人數","所得總額","總額元"
)]


# select variables dataset(少)
HouseCon <- HouseRe[c("建物現況格局-房","建物現況格局-廳","建物現況格局-衛","F",
                      "parking_lot","subwayCount","ParkCount","GasCount","EightCount",
                      "govCount","martCount","clinicCount","Year",
                      "firewayCount","每戶人數","所得總額","總額元",
                      "建物總坪數"
                      
                      # #delect variables below
                      #
                      # 
                      # "CrimeCount",
                      # "FuneralCount","PoliceCount",
                      # "busCount","hospitalCount",
                      # "pharmacyCount","fireareaCount",
                      # "mallCount","cinemaCount",
                      # "男性人數","女性人數","男女比","土地面積",
                      # "每戶成年人數",
                      # "所得收入總計","消費支出","可支配所得",
                      # "人口密度","儲蓄","總人口數"
                      
)]
# # HouseCon[1:13] <- lapply(HouseCon[1:13], as.numeric)
str(HouseCon)
summary(HouseCon)

# 3. Modeling ####

## 3.1 Cor ####
cor_ <- cor(HouseCon, method = 'pearson') %>% round(3)
# View(cor_)

# 3.2 Normalization ####
# HouseConSca <- scale(HouseCon) %>% as.data.frame()
# HouseConNor <- normalize(HouseCon) %>% as.data.frame()
HouseConSca <- HouseCon %>% mutate_at(scale, .vars = vars(-總額元 ))

## 3.3 Split data ####
# train=0.8, test=0.2 
set.seed(22)
train.index <- sample(x=1:nrow(HouseConSca),
                      size=ceiling(0.8*nrow(HouseCon)))
#ceiling():無條件進位
train <- HouseConSca[train.index, ]
test <- HouseConSca[-train.index, ]

## 3.2 Mutiple Regression ####
mOri <- lm(總額元 ~ ., data = train)
summary(mOri)
par(mfrow=c(2,2))
plot(mOri)

## 3.3 Check Multicollinearity ####
library(car)
vif(mOri) #VIF > 10 --> remove

# 3.4 Make predictions ####
distPred <- predict(mOri, test)  # predict distance
actuals_preds <- data.frame(cbind(actuals=test$總額元 , predicteds=distPred))  
correlation_accuracy <- cor(actuals_preds)  
correlation_accuracy

# 3.5 Final model
# library(dataPreparation)
mFinal <- lm(總額元 ~ ., data = HouseConSca)
summary(mFinal)


# 3.6 Predict     
HouseRe2$pred <- fitted(mFinal)
HouseRe2$漲跌 <- HouseRe2$pred-HouseRe2$總額元 

# 4. Summarize
updown <- HouseRe2 %>% group_by(Area) %>% summarise(count = n(),
                                                    avg_總額元 = mean(總額元 ), 
                                                    avg_漲跌 = mean(漲跌)) 
updown$pre_總額元  <- updown$avg_總額元  + updown$avg_漲跌

library(sqldf)

HouseCount <-  sqldf("SELECT Area, count
                  FROM updown
                  LEFT JOIN HouseRe2 USING(Area)")

# 錯誤
# (HouseCount<- data.table(key = "Area"))
# (HouseRe2 <- data.table(key = "Area"))
# merge(HouseCount, HouseRe2, all = TRUE)
# 
# HouseRe2$交易量 <- HouseCount$count(key='Area')

# merge(HouseRe2, HouseCount, by = "Area", all.x = TRUE)

# options(scipen=999)

write.csv(updown,'C://Shared/BDSE15_R/RentAreaSummary_modify.csv')
write.csv(HouseRe2,'C://Shared/BDSE15_R/RentHouseRe2_modify.csv')
write.csv(HouseRe,'C://Shared/BDSE15_R/RentHouseRe_modify.csv')


# #後向式
# system.time(reducedSolMdl <- step(mFinal, direction='backward'))
# 
# 
# #雙向式
# system.time(fwdSolMdl <-step(mFinal, direction = "both", trace = FALSE))
# fwdSolMdl

