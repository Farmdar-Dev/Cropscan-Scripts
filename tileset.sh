#!/bin/bash
USERNAME="ali-akber-79"
SOURCE_ID=$1
FILE_PATH=$2

tilesets upload-source $USERNAME $SOURCE_ID $FILE_PATH

if [ $? -ne 0 ]; then
    echo "Source upload failed"
    exit 1
fi

RECIPE_FILE="recipe.json"
cat > $RECIPE_FILE << EOF
{
  "version": 1,
  "layers": {
    "${SOURCE_ID}": {
      "source": "mapbox://tileset-source/${USERNAME}/${SOURCE_ID}",
      "minzoom": 0,
      "maxzoom": 16
    }
  }
}
EOF

tilesets create $USERNAME.$SOURCE_ID --recipe $RECIPE_FILE --name "${SOURCE_ID}"

if [ $? -ne 0 ]; then
    echo "Tileset creation failed"
    rm $RECIPE_FILE
    exit 1
fi

tilesets publish $USERNAME.$SOURCE_ID

if [ $? -ne 0 ]; then
    echo "Tileset publish failed"
    rm $RECIPE_FILE
    exit 1
fi

echo "Tileset created and published successfully"
rm $RECIPE_FILE
