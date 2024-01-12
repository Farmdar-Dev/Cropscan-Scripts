
# GeoProcessing Application
## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.x
- Compatible with both Windows and Unix-based systems

## Installation

Follow these steps to set up the GeoProcessing application:

### 1. Clone the Repository

### 2. Navigate to the Project Directory

```bash
cd geoprocessing
```

### 3. Virtual Environment Setup

It's recommended to use a virtual environment for Python projects. This isolates your project dependencies from other projects.

#### For Unix-based Systems:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### For Windows:

```bash
python -m venv venv
.env\Scriptsctivate
```

### 4. Install Dependencies

Install all required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the GeoProcessing application, use the following command:

```bash
python3 main.py
```

## Sample config.json

```bash
{
    "shp_name_s3": "s3://farmdar-classification/plant-health/test/ASML_PlantHealth.shp",
    "user_name": "ASML",
    "season": "2023",
    "crop": "Sugarcane",
    "report_type": "Plant Health",
    "unit": "acre",
    
    "date": "2023-11-11",
    "boundary_details": {
      "aoi": "s3://farmdar-classification/plant-health/test/asml_aoi.geojson",
      "tehsil": "s3://farmdar-classification/plant-health/test/asml_tehsil.geojson",
      "gates" : "s3://farmdar-classification/plant-health/test/asml_gates.geojson",
      "uc": "s3://farmdar-classification/plant-health/test/asml_uc.geojson"},
    "save_path": "C:/Users/Administrator/Desktop/ASML/New folder",
    "esurvey_path": ""
}
```

## .env
```bash

AWS_ACCESS_KEY_ID=asdf
AWS_SECRET_ACCESS_KEY=1234
bucket=buck

```



# Steps to run.
Make a file named config.json. 
Copy the contents above and fill it accordingly
python<version> main.py
The output folder will be created in given save paths
Upload that zipped folder on S3 with the model files

Extra note -For field level reports - the boundary detail title will be 
"aoi" only 



# Date format 
Date should be in YYYY-MM-DD format

## Report Type Names
1. Yield Estimation
2. Plant Health
3. Crop Scan
4. Sowing Date
5. Variety Scan
6. Plant Stress
7. Harvest Monitoring
8. VRA
9. SOM
10. Nitrogen Report
11. Water Stress

## Crop Names
1. Urban
2. Cotton
3. Maize
4. Others
5. Orchards
6. Juaar
7. Rice
8. Other Vegetation
9. Chillis
10. Musturd
11. Canola
12. Banana
13. Tobacco
14. Wheat
15. Tomato
16. Mountain
17. Sugarcane
18. Watermelon
19. Grapes
20. Potato

## Boundary Titles
1. aoi
2. district
3. tehsil
4. uc
5. gates
6. deh
7. zone
8. village
9. fields
10. Dekab Region
11. Dekab Territory