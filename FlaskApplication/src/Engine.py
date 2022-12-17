## Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#matplotlib inline
#from ML_Pipeline.utlis import read_data
from sklearn.model_selection import train_test_split
#from ML_Pipeline.models import model_zoo, evaluate_models
#from ML_Pipeline.hyperparameter import model,parameters
#from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from lightgbm import LGBMClassifier
from ML_Pipeline.feature_eng import AddFeatures
#from ML_Pipeline.scaler import CustomScaler
from ML_Pipeline.encoding import CategoricalEncoder
from sklearn.metrics import roc_auc_score, f1_score, recall_score, confusion_matrix, classification_report
import joblib

#read the data
df = pd.read_csv("https://s3.amazonaws.com/hackerday.datascience/360/Churn_Modelling.csv")

## Separating out different columns into various categories
target_var = ['Exited']
cols_to_remove = ['RowNumber', 'CustomerId']
#num_feats = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']
#cat_feats = ['Surname', 'Geography', 'Gender', 'HasCrCard', 'IsActiveMember']

## Separating out target variable and removing the non-essential columns
y = df[target_var].values
df.drop(cols_to_remove, axis=1, inplace=True)

## Keeping aside a test/holdout set
df_train_val, df_test, y_train_val, y_test = train_test_split(df, y.ravel(),
                                                              test_size = 0.1,
                                                              random_state = 42)

## Splitting into train and validation set
df_train, df_val, y_train, y_val = train_test_split(df_train_val,
                                                    y_train_val,
                                                    test_size = 0.12,
                                                    random_state = 42)


### FINAL MODEL - Train final, best model ; Save model and its parameters ###
## Re-defining X_train and X_val to consider original unscaled continuous features. y_train and y_val remain unaffected
X_train = df_train.drop(columns = ['Exited'], axis = 1)
X_val = df_val.drop(columns = ['Exited'], axis = 1)

X_train.shape, y_train.shape
X_val.shape, y_val.shape

best_f1_lgb = LGBMClassifier(boosting_type = 'dart', class_weight = {0: 1, 1: 3.0}, min_child_samples = 20, n_jobs = - 1
                     , importance_type = 'gain', max_depth = 6, num_leaves = 63, colsample_bytree = 0.6, learning_rate = 0.1
                     , n_estimators = 201, reg_alpha = 1, reg_lambda = 1)

best_recall_lgb = LGBMClassifier(boosting_type='dart', num_leaves=31, max_depth= 6, learning_rate=0.1, n_estimators = 21
                                 , class_weight= {0: 1, 1: 3.93}, min_child_samples=2, colsample_bytree=0.6, reg_alpha=0.3
                                 , reg_lambda=1.0, n_jobs=- 1, importance_type = 'gain')


final_model = Pipeline(steps = [('categorical_encoding', CategoricalEncoder()),
                          ('add_new_features', AddFeatures()),
                          ('classifier', best_f1_lgb)
                         ])


## Fitting final model on train dataset
final_model.fit(X_train, y_train)

# Predict target probabilities
val_probs = final_model.predict_proba(X_val)[:,1]

# Predict target values on val data
val_preds = np.where(val_probs > 0.45, 1, 0) # The probability threshold can be tweaked

## Validation metrics
roc_auc_score(y_val, val_preds)
recall_score(y_val, val_preds)
confusion_matrix(y_val, val_preds)
##print(classification_report(y_val, val_preds))

## Save model object
joblib.dump(final_model, '../output/final_churn_model_f1_0_45.sav')

## testing


## Load model object
model = joblib.load('../output/final_churn_model_f1_0_45.sav')
#model = final_model
X_test = df_test.drop(columns = ['Exited'], axis = 1)
print(X_test.shape)
print(y_test.shape)
## Predict target probabilities
test_probs = model.predict_proba(X_test)[:,1]
## Predict target values on test data
test_preds = np.where(test_probs > 0.45, 1, 0) # Flexibility to tweak the probability threshold
#test_preds = model.predict(X_test)

## Test set metrics
roc_auc_score(y_test, test_preds)
recall_score(y_test, test_preds)
confusion_matrix(y_test, test_preds)
print(classification_report(y_test, test_preds))

## Adding predictions and their probabilities in the original test dataframe
test = df_test.copy()
test['predictions'] = test_preds
test['pred_probabilities'] = test_probs

high_churn_list = test[test.pred_probabilities > 0.7].sort_values(by = ['pred_probabilities'], ascending = False
                                                                 ).reset_index().drop(columns = ['index', 'Exited', 'predictions'], axis = 1)
print(high_churn_list.shape)
print(high_churn_list.head())
high_churn_list.to_csv('../output/high_churn_list.csv', index = False)

print("DONE")