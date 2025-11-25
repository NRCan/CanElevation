# Environment Setup for Vertical Transformations

This guide explains how to set up the necessary software environment to perform vertical transformations of geospatial data in Canada.

## Software Installation

We recommend using the latest version of the [OSGeo4W](https://trac.osgeo.org/osgeo4w/) free software suite. This suite includes several widely used open-source geospatial tools, including GDAL, PDAL, PROJ, and QGIS.

!!! tip "Install tips"
    We recommend that you choose the *Express install* option and select *QGIS LTR* in the *Select Packages* window. This will give you all the tools you need for the tutorial.
    By default, the OSGeo4W installer performs the installation in the C:\OSGeo4W directory. The command prompt to use is the one located in this directory.

The versions used for this tutorial are:

* GDAL 3.10
* PDAL 2.8
* PROJ 9.6
* QGIS 3.40

These software packages can be used in various ways: via command line, as Python libraries, or interactively through a graphical interface (e.g., QGIS). In this guide, examples are primarily presented using the command-line environment provided by the OSGeo4W console.

