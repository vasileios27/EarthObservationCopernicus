import os
import numpy as np
import xarray as xr
from scipy.interpolate import RegularGridInterpolator

class NetCDFInterpolator:
    def __init__(self, input_file, variable_name, grid_step=0.02, method='linear'):
        """
        Initialize the interpolator with the specified parameters.

        Parameters:
        - input_file (str): Path to the input NetCDF file.
        - variable_name (str): Name of the variable to interpolate.
        - grid_step (float): Desired grid step size for interpolation. Default is 0.02 degrees.
        - method (str): Interpolation method. Options are 'linear' or 'nearest'. Default is 'linear'.
        """
        self.input_file = input_file
        self.variable_name = variable_name
        self.grid_step = grid_step
        self.method = method
        self.dataset = xr.open_dataset(input_file)
        self.interpolated_data = []

    def interpolate(self):
        """
        Perform interpolation over all time steps for the specified variable.
        """
        for time in self.dataset.valid_time:
            # Select data for the current time step
            time_step = self.dataset.sel(valid_time=time)
            
            lat = time_step['latitude'].values
            lon = time_step['longitude'].values
            variable = time_step[self.variable_name].values

            # Define the number of points for interpolation
            num_lat_points = int((lat.max() - lat.min()) / self.grid_step) + 1
            num_lon_points = int((lon.max() - lon.min()) / self.grid_step) + 1

            # Generate new latitude and longitude values including endpoints
            new_lat = np.linspace(lat.min(), lat.max(), num=num_lat_points)
            new_lon = np.linspace(lon.min(), lon.max(), num=num_lon_points)

            # Create the interpolating function
            interpolating_function = RegularGridInterpolator(
                (lat, lon), variable, method=self.method
            )

            # Generate a grid of new points
            new_lon_grid, new_lat_grid = np.meshgrid(new_lon, new_lat)
            new_points = np.array([new_lat_grid.flatten(), new_lon_grid.flatten()]).T

            # Perform interpolation
            interpolated_values = interpolating_function(new_points)
            interpolated_variable = interpolated_values.reshape(new_lat_grid.shape)

            # Create a new Dataset for the interpolated variable
            interpolated_ds = xr.Dataset(
                {
                    self.variable_name: (['latitude', 'longitude'], interpolated_variable)
                },
                coords={
                    'latitude': new_lat,
                    'longitude': new_lon,
                    'valid_time': time.values
                }
            )
            # Append the Dataset to the list
            self.interpolated_data.append(interpolated_ds)

    def save_to_netcdf(self, output_file):
        """
        Save the interpolated data to a new NetCDF file.

        Parameters:
        - output_file (str): Path to the output NetCDF file.
        """
        # Concatenate all time steps along the 'valid_time' dimension
        interpolated_ds = xr.concat(self.interpolated_data, dim='valid_time')
        interpolated_ds.to_netcdf(output_file)
        self.interpolated_ds = interpolated_ds
        print(f"Interpolated data saved to {output_file}")

if __name__ == "__main__":

    #Replace "path_era5_data" with the actual path to your NetCDF file.
    path_era5_data = "/home/vvatellis/storage/weatherProject/datasets/ERA5/reanalysis-era5-single-levels"

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


        # Initialize the interpolator
        interpolator = NetCDFInterpolator(
            input_file=dataPath,
            variable_name=variable_name,
            grid_step=0.02,
            method='linear'
        )

        # Perform interpolation
        interpolator.interpolate()

        # Save the interpolated data to a new NetCDF file
        interpolator.save_to_netcdf(f'{directory_path}/interpolated_{file}')
        print(f'Variable: {variable_name}\nstarting time: {ds.valid_time.values[0]} (yyyy/mm/dd/hour)\nfinal time: {ds.valid_time.values[-1]} (yyyy/mm/dd/hour)')
        print(f'Data saved at: {directory_path}/interpolated_{file} \n')
        print(f'Latitude {interpolator.interpolated_ds["latitude"].values.min()}-{interpolator.interpolated_ds["latitude"].values.max()}\nLongitude {interpolator.interpolated_ds["longitude"].values.min()}-{interpolator.interpolated_ds["longitude"].values.max()}')
