# B2B-Console-Data-Preparation

SOP L1

Inputs


The Script will take 2 files as input.

Model File 

This file will be in .shp format.
It will have one compulsory column of predicted  ( IT SHOULD BE  STRING) which will have the crop id or esurvey id  that is contained in Color Standardization Sheet.
Esurvey id is 100
To identify no of  growers passbook should be added. If the passbook is not available, donot add this column

Boundary file 
	
This file will be in .geojson format.
It must be of name as follow : 
aoi.geojson
district.geojson
tehsil.geojson
uc.geojson
gate_circles.geojson
deh.geojson
mouza.geojson
any other new area zone

It should  contain 2 column with name as Boundary Name and id starting with 1

FOR E SURVEY GEOJSON
1) Field ID (String / Text) 
2) Passbook No (String / Text)
3)  id (incremental)


The Survey Point File needs to be prepared and provide separately,
1) Geojson 2) id (incremental 3) Crop (text) (Sugarcane)


SOP L3

L-3 REQUIREMENTS FOR NAMRA


This file will be in .shp format.
It will have one compulsory column of predicted  ( IT SHOULD BE  STRING/text) 

GEOJSON
 for mapbox geojson L3 requirements columns: 
id (row number), 
Area Acres, 
Variety (includes names of variety), 
c_id (mention in the sheet of color standardization).c_id ki type INTEGER rakhna


b) Working

The script will ask 

How many model files? (n)
Enter path of model file no? (1 to n)
How many boundary files? (n)
Enter path of boundary files? (1 to n)
Enter column on which boundary needs to dissolved? (1 to n)
Enter user name? (jksm etc)
Enter survey season? (2022 or 2023 or 2018 etc)
Enter date? (2023-08-01 etc) 
