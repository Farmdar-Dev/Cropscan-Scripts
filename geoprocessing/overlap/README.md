## Running the Application

To run the overlap script, use the following command:

```bash
python<version> overlap.py
```

## Sample config.json

```bash
{
    "boundaries" : {
        "aoi": "C:/Users/hiban/Downloads/Corteva_Overlaps/boundaries/corteva_2024_aoi.geojson",
        "province": "C:/Users/hiban/Downloads/Corteva_Overlaps/boundaries/corteva_2024_province.geojson",
        "tehsil": "C:/Users/hiban/Downloads/Corteva_Overlaps/boundaries/corteva_2024_tehsil.geojson",
        "district": "C:/Users/hiban/Downloads/Corteva_Overlaps/boundaries/corteva_2024_district.geojson",
        "uc": "C:/Users/hiban/Downloads/Corteva_Overlaps/boundaries/corteva_2024_uc.geojson"
    },

    "shapefiles" : {
        "rice": "C:/Users/hiban/Downloads/rice_corteva/rice_corteva_punjab_sindh_2023.shp",
        "wheat": "C:/Users/hiban/Downloads/wheat_corteva/wheat_corteva_punjab_sindh_2023.shp"
    },
    "output_path" : "C:/Users/hiban/Downloads/results",
    "unit" : "acre",
    "overlap": "Spring Maize and Fall Maize"
  }
```

## Steps to run.
Make a file named config.json and place it in the directory as this README.md file.
Copy the contents above and replace values respectively.
For 'overlap' strictly follow the naming reference  provided below. Custom naming is not acceptable (literally).
The output folder will be created in given "output_path".

## Overlap Types.
1. Spring Maize and Wheat
2. Rice and Wheat
3. Rice and Potato
4. Spring Maize and Rice
5. Spring Maize and Potato
5. Spring Maize and Emptyland
7. Spring Maize and Fall Maize