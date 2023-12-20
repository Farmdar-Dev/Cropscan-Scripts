import geopandas as gdp
import pandas as pd
from constants.generic import Column_to_dissolve 

def crop_dic_creator():
    
    """
    function that creates a dictonary with 'Crop ID' as keys and 'Crop Name' as values
    """

     # l1 crop names and id
    
    l1_names = ['urban','sugarcane','cotton','maize','others','orchards','juaar','rice','other vegetation','chilli','mustard','canola','banana','tobacco','wheat','tomato','mountain']
    l1_id =    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    
    # l3 crop names and id
    
    l3_names = ["Other Variety", "CoL-29", "CoL-44", "CoL-54", "BL-19", "BL-4", "L-116", "L-118", "Triton", "BF-162", "CP43-33", "CP72-2086", "CP-77400", "CoJ-84", "SPF-213", "CPF-237", "HSF-240", "SPF-234", "SPF-245", "HSF-242", "CPF-243", "CPF-246", "CPF-247", "CPF-248", "CPF-249", "CPF-250", "CPF-251", "CPF-252", "CPF-253", "NSG-59", "SP-93", "US-133", "US-252", "US-633", "CPF-238", "YT-55", "CPF-213", "US-127", "CO-1148", "SPF-239", "SPF-238", "CPF-254", "CO-84", "PONDA", "FD-19", "SP-30","AUS-133","CP-90",'US-54','CPF-239']
    l3_id =    [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046,1047,1048,1049]

    
    # Combining l1 and l3
    
    crops = l1_names + l3_names
    cid = l1_id + l3_id
    
    
    # Making Dictonary
    crop_types_dic = dict(zip(cid,crops))

    
    crop_types_dic[100] = 'esurvey'
    
    # Stress 
    crop_types_dic[77] = 'Stress'
    crop_types_dic[78] = 'Potential Stress'
    crop_types_dic[79] = 'No Stress'
    crop_types_dic[80] = 'High Vigour'
    
    
    
    # Health
    
    crop_types_dic[73] = 'Low Vegetation'
    crop_types_dic[74] = 'Moderate'
    crop_types_dic[75] = 'Good'
    crop_types_dic[76] = 'Excellent'
    
    
    # VRA
    
    crop_types_dic[83] = 'Low Zone'
    crop_types_dic[84] = 'Medium Zone'
    crop_types_dic[85] = 'High Zone'
    
    
    # SOM
    
    crop_types_dic[96] = 'High'
    crop_types_dic[97] = 'Medium'
    crop_types_dic[98] = 'Low'
    
    
    # Harvest Monitering
    
    crop_types_dic[81] = 'Remaining Sugarcane'
    crop_types_dic[82] = 'Harvested'
    
    # Silage or Grain
    
    crop_types_dic[101] = 'Grain'
    crop_types_dic[102] = 'Silage'
    
    # Sowing
    
    crop_types_dic[61] = 'January'
    crop_types_dic[62] = 'February'
    crop_types_dic[63] = 'March'
    crop_types_dic[64] = 'April'
    
    crop_types_dic[65] = 'May'
    crop_types_dic[66] = 'June'
    crop_types_dic[67] = 'July'
    crop_types_dic[68] = 'August'
    
    crop_types_dic[69] = 'September'
    crop_types_dic[70] = 'October'
    crop_types_dic[71] = 'November'
    crop_types_dic[72] = 'December'
    
    
    # Nitorgen Report 
    
    crop_types_dic[103] = 'Low'
    crop_types_dic[104] = 'Medium'
    crop_types_dic[105] = 'High'
    
    # More Crops
    
    crop_types_dic[20] = 'greenhouse'
    crop_types_dic[23] = 'watermelon'
    
    
    
            
    return crop_types_dic





# Writing intersect_caller function
def intersect_caller(model_df, boundary_file_path):
    """
    function that takes a dataframe of a specific crop and a list of paths to boundary files
    and returns a list of dataframes of the intersected files
    """
    
    bound_dfs = []
    intersect_dfs = []

    for file in boundary_file_path:
        bound_dfs.append(gdp.read_file(file))
    # # adding id to boundary file
    # for i in range(len(bound_dfs)):
    #     bound_dfs[i]['id'] = bound_dfs[i].index + 1
    
    for i in bound_dfs:
        intersect_dfs.append(intersect(i,model_df, name = Column_to_dissolve, crop_id_to_name_dic = crop_dic_creator()))
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
