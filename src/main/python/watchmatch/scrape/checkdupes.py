import pandas as pd

def check_duplicates(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Check for duplicate rows
    duplicate_rows = df[df.duplicated()]

    if not duplicate_rows.empty:
        print("Duplicate rows found:")
        print(duplicate_rows)
    else:
        print("No duplicate rows found.")

# Replace 'your_file.csv' with the actual path to your CSV file
check_duplicates('./src/main/ressources/watches.csv')