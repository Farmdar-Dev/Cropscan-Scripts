from constants.generic import AREA_CONVERSION_FACTORS
import math
def calculate_area(df, area_unit):
    """
    Calculates the area of a dataframe in the specified unit.
    """
    area_unit = area_unit.upper()
    if area_unit in AREA_CONVERSION_FACTORS:
       return (df.area / AREA_CONVERSION_FACTORS[area_unit]).round(2)
    else:
        raise ValueError("Invalid area unit")