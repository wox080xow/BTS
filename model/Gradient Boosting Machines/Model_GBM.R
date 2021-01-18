library(rsample)      
library(gbm)          
library(xgboost)      
library(caret)       
library(h2o)          
library(pdp)          
library(ggplot2)      
library(lime)         
library(vtreat)
library(dplyr)

# 1. Import data ####
house <- read.csv("HouseVar.csv", row.names = 1L)

# 2. Fliter data ####
HouseRe <- house[house$建物型態 %in% c("住宅大樓", "公寓", "套房", "華廈"), ] 
HouseRe <- HouseRe %>% filter(建物現況格局.房<11, 建物現況格局.衛<10, 車位數<5,
                                    總坪數 < 75 & 總坪數 > 10 & 總價元 > 7000000 &
                                        總價元 < 30000000 & 單價元坪 < 1000000 &
                                        單價元坪 > 150000 & year > 2012) 
HouseRe <- HouseRe %>% rename(廳數=建物現況格局.廳, 房間數=建物現況格局.房,
                              衛浴數 = 建物現況格局.衛, 隔間=建物現況格局.隔間,
                              管理組織 = 有無管理組織)
names(HouseRe)
HouseRe_copy <- HouseRe

# 3. Split data ####
HouseCon <- HouseRe[,c(8:13,15:47)]

set.seed(123)
train.index <- sample(x=1:nrow(HouseCon),
                      size=ceiling(0.8*nrow(HouseCon)))
#ceiling():無條件進位
train <- HouseCon[train.index, ]
test <- HouseCon[-train.index, ]

# 4.Modeling ####
## 4.1 Train Model ####
set.seed(123)

# train GBM model
system.time(
    gbm.fit <- gbm(
        formula = 單價元坪 ~ .,
        distribution = "gaussian",
        data = train,
        n.trees = 10000, # 總迭代次數
        interaction.depth = 1, # 弱模型的切割數
        shrinkage = 0.001, # learning rate
        cv.folds = 5, # cross validation folds
        n.cores = NULL, # will use all cores by default
        verbose = FALSE
    )  
)

print(gbm.fit) 

sqrt(min(gbm.fit$cv.error))
gbm.perf(object = gbm.fit, plot.it = TRUE, method = "cv")
  
## 4.2 Tuning - grid search ####
# create hyperparameter grid
hyper_grid <- expand.grid(
    shrinkage = c(.01, .05, .1),     
    interaction.depth = c(3, 5, 7), 
    n.minobsinnode = c(5, 7, 10),    
    bag.fraction = c(.65, .8, 1),    
    optimal_trees = 0,               
    min_RMSE = 0                    
)

# total number of combinations
nrow(hyper_grid)
## [1] 81

# randomize data
random_index <- sample(1:nrow(train), nrow(train))
random_train <- train[random_index, ]

# grid search 
for(i in 1:nrow(hyper_grid)) {
    set.seed(123)
    # train model
    gbm.tune <- gbm(
        formula = 單價元坪 ~ .,
        distribution = "gaussian",
        data = random_train,
        n.trees = 1000, # 使用500個樹模型
        interaction.depth = hyper_grid$interaction.depth[i],
        shrinkage = hyper_grid$shrinkage[i],
        n.minobsinnode = hyper_grid$n.minobsinnode[i],
        bag.fraction = hyper_grid$bag.fraction[i],
        train.fraction = .75, 
        n.cores = NULL, 
        verbose = FALSE
    )
    hyper_grid$optimal_trees[i] <- which.min(gbm.tune$valid.error)
    hyper_grid$min_RMSE[i] <- sqrt(min(gbm.tune$valid.error))
}

hyper_grid %>% 
    dplyr::arrange(min_RMSE) %>%
    head(10)

# 4.3 Run model after tuning ####
set.seed(123)
system.time(
    # train GBM model
    gbm.fit.final <- gbm(
        formula = 單價元坪 ~ .,
        distribution = "gaussian",
        data = train,
        n.trees = 1000,
        interaction.depth = 7,
        shrinkage = 0.1,
        n.minobsinnode = 10,
        bag.fraction = .8, 
        train.fraction = 1, 
        cv.folds = 4, 
        n.cores = NULL, 
        verbose = FALSE
    )
)

sqrt(min(gbm.fit.final$cv.error))

# 5. Visualizaiton ####
## 5.1 特徵重要度（Feature Importance） ####
par(mar = c(5, 8, 1, 1))

summary(
    gbm.fit.final,
    # gbm object
    cBars = 10,
    plotit = TRUE,
    method = relative.influence,
    las = 2,
    family="黑體-繁 中黑"
)

gbminfluence <- summary(gbm.fit.final) 
gbminfluence$rel.inf <- gbminfluence$rel.inf %>% round(2)
View(gbminfluence)

# 5.2 Partial dependence plots(PDPs) ####
gbm.fit.final %>%
    partial(
        object = .,
        pred.var = "總坪數",
        n.trees = gbm.fit.final$n.trees,
        grid.resolution = 1000
    ) %>%
    autoplot(rug = TRUE, train = train) + 
    scale_y_continuous(labels = scales::dollar) + 
    theme(text = element_text(family = "黑體-繁 中黑"))

# 6. Predict ####

# 6.1 Predict test data  ####
# Predict values for test data
pred <- predict(gbm.fit.final, n.trees = gbm.fit.final$n.trees, test)

# results
caret::RMSE(pred, test$單價元坪)

# 6.2 Predict all ####
predAll <- predict(gbm.fit.final, 
                   n.trees = gbm.fit.final$n.trees, 
                   HouseCon) %>% as.data.frame()
caret::RMSE(predAll, HouseCon$單價元坪)

names(predAll)[1] <- "pred"

# 7. Combine original Dataset ####
ComData <- cbind(HouseRe_copy, predAll)
ComData$pred - ComData$單價元坪
ComData$漲跌 <- (ComData$pred-ComData$單價元坪) %>% round(2)

## 2.2 Comebine Predict & coord
coord <- read.csv("HouseVarCoFinal.csv")
names(coord)
coordSe <- coord[,c('Address', 'Lontitude', 'Latitude')]
coordReduce <- unique(coordSe) %>%na.omit()

HouseVarCo2 <- merge(ComData, coordReduce, by='Address', on='inner')
HouseVarCo2 %>% head()

# 8. Summarize ####
# 8.1 By Area ####
updown <- ComData %>% group_by(Area) %>% summarise(count = n(),
                                                    avg_單價元坪 = mean(單價元坪), 
                                                    avg_漲跌 = mean(漲跌)) 
updown$pre_單價元坪 <- updown$avg_單價元坪 + updown$avg_漲跌
View(updown)

# 8.2 By St ####
library(dplyr)
updown2 <- HouseVarCo2 %>% group_by(St) %>% summarise(count = n(),
                                                  avg_單價元坪 = mean(單價元坪), 
                                                  avg_漲跌 = mean(漲跌)) 
updown2$pre_單價元坪 <- updown2$avg_單價元坪 + updown2$avg_漲跌
View(updown)