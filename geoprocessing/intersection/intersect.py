import geopandas as gdp
import pandas as pd

# Writing intersect_caller function
def intersect_caller(model_df, boundary_file_path):
    """
    function that takes a dataframe of a specific crop and a list of paths to boundary files
    and returns a list of dataframes of the intersected files
    """
    
    bound_dfs = []
    intersect_dfs = []

    for file in boundary_file_path:
        intersect_dfs.append(intersect(gdp.read_file(file),model_df,))
    # # adding id to boundary file
    # for i in range(len(bound_dfs)):
    #     bound_dfs[i]['id'] = bound_dfs[i].index + 1
    # for i in bound_dfs:
        

    return intersect_dfs


"""
Model Dataframe is the dataframe of a specific crop
"""
def intersect(bound_df,model_df,name, crop_id_to_name_dic):
    
    """Takes in boundary and model file and returns areawise stats

    Args:
        bound_df: Geodataframe of UC or District or Tehsil
        model_df: Geodataframe of maize or other or other vegetation
        area : string that tells if bound_df is UC or Tehsil or District
    Returns:
        intersection: Geodataframe that tells UC or District or Tehsilwise stats
        
    """
    
    # Removing passbook before intersecting
    
    if 'passbook' in model_df.columns:
        model_df = model_df.drop('passbook',axis = 1)
    
    
    # Changing Crs of both Boundary Data and Model Data
    orignal_crs = bound_df.crs
    
    estimated_utm_crs_bound = bound_df.estimate_utm_crs().to_string()
    estimated_utm_crs_model = model_df.estimate_utm_crs().to_string()
    
    bound_df = bound_df.to_crs(estimated_utm_crs_bound)
    model_df = model_df.to_crs(estimated_utm_crs_model)
    

    crop_name = crop_id_to_name_dic[model_df['crop id'][0]]
        
    # Boundary file and Model file(for a crop) intersection
    intersection = bound_df.overlay(model_df, how = "intersection")

    # Dissolving intersection polygons based on same UC
    intersection = intersection.dissolve(by = name)
    intersection = intersection.reset_index()
    
    # TODO: check by plotting before and after dissolving
    

    # Finding crop_area and crop_perc  
    intersection[crop_name + '_area'] = intersection.area / 4046.8564224 

    # dropping crop id
    
    intersection = intersection.drop(['crop id'], axis = 1)
    
    
    # to store geometry for later use
    tb_short = bound_df[[name,'geometry']]
    

    # To cater all those UC's with 0 Crops
    tb_UC = set(bound_df[name])
    intersection_UC = set(intersection[name])
    no_crop_UC = tb_UC.difference(intersection_UC)
    tb_no_crop = bound_df[bound_df[name].isin(no_crop_UC)]
    tb_no_crop[crop_name + '_area'] = 0
    intersection = pd.concat([intersection,tb_no_crop],axis = 0)
    
    # Changing datatype from float to int
 
    intersection[crop_name + '_area'] = intersection[crop_name + '_area'].astype(int)
    
    
    intersection = intersection.rename(columns = {'geometry' : 'Geo'})
    intersection = intersection.set_geometry('Geo')
    intersection = intersection.merge(tb_short, on= name, how='inner')
    intersection = intersection.set_geometry('geometry')
    intersection.drop(columns = ['Geo'],inplace = True)
    
    
    # Converting back to orignal Crs
    intersection = intersection.to_crs(orignal_crs)
    
    return intersection
