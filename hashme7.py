import pandas as pd
import hashlib
import argparse
import os
from datetime import datetime

def generate_salt():
    """Generate a salt by hashing the current date and time."""
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return hashlib.sha256(current_datetime.encode()).hexdigest()

def hash_column(value, salt):
    """Hash a single value using SHA-256, with a salt."""
    if pd.isnull(value):  # Handle NaN values to avoid hashing issues
        return None
    # Combine the value with the salt before hashing
    value_with_salt = str(value) + salt
    return hashlib.sha256(value_with_salt.encode()).hexdigest()

def find_sample_value(df, column):
    """Find a sample value in the column that is not NaN. Return '<empty>' if all values are NaN."""
    for value in df[column]:
        if pd.notnull(value):
            return value
    return "<empty>"

def interactive_column_selection(df):
    """Interactively ask the user which columns to hash, with default choice and case-insensitivity."""
    columns_to_hash = []
    print("For each column, decide whether to hash it (Y/N) or skip the rest (S). Default is N.")
    for column in df.columns:
        sample_value = find_sample_value(df, column)
        while True:  # Loop to ensure valid input
            decision = input(f"Column: {column}, sample value: {sample_value}. Hash this column? [Y/N/S]: ").strip().upper()
            if decision == '':  # Default option
                decision = 'N'
            if decision in ['Y', 'N', 'S']:
                break
            else:
                print("Invalid input. Please enter Y, N, or S (case-insensitive).")
        if decision == 'Y':
            columns_to_hash.append(column)
        elif decision == 'S':
            break
    return columns_to_hash

def hash_columns_in_csv(input_csv_path, columns_to_hash, output_csv_path, salt):
    """
    Hash specified columns in a CSV file and save the result to a new file.
    
    :param input_csv_path: Path to the input CSV file.
    :param columns_to_hash: List of column names to hash.
    :param output_csv_path: Path to save the output CSV file.
    :param salt: Salt value for hashing.
    """
    # Load the CSV file
    df = pd.read_csv(input_csv_path)
    
    # Hash specified columns
    for column in columns_to_hash:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: hash_column(x, salt))
        else:
            print(f"Column '{column}' not found in the CSV.")
    
    # Save the result to a new CSV file
    df.to_csv(output_csv_path, index=False)

def main():
    parser = argparse.ArgumentParser(description='Interactively hash specific columns of a CSV file using SHA-256 and a dynamic salt based on the current date and time.')
    parser.add_argument('input_csv_path', type=str, help='Path to the input CSV file.')
    parser.add_argument('--columns', type=str, nargs='+', help='Column names to hash (optional).')

    args = parser.parse_args()

    # Generate a dynamic salt based on the current date and time, then print it
    salt = generate_salt()
    print(f"Using salt: {salt}")

    # Generate the output file name by prepending "hashed_" to the input file name
    input_dir, input_filename = os.path.split(args.input_csv_path)
    output_csv_path = os.path.join(input_dir, "hashed_" + input_filename)

    # Load the CSV file to determine column actions
    df = pd.read_csv(args.input_csv_path)

    if args.columns:
        # Non-interactive mode: Show all columns and highlight ones to be hashed
        print("Found columns in the CSV:")
        for column in df.columns:
            if column in args.columns:
                print(f"  * {column} (will be hashed)")
            else:
                print(f"  - {column}")
        hash_columns_in_csv(args.input_csv_path, args.columns, output_csv_path, salt)
    else:
        # Interactive mode
        columns_to_hash = interactive_column_selection(df)
        hash_columns_in_csv(args.input_csv_path, columns_to_hash, output_csv_path, salt)
        
        # Show sample command for non-interactive mode based on selection
        if columns_to_hash:
            print("\nTo repeat this hashing without interactive mode, use the following command:")
            columns_arg = ' '.join([f'"{col}"' for col in columns_to_hash])
            print(f"python {os.path.basename(__file__)} {args.input_csv_path} --columns {columns_arg}")

if __name__ == "__main__":
    main()
