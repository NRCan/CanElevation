# Vertical Transformations - CanElevation Series

## Context

In Canada, the management and integration of 3D geospatial data—especially lidar data and its derivatives—are central to many application domains: hydrological modeling, forest inventories, topographic mapping, land management, and more. For many of these fields, consistency and alignment of 3D geospatial data is often a critical requirement.

A key challenge in the Canadian context is the coexistence of multiple reference systems, both horizontal and vertical. For example, different versions (epochs) of NAD83(CSRS) are still in use depending on jurisdiction and acquisition period. Vertically, two height systems may be encountered: CGVD28 (historically used) and CGVD2013 (the current Canadian standard). This diversity can complicate the combination and analysis of datasets from multiple sources. Rigorous identification of the systems in use, as well as the implementation of appropriate (horizontal and vertical) transformations, may be necessary.

This tutorial is a practical guide showing concrete examples of vertical transformations for point clouds and digital elevation models (DEM) in the Canadian context. It is intended for advanced users or those with some background in geospatial tools and reference systems.

For a deeper understanding of Canadian reference systems, their conventions, and their evolution, see the [Canadian Geodetic Survey website](https://natural-resources.canada.ca/science-data/science-research/geomatics/science-research-geodetic-reference-systems).

## Contents

* [Environment Setup](./environment-setup.md) - Installation and configuration of required tools
* [Raster Transformations](./raster-transformations.md) - Transformations for Digital Elevation Models (DEM)
* [Point Cloud Transformations](./pointcloud-transformations.md) - Transformations for LiDAR point clouds, including epoch transformations

## Target Audience

This tutorial is designed for advanced users and provincial/territorial partners who need to perform accurate vertical transformations of geospatial data in Canada.
