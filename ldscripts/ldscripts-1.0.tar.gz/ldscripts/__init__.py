def csv(df, name = 'df'):
        """ Saves csv to Temp folder (created temp folder if not found)
        Arguments:
            df {[df]} -- Dataframe to save

        Keyword Arguments:
            name {string} -- Optional name for the saved csv (default: {df})
        """
        import subprocess
        import os
        from datetime import datetime
        import inspect
        current_dir = os.getcwd()
        temp_dir = os.path.join(current_dir, 'Temp')
        #Create temp folder if it exists
        if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)
        file_name = name + '_'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.csv'
        save_location = os.path.join(temp_dir, file_name)
        df.to_csv(save_location, index=False)
        print("Saved to:")
        print(save_location)
        os.startfile(save_location)



def merge_overlaps_new(left_df, right_df, on=None, left_on=None, right_on=None, lower=None, upper= None, left_lower=None, left_upper=None, right_lower=None, right_upper=None, how='inner', include_bounds = True):
        import pandas as pd
        import numpy as np
        """
        Arguments:
            left_df {[df]} -- Left dataframe
            right_df {[df]} -- Right dataframe

        Keyword Arguments:
            on {string or list} -- Join on common columns (default: {None})
            left_on {string or list} -- Left join columns (default: {None})
            right_on {string or list} -- Right join columns (default: {None})
            lower {string or list} -- Lower range bounds  (default: {None})
            upper {string or list} -- Upper range bounds (default: {None})
            left_lower {string or list} -- Left df lower range bounds (default: {None})
            left_upper {string or list} -- Left df upper range bounds (default: {None})
            right_lower {string or list} -- Right df lower range bounds (default: {None})
            right_upper {string or list} --Right df upper range bounds (default: {None})
            how {str} -- merge type ('inner' or 'left') (default: {'inner'})
            include_bounds {bool} -- Include the bounds in the range (default: {True})
        """
        #If cols are specified as same for both dataframes, set the left/right parameters
        if on is not None:
                left_on = on
                right_on = on
        if lower is not None:
                left_lower = lower
                right_lower = lower
                left_upper= upper
                right_upper = upper

        #Convert values to lists if they are entered as strings
        if type(left_on) != list:
                left_on = [left_on]
                right_on = [right_on]
        if type(left_lower) != list:
                left_lower = [left_lower]
                left_upper = [left_upper]
                right_lower = [right_lower]
                right_upper = [right_upper]

        #Collect the common output columns after converting to lists
        common_output_cols = []
        if on is not None:
                common_output_cols.extend(left_on)
        if lower is not None:
                common_output_cols.extend(left_lower)
                common_output_cols.extend(left_upper)

        #Loop through the range paramaters and build the conditions array
        conditions = True #Initalise conditions
        for idx, val in enumerate(left_lower):
                left_lower_vals = left_df[left_lower[idx]].values
                left_upper_vals = left_df[left_upper[idx]].values
                right_lower_vals = right_df[right_lower[idx]].values
                right_upper_vals = right_df[right_upper[idx]].values
                if include_bounds:
                        conditions = conditions & (left_lower_vals[:, None] <= right_upper_vals) & (left_upper_vals[:, None] >= right_lower_vals)
                else:
                      conditions = conditions & (left_lower_vals[:, None] < right_upper_vals) & (left_upper_vals[:, None] > right_lower_vals)

        #Loop through the id paramaters and build the conditions array
        for idx, val in enumerate(left_on):
                left_id_vals = left_df[left_on[idx]].values
                right_id_vals = right_df[right_on[idx]].values
                conditions = conditions & (left_id_vals[:, None] == right_id_vals)

        #Find where conditions are met
        i, j = np.where(conditions)

        #Check column names are unique- append x to left duplciated cols, y to right duplciated cols
        #Keep common columns if they are in the join/range entries
        duplicated_columns = left_df.columns.intersection(right_df.columns)
        duplicated_columns = duplicated_columns[~duplicated_columns.isin(common_output_cols)].tolist()
        left_cols = [col+'_x' if col in duplicated_columns else col for col in left_df.columns.tolist()]
        right_cols = [col+'_y' if col in duplicated_columns else col for col in right_df.columns.tolist()]
        cols = left_cols+right_cols
        #Create merged dataframe
        df_merged = pd.DataFrame(np.column_stack([left_df.values[i], right_df.values[j]]),
        columns=cols)

        #Reassign the dtypes (otherwise will always be objects)
        dtype = pd.concat([left_df.dtypes, right_df.dtypes])
        for k, v in dtype.items():
                df_merged[k] = df_merged[k].astype(v)

        #Drop the duplicated columns
        df_merged = df_merged.loc[:,~df_merged.columns.duplicated()]

        #If the merge is left, add the missing data
        if how == 'left':
                non_matching_df = left_df[~np.in1d(np.arange(len(left_df)), np.unique(i))]
                non_matching_df.columns = right_cols
                #Reassign the dtypes before appending
                dtype = left_df.dtypes
                for k, v in dtype.items():
                        non_matching_df[k] = non_matching_df[k].astype(v)
                df_merged = df_merged.append(non_matching_df, ignore_index=True, sort=False)

        return df_merged
