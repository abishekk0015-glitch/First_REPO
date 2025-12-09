import csv
import os

# --- Configuration ---
source_folder = '/Users/abisheka.vc/Downloads'
csv_filename = 'FIX1 - Sheet1.csv'
output_filename = 'update_fix1.sql'
# ---------------------

csv_file_path = os.path.join(source_folder, csv_filename)
output_file_path = os.path.join(source_folder, output_filename)

if not os.path.exists(csv_file_path):
    print(f"Error: Could not find file at {csv_file_path}")
    print("Please ensure 'FIX1 - Sheet1.csv' is in your Downloads folder.")
else:
    print(f"Reading {csv_filename}...")
    
    queries = []
    
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        # Clean up field names in case of extra spaces
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        
        row_count = 0
        
        for row in reader:
            # Get the values from the columns
            # Assuming headers are 'id' and 'vendor_pickup_location_id'
            # We use .get() to avoid errors if a cell is empty
            record_id = row.get('id')
            vendor_id = row.get('vendor_pickup_location_id')
            
            if record_id and vendor_id:
                # Construct the JSON string
                json_val = f'{{"vendorPickupLocationId":"{vendor_id}"}}'
                
                # Construct the query line
                # Template: update pickup_location set vendor_pickup_location_id = '...' , registration_status = 'REGISTERED' where id=...;
                query = f"update pickup_location set vendor_pickup_location_id = '{json_val}' , registration_status = 'REGISTERED' where id={record_id};"
                
                queries.append(query)
                row_count += 1

    print(f"Generated {row_count} queries.")

    # Save to file
    with open(output_file_path, 'w') as f:
        for query in queries:
            f.write(query + "\n")

    print("------------------------------------------------------")
    print(f"SUCCESS! SQL file saved to: {output_file_path}")
    print("------------------------------------------------------")
