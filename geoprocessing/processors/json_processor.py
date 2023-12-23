import json
import geopandas as gpd


def read_config_json(file_path):
    """
    Read configuration parameters from a JSON file.
    Args:
    file_path: Path to the JSON configuration file.
    Returns:
    A dictionary containing configuration parameters.
    """
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

# # TODO: To be rewritten


def survey_json_creator(intersected_dataframes, config):
    """
    Creates a JSON object for survey data for the dashboard 
    Args:
        boundary_data: GeoJSON data of the boundary
        bound_df: Geodataframe of the boundary
        survey_title: Title of the survey
        date: Date of the survey
        report_type: Type of the report
        crop: Crop name
        crop_id_to_name_dic: Dictionary mapping crop id to crop name
    Returns:
        A JSON object
    """
    # user_name = config["user_name"]
    # season = config["season"]
    # crop = config["crop"]
    # date = config["date"]
    # report_type = config["report_type"]
    # # TODO : to be done
    # total_stats = config["total_stats"]
    # surveys = [
    #     {
    #         'user_name': user_name,
    #         'survey_season': season,
    #         'crop': crop,
    #         'total_stats': total_stats,
    #         'survey_array': []
    #     }
    # ]
    
    
    
    survey_array = []
    survey_obj_template = {
        'survey_title': '',
        'agg_stats': {
           "date" : {
                "report_type": {},
            }
        },
        'geometry': [
        
            
        ]
    }

    geometry_properties = {}
    report_properties = {}
    
    for df in intersected_dataframes:
            survey_title = df['survey_title'].iloc[0]
            df = df.drop(columns=['survey_title'])

            for index, row in df.iterrows():
                # Extract specific columns
                boundary_name = row['Boundary Name']
                boundary_id = row['id']
                esurvey_area = row['Esurvey Area']
                geometry_geojson = json.loads(gpd.GeoSeries(row['geometry']).to_json())
                
                # Print values separately
                print("Survey Title:", survey_title)
                print("Boundary Name:", boundary_name)
                print("ID:", boundary_id)
                print("Esurvey Area:", esurvey_area)
                
               
                other_properties = {
                    column: row[column] for column in df.columns if column not in ['Boundary Name', 'id', 'Esurvey Area', 'geometry']
                }
                print("Other Properties:", other_properties)

               
                print("Geometry GeoJSON:", geometry_geojson)
                
                
       
        
    


def json_validator(json_object):
    """
    Validates the JSON object
    Args:
        json_object: JSON object
    Returns:
        Boolean value
    """


if __name__ == "__main__":
    config = read_config_json("config.json")
    print(config)
