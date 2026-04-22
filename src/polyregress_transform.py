import numpy as np
import pandas as pd
from numpy.polynomial.polynomial import Polynomial

def apply_transformation(input_csv, output_csv):
    """
    Fits a quadratic model predicting CO2_ppm based on PM_ug/m3 and
    applies it directly to the PM2.5 columns to generate CO2-equivalent values.

    Parameters:
    - input_csv (str): Path to the merged CSV file.
    - output_csv (str): Path to the output CSV file.
    """
    df = pd.read_csv(input_csv)
    df.dropna(subset=['CO2_ppm', 'PM_ug/m3'], inplace=True)

    # Independent: PM_ug/m3, Dependent: CO2_ppm
    x = df['PM_ug/m3'].values
    y = df['CO2_ppm'].values

    # Fit degree-2 polynomial CO2 = f(PM)
    degree = 2
    coefs = Polynomial.fit(x, y, deg=degree).convert().coef

    # Predict CO2 based on PM_ug/m3 for validation / optional
    df['CO2_predicted'] = coefs[0] + coefs[1] * df['PM_ug/m3'] + coefs[2] * df['PM_ug/m3'] ** 2
    df['CO2_predicted'] = df['CO2_predicted'].clip(lower=0)

    # Now apply the same polynomial directly to each PM2.5_File column
    pm_columns = [col for col in df.columns if col.startswith('PM2.5_File')]
    for col in pm_columns:
        df[f'{col}_CO2_equivalent'] = coefs[0] + coefs[1] * df[col] + coefs[2] * df[col] ** 2
        df[f'{col}_CO2_equivalent'] = df[f'{col}_CO2_equivalent'].clip(lower=0)

    # Round results
    df = df.round(3)

    # Save output
    df.to_csv(output_csv, index=False)
    print(f"Transformation complete. Output saved to {output_csv}")