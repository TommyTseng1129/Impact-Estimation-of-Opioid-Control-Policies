#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import pandas and numpy
import pandas as pd
import numpy as np


# In[2]:


# Read in the entire .tsv, with chunk size equal to 100000
national = pd.read_csv('/Users/lin-chuntseng/Desktop/arcos_all_washpost.tsv', sep='\t', chunksize = 100000 , low_memory=False)

# Extract rows that are from the chosen states
keepers = list()

# We choose 7 states for the first time (AL was wrongly picked...)
states = ['GA', 'AR', 'MS', 'SC', 'LA', 'NC', 'AL','FL']

# We chose 10 states for the second time to find similar-slope states before policy implementation
states2 = [ 'GA', 'AR', 'MS', 'MI', 'TN', 'NC', 'NH', 'IA','IL', 'FL']

# The finalized 4 chosen states for opioid shipment analysis
states3 = [ 'AR','TN','FL','GA' ]
for i in national:
    test = i['BUYER_STATE'].isin(states3)
    rows_to_keep = i.loc[test]
    keepers.append(rows_to_keep)
new_df = pd.concat(keepers)


# In[3]:


# Quick display of BUER_STATE column, making sure new_df only contains the chosen 4 states
new_df['BUYER_STATE'].unique()


# In[4]:


# Add a YEAR column by extracting the last 4 digit from TRANSACTION_DATE
new_df['YEAR'] = new_df['TRANSACTION_DATE'].astype('str').str[-4:]


# In[5]:


# Quick display of the YEAR column, making sure new_df only contains year from 2006-2012
new_df['YEAR'].unique()


# In[6]:


# Add a Total_Weight column that is the multiple of MME_Conversion_Factor and CALC_BASE_WT_IN_GM
new_df['Total_Weight'] = new_df['MME_Conversion_Factor'] * new_df['CALC_BASE_WT_IN_GM']


# In[29]:


# Keep necessary columns for the dataframe
necessary_col = ['BUYER_COUNTY','BUYER_STATE', 'YEAR','Total_Weight']

# Rename the trimmed new_df as prescription
prescription = new_df[necessary_col]


# In[30]:


# Quick display of the first 10 rows of prescription dataframe, making sure we only have 4 columns
prescription.head(10)


# In[31]:


# Quick display of the size of prescription dataframe (26577645)
prescription.shape


# In[32]:


# We have 130 missing counties
prescription.isnull().sum()


# In[39]:


# Checking total number of counties that are not missing (26577515), so we have around 0.000489% missing counties (130/26577645)
sum(prescription['BUYER_COUNTY'].value_counts())


# In[40]:


# Trying to figure out why we have missing values, and their corresponding patterns (Null doesnt work...)
prescription.loc[prescription['BUYER_COUNTY'] == 'Null']


# In[41]:


# Trying to figure out why we have missing values, and their corresponding patterns  (np.nan doesnt work...)
prescription.loc[prescription['BUYER_COUNTY'] == np.nan]


# In[42]:


# Trying to figure out why we have missing values, and their corresponding patterns  (None doesnt work...)
prescription.loc[prescription['BUYER_COUNTY'] == None]


# In[43]:


# Since the percentage of missing values are and I really can't find those missing rows by subsetting
# I will simply drop the missing counties and move on

prescription = prescription.dropna()
prescription.isnull().sum()


# In[44]:


# GroupBy State, county, year
prescription = prescription.groupby(['BUYER_STATE','BUYER_COUNTY','YEAR'], as_index=False).sum()


# In[45]:


# Check the size of prescription after performing groupBy (2711 rows, 4 columns)
prescription.shape


# In[46]:


# Export prescription to a .csv for later use
prescription.to_csv(r'/Users/lin-chuntseng/Desktop/2006-2012_prescription_finalStates.csv', index = False, header = True)

