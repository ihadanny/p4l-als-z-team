
# coding: utf-8

# ## Builds all our models x-validated
# 

# In[1]:

from IPython.display import display

import pandas as pd
import numpy as np
import pickle, cPickle
from sklearn.cluster import KMeans
from StringIO import StringIO
from sklearn import metrics
from sklearn.cross_validation import KFold

from vectorizing_funcs import *
from modeling_funcs import *


# In[2]:

df = pd.read_csv('../all_data.csv', sep = '|', error_bad_lines=False, index_col=False, dtype='unicode')
slope = pd.read_csv('../all_slope.csv', sep = '|', index_col="SubjectID")
slope.index = slope.index.astype(str)

print "df: ", df.shape, df.SubjectID.unique().size
print "slope: ", slope.shape, slope.index.unique().size
display(df.head(2))
display(slope.head(2))


# In[3]:

from datetime import datetime

def train_and_test(df, slope, my_n_clusters=2):
    kf = KFold(df.SubjectID.unique().size, n_folds=3)
    fold, test_rmse, train_rmse, fold_test_rmse, fold_train_rmse = 0, 0.0, 0.0, 0.0, 0.0

    for train, test in kf:
        train_data = df[df.SubjectID.isin(df.SubjectID.unique()[train])]
        test_data = df[df.SubjectID.isin(df.SubjectID.unique()[test])]
        print
        print "*"*30
        print "fold: %d" % fold
        tick = datetime.now()
        
        all_feature_metadata,                     train_data_means, train_data_std, train_data_medians, train_data_mads,                     bins, forest, best_features_per_cluster, model_per_cluster = train_it(train_data, slope, my_n_clusters)

        input_for_model, pred = apply_on_test(train_data, all_feature_metadata, 
                    train_data_means, train_data_std, train_data_medians, train_data_mads,
                    clustering_columns, bins, forest, best_features_per_cluster, model_per_cluster)
        res = pred.join(slope)
        fold_train_rmse = np.sqrt(np.mean((res.prediction - res.ALSFRS_slope) ** 2))

        input_for_model, pred = apply_on_test(test_data, all_feature_metadata, 
                    train_data_means, train_data_std, train_data_medians, train_data_mads, 
                    clustering_columns, bins, forest, best_features_per_cluster, model_per_cluster)
        res = pred.join(slope)
        fold_test_rmse = np.sqrt(np.mean((res.prediction - res.ALSFRS_slope) ** 2))

        input_for_model.to_csv('../x_results/test_%d_input_for_model.csv' % fold,sep='|')
        res.to_csv('../x_results/test_%d_prediction.csv' % fold,sep='|')

        fold += 1
        print "fold RMS Error train, test: ", fold_train_rmse, fold_test_rmse
        print 'pearson correlation r = %.2f ' % scipy.stats.pearsonr(res.prediction, res.ALSFRS_slope)[0]
        train_rmse += fold_train_rmse
        test_rmse += fold_test_rmse

        tock = datetime.now()   
        diff = tock - tick 
        print "minutes for fold: ", diff.seconds / 60

            
    print "X-validated RMS Error train, test: ", train_rmse / kf.n_folds, test_rmse / kf.n_folds



# In[ ]:




# In[6]:

for n_clusters in range(7, 13):
    print "*"*60
    print "n_clusters", n_clusters
    print "*"*60
    train_and_test(df, slope, n_clusters)


# In[ ]:



