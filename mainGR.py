# The script aims to prepare the data 

import os, zipfile
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import shutil
import argparse


# ---------------------------
# 1. arguments
# ---------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Data preparation script")
    parser.add_argument("--data_dir", type=str, required=True, default= "/home/vvatellis/WeatherData/ERA5_hourly_data/single_levels/",
                        help="Path to the folder where the data are saved in zip format")
    parser.add_argument("--extract_dir", type=str, default="/home/vvatellis/WeatherData/ERA5_hourly_data/single_level_extracted/", 
                        help="Path to the folder where the data will be extracted")
    parser.add_argument("--output_dir", type=str, default="/home/vvatellis/WeatherData/ERA5_hourly_data/single_level_ERA5_Greece", 
                        help="Path to the output folder where the data for greece will be extracted")
    
    return parser.parse_args()


def merge_and_filter_nc(data_dir, file_pattern="GR_*.nc", filter_hour=19, output_filename="GR_merged_filtered.nc"):
    """
    Merges multiple NetCDF files from the specified directory, filters out time steps where the hour equals 'filter_hour',
    and saves the merged and filtered dataset to a new NetCDF file.

    Parameters:
      data_dir (str): Directory containing the NetCDF files.
      file_pattern (str): Glob pattern to match files for merging (default: "GR_*.nc").
      filter_hour (int): Hour value to filter out (default: 19 to remove 19:00 data).
      output_filename (str): Name of the output NetCDF file (default: "GR_merged_filtered.nc").

    Returns:
      str: Full path to the saved merged and filtered NetCDF file.
    """
    # Build the file pattern path (e.g., "/path/to/greece_data/GR_*.nc")
    file_path = os.path.join(data_dir, file_pattern)
    
    # Merge all NetCDF files matching the pattern using xarray's open_mfdataset.
    # 'combine="by_coords"' merges datasets based on their coordinate values.
    merged_ds = xr.open_mfdataset(file_path, combine='by_coords')
    
    # Filter out the time steps where the hour equals filter_hour.
    # The dt.hour accessor extracts the hour from the time coordinate.
    filtered_ds = merged_ds.sel(valid_time=merged_ds.valid_time.dt.hour != filter_hour)
    
    # Build the full output path.
    output_path = os.path.join(data_dir, output_filename)
    
    # Save the merged and filtered dataset to a new NetCDF file.
    filtered_ds.to_netcdf(output_path)
    
    print(f"Merged and filtered dataset saved to {output_path}")
    return output_path


def extract_zip_files(data_dir, extract_dir):
    """
    Extracts all ZIP files from the specified directory and saves their contents in the extraction directory.

    The function does the following:
      - Iterates over all files in the 'data_dir'.
      - For each file ending with ".zip":
          - Opens the ZIP file and lists its contents.
          - If the ZIP contains exactly one file:
              - Checks if the output file (with a ".nc" extension) already exists.
              - If it does not exist, extracts that file and renames it (e.g., "data1.zip" becomes "data1.nc").
              - Otherwise, skips extraction to save time.
          - If the ZIP contains multiple files:
              - For each member file, it checks if the output file (with a prefix based on the ZIP name) already exists.
              - If it does not exist, extracts and renames the file.
              - Otherwise, skips that member.
    
    Parameters:
      data_dir (str): Directory path where the ZIP files are located.
      extract_dir (str): Directory path where the extracted files will be saved.
    
    Returns:
      None
    """
    # Loop over all files in the data directory.
    for zip_file in os.listdir(data_dir):
        if zip_file.endswith(".zip"):
            zip_path = os.path.join(data_dir, zip_file)
            
            # Open the ZIP file
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # Get list of all files contained in the ZIP
                name_list = zip_ref.namelist()
                
                # If there is exactly one file in the ZIP, extract and rename it.
                if len(name_list) == 1:
                    # Create output file name by removing the ".zip" extension and appending ".nc"
                    output_name = os.path.splitext(zip_file)[0]
                    output_path = os.path.join(extract_dir, output_name)
                    
                    # Check if the file already exists
                    if os.path.exists(output_path):
                        print(f"File {output_name} already exists. Skipping extraction.")
                    else:
                        # Extract the file from the ZIP and save it to the output path.
                        with zip_ref.open(name_list[0]) as source_file:
                            with open(output_path, "wb") as target_file:
                                shutil.copyfileobj(source_file, target_file)
                        print(f"Extracted: {zip_file} -> {output_name}")
                else:
                    # If there are multiple files in the ZIP, extract each file and rename accordingly.
                    for member in zip_ref.infolist():
                        # Build output name: ZIP base name plus the member's file name.
                        member_name = os.path.basename(member.filename)
                        output_name = os.path.splitext(zip_file)[0] + "_" + member_name
                        output_path = os.path.join(extract_dir, output_name)
                        
                        # Check if this member has already been extracted
                        if os.path.exists(output_path):
                            print(f"File {output_name} already exists. Skipping extraction of this member.")
                        else:
                            # Extract each member and write to the output path.
                            with zip_ref.open(member) as source_file:
                                with open(output_path, "wb") as target_file:
                                    shutil.copyfileobj(source_file, target_file)
                            print(f"Extracted member: {output_name}")
            
            print(f"Completed processing of {zip_file}.\n")


def process_netcdf_files(extract_dir, output_dir, lat_min, lat_max, lon_min, lon_max):
    """
    Processes extracted NetCDF files by subsetting the data to a specified geographic region and saving the results.

    The function performs the following steps for each NetCDF file in 'extract_dir':
      - Loads the NetCDF file using xarray.
      - Subsets the dataset using the provided latitude and longitude boundaries.
      - Generates an output filename with a prefix (e.g., "GR_") to indicate that the file contains data for a specific region.
      - Checks if the processed file already exists in 'output_dir'. If it does, skips processing for that file.
      - Saves the subsetted dataset to the 'output_dir'.
    
    Parameters:
      extract_dir (str): Directory containing the extracted NetCDF files.
      output_dir (str): Directory where the processed (subsetted) NetCDF files will be saved.
      lat_min (float): Minimum latitude of the target region.
      lat_max (float): Maximum latitude of the target region.
      lon_min (float): Minimum longitude of the target region.
      lon_max (float): Maximum longitude of the target region.
    
    Returns:
      None
    """
    # Iterate over all files in the extraction directory.
    for file in os.listdir(extract_dir):
        if file.endswith(".nc"):  # Process only NetCDF files.
            output_filename = f"GR_{file}"
            output_path = os.path.join(output_dir, output_filename)
            
            # Check if the file has already been processed.
            if os.path.exists(output_path):
                print(f"File {output_filename} already processed, skipping.")
                continue
            
            file_path = os.path.join(extract_dir, file)
            
            # Load the dataset with xarray.
            ds = xr.open_dataset(file_path)
            
            # Subset the dataset using the provided coordinate boundaries.
            # Note: The order of latitude slicing (lat_max, lat_min) depends on how the data is ordered.
            ds_region = ds.sel(latitude=slice(lat_max, lat_min), longitude=slice(lon_min, lon_max))
            
            # Save the subsetted dataset to a new NetCDF file.
            ds_region.to_netcdf(output_path)
            print(f"Processed: {file} -> {output_filename}")
    
    print("✅ All NetCDF files processed successfully!")


if __name__ == "__main__":
    args = parse_args()

    # Step 1: Define Paths
    os.makedirs(args.extract_dir, exist_ok=True)  # Ensure extraction folder exists
    os.makedirs(args.output_dir, exist_ok=True)  # Ensure output folder exists

    # Step 2: Define Greece Region (Latitude & Longitude Bounds)
    lat_min, lat_max = 34, 42
    lon_min, lon_max = 19, 28

    # Step 3: Loop Over ZIP Files and Extract
    # Loop over ZIP files in the data directory
    extract_zip_files(args.data_dir, args.extract_dir)
    process_netcdf_files(args.extract_dir, args.output_dir, lat_min, lat_max, lon_min, lon_max)

    # Example usage:
    # data_dir = "/path/to/greece_data"
    output_filename = os.path.join("/home/vvatellis/storage/DoctoralThesis/RepresentationEOcode","GR_merged_filtered.nc")
    merge_and_filter_nc(args.output_dir, file_pattern="GR_*.nc", filter_hour=19, output_filename=output_filename)


