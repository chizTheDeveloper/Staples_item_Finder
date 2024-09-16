import pandas as pd

# Load the CSV file
def load_csv(file_path):
    """Loads a CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading CSV: {str(e)}")


# Remove duplicates
def remove_duplicates(df, subset=None):
    """Removes duplicate rows from a DataFrame."""
    if subset is None:
        return df.drop_duplicates()
    else:
        return df.drop_duplicates(subset=subset)


# Save the cleaned CSV
def save_csv(df, file_path):
    """Saves a DataFrame to a CSV file."""
    try:
        df.to_csv(file_path, index=False)
        print("CSV saved successfully.")
    except Exception as e:
        print(f"Error saving CSV: {str(e)}")


# Main function
def main():
    file_path = "AisleData-sheet.csv"  # Replace with your CSV file path
    cleaned_file_path = "AisleData.csv"  # Replace with your desired output file path

    # Load the CSV
    df = load_csv(file_path)

    # Print original shape
    print(f"Original shape: {df.shape}")

    # Remove duplicates
    df = remove_duplicates(df, subset="Item Name")  # Replace with your desired column(s)

    # Print cleaned shape
    print(f"Cleaned shape: {df.shape}")

    # Save the cleaned CSV
    save_csv(df, cleaned_file_path)

if __name__ == "__main__":
    main()