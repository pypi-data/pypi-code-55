import pandas as pd

import numpy as np

class Mdummies:
    
    """The Mdummies class represents an column which has multiple values included in it"""
    def __init__(self,df,col):
        
        """Method for initializing a Mdummies object
    
        Args: 
            df (dataframe)
            col (dataframe column name)
            
        Attributes:
            df: A dataframe which has categorical column with multiple values.
            col: the column name which has multiple values example column amenities each row has ['Swimming pool', 'Gym', 'Play area', etc]
        """
        
        self.df=df
        
        self.col=col
    
        
    def create_dummies(self):
        """create_dummies method provides a dataframe with dummy columns created """
        
        self.df[self.col] =  self.df[self.col].apply(lambda x: x.replace('{','').replace('}','').
            replace('[','').replace(']','').replace("''",'').replace('"',''))
        
        df1=self.df[self.col].str.get_dummies(sep=',')
        
        df1.reset_index(drop=True, inplace=True)
        
        final_df= pd.concat([self.df, df1],axis=1)
        
        return final_df