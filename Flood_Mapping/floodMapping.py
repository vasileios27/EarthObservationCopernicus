import ee
import geemap

# Initialize the Google Earth Engine
try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()

# Define a function to preprocess Sentinel-1 SAR GRD data
def preprocess_sentinel1(image):
    """
    Preprocess Sentinel-1 SAR GRD data.
    Args:
        image: The Sentinel-1 image to preprocess.
    Returns:
        Processed image with added ratio bands.
    """
    # Select VV and VH polarizations
    vv = image.select('VV')
    vh = image.select('VH')
    ratio = vh.divide(vv).rename('VH_VV_ratio')
    return image.addBands([ratio])

# Define area of interest (AOI)
aoi = ee.Geometry.Rectangle([72.5, 19, 75, 22])

# Define dates for before and after flood events
before_start = '2017-07-15'
before_end = '2019-08-10'
after_start = '2019-08-10'
after_end = '2023-03-23'

# Load Sentinel-1 SAR GRD collection
sentinel1_collection = ee.ImageCollection('COPERNICUS/S1_GRD')\
    .filterBounds(aoi)\
    .filter(ee.Filter.eq('instrumentMode', 'IW'))\
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))\
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))\
    .filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))\
    .filter(ee.Filter.eq('resolution_meters', 10))\
    .select(['VH'])

# Filter imagery within preferred dates
before_collection = sentinel1_collection.filter(ee.Filter.date(before_start, before_end))
after_collection = sentinel1_collection.filter(ee.Filter.date(after_start, after_end))

# Clip and mosaic imagery within AOI
before = before_collection.mosaic().clip(aoi)
after = after_collection.mosaic().clip(aoi)

# Function to add ratio band
def add_ratio_band(image):
    ratio_band = image.select('VH').divide(image.select('VH')).rename('VV/VH')
    return image.addBands(ratio_band)

# Create RGB imagery for before and after
before_rgb = add_ratio_band(before)
after_rgb = add_ratio_band(after)

# Visualization parameters
vis_params = {
    'min': [-25, -25, 0],
    'max': [0, 0, 2]
}

# Create a map to visualize the results
Map = geemap.Map()
Map.centerObject(aoi, 8)
Map.addLayer(before_rgb, vis_params, 'Before Floods RGB')
Map.addLayer(after_rgb, vis_params, 'After Floods RGB')
Map.addLayer(before, {'min': -25, 'max': 0}, 'Before Floods', False)
Map.addLayer(after, {'min': -25, 'max': 0}, 'After Floods', False)

# Function to convert to natural units (from dB)
def to_natural(img):
    return ee.Image(10.0).pow(img.select(0).divide(10.0))

# Function to convert to dB
def to_db(img):
    return ee.Image(img).log10().multiply(10.0)

# Function to apply refined Lee filter (simplified version)
def refined_lee(img):
    # Image must be in the natural unit i.e., not in dB!
    # Set up 3x3 kernels
    weights3 = ee.List.repeat(ee.List.repeat(1, 3), 3)
    kernel3 = ee.Kernel.fixed(3, 3, weights3, 1, 1, False)
    # Apply the filter (dummy implementation for example purposes)
    return img.convolve(kernel3)

# Apply refined Lee filter and convert back to dB
before_filtered = to_db(refined_lee(to_natural(before)))
after_filtered = to_db(refined_lee(to_natural(after)))

Map.addLayer(before_filtered, {'min': -25, 'max': 0}, 'Before Filtered', False)
Map.addLayer(after_filtered, {'min': -25, 'max': 0}, 'After Filtered', False)

# Calculate difference and apply threshold for flooded areas
difference = after.divide(before)
diff_threshold = 1.5
flooded = difference.gt(diff_threshold).rename(['Water']).selfMask()
Map.addLayer(flooded, {'min': 0, 'max': 1, 'palette': ['orange']}, 'Initial Flood Initiate')

# Mask permanent water areas
permanent_water = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select('seasonality').gt(5).clip(aoi)
flooded = flooded.updateMask(permanent_water)

# Mask based on slope
slope_threshold = 5
terrain = ee.Algorithms.Terrain(before)
slope = terrain.select('slope')
flooded = flooded.updateMask(slope.lt(slope_threshold))

# Mask based on connected pixel count
connected_pixel_threshold = 2
connections = flooded.connectedPixelCount(25)
flooded = flooded.updateMask(connections.gt(connected_pixel_threshold))

Map.addLayer(flooded, {'min': 0, 'max': 1, 'palette': ['Red']}, 'Flooded Area', False)

# Calculate the area of flooded regions
stats = flooded.multiply(ee.Image.pixelArea()).reduceRegion({
    'reducer': ee.Reducer.sum(),
    'geometry': aoi,
    'scale': 30,
    'maxPixels': 1e10,
    'tileScale': 16
})

flooded_area = ee.Number(stats.get('Water')).divide(10000)
print('Flooded Area (hectares):', flooded_area.getInfo())

# Display the map
Map
