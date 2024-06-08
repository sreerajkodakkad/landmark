import csv
import psycopg2

# Database connection parameters
conn = psycopg2.connect(
    dbname='sales_db',
    user='postgres',
    password='mangotree',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

# Path to your CSV file
csv_file_path = r'C:\Users\sreeraj v s\Downloads\landmarktakehomeassignmentsad\export_2019.csv'

try:
    with open(csv_file_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Skip the header row
        for line_number, row in enumerate(reader, start=2):  # Start at 2 to account for header
            try:
                # Replace 'null' with None for SQL NULL
                row = [None if val.lower() == 'null' else val for val in row]

                # Remove commas from numeric fields
                row = [val.replace(',', '') if val and val.replace(',', '').replace('.', '').isdigit() else val for val in row]

                # Construct the INSERT query
                query = """
                INSERT INTO csvdb (
                    "Invoice/Item Number", "Date", "Store Number", store_name, "Address", "City", 
                    "Zip Code", "Store Location", "County Number", "County", "Category", category_name, 
                    "Vendor Number", vendor_name, "Item Number", item_desc, "Pack", "Bottle Volume (ml)", 
                    "State Bottle Cost", "State Bottle Retail", "Bottles Sold", "Sale (Dollars)", 
                    "Volume Sold (Liters)", "Volume Sold (Gallons)"
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(query, row)
            except Exception as e:
                print(f"Error occurred at line {line_number}: {e}")
                print("Problematic line:", row)
                continue  # Continue with the next line
        conn.commit()
    print("CSV data successfully imported into PostgreSQL table.")
except Exception as e:
    print("An unexpected error occurred:", e)
finally:
    # Close the cursor and connection
    cur.close()
    conn.close()
