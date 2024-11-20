#ERA5_Interpolation

import xarray as xr
import numpy as np
import os
from scipy.interpolate import RegularGridInterpolator

#Replace "path_era5_data" with the actual path to your NetCDF file.
path_era5_data = "/home/vvatellis/storage/weatherProject/datasets/ERA5/reanalysis-era5-single-levels/"

all_entries = os.listdir(path_era5_data)
files = [entry for entry in all_entries if os.path.isfile(os.path.join(path_era5_data, entry))]

# Define the directory path
directory_path = "/home/vvatellis/storage/weatherProject/datasets/ERA5/Interpolation_reanalysis-era5-single-levels"
# Check if the directory exists
if not os.path.exists(directory_path):
    # Create the directory
    os.makedirs(directory_path)
    print(f"Directory '{directory_path}' created.")

for file in files:
    dataPath = os.path.join(path_era5_data,file)
    print("path to data: ",dataPath)
    ds = xr.open_dataset(dataPath)
    all_variables = list(ds.data_vars)
    excluded_vars = ['latitude', 'longitude']
    selected_variables = [var for var in all_variables if var not in excluded_vars]
    #print("Selected variables:", selected_variables)
  
    variable_name = selected_variables[0]  # Example: selecting the first variable
    data_array = ds[variable_name]

    interpolated_data = []
    for time in ds.valid_time:
        # Select data for the current time step
        time_step = ds.sel(valid_time=time)
        
        lat = time_step['latitude'].values
        lon = time_step['longitude'].values
        variable = time_step[variable_name].values  # Replace 'temperature' with your variable name
        #print("shape before interpolation",temperature.shape)

        new_lat = np.arange(lat.min(), lat.max(), 0.02)
        new_lon = np.arange(lon.min(), lon.max(), 0.02)

        interpolating_function = RegularGridInterpolator((lat, lon), variable, method='linear')

        new_lon_grid, new_lat_grid = np.meshgrid(new_lon, new_lat)
        new_points = np.array([new_lat_grid.flatten(), new_lon_grid.flatten()]).T

        interpolated_values = interpolating_function(new_points)
        interpolated_variable = interpolated_values.reshape(new_lat_grid.shape)

        #print("shape after interpolation",interpolated_temperature.shape)
        interpolated_ds = xr.Dataset(
            {
                variable_name : (['latitude', 'longitude'], interpolated_variable)
            },
            coords={
                'latitude': new_lat,
                'longitude': new_lon
            }
            )
        # Append the DataArray to the list
        interpolated_data.append(interpolated_ds)

        #break
    interpolated_ds = xr.concat(interpolated_data, dim='valid_time')
    interpolated_ds.to_netcdf(f'{directory_path}/interpolated_{file}')

    print(f'Variable: {variable_name}\nstarting time: {ds.valid_time.values[0]} (yyyy/mm/dd/hour)\nfinal time: {ds.valid_time.values[-1]} (yyyy/mm/dd/hour)')
    print(f'Data saved at: {directory_path}/interpolated_{file} \n')
