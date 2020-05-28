"""Main module."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

class ez_linear():
    
    def __init__(self, fitted_model):
        self.model = fitted_model
    
    def feature_importance(self, plot = True):
        df = pd.DataFrame(self.model.tvalues)
        df.drop('Intercept', inplace = True)
        df.reset_index(inplace = True)
        df.columns = ['Features', 'Importance']
        # take the absolute value of the T statistic
        df['Abs_Importance'] = np.abs(df['Importance'])
        df.sort_values('Abs_Importance', inplace = True)
        df.drop('Importance', axis = 1, inplace = True)
        df.set_index('Features', inplace = True)
        df.columns = ['Feature_Importance']
        if plot:
            with plt.style.context('fivethirtyeight'):
                fig = plt.figure(figsize = (12, 4))
                plt.barh(df.index, df['Feature_Importance'], color = '#2e8b57')
                plt.xlabel('Feature Importance')
            return df, fig
        return df
    
    def weight_plot(self):
        df = pd.DataFrame(self.model.params)
        df['standard_error'] = self.model.bse * 1.96
        df.columns = ['coef', 'standard_error']
        df.drop('Intercept', inplace = True)
        df.sort_values('coef', inplace = True)
        df.reset_index(inplace = True)
        df=df.rename(columns = {'index':'columns'})
        with plt.style.context('fivethirtyeight'):
            fig = plt.figure(figsize = (12, 4))
            plt.scatter(x = df['coef'], y = range(len(df)), s = 50, c = 'k')
            plt.errorbar(x = df['coef'], y =  range(len(df)), 
                         xerr=df['standard_error'], fmt='none', marker='o', color='k', capsize = 0,
                        lw = 2)
            plt.yticks(range(len(df)), df['columns'])
            plt.axvline(0, lw = 1, color = 'red', ls = '--')
            plt.xlabel('Weight Estimate')
        return df, fig
    
    def effect_dataframe(self, raw_data, categorical_dictionary):
        df1 = pd.DataFrame(self.model.params)
        df1.columns = ['coef']
        df1.drop('Intercept', inplace = True)

        # make list of all columns from categorical dictionary 
        cat_cols = []
        for col in categorical_dictionary.keys():
            for col1 in categorical_dictionary[col]:
                cat_cols.append(col1)

        col_name = []
        col_vals = []
        for col in df1.index:
            if col not in cat_cols:
                for val in raw_data[col]:
                    col_name.append(col)
                    col_vals.append(val * df1.loc[col, 'coef'])
            else:
                cat_name = ''
                for x in categorical_dictionary.keys():
                    if col in categorical_dictionary[x]:
                        cat_name = x
                for val in raw_data[col]:
                    col_name.append(cat_name)
                    col_vals.append(val * df1.loc[col, 'coef'])

        df2 = pd.DataFrame({'name': col_name, 'val': col_vals})
        df2['name'] = pd.Categorical(df2['name'], list((df2.groupby('name')['val'].mean().sort_values()).index))
        return df2
    
    def effect_plot(self, raw_data, categorical_dictionary):
        df = self.effect_dataframe(raw_data, categorical_dictionary)
        with plt.style.context('fivethirtyeight'):
            fig = plt.figure(figsize = (12, 4))
            sns.boxplot(x = 'val', y = 'name', data = df)
            plt.xlabel('Feature Effect')
            plt.axvline(0, lw = 1, color = 'red', ls = '--')
        return fig
    
    def effect_plot_with_local_pred(self, raw_data, categorical_dictionary, local_pred, target_variable):
        my_df = self.effect_dataframe(raw_data, categorical_dictionary)
        df1 = pd.DataFrame(self.model.params, columns=['coef'])
        df1['indv_resp'] = pd.DataFrame(local_pred, index = [0]).T
        df1['indv_res'] = df1['coef'] * df1['indv_resp']
        pred = df1['indv_res'].sum() + df1.loc['Intercept', 'coef']

        my_dict = {}
        for col in my_df['name'].unique():
            if col in categorical_dictionary.keys():
                for cat_col in categorical_dictionary[col]:
                    if df1.loc[cat_col, 'indv_resp'] != 0:
                        my_dict[col] = df1.loc[cat_col, 'indv_res']
                        break
                    else:
                        my_dict[col] = 0
            else:
                my_dict[col] = df1.loc[col, 'indv_res']

        df_indv = pd.DataFrame(my_dict, index = [0]).T
        df_indv.columns = ['val']

        df_indv['order'] = 0
        for count, x in enumerate(pd.Categorical(my_df['name']).categories):
            df_indv.loc[x, 'order'] = count

        df_indv = df_indv.sort_values(by = 'order').copy()

        with plt.style.context('fivethirtyeight'):
            fig = plt.figure(figsize = (12, 4))
            sns.boxplot(x = 'val', y = 'name', data = my_df)
            plt.xlabel('Feature Effect')
            plt.axvline(0, lw = 1, color = 'red', ls = '--')
            plt.scatter(df_indv['val'], df_indv.index, marker = 'X', color = 'red', s = 125, zorder = 10)
            plt.title(f'Prediction: {np.round(pred, 0)} - Actual: {local_pred[target_variable]}')
            plt.ylabel('')
        return fig