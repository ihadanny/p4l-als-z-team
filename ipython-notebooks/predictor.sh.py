
# coding: utf-8

# ## Run predictor.sh
# Read the challenge standard selected features and emit a prediction

# In[25]:

import pickle
import pandas as pd
import sys
from os import listdir
from os.path import isfile, join
from StringIO import StringIO
from vectorizing_funcs import *

if "IPython" not in sys.argv[0]:
    models_folder, input_file, output_file= sys.argv[1], sys.argv[2], sys.argv[3]
else:
    models_folder, input_file, output_file= "../", "../selected_19871.txt", "../predicted_19871.txt"

all_feature_metadata = pickle.load( open(models_folder + '/all_feature_metadata.pickle', 'rb') )
train_data_means = pickle.load( open(models_folder + '/all_data_means.pickle', 'rb') )
train_data_std = pickle.load( open(models_folder + '/all_data_std.pickle', 'rb') )
train_data_medians = pickle.load( open(models_folder + '/all_data_medians.pickle', 'rb') )
train_data_mads = pickle.load( open(models_folder + '/all_data_mads.pickle', 'rb') )
model_per_cluster = pickle.load( open(models_folder + '/model_per_cluster.pickle', 'rb') )

def calc(x):
    c = x['cluster']
    model = model_per_cluster[c]['model']
    pred = float(model.predict(x))
    return pd.Series({'prediction':pred, 'confidence': 0.5})
    
with open(input_file, 'r') as f:
    content = f.readlines()
    c = int(content[0].split(":")[1])
    # adding a bogus subject as we suspect a bug if the subject comes empty from the selector 
    s = "-1|bbb|k|v|u|0\n" + "".join(content[1:])
    df = pd.read_csv(StringIO(s), sep='|', index_col=False, dtype="unicode",
                    names =["SubjectID","form_name","feature_name","feature_value","feature_unit","feature_delta"])
    vectorized, _ = vectorize(df, all_feature_metadata)
    cleaned = clean_outliers(vectorized, all_feature_metadata, train_data_medians, train_data_mads, train_data_std)    
    normalized, _ = normalize(cleaned, all_feature_metadata, train_data_means, train_data_std)
    normalized.loc[:, "cluster"] = c
    normalized = normalized[normalized.index != '-1']
    pred = normalized.apply(calc, axis=1)
    print pred
    pred.to_csv(output_file ,sep='|', header=False, index=False, 
                columns=["prediction", "confidence"])


# In[ ]:



