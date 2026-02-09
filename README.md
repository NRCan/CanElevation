![NRCan banner](docs/assets/images/nrcan-banner.png)

[Version française](README_FR.md)

# CanElevation

The CanElevation repository provides comprehensive documentation, examples, and tools for working with Canadian elevation data, including LiDAR point clouds and vertical datum transformations.

## Overview

This repository contains:

- **Interactive Jupyter Notebooks** - Step-by-step tutorials for processing elevation data
- **Documentation** - Comprehensive guides in both English and French
- **Sample Data** - Example datasets for testing and learning

## 🪄Key Features

### STAC DEM Mosaics

- Discover how to search, access, and mosaic Digital Elevation Models (DEMs) using STAC (SpatioTemporal Asset Catalog) APIs
- Example workflows for integrating STAC-based DEMs into your analysis

### Point Cloud Processing
- Creating Digital Elevation Models (DEMs) from LiDAR data
- Working with COPC (Cloud Optimized Point Cloud) formats
- Filtering and classifying point cloud data
- Integration with QGIS for visualization

### Vertical Transformations
- Converting between Canadian vertical datums (CGVD2013, CGVD28)
- Raster-based transformations
- Point cloud datum and epoch conversions

### Using the GeoParquet Optimized Building Layer

- Learn how to use the GeoParquet optimized building layer with Python and GDAL: see [acces-python-gdal.md](docs/en/optimized_building_footprint/acces-python-gdal.md)
- Visualize the layer using QGIS: see [acces-qgis.md](docs/en/optimized_building_footprint/acces-qgis.md)

## 📖 Documentation

**Visit our comprehensive documentation:** [https://nrcan.github.io/CanElevation/](https://nrcan.github.io/CanElevation/)

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NRCan/CanElevation.git
   cd CanElevation
   ```

2. **Set up the environment:**
   ```bash
   conda env create -n CanElevation --file docs/assets/env/environment.yml
   conda activate CanElevation
   ```

3. **Launch Jupyter Notebook (Point cloud examples):**
   ```bash
   jupyter notebook
   ```

4. **Open a tutorial notebook** from the `docs/en/pointclouds/` or `docs/fr/pointclouds/` directory

## Data Sources

This repository works with [Point cloud data](https://open.canada.ca/data/en/dataset/7069387e-9986-4297-9f55-0288e9676947) and  [digital elevation models](https://open.canada.ca/data/en/dataset/957782bf-847c-4644-a757-e383c0057995) data from the CanElevation Series, which provides high-quality elevation data for Canada.

## License

This project is licensed under the [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada).

## Support

For questions or support:
- 📖 Check the [documentation](https://nrcan.github.io/CanElevation/)
- 🐛 Report issues on [GitHub Issues](https://github.com/NRCan/CanElevation/issues)

