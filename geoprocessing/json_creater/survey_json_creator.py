
import json



def json_creator(boundary_data,bound_df,survey_title,date,
                 report_type,crop,crop_id_to_name_dic):

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

