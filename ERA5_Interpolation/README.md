# Project Title


Brief description of the project.

## Script Overview

This script `era5_surface_data_acquisition.py` facilitates the automated download of selected meteorological variables from the Copernicus Climate Data Store (CDS) ERA5 dataset. By specifying desired variables, years, and months, users can efficiently retrieve data for a defined geographical area. The script leverages the cdsapi library to interact with the CDS API, streamlining the data acquisition process for research and analysis purposes.

- Download meteorological data from the Copernicus Climate Data Store (CDS).
- Retrieve variables such as:
  - Volumetric soil water layers
  - Convective available potential energy
  - Convective inhibition
  - K index
  - Total column water vapour
  - 10m u-component of wind
  - 10m v-component of wind
- Save the data in NetCDF format for specified years and months.

## ERA5 Data Interpolation Script
This repository contains a Python script designed to perform spatial interpolation on ERA5 reanalysis data, specifically focusing on the swvl1 variable, which represents volumetric soil water in the first layer. The script enhances the spatial resolution of the data by interpolating it onto a finer grid, facilitating more detailed analysis.

### Features
Data Loading: Utilizes the xarray library to load ERA5 NetCDF datasets.
Spatial Interpolation: Employs scipy's RegularGridInterpolator to interpolate data onto a finer grid with 0.1-degree intervals.
Data Saving: Saves the interpolated data as NetCDF files for subsequent analysis.
Prerequisites
Ensure the following Python libraries are installed:

 - xarray
 - numpy
 - scipy


## Usage

1. Ensure you have the `cdsapi` library installed:
   ```bash
   pip install cdsapi
   ```
   further information of [`cdsapi`](https://cds.climate.copernicus.eu/how-to-api) can be found in 

2. ```bash
   pip install xarray numpy scipy
   ```

3. ```bash
    git clone https://github.com/vasileios27/EarthObservationCopernicus.git
    cd era5-interpolation
    ```
4. Set the Path to Your ERA5 Data:
    In the script, replace the path_era5_data variable with the path to your ERA5 NetCDF file:
  ```bash
    path_era5_data = "/path/to/your/data_stream-oper.nc"
  ```
5. Run the Script:
  ```bash
  python era5_interpolation.py
  ```

# Output



# License
This project is licensed under the MIT License. See the LICENSE file for details.