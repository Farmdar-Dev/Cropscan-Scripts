# ReadMe

Mapbox.py is to be used to generate geojson reports 'L1 (Crop Scan), 'L3' (Variety Scan) or others that must be uploaded to MapBox. 


## Usage



For L1 (Crop Scan) :
```json
{
    "report_type" : "L1",
    "file_path" : "<path to shapefile>",
    "unit" : "acres"

  }

```
For L2 (Variety Scan) :
```json
{
    "report_type" : "L2",
    "file_path" : "<path to shapefile>",
    "unit" : "acres"

  }
```

For any other report mention the name of the report, for eg:
```json
{
    "report_type" : "Nitrogen Report",
    "file_path" : "<path to shapefile>",
    "unit" : "acres"

  }
```

For international reports consider using hectares:
```json
{
    "report_type" : "<Report Name>",
    "file_path" : "<path to shapefile>",
    "unit" : "hectares"

  }
```


