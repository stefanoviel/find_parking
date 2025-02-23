import csv
import json

def convert_csv_to_json():
    parking_slots = []
    
    with open('frontend/data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            # Only process first 100 rows
            # if i >= 1000:
            #     break
                
            # Skip empty rows
            if not row['parkdauer']:
                continue

            print(row)
                
            # Extract coordinates from the POINT string
            # Format is "POINT (x y)"
            coords = row['geometry'].replace('POINT (', '').replace(')', '').split()
            x = float(coords[0])
            y = float(coords[1])
            
            parking_slot = {
                'id': row['\ufeff"id1"'].strip('"'),  # Handle quotes
                'x': x,
                'y': y,
                'duration': int(row['parkdauer']),  # parking duration in minutes
                'type': row['art'],                 # parking type
                'paid': row['gebuehrenpflichtig'] == 'gebührenpflichtig'  # whether parking is paid
            }
            parking_slots.append(parking_slot)
    
    # Write to JSON file
    with open('frontend/parkings.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(parking_slots, jsonfile, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    convert_csv_to_json()