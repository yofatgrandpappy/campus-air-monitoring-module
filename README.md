# Campus Air Quality Sensor Data Pipeline

## Project Context

Undergraduate research project at the University of Waterloo investigating low-cost sensor alternatives for municipal GHG monitoring. Deployed a 5-sensor network (4 PM2.5 sensors, 1 CO2 reference sensor from UBC's BEACO2N program) for 30+ days of continuous monitoring on campus.

The research question: can distributed low-cost PM2.5 sensors serve as proxies for more expensive CO2 monitoring equipment?

Infrastructure has since been decommissioned. This repository contains the data processing pipeline developed for the project.

---

## Overview

This pipeline:
1. Ingests CSV data from multiple asynchronous sensor sources
2. Aligns timestamps across sensors (15-minute intervals)
3. Merges data streams into unified dataset
4. Fits polynomial regression model (CO2 as function of PM2.5)
5. Applies model to estimate CO2-equivalent values from PM2.5 readings

---

## Repository Structure

```
/campus-air-quality-monitoring
│
├── README.md
├── requirements.txt
│
└── /src
    ├── csv_builder.py           # Data merging and cleaning
    ├── polyregress_transform.py # Polynomial regression model
    └── main.py                  # Pipeline orchestration

```

---

## Pipeline Details

### Data Merging (`csv_builder.py`)

Handles the challenge of combining data from sensors with different output formats and timing:

- **Time column flexibility**: Handles `time`, `datetime`, or other column names
- **Timestamp alignment**: Rounds all timestamps to 15-minute intervals for joins
- **Outer join strategy**: Preserves all data points across sensors
- **Gap handling**: Forward-fill addresses sensor dropouts and missing values

### Regression Model (`polyregress_transform.py`)

Fits a degree-2 polynomial relationship between PM2.5 and CO2 concentrations:

```
CO2_predicted = β₀ + β₁(PM2.5) + β₂(PM2.5)²
```

- Uses reference CO2 sensor data to train model
- Applies fitted model to all PM2.5 sensors to generate CO2-equivalent estimates
- Clips negative predictions to zero (physical constraint)

---

## Usage

```python
from csv_builder import merge_pollution_csv_files
from polyregress_transform import apply_transformation

# Define input sensor files
input_files = [
    "data/sensor1.csv",
    "data/sensor2.csv",
    "data/sensor3.csv",
    "data/sensor4.csv",
    "data/sensor5.csv"
]

# Merge sensor data
merge_pollution_csv_files(input_files, "data/merged.csv")

# Apply regression transformation
apply_transformation("data/merged.csv", "data/transformed.csv")
```

Or run directly:

```bash
python src/main.py
```

---

## Technical Stack

- **Python 3.8+**
- **pandas**: Data manipulation and merging
- **NumPy**: Polynomial regression fitting

---

## Methods

### Sensor Selection
Conducted gap analysis evaluating:
- Measurement reliability
- Calibration drift characteristics
- Coverage vs. cost trade-offs
- Real-time telemetry capabilities

### Data Quality
- Timestamp normalization across asynchronous sources
- Forward-fill imputation for sensor dropouts
- Outlier handling via physical constraints (non-negative concentrations)

### Modeling Approach
Polynomial regression chosen over linear model after exploratory analysis showed non-linear relationship between PM2.5 and CO2 concentrations in the deployment environment.

---

## Project Scope (Full Research)

This repository represents the data pipeline component. The full project included:

- Research and selection of low-cost sensor hardware
- Physical deployment of 5-sensor network on campus
- Stakeholder outreach with municipal air quality professionals
- Vendor communications for API specifications and cost estimates
- Interactive dashboard for real-time data visualization
- Analysis of PM2.5 as proxy for GHG monitoring

---

## Requirements

```
pandas>=1.3.0
numpy>=1.20.0
```

Install with:

```bash
pip install -r requirements.txt
```

---

## Author

Rafay Chishty  
Computational Mathematics, University of Waterloo  
r.chishty@hotmail.com

---

## License

MIT License - feel free to use and adapt.
```
