#!/usr/bin/env python
# coding: utf-8

# In[70]:


#Importing Required librairies
import pandas as pd
import geopandas as gp
import json


# In[97]:


# Global Variables

global user_name
global season
global crop
global report_type
global dfs
dfs = []
global date
global no_boundaries
global survey_titles
global r_type
global save_path
global diss_column
global paths
global area
global output_path
global paths_boundaries


# In[72]:


# Writing 3 important functions

def area_acres(df_merged):
    
    """
    function that takes in a dataframe as input and adds column of area acre in it
    """
    
    df_merged['area acre'] =  (df_merged.area / 4046.8564224).round(2)
    
def area_hectares(df_merged):
    
    """
    function that takes in a dataframe as input and adds column of area hectare in it
    """
    
    df_merged['area hectare'] =  (df_merged.area / 10000).round(2)

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


# In[73]:


# Writing main intersect function

def intersect(bound_df,model_df,name):
    
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
        
    
    intersection = bound_df.overlay(model_df, how = "intersection")

    # Dissolving intersection polygons based on same UC
    intersection = intersection.dissolve(by = name)
    intersection = intersection.reset_index()
    

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


# In[74]:


# Writing the questions asking function

def questions():

    """
    Asking file no's that need to merged ans storing it in variable "files"
    
    """
    
    global user_name
    global season
    global crop
    global report_type
    global r_type
    
    
    print('Enter User Name?')
    user_name = input()
    
    print('Enter Season ?')
    season = input()
    
    print('Enter Crop Name ?')
    crop = input()
    
    print('Enter Report Type?')
    report_type = input()
    
    print('For L1 Enter "1", For any other Enter "2"')
    r_type = input()
    
    
    print('How Many Files to be Merged?')
    files = int(input())
    
    # Asking path of each file and storing in array "paths"

    for i in range(files):

        print('Enter Path of File No ', i + 1)
        path = input()    
        path = path.strip('"')
        paths.append(path)
        
          
    # Asking  Unit of Area and storing it in variable "area"
    print('Do you need Area in Hectares or Acres ? (Type H for Hectares or A for Acres)')
    area = input()


# In[75]:


# Writing report_tileset_Creation function

def report_tileset_creation():
   

    # Reading all dataframes from paths to array "dfs"

    for i in paths:
        dfs.append(gp.read_file(i))


    # combining all dataframes from array "dfs" to make one dataframe "df_merged"

    df_merged = pd.concat(dfs, ignore_index=True)

    # storing orignal crs of dataframe

    og_crs = df_merged.crs
    
    
    # Changing the crs of dataframe to estimate crs

    estimated_utm_crs = df_merged.estimate_utm_crs().to_string()

    df_merged = df_merged.to_crs(estimated_utm_crs)

    # changing datatype of column 'predicted' to integer

    df_merged['predicted'] = df_merged['predicted'].astype(int)

    # changing name of column 'predicted' to 'crop id'

    df_merged = df_merged.rename(columns = {'predicted': 'crop id'})
    

    # making variable called 'pred_arr' that stores all unique crop id in data

    pred_arr = df_merged['crop id'].unique()

    
    # Splitting merged_df to different dataframes that has seperate crops and storing them in array "dfs_out"

    dfs_out = []

    for i in pred_arr:
        dfs_out.append(df_merged[df_merged['crop id'] == i]) 
        
    # For each dataframe in dfs_out


    for i in range(len(dfs_out)):

        # Adding area column

        if area == 'A':
            area_acres(dfs_out[i])
        elif area == 'H':
            area_hectares(dfs_out[i])

        # Changing crs back to orignal crs    

        dfs_out[i] = dfs_out[i].to_crs(og_crs)
        
        # reseting index of all dataframes

        dfs_out[i] = dfs_out[i].reset_index(drop=True)
        
    return dfs_out


# In[76]:


# Writing the bound_questions function

def bound_questions():
    
    """
    Function that asks boundary questions
    """
    
    
    global date
    global no_boundaries
    global survey_titles
    
    survey_titles = []
    
    
    
    # Asking Number of Boundary Files and storing them in variable "no_boundaries"

    print('Enter Number Of Boundary Files')
    no_boundaries = int(input())
    
    print('Enter Date for this boundary')
    date = input()
    

    # Asking path of each boundary file and storing in array "paths_boundaries"

    for i in range(no_boundaries):
        print('Enter Path of Boundary File No ', i + 1)
        path = input()    
        path = path.strip('"')
        paths_boundaries.append(path)
        
        
        print('Enter Survey Title Of This Boundary')
        survey_titles.append(input()) 
        
        


# In[77]:


# Writing intersect_caller function

def intersect_caller(model_df):
    
    """
    function that takes in 1 model dataframe and intersects with all boundary dataframes also adds id to boundary
    """
    
    bound_dfs = []
    intersect_dfs = []

    for i in paths_boundaries:
        bound_dfs.append(gp.read_file(i))
    
    # adding id to boundary file
    for i in range(len(bound_dfs)):
        bound_dfs[i]['id'] = bound_dfs[i].index + 1
    
    
    area = ''
    dissolve = []
    
    for i in bound_dfs:
        
        intersect_dfs.append(intersect(i,model_df,'Boundary Name'))

    return intersect_dfs


# In[78]:


# Calling report tileset creation

save_path = 'C:/Users/FARMDAR/Desktop/Abbas/Output/json/'

diss_column = []
paths = []
area = ''
output_path = ''

no_boundaries = 0
paths_boundaries = []


crop_id_to_name_dic = crop_dic_creator()


# -- converted -- 
questions()
bound_questions()


# In[79]:


dfs_out = report_tileset_creation()


# In[80]:


# Checking the dataframes

crop_id_to_name_dic


# In[81]:


# Data frame for each crop 
# sugarcane , maize  -- dataframe 

# L3 -> CP-77400 , CP-72-2086 , CP-43-33 , CP-43-33
# Stress - > Low , Medium , High

ans_dfs = []


# Iterate over each DataFrame in dfs_out and apply intersect_caller
for df in dfs_out:
    ans_dfs.append(intersect_caller(df))


# In[82]:


# Joining Dataframes


"""
ans_dfs is 2d array
with 1st index as crop id
2nd Index as boundary
ans is 1d array of dataframes
(obtained after joining dataframes in ans_dfs of same boundary)
"""

# Initialize the ans list with copies of the first DataFrame in ans_dfs
ans = [ans_dfs[0][j].copy() for j in range(len(ans_dfs[0]))]

# Extract the columns from the first DataFrame as potential merge columns
merge_columns = list(ans[0].columns)

# Loop through each DataFrame in ans_dfs
for i in range(1, len(ans_dfs)):  # Start from the second DataFrame (index 1)
    for j in range(len(ans_dfs[i])):
        # Extract the common columns between the current DataFrame and merge_columns
        common_columns = list(set(merge_columns) & set(ans_dfs[i][j].columns))
        


        # Merge the current DataFrame with ans[j] based on the dynamically determined common columns
        ans[j] = ans[j].merge(ans_dfs[i][j], on=common_columns, how='inner')

# ans now contains the merged DataFrames with dynamically determined merge columns


# Removing Duplicated Columns
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
    
    


# In[83]:


ans[0].head()


# In[98]:


# Making total_stats dictonary

total_stats = {}

# Finding Total Area
Total_Area = 0


#will not work when no aoi
for df in ans:
    
    if len(df) == 1 : 
        
        estimated_utm_crs = df.estimate_utm_crs().to_string()
        df = df.to_crs(estimated_utm_crs)
        Total_Area = int((df.area / 4046.8564224).sum())


total_stats['Total Area'] = str(Total_Area)
    
# Finding Total Growers
growers = 0 

for df in dfs:
    if 'passbook' in df.columns:
        growers = str(df['passbook'].nunique())

total_stats['Total Growers'] = str(growers)


#Finding Total Esurvey

esurvey = 0

if 'esurvey_area' not in list(ans[0].columns):
    esurvey = 'N/A'
else:
    for df in dfs:
        if df['predicted'].iloc[0] == '100' or df['predicted'].iloc[0] == 100 :
            estimated_utm_crs = df.estimate_utm_crs().to_string()
            df = df.to_crs(estimated_utm_crs)
            esurvey = ((df.area / 4046.8564224).round(2)).sum().round(2)
            
total_stats['Total Esurvey'] = str(esurvey)

# Finding Total Crop Area
total_crop_area = 0

if r_type == '1':
    #For L1
    
    array = [str(num) for num in range(30) if num != 1]


    for df in dfs:

        if df['predicted'].nunique() > 1:

            print(df['predicted'].unique())

            df = df[~df['predicted'].isin(array)]


            print(df['predicted'].unique())

            estimated_utm_crs = df.estimate_utm_crs().to_string()
            df = df.to_crs(estimated_utm_crs)
            total_crop_area += int((df.area / 4046.8564224).round(2).sum().round(2))
        

elif r_type == '2':        
# for stress,health and all others

    for df in ans:
        if len(df) == 1 :
            for i in df.columns:
                if i.endswith('_area'):
                    total_crop_area += df[i].sum()     
        


total_stats['Total Crop Area'] = str(total_crop_area)
                
total_stats   


# In[85]:


ans[0]['Boundary Name'].dtype


# In[86]:


list(ans[0].columns)


# In[87]:


bound_json = []

for i in ans:
    bound_json.append(json.loads(i.to_json()))


# In[88]:


# Saving all dataframes as json geojson
for i in range(len(ans)):
    ans[i].to_file(save_path + survey_titles[i] +' '+user_name+ ' '+ report_type+ ' '+  date +  '.geojson', driver='GeoJSON')


# In[89]:


ans[0]


# In[90]:


def json_creator(boundary_data,bound_df,survey_title,date):

    date_key = date
    crop_scan_report_type = report_type


    desired_json_object = {
        'survey_title': survey_title,
        'agg_stats': {
            date_key: {
                crop_scan_report_type: {},
            }
        },
        'geometry': []
    }

    
    bound_cols = list(bound_df.columns)
    bound_cols.remove('geometry')

    crop_scan_entry = {}
    prop_dic = {}


    # Iterate through features and add entries to the 'agg_stats' dictionary
    
    for feature in boundary_data['features']:
        
        crop_scan_entry = {}  # Create a new dictionary for each feature
        prop_dic = {}
        
        for i in bound_cols:
            if i != 'esurvey_area':
                if i.replace("_area", "") in crop_id_to_name_dic.values():
                    crop_scan_entry[i.replace("_area", "").title()] = feature['properties'][i]
                else:
                    
                    j = i.replace("_area", "").title()
                    
                    if j == 'Id':
                        j = 'id'
                    
                    prop_dic[j] = feature['properties'][i] 
            else:
                
                j = i.replace("_area", "").title()
                    
                if j == 'Id':
                    j = 'id'
                prop_dic[j] = feature['properties'][i]

        # Extract geometry information
        
        geometry = {
            'type': bound_df['geometry'].geom_type[0],
            'coordinates': feature['geometry']['coordinates']
        }
        
        
        
        
        
        desired_json_object['agg_stats'][date_key][crop_scan_report_type][prop_dic['id']] = crop_scan_entry

        if report_type == 'Crop Scan':
            prop_dic['Crop Area'] = crop_scan_entry[crop]
        else:
            c_area = 0
            
            for i in crop_scan_entry.values():
                c_area += i
            
            prop_dic['Crop Area'] = c_area
            
              
        
        if 'Esurvey' not in prop_dic.keys():
             prop_dic['Esurvey'] = '-'    
        
        prop_dic['Esurvey Area'] = prop_dic['Esurvey']
        del prop_dic['Esurvey']

        # Add the geometry information directly to the JSON object
        desired_json_object['geometry'].append({
            'type': 'FeatureCollection',
             'properties' : prop_dic,
             'geometry': geometry
        })


    # Convert the JSON object to a JSON string
    desired_json_string = json.dumps(desired_json_object, indent=2)

    # Print the desired JSON string
    print(desired_json_string)
    

    return desired_json_object




# In[91]:


json_obj = []

for i in range(len(ans)):
    json_obj.append(json_creator(bound_json[i] , ans[i] , survey_titles[i],date))

    

json_obj[0]


# In[92]:


json_obj


# In[93]:


# Final Json


# Structure
surveys = [
    {
        'user_name': user_name,
        'survey_season': season,
        'crop' : crop,
        'total_stats' : total_stats,
        'survey_array': []
    }
]


for i in json_obj:
    surveys[0]['survey_array'].append(i)


# In[94]:


# Save surveys as a JSON object
with open(save_path + user_name + ' ' + report_type + ' ' + date +  '.json', 'w') as json_file:
    json.dump(surveys, json_file, indent=2)

print("your json file has been created.")

