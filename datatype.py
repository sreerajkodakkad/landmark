import csv

def infer_data_types(csv_file_path):
    with open(csv_file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Read the header row
        data_types = {}

        # Initialize data type dictionary with empty strings
        for column_name in header:
            data_types[column_name] = ''

        # Read a few rows to infer data types
        for row in reader:
            for column_name, value in zip(header, row):
                # Try to convert value to int
                try:
                    int(value)
                    if data_types[column_name] != 'FLOAT':
                        data_types[column_name] = 'INT'
                except ValueError:
                    # Try to convert value to float
                    try:
                        float(value)
                        data_types[column_name] = 'FLOAT'
                    except ValueError:
                        # Otherwise, treat as string
                        data_types[column_name] = 'VARCHAR'
    return data_types

# Example usage
csv_file_path = r'C:\Users\sreeraj v s\Downloads\landmarktakehomeassignmentsad\export_2019.csv'
column_data_types = infer_data_types(csv_file_path)

# Print column names and corresponding data types
for column_name, data_type in column_data_types.items():
    print(f"{column_name}: {data_type}")
