import json
import math
import geopandas as gpd
import os
from utils.area_calculation import calculate_area
from processors.dataframe_processor import reproject_df_crs


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

def validate_config(config):
    """
    Validate the configuration parameters.
    Args:
    config: A dictionary containing configuration parameters.
    Returns:
    A boolean value.
    """
    pass

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

    total_area = ""
    total_esurvey = ""
    total_crop_area = ""
    for df in intersected_dataframes:
        survey_title = df['survey_title'].iloc[0]
        df = df.drop(columns=['survey_title'])

        # make a copy of survey obj template
        survey_obj = survey_obj_template_creator(
            survey_title, config["date"], config["report_type"])
        geometry_objects = []
        report_properties = {}

        # TODO : refactor this function which has turned into a spaghetti
        if survey_title == "aoi":
            # we need to extract total crop area from the df
            # generate new df with only crop area columns
            col_to_keep = [col for col in df.columns if col not in [
                'Boundary Name', 'id', 'Esurvey Area', 'geometry', 'area']]
            crop_df = df[col_to_keep]
            total_area_, total_esurvey_, total_crop_area_ = get_total_aoi_stats(
                df, crop_df, config["crop"], config["unit"])
            total_area = total_area_
            total_esurvey = total_esurvey_
            total_crop_area = total_crop_area_

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
           # replace NaN values with 0 
            rep_properties = {k: 0 if math.isnan(
                v) else v for k, v in rep_properties.items()}

            Crop_Area = get_main_crop_area(
                rep_properties, config["crop"], config["report_type"])
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
    save_path = config["save_path"] + "/Json/"
    file_name = "survey.json"

    # Check if the directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Now, save the file in the directory
    full_path = os.path.join(save_path, file_name)
    with open(full_path, 'w') as outfile:
        json.dump(survey_json, outfile)


def get_total_aoi_stats(aoi_df, crop_df, crop_name, unit):
    #make a copy of aoi_df 
    aoi_df_cpy = aoi_df.copy()
    reproject_df_crs(aoi_df_cpy)
    aoi_df_cpy['area'] = calculate_area(aoi_df_cpy, unit)
    total_area = aoi_df_cpy['area'].sum().round(2)
    # drop the area column
    aoi_df_cpy.drop(columns=['area'], inplace=True)

    total_esurvey_area = 0
    if not aoi_df_cpy['Esurvey Area'].eq('-').any():
        total_esurvey_area = aoi_df_cpy['Esurvey Area'].sum().round(2)
        
    total_crop_area = 0
    if crop_name in crop_df.columns:
        total_crop_area = round(crop_df[crop_name].sum(), 2)
        return total_area, total_esurvey_area, total_crop_area

    total_crop_area = round(crop_df.sum().sum(), 2)
    return total_area, total_esurvey_area, total_crop_area


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
        total_crop_area = round(total_crop_area, 2)
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
