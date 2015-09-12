
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np

df = pd.read_csv('../train_data.csv', sep = '|', error_bad_lines=False, index_col=False, dtype='unicode')
df.head()


# In[9]:

feature_names = df[["form_name", "feature_name"]].drop_duplicates()
feature_names.to_csv('../feature_names.csv', sep='|', index=False)


# In[19]:

feature_values = df[["form_name", "feature_name", "feature_value"]].drop_duplicates()
feature_values = feature_values[np.isnan(feature_values.feature_value.convert_objects(convert_numeric=True))]
feature_values.to_csv('../feature_values.csv', sep='|', index=False)


# In[ ]:


