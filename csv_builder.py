import pandas as pd
import os


def merge_pollution_csv_files(input_files, output_file, time_columns=['time', 'datetime']):
    """
    Merges multiple CSV files containing time and pollution data into a single CSV file.
    - Rounds timestamps to the nearest 15-minute interval.
    - Preserves original column names for CO2_ppm and PM_ug/m3.
    - Handles variations in time columns ('Times' or 'datetime').

    Parameters:
    - input_files (list of str): List of paths to the input CSV files.
    - output_file (str): Path to the output CSV file.
    - time_columns (list of str): Possible names for the time column.
    """
    renamed_dfs = []

    for i, file in enumerate(input_files):
        df = pd.read_csv(file)

        # Identify time column
        time_col = next((col for col in time_columns if col in df.columns), None)
        if not time_col:
            raise ValueError(f"No time column found in {file}. Expected one of: {time_columns}")

        # Convert time column to datetime
        df[time_col] = pd.to_datetime(df[time_col], errors='coerce')

        # Round timestamps to the nearest 15-minute interval
        df[time_col] = df[time_col].dt.round('15min')

        # Rename time column for consistency
        df = df.rename(columns={time_col: 'Time'})

        # Rename 'value' column to distinguish between sources
        if 'value' in df.columns:
            df = df.rename(columns={'value': f'PM2.5_File{i + 1}'})

        renamed_dfs.append(df)

    # Merge all dataframes on 'Time' column using an outer join
    merged_df = renamed_dfs[0]
    for df in renamed_dfs[1:]:
        merged_df = pd.merge(merged_df, df, on='Time', how='outer')

    # Rename 'Time' column back to 'Times' for consistency in output
    merged_df = merged_df.rename(columns={'Time': 'Times'})

    # Forward fill to handle NaN values.
    pm_columns = [col for col in merged_df.columns if col.startswith('PM2.5_')]
    merged_df[pm_columns] = merged_df[pm_columns].ffill()

    # Save merged CSV
    merged_df.to_csv(output_file, index=False)
    print(f"Merged CSV saved to {output_file}")


