#ERA5_Interpolation

import xarray as xr
import numpy as np
from scipy.interpolate import RegularGridInterpolator

#Replace "path_era5_data" with the actual path to your NetCDF file.
path_era5_data = "~/storage/weatherProject/datasets/ERA5ttu/ERA5/nc_SURFACE/data_stream-oper.nc"
ds = xr.open_dataset(path_era5_data)

varibale_name = 'swvl1'

interpolated_data = []
for time in ds.valid_time:
    # Select data for the current time step
    time_step = ds.sel(valid_time=time)
    
    lat = time_step['latitude'].values
    lon = time_step['longitude'].values
    variable = time_step[varibale_name].values  # Replace 'temperature' with your variable name
    #print("shape before interpolation",temperature.shape)

    new_lat = np.arange(lat.min(), lat.max(), 0.1)
    new_lon = np.arange(lon.min(), lon.max(), 0.1)

    interpolating_function = RegularGridInterpolator((lat, lon), variable, method='linear')

    new_lon_grid, new_lat_grid = np.meshgrid(new_lon, new_lat)
    new_points = np.array([new_lat_grid.flatten(), new_lon_grid.flatten()]).T

    interpolated_values = interpolating_function(new_points)
    interpolated_variable = interpolated_values.reshape(new_lat_grid.shape)

    #print("shape after interpolation",interpolated_temperature.shape)
    interpolated_ds = xr.Dataset(
        {
            varibale_name : (['latitude', 'longitude'], interpolated_variable)
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
interpolated_ds.to_netcdf(f'interpolated_era5_data_{varibale_name}.nc')

print(f'Variable: {varibale_name}\nstarting time: {ds.valid_time[0].item()} (yyyy/mm/dd/hour)\nfinal time: {ds.valid_time[-1].item()} (yyyy/mm/dd/hour)')
