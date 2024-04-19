import pandas as pd

def csv_to_dict(csv_filepath):
    """Reads a CSV file using pandas and returns a Dictionary.

    Args:
        csv_filepath (str): The path to the CSV file.

    Returns:
        python.Dictioanry: The Dictioanry containing the CSV data.
    """
    df =pd.read_csv(csv_filepath)
    # Prepare data for JSON serialization
    data = df.to_dict(orient='records')
    return data



