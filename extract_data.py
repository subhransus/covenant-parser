import re
import pandas as pd
from datetime import datetime
import argparse

# Function to read data from a text file
def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to extract data using patterns
def extract_data(data):
    patterns = {
        'Buy/Sell': r'Buy/Sell\s*[:：]\s*(Buy|Sell)',
        'Product Name': r'(?:Product|Product Name)\s*[:：]\s*(.*?)(?:\n|$)',
        'CAS No.': r'(\d{2,7}-\d{2,7}-\d)',
        'Quantity': r'Quantity\s*[:：]\s*(.*?)(?:\n|$)',
        'Market': r'Market\s*[:：]\s*(.*?)(?:\n|$)',
        'Delivery': r'Delivery\s*[:：]\s*(.*?)(?:\n|$)',
        'Company': r'Company\s*[:：]\s*(.*?)(?:\n|$)',
        'Name': r'(?<!Product\s)Name\s*[:：]\s*(.*?)(?:\n|$)',
        'Designation': r'Designation\s*[:：]\s*(.*?)(?:\n|$)',
        'Contact No.': r'(?:Phone Number|Phone No\.|Phone|Contact Number|Contact No|Contact)\s*[:：]\s*(.*?)(?:\n|$)',
        'Email id': r'E[-]?mail.*?[:：]\s*(.*?)(?:\n|$)',
        'Stock': r'Stock\s*[:：]\s*(.*?)(?:\n|$)'
    }

    extracted_data_list = []
    blocks = data.split('===============')
    for block in blocks:
        extracted_data = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, block, re.IGNORECASE | re.DOTALL)
            if match:
                extracted_data[key] = match.group(1).strip()
        
        if not extracted_data.get('Buy/Sell'):
            if re.search(r'\bbuy\b', block, re.IGNORECASE):
                extracted_data['Buy/Sell'] = 'Buy'
            elif re.search(r'\bsell\b', block, re.IGNORECASE):
                extracted_data['Buy/Sell'] = 'Sell'
            else:
                # Default to 'Buy' if not found
                extracted_data['Buy/Sell'] = 'Buy'

        cas_matches = list(re.finditer(patterns['CAS No.'], block, re.IGNORECASE | re.DOTALL))
        # if there are multiple CAS No. in a block, extract each one with product name
        if len(cas_matches) > 1:
            for cas_match in cas_matches:
                cas_no = cas_match.group(1).strip()
                preceding_text = block[:cas_match.start()].strip().split()[-1]
                if preceding_text not in extracted_data.values():
                    new_data = extracted_data.copy()
                    new_data['Product Name'] = preceding_text
                    new_data['CAS No.'] = cas_no
                    extracted_data_list.append(new_data)
        else:
            extracted_data_list.append(extracted_data)
        
    return extracted_data_list

# Function to save extracted data to CSV
def save_to_csv(extracted_data_list, output_file_path):
    # Create a DataFrame
    df = pd.DataFrame(extracted_data_list)

    # Save to CSV
    df.to_csv(output_file_path, sep=';', index=False)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract data from text file and save to CSV.')
    parser.add_argument('input_file', type=str, help='Path to the input text file.')
    parser.add_argument('output_file', type=str, nargs='?', default='extracted_data.csv', help='Path to the output CSV file (default: extracted_data.csv).')

    args = parser.parse_args()

    # Read data from the input file
    data = read_data_from_file(args.input_file)

    # Extract data
    extracted_data_list = extract_data(data)

    # Save extracted data to CSV
    save_to_csv(extracted_data_list, args.output_file)

    print(f'Data has been extracted and saved to {args.output_file}')

if __name__ == '__main__':
    main()