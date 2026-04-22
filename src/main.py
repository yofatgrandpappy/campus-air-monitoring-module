import csv_builder
import polyregress_transform

if __name__ == "__main__":
    input_files = [
        "data/sample_times_pollution_data1.csv",
        "data/sample_times_pollution_data2.csv",
        "data/sample_times_pollution_data3.csv",
        "data/sample_times_pollution_data4.csv",
        "data/sample_times_pollution_data5.csv"
    ]
    merged = "data/merged_pollution_data.csv"
    csv_builder.merge_pollution_csv_files(input_files, merged)
    transformed = "data/transformed_pollution_data.csv"
    polyregress_transform.apply_transformation(merged, transformed)