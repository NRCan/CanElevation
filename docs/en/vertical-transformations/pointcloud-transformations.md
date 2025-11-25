# Vertical Transformations for Point Clouds

This guide demonstrates how to perform vertical and epoch transformations on point cloud data. Understanding the relationship between vertical datums and epochs is crucial for accurate transformations. Aerial lidar data often reach accuracy in the centimeter range, making these considerations essential.

## Understanding Vertical Datums and Epochs

### CGVD28 - Epoch-less Convention
CGVD28 heights are considered **epoch-less** by convention. This means:

- Orthometric heights in CGVD28 do not change over time
- CGVD28 was based on decades of levelling data
- Heights remain constant regardless of crustal movement

However, since ellipsoidal heights from GNSS **do** change over time, different versions of the HT2 geoid model were created to convert between ellipsoidal heights at specific epochs and CGVD28 orthometric heights:

- **HT2_1997** – converts NAD83(CSRS) ellipsoidal heights in epoch 1997 to CGVD28 orthometric heights
- **HT2_2002** – converts NAD83(CSRS) ellipsoidal heights in epoch 2002 to CGVD28 orthometric heights  
- **HT2_2010** – converts NAD83(CSRS) ellipsoidal heights in epoch 2010 to CGVD28 orthometric heights

### CGVD2013 - Epoch-dependent Heights
CGVD2013 heights **do change over time** as they follow the movement of the Earth's crust:

- Geoid heights (CGG2013a) are considered static in NAD83(CSRS) by convention
- CGVD2013 orthometric heights change at the same rate as ellipsoidal heights (H = h - N)
- The vertical transformation between CGVD28 and CGVD2013 changes over time

## Transformation Scenarios

We cover the following transformation scenarios:

1. **UTM 17N NAD83(CSRS) epoch 2010 CGVD28 → UTM 17N NAD83(CSRS) epoch 2010 CGVD2013** (vertical datum transformation only)
2. **MTM 7 NAD83(CSRS) epoch 1997 CGVD28 → MTM 7 NAD83(CSRS) epoch 2010 CGVD2013** (vertical datum transformation with epoch conversion)
3. **UTM 10N NAD83(CSRS) epoch 2002 CGVD28 → UTM 10N NAD83(CSRS) epoch 2010 CGVD2013** (vertical datum transformation with epoch conversion)

Each scenario is illustrated with examples using both PROJ string notation and NRCAN URN notation. The notation formats are explained in the next section.

## Notation Formats for Vertical Transformations

Before performing transformations, it is important to understand the two notations this tutorial uses to specify coordinate reference systems and vertical datums in PDAL and PROJ. Please note that there are many ways to perform transformations using PROJ definitions. Advanced users can refer to the [online PROJ documentation](https://proj.org/en/stable/usage/index.html).

### PROJ String Notation

The PROJ string notation uses a combination of EPSG codes and geoid grid files to define both the horizontal and vertical reference systems. For example:

```bash
+init=EPSG:2958 +geoidgrids=ca_nrc_HT2_2010v70.tif
```

- `+init=EPSG:xxxx` specifies the horizontal coordinate system (e.g., UTM zone, MTM).
- `+geoidgrids=...` points to the geoid grid file that defines the vertical datum.

This notation is widely supported and allows precise control over the transformation parameters. For this tutorial, **we use it for vertical datum transformations only**. For transformations that include epochs, we use the URN notation.

### NRCAN PROJ URN Notation

NRCan has worked with the PROJ development team to facilitate epoch and vertical datum conversions. Starting with PROJ 9.6, specific `CoordinateMetadata` definitions were added to PROJ, allowing users to reference complex Canadian coordinate systems and vertical datums using a Uniform Resource Name (URN).

The full list of available NRCAN definitions can be queried using:
```bash
sqlite3 %PROJ_DATA%/proj.db "select code from coordinate_metadata where auth_name = 'NRCAN';"
```

The URN must be formatted as:
```
urn:ogc:def:coordinateMetadata:NRCAN::<code>
```
where `<code>` is the identifier from the database.

!!! warning "Missing definitions"
    For now, some definitions are missing from the default PROJ installation. You must install them locally for the next transformations to work.

These definitions can be added to your local PROJ installation by running the following command:

!!! info "Files"
    [📄 Download nrcan_additional_coordinate_metadata.sql](../assets/scripts/nrcan_additional_coordinate_metadata.sql){ .md-button .md-button--primary }

```bash
sqlite3 %PROJ_DATA%/proj.db ".read D:/dev/CanElevation/docs/assets/scripts/nrcan_additional_coordinate_metadata.sql"
```

This notation simplifies the specification of common Canadian coordinate systems, **including epoch and vertical datum**, and ensures consistency with official NRCAN definitions.

---

## Performing Transformations with PDAL

[PDAL (Point Data Abstraction Library)](https://pdal.io/) is a powerful tool for processing point cloud data. We use its `translate` command with the `filters.reprojection` filter to perform transformations.

### Vertical Datum Transformation: Same Horizontal Epoch

For transformations within the same horizontal epoch, both PROJ String notation and URN notation can be used.
We will show how to apply a vertical datum transformation from **UTM 17N NAD83(CSRS) epoch 2010 CGVD28** to **UTM 17N NAD83(CSRS) epoch 2010 CGVD2013**. Since CGVD28 is epoch-less, we specify the epoch (2010) for the appropriate HT2 grid to convert to CGVD2013.

<!-- Validated using gps-h 
input coordinates: 673375.980 4891478.970 263.760
output coordinates: 673375.980 4891478.970 263.409-->
!!! info "Files"
    [📄 Download input_utm17n_nad83csrs2010_cgvd28.laz](../assets/sample_data/pointcloud/input_utm17n_nad83csrs2010_cgvd28.laz){ .md-button .md-button--primary }

**PROJ string notation:**

```bash
pdal translate ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\input_utm17n_nad83csrs2010_cgvd28.laz ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\output_utm17n_nad83csrs2010_cgvd2013.laz ^
--filters.reprojection.in_srs="+init=EPSG:2958 +geoidgrids=ca_nrc_HT2_2010v70.tif" ^
--filters.reprojection.out_srs="+init=EPSG:2958 +geoidgrids=ca_nrc_CGG2013an83.tif" ^
filters.reprojection
```

**NRCAN URN notation:**
```bash
pdal translate ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\input_utm17n_nad83csrs2010_cgvd28.laz ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\output_utm17n_nad83csrs2010_cgvd2013.laz ^
--filters.reprojection.in_srs="urn:ogc:def:coordinateMetadata:NRCAN::NAD83_CSRS_2010_UTM17_HT2_2010" ^
--filters.reprojection.out_srs="urn:ogc:def:coordinateMetadata:NRCAN::NAD83_CSRS_2010_UTM17_CGVD2013_2010" ^
filters.reprojection
```

### Working with Different Horizontal Epochs

For point clouds with centimeter-level accuracy, accounting for differences in horizontal epochs is important when converting from CGVD28 to CGVD2013. The PROJ String notation used in the previous example cannot handle epoch conversion. Therefore, the following transformation scenarios use the **NRCAN URN** notation only.

### MTM 7 NAD83(CSRS) epoch 1997 CGVD28 → MTM 7 NAD83(CSRS) epoch 2010 CGVD2013

This transformation handles input data where the horizontal coordinates were acquired in epoch 1997. The appropriate HT2_1997 grid is used for the CGVD28 conversion, and the output converts both horizontal coordinates to epoch 2010 and vertical to CGVD2013.

<!-- Validated using both TRX and gps-h 
Conversion du vertical dans gps-h en utilisant HT2_1997_TO_CGG2013a. 71.525 -> 71.192.
Utilisation de la valeur 71.192 dans TRX afin d'appliquer la transformation d'époque.
input coordinates: 259800.461 5359998.81 71.525
output coordinates:   259800.494 5359998.810 71.25-->

!!! info "Files"
    [📄 Download input_mtm7_nad83csrs1997_cgvd28.laz](../assets/sample_data/pointcloud/input_mtm7_nad83csrs1997_cgvd28.laz){ .md-button .md-button--primary }

```bash
pdal translate ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\input_mtm7_nad83csrs1997_cgvd28.laz ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\output_mtm7_nad83csrs2010_cgvd2013.laz ^
 --filters.reprojection.in_srs="urn:ogc:def:coordinateMetadata:NRCAN::NAD83_CSRS_1997_MTM7_HT2_1997" ^
 --filters.reprojection.out_srs="urn:ogc:def:coordinateMetadata:NRCAN::NAD83_CSRS_2010_MTM7_CGVD2013_2010" ^
 filters.reprojection
```

### UTM 10N NAD83(CSRS) epoch 2002 CGVD28 → UTM 10N NAD83(CSRS) epoch 2010 CGVD2013

This transformation handles input data where the horizontal coordinates were acquired in epoch 2002. The appropriate HT2_2002 grid is used for the CGVD28 conversion, and the output converts both horizontal coordinates to epoch 2010 and vertical to CGVD2013.

<!-- Validated using both TRX and gps-h 
Conversion du vertical dans gps-h en utilisant HT2_2002_TO_CGG2013a. 1808.58 -> 1808.876.
Utilisation de la valeur 1808.876 dans TRX afin d'appliquer la transformation d'époque.
input coordinates: 550723.16 5659804.74 1808.58
output coordinates: 550723.19 5659804.76 1808.89-->

!!! info "Files"
    [📄 Download input_utm10n_nad83csrs2002_cgvd28.laz](../assets/sample_data/pointcloud/input_utm10n_nad83csrs2002_cgvd28.laz){ .md-button .md-button--primary }

```bash
pdal translate ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\input_utm10n_nad83csrs2002_cgvd28.laz ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\output_utm10n_nad83csrs2010_cgvd2013.laz ^
--filters.reprojection.in_srs="urn:ogc:def:coordinateMetadata:NRCAN::NAD83_CSRS_2002_UTM10_HT2_2002" ^
--filters.reprojection.out_srs="urn:ogc:def:coordinateMetadata:NRCAN::NAD83_CSRS_2010_UTM10_CGVD2013_2010" ^
filters.reprojection
```

## Verifying Transformation Results

Once the point cloud has been transformed, it is recommended to perform an independent verification to ensure that the vertical transformation has been correctly applied. Here are two complementary validation methods: inspection in QGIS and comparison with values calculated using [GPS.H](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/gpsh.php?locale=en) and [TRX](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/trx.php?locale=en) tools provided by the [Canadian Geodetic Survey](https://natural-resources.canada.ca/science-data/science-research/geomatics/geodetic-reference-systems).

### Validation Steps in QGIS

These steps can be used to validate vertical datum transformations only. **To validate epoch conversion, please use the instructions in the next section.**

1. Open the input point cloud (in CGVD28) and the converted point cloud (in CGVD2013) in QGIS.
2. Add the conversion grid corresponding to the transformation you performed (see the table below).
3. Use the 'Identify Features' tool or the point cloud profile tool to query elevation values at the same location.
4. Compare the obtained values: they should show a difference corresponding to the variation between the two geoids at that location, according to the grids used in the transformation.

The following screenshot illustrates the result obtained. The value of the separation grid (HT2_2010_CGG2013a_tif) is 35 cm, which corresponds to the difference between the point elevation in CGVD28 and CGVD2013 at the same location, which are 266.57 m and 266.22 m respectively.

![image](../assets/images/QGIS_validation.png)

**Conversion grids for CGVD28 to CGVD2013 datum conversion**

The conversion grid to use depends on the **target epoch** of your CGVD2013 output, since CGVD2013 heights change over time while CGVD28 heights remain constant.

| Target CGVD2013 Epoch | Grid link |
| ----- | --------- |
| 1997 | [HT2_1997_CGG2013a_tif](https://cdn.proj.org/ca_nrc_HT2_1997_CGG2013a.tif) |
| 2002 | [HT2_2002_CGG2013a_tif](https://cdn.proj.org/ca_nrc_HT2_2002v70_CGG2013a.tif) |
| 2010 | [HT2_2010_CGG2013a_tif](https://cdn.proj.org/ca_nrc_HT2_2010v70_CGG2013a.tif) |

### Validation with GPS.H and TRX Tools

#### GPS.H

After completing the analysis in QGIS, you can confirm the validity of the converted elevations by querying the same XY coordinate in the [GPS.H tool](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/gpsh.php?locale=en) from the [Canadian Geodetic Survey](https://natural-resources.canada.ca/science-data/science-research/geomatics/geodetic-reference-systems). This will confirm that the vertical transformation of the point cloud has been applied correctly.

Here, we are using the resulting file from the last conversion (UTM 10N NAD83(CSRS) epoch 2002 CGVD28 → UTM 10N NAD83(CSRS) epoch 2010 CGVD2013). We test the following input coordinate:

|| X | Y | Z |
|| --- | ----| ----|
| input | 550723.16 | 5659804.74 | 1808.58 |
| output | 550723.19 | 5659804.76 | 1808.89 |

The following command is useful to get a single point's details using PDAL. By using it on both the input and output files for the same point ID, you get the coordinates of a point before and after the transformation.

```bash
cd docs\assets\sample_data\pointcloud
pdal info output_utm10n_nad83csrs2010_cgvd2013.laz -p 0
```

In GPS.H, we choose the appropriate mode (Convert) and the grid corresponding to the transformation we performed. Again, since CGVD28 heights are static, we use the conversion grid corresponding to the **target epoch**, which is **HT2_2010_to_CGG2013a**. We then add the input coordinates and calculate the corresponding CGVD2013 height.

![image](../assets/images/gps-h_scenario3.png)


#### TRX

Using TRX, we can validate the X and Y coordinates we obtained to ensure the epoch conversion was performed properly.
We will use the same input values we used in the last section. We can skip the Z value since GPS.H already provided a value that included the epoch conversion. 

![image](../assets/images/TRX_scenario3.png)

The resulting h value represents the height difference caused by the epoch change (2002 to 2010) at the given X and Y coordinates. Again, this epoch change was considered for the Z conversion using GPS.H, so we don't have to address it separately.

**You should** ensure that the resulting X and Y coordinates match those in the resulting files. If this is not the case, please review the coordinates and parameters you have used to make sure they are correct.







