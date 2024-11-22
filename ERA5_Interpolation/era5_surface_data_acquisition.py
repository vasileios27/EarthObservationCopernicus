#data acqusition 
# The provided Python script automates the download of specific meteorological variables 
# lsfrom the Copernicus Climate Data Store (CDS) using the cdsapi library.
import cdsapi
import os

# Define the directory path
directory_path = "/home/vvatellis/storage/weatherProject/datasets/ERA5"
# Change to a new directory
os.chdir(directory_path)

dataset = "reanalysis-era5-single-levels"
client = cdsapi.Client()

# years = ["1990","2001", "2002", "2003",
#         "2004", "2005", "2006",
#         "2007", "2008", "2009",
#         "2010"]
years = [1990,2010]
months = ["06", "07", "08"]
variables= [ 
        # "volumetric_soil_water_layer_1",
        # "volumetric_soil_water_layer_2",
        # "volumetric_soil_water_layer_3",
        # "volumetric_soil_water_layer_4",
        # "convective_available_potential_energy", 
        "convective_inhibition",
        "k_index","total_column_water_vapour",
        "10m_u_component_of_wind",
        "10m_v_component_of_wind"
        ]

for variable in variables:
    for year in range(years[0], years[-1],1):

        request = {
             "product_type": ["reanalysis"],
            "variable": variable,
            "year": year,
            "month": months,
            "day": [
                "01", "02", "03",
                "04", "05", "06",
                "07", "08", "09",
                "10", "11", "12",
                "13", "14", "15",
                "16", "17", "18",
                "19", "20", "21",
                "22", "23", "24",
                "25", "26", "27",
                "28", "29", "30",
                "31"
            ],
            "time": [
                "00:00", "01:00", "02:00",
                "03:00", "04:00", "05:00",
                "06:00", "07:00", "08:00",
                "09:00", "10:00", "11:00",
                "12:00", "13:00", "14:00",
                "15:00", "16:00", "17:00",
                "18:00", "19:00", "20:00",
                "21:00", "22:00", "23:00"
            ],
            "data_format": "netcdf",
            "download_format": "unarchived",
            "area": [50.5, 5, 47.5, 10]
        }

        target = f"{variable}_Y{year}.nc"
        client.retrieve(dataset, request, target)
        print(f"Downloaded data for {year}")
