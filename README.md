
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
  "user_name": "Omni",
  "season": "2023",
  "crop": "Sugarcane",
  "report_type": "SOM",
  "unit": "acre",
  "shapefile_paths": [
    "/Users/mac/Desktop/Farmdar/Cropscan-Scripts/test_data/Omni/Omni_OM_aoi_level/Omni_OM_aoi_level.shp"
  ],
  "date": "2023-08-21",
  "boundary_details": {
    "aoi": "/Users/mac/Desktop/Farmdar/Cropscan-Scripts/test_data/Omni/omni_aoi_slack.geojson",
    "gates" : "Path to gates file"
  },
  "save_path": "/Users/mac/Desktop/Farmdar/Cropscan-Scripts/geoprocessing",
  "esurvey_path": ""
}
```
