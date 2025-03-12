# ERA5 Single-Level Data Downloader

This repository contains a Python script that automates the download of ERA5 single-level meteorological data from the Copernicus Climate Data Store (CDS) using the [cdsapi](https://cds.climate.copernicus.eu/api-how-to) library.

## Overview

ERA5 is a state-of-the-art global reanalysis dataset produced by the European Centre for Medium-Range Weather Forecasts (ECMWF) and provided by the Copernicus Climate Data Store. The ERA5 single-level dataset includes key meteorological variables such as:
- 10m u component of wind
- 10m v component of wind
- 2m temperature
- Mean sea level pressure
- Total precipitation

This script is designed to download these variables over specified years, months, days, and times. It saves the data in NetCDF format within a ZIP archive.

## Prerequisites

- **Python 3.x**  
- **cdsapi**: Install via pip:
  ```
  pip install cdsapi
  ```
- **CDS API Key**:  
  You must register for an account on the [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/). Once registered, follow the [CDS API Quickstart guide](https://cds.climate.copernicus.eu/api-how-to) to obtain your API key. Typically, you will create a `~/.cdsapirc` file with your credentials.

## How It Works

1. **Dataset & Variables**  
   The dataset used is `reanalysis-era5-single-levels`. The script downloads data for the following variables:
   - `10m_u_component_of_wind`
   - `10m_v_component_of_wind`
   - `2m_temperature`
   - `mean_sea_level_pressure`
   - `total_precipitation`

   More information about the dataset can be found on the [ERA5 Single Levels Overview page](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels).

2. **Time Parameters**  
   The script is configured to loop over a specified range of years (e.g., 1990 to 1999), with data for all 12 months, every day of the month, and at four times during the day (00:00, 06:00, 12:00, 18:00).

3. **Request Parameters**  
   A request dictionary defines the download parameters:
   ```python
   request = {
       "product_type": ["reanalysis"],
       "variable": variable,
       "year": year,
       "month": ["01", "02", "03", "04", "05", "06",
                 "07", "08", "09", "10", "11", "12"],
       "day": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
               "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24",
               "25", "26", "27", "28", "29", "30", "31"],
       "time": ["00:00", "06:00", "12:00", "18:00"],
       "data_format": "netcdf",
       "download_format": "zip",
   }
   ```
   - **data_format**: The output format (NetCDF).
   - **download_format**: The file format in which the data will be packaged (ZIP).

5. **Downloading Process**  
   The script iterates over each variable and year, downloading the data and saving it with filenames such as `10m_u_component_of_wind_Y1990.nc.zip`.

## Running the Script

1. **Configure Your Environment**  
   - Ensure Python 3.x and `cdsapi` are installed.
   - Set up your CDS API key as described above.

2. **Modify Parameters (if needed)**  
   - Update the `directory_path` to your desired download directory.
   - Change the list of years, variables, or other parameters as needed.

3. **Execute the Script**  
   Run the script from the command line:
   ```
   python download_era5.py
   ```

   The data will be downloaded into the specified directory.

## Additional Resources

- **Copernicus Climate Data Store**:  
  [CDS Website](https://cds.climate.copernicus.eu/)
  
- **ERA5 Single Levels Dataset**:  
  [ERA5 Single Levels Overview](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels)

- **CDS API Documentation**:  
  [CDS API How-To](https://cds.climate.copernicus.eu/api-how-to)



# Data Manipulation and Preprocessing Techniques

This script `mainGR.py` extracts from the clobe NetCDF file the region of Greece and merges all Greece-specific NetCDF files into one dataset, removes any data corresponding to 19:00 (to eliminate an extra hour mistakenly downloaded), and saves the cleaned dataset as a new NetCDF file. It uses xarray’s multi-file dataset opening (open_mfdataset) with coordinate-based merging and the dt accessor for time filtering.



# License

Include your preferred license here (e.g., MIT License).
