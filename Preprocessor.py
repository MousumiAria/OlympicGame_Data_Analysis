import numpy as np
import pandas as pd


def preprocess(athlete,noc):    
    #filtering for summer olymoics
    athlete=athlete[athlete['Season']== 'Summer']
    #merge with noc
    athlete=athlete.merge(noc,on='NOC',how='left')
    # Drop all duplicates
    athlete.drop_duplicates(inplace=True)
    #one hot encoding medals
    athlete=pd.concat([athlete,pd.get_dummies(athlete['Medal'])],axis=1)
    return athlete