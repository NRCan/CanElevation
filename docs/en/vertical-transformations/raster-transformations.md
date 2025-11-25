# Raster Vertical Transformations

This guide demonstrates how to perform vertical transformations on Digital Elevation Models (DEMs) in the Canadian context, specifically converting between CGVD28 and CGVD2013 vertical datums.

## Transformation Procedure

The following example demonstrates how to convert elevations in a DEM from CGVD28 to CGVD2013, without horizontal transformation or epoch change. The DEM has a resolution of 1m. The GDAL gdalwarp tool is used. 

In the OSGeo4W Shell command prompt, enter the following command, taking care to adapt the directories and DEM names:

!!! info "Files"
    [📄 Download dtm_utm14_CGVD28.tif](../assets/sample_data/raster/dtm_utm14_CGVD28.tif){ .md-button .md-button--primary }

```bash
gdalwarp ^
-s_srs "+init=EPSG:3158 +geoidgrids=ca_nrc_HT2_2010v70.tif" ^
-t_srs "+init=EPSG:3158 +geoidgrids=ca_nrc_CGG2013an83.tif" ^
-co COMPRESS=LZW ^
D:\dev\CanElevation\docs\assets\sample_data\raster\dtm_utm14_CGVD28.tif ^
D:\dev\CanElevation\docs\assets\sample_data\raster\dtm_utm14_CGVD2013.tif
```

### Explanations and Other Considerations

- The `-s_srs` parameter indicates the horizontal reference system and projection of the input DEM (via the EPSG code), as well as its vertical reference system (via the geoid grid). The `-t_srs` parameter indicates all these parameters for the output DEM.

- In this example, the NAD83(CSRS) / UTM zone 14N (EPSG:3158) projection is used, for both input and output. Additionally, geoid grids referenced to the 2010 epoch are used. To perform the reverse transformation (i.e., CGVD2013 to CGVD28), simply invert the geoid grids.

- This gdalwarp command applies the transformation to a single DEM at a time. To perform the same transformation on all DEMs in a folder, you can use and adapt the [.bat file](../assets/scripts/cgvd2013_to_cgvd28_entirefolder.bat).

- When performing a vertical transformation, it is generally recommended to use the geoid grid corresponding to the epoch of the geometric reference system associated with the dataset. However, the differences due to an epoch change -- for example, between 1997 and 2010 in the context of NAD83(CSRS) -- are generally on the order of a few centimeters across the country. Their impact may therefore be negligible for a DEM, especially if the resolution and vertical accuracy of the DEM are not sufficient to detect such a variation.

## Verifying the Transformation Result

Once the DEM is converted, it is recommended to perform an independent verification to ensure that the vertical transformation has been correctly applied. Here are two complementary validation methods: inspection in QGIS and comparison with values calculated using the [GPS.H](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/gpsh.php) tool provided by the [Canadian Geodetic Survey](https://natural-resources.canada.ca/science-data/science-research/geomatics/geodetic-reference-systems).

### Verification Steps in QGIS

1. Open the input DEM (in CGVD28) and the converted DEM (in CGVD2013) in QGIS.
2. Use the 'Identify Features' tool to query the elevation values at the same location.
3. Compare the obtained values: they should show a difference corresponding to the variation between the two geoids at that location, according to the grids used in the transformation.

Example comparison for a given coordinate:

| **XY Coordinates** | **CGVD28 DEM (Z)** | **CGVD2013 DEM (Z)** |
|--------------------|--------------------|--------------------|
| 631 182 E, 5 519 465 N | 232.56 m | 232.18 m |

<img width="1035" height="614" alt="image" src="https://github.com/user-attachments/assets/8203eb85-f05b-4ec8-af91-7f393c40aa54" />



### Validation with the GPS.H Tool

After completing the analysis in QGIS, you can confirm the validity of the converted elevations by querying the same XY coordinate in the [GPS.H tool](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/gpsh.php?locale=en) from the [Canadian Geodetic Survey](https://natural-resources.canada.ca/science-data/science-research/geomatics/geodetic-reference-systems). This will confirm that the vertical transformation of the DEM has worked correctly.

<img width="1187" height="731" alt="image" src="https://github.com/user-attachments/assets/8165ec3c-d070-4553-9a2b-5d6b5f724734" />



