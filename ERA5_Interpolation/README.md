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

## Usage

1. Ensure you have the `cdsapi` library installed:
   ```bash
   pip install cdsapi
