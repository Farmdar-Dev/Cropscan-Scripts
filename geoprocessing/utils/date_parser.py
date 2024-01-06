
import re
from datetime import datetime

def validate_date(date_string):
    """
    Validates if the given string is in the YYYY-MM-DD format and represents a valid date.

    Args:
    date_string (str): The date string to validate.

    Returns:
    bool: True if valid, False otherwise.
    """
    if not re.match(r'\d{4}-\d{2}-\d{2}', date_string):
        return False

    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    # Example usage
    example_date = "2024-13-06"
    is_valid = validate_date(example_date)
    print(f"Is '{example_date}' a valid date? {is_valid}")
