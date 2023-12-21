from constants.generic import AREA_CONVERSION_FACTORS

def calculate_area(df, area_unit):
    """
    Add a column of area in the specified unit to the dataframe.
    """
    area_unit = area_unit.upper()
    if area_unit in AREA_CONVERSION_FACTORS:
       return df.area / AREA_CONVERSION_FACTORS[area_unit]
    else:
        raise ValueError("Invalid area unit")