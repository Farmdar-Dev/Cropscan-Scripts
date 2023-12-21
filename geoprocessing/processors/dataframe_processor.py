

def process_dataframe(dataframe):
    converted_dataframe = process_2d_dataframe (dataframe)
    return converted_dataframe

# TODO : Figure what the function is doing and rename it
def process_2d_dataframe(ans_dfs):
    """
    Takes in a 2d dataframe and returns a list of dataframes of the intersected files

    Args:
        dataframe (List): _description_
    """
    ans = [ans_dfs[0][j].copy() for j in range(len(ans_dfs[0]))]

    merge_columns = list(ans[0].columns)

    # Loop through each DataFrame in ans_dfs
    for i in range(1, len(ans_dfs)):  # Start from the second DataFrame (index 1)
        for j in range(len(ans_dfs[i])):
            # Extract the common columns between the current DataFrame and merge_columns
            common_columns = list(set(merge_columns) & set(ans_dfs[i][j].columns))

            # Merge the current DataFrame with ans[j] based on the dynamically determined common columns
            ans[j] = ans[j].merge(ans_dfs[i][j], on=common_columns, how='inner')
    
    
 
def remove_duplicate_columns(ans):
    """
    Takes in a dataframe and returns a dataframe with duplicate columns removed

    Args:
        dataframe (List): _description_
    """
    for i in range(len(ans)):

        # Get a list of columns to drop based on suffixes
        columns_to_drop = [col for col in ans[i].columns if col.endswith(('_y', '_z'))]

        # Drop the columns with the specified suffixes
        ans[i] = ans[i].drop(columns=columns_to_drop)
        
        # stripping all columns with name ending with _x

        cols = list(ans[i].columns)
        new_cols = []

        for j in ans[i].columns:
            j = j.strip('_x')
            new_cols.append(j)

        ans[i].columns = new_cols
            
            
            
        ans[i] = ans[i].loc[:, ~ans[i].columns.duplicated()]


if __name__ == "__main__":
    process_dataframe()