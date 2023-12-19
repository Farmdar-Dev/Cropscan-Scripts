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



# Checking the dataframes

crop_id_to_name_dic


# In[81]:




# In[82]:


# Joining Dataframes

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

