import random
import string
import datetime
import pandas as pd
import argparse
from itertools import product

def generate_blinded_id():
    """Generates ID: <3 random letters>YYYYMMDDHHMMSS<1 random letter>"""
    prefix = ''.join(random.choices(string.ascii_letters, k=3))
    # Using YYYY for clarity and long-term sorting
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = random.choice(string.ascii_letters)
    return f"{prefix}{timestamp}{suffix}"

def main():
    # Setup command line arguments
    parser = argparse.ArgumentParser(description="Generate Blinded IDs for ADC Screening.")
    parser.add_argument('--file1', required=True, help="Path to adc.txt")
    parser.add_argument('--file2', required=True, help="Path to cell_line.txt")
    parser.add_argument('--output', default="screening_manifest.csv", help="Output filename")

    args = parser.parse_args()

    try:
        # 1. Load data from files
        with open(args.file1, 'r') as f:
            adcs = [line.strip() for line in f if line.strip()]
        
        with open(args.file2, 'r') as f:
            cell_lines = [line.strip() for line in f if line.strip()]

        # 2. Create combinations and Generate IDs
        combinations = list(product(adcs, cell_lines))
        df = pd.DataFrame(combinations, columns=['Binder', 'Cell_line'])
        df['Blinded_ID'] = [generate_blinded_id() for _ in range(len(df))]

        # 3. Save to CSV
        df.to_csv(args.output, index=False)
        print(f"Successfully generated {len(df)} IDs.")
        print(f"Manifest saved to: {args.output}")
        print("\nPreview:")
        print(df.head())

    except FileNotFoundError as e:
        print(f"Error: Could not find one of the files. {e}")

if __name__ == "__main__":
    main()