import json
import geopandas as gpd
import os
from utils.area_calculation import calculate_area
<<<<<<< HEAD
from processors.dataframe_processor import reproject_df_crs
=======
>>>>>>> main


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
    survey_array = []
    geometry_obj_template = {
        "type": "FeatureCollection",
        "properties": {},

    }

    total_aoi_stats = {}
    total_area = ""
    total_esurvey = ""
    for df in intersected_dataframes:
        survey_title = df['survey_title'].iloc[0]
        df = df.drop(columns=['survey_title'])

        # make a copy of survey obj template
        survey_obj = survey_obj_template_creator(
            survey_title, config["date"], config["report_type"])
        geometry_objects = []
        report_properties = {}

        for index, row in df.iterrows():
            # Extract specific columns
            boundary_name = row['Boundary Name']
            boundary_id = row['id']
            esurvey_area = row['Esurvey Area']

            geometry_geojson = json.loads(
                gpd.GeoSeries(row['geometry']).to_json())
            geometry_geojson = clean_geometry(geometry_geojson)
            rep_properties = {
                column: row[column] for column in df.columns if column not in ['Boundary Name', 'id', 'Esurvey Area', 'geometry']
            }

            Crop_Area = get_main_crop_area(rep_properties, config["crop"], config["report_type"])
            Crop_Area = round(Crop_Area, 2)
            report_properties[boundary_id] = rep_properties

            geo_obj = geometry_obj_template.copy()
            geo_obj['properties'] = {
                "id": boundary_id,
                "Boundary Name": boundary_name,
                "Crop Area": Crop_Area,
                "Esurvey Area": esurvey_area
            }
            geo_obj['geometry'] = geometry_geojson
            geometry_objects.append(geo_obj)

            if survey_title == "aoi":
                total_crop_area = get_main_crop_area(rep_properties, config["crop"], config["report_type"])
<<<<<<< HEAD
                total_area_, total_esurvey_ = get_total_aoi_stats(df, intersected_dataframes[index])
=======
                total_area_, total_esurvey_ = get_total_aoi_stats( df, intersected_dataframes[index])
>>>>>>> main
                total_area = total_area_
                total_esurvey = total_esurvey_
                
        survey_obj['geometry'] = geometry_objects
        survey_obj['agg_stats'][config["date"]
                                ][config["report_type"]] = report_properties
        survey_array.append(survey_obj)


    total_growers = get_esurvey_stats(config["esurvey_path"])

    total_stats = {
        "Total Growers": total_growers,
        "Total Area": total_area,
        "Total Esurvey": total_esurvey,
        "Total Crop Area": total_crop_area
    }

    survey_json = {
        "user_name": config["user_name"],
        "survey_season": config["season"],
        "crop": config["crop"],
        "total_stats": total_stats,
        "survey_array": survey_array
    }
    # save the json file
    save_path = config["save_path"] + "Json/"
    file_name = "survey.json"

    # Check if the directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Now, save the file in the directory
    full_path = os.path.join(save_path, file_name)
    with open(full_path, 'w') as outfile:
        json.dump(survey_json, outfile)


def get_total_aoi_stats(df, aoi_df):
<<<<<<< HEAD
    reproject_df_crs(aoi_df)
    aoi_df['area'] = calculate_area(aoi_df, 'acre')
    total_area = aoi_df['area'].sum().round(2)
=======
    aoi_df = aoi_df.drop(columns=[col for col in ['id', 'Boundary Name', 'geometry', 'Esurvey Area', 'survey_title'] if col in aoi_df.columns])
    total_area = aoi_df.sum().sum().round(2)
>>>>>>> main
    total_esurvey_area = df['Esurvey Area'].iloc[0] if 'Esurvey Area' in df.columns else 0
    return total_area, total_esurvey_area



def get_main_crop_area(report_properties, crop, report_type):
    """
    Returns the area of the main crop
    Args:
        report_properties: Dictionary containing the report properties
        crop: Crop name
    Returns:
        Area of the main crop
    """
    if report_type != "Crop Scan":
        total_crop_area = 0
        for key in report_properties:
           total_crop_area += report_properties[key]
        return total_crop_area
    
    
    return report_properties[crop]


def get_esurvey_stats(esurvey_path):
    """
    Returns the total number of growers in the esurvey
    Args:
        esurvey_path: Path to the esurvey file
    Returns:
        Total number of growers
    """
    if esurvey_path == "":
        return "N/A"

    esurvey_df = gpd.read_file(esurvey_path)
    # get passbook number column and unique values
    # TODO: add check if no passbook number column found
    if esurvey_df.get('Passbook No') is not None:
        passbook_number = esurvey_df['Passbook No']
        return str(len(passbook_number.unique()))

    return "N/A"


def clean_geometry(geometry_obj):
    """
    Cleans the geometry object
    Args:
        geometry_obj: Geometry object
    Returns:
        Cleaned geometry object
    """
    clean_geometry_obj = {}
    clean_geometry_obj = geometry_obj['features'][0]['geometry']
    return clean_geometry_obj


def survey_obj_template_creator(survey_title, date, report_type):

    return {
        "survey_title": survey_title,
        "agg_stats": {
            date: {
                report_type: {

                }
            }
        }
    }
    pass


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
