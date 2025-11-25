
# Using the [LiDAR Point Clouds - CanElevation Series](https://open.canada.ca/data/en/dataset/7069387e-9986-4297-9f55-0288e9676947) product in QGIS

This tutorial shows how to find and load point clouds using [QGIS software](https://qgis.org/).

The instructions are compatible with version **QGIS 3.40**.

Steps:

* [Add the lidar project index](#add-the-lidar-project-index)
* [Zoom in on a region of interest](#zoom-in-on-a-region-of-interest)
* [Add the lidar tile index](#add-the-lidar-tile-index)
* [Open a lidar tile in 2D](#open-a-lidar-tile-in-2d)
* [Open a 3D view of the tile](#open-a-3d-view-of-the-tile)

## Add the lidar project index

Click on the icon to access the *Datasource Manager*.

<kbd><img src= "https://github.com/user-attachments/assets/c7fb6e3e-785f-48da-935a-63da70953ccd" alt="your-image-description"></kbd>

Then select the *Vector* type. For this example, we will use the index directly from the s3 bucket. 
Here is the URL of the project index: 
https://canelevation-lidar-point-clouds.s3-ca-central-1.amazonaws.com/pointclouds_nuagespoints/Index_LiDARprojects_projetslidar.gpkg

![image](https://github.com/user-attachments/assets/83d8dace-4b82-4855-a572-72d86f4b49fa)

## Zoom in on a region of interest

At this point, it may be useful to zoom in on a region of interest. In the *Browser panel* on the left, you can load the OpenStreetMap basemap to have a cartographic background that allows you to locate yourself.

![image](https://github.com/user-attachments/assets/6820f0d3-3134-4287-9be0-608c946172a4)

If the basemap doesn't load, change the map projection to Web Mercator. Simply click on the icon located at the bottom right of the map.

![image](https://github.com/user-attachments/assets/2de5dfdf-5cac-470a-afcd-b3b752f6211b)

You can now zoom in on an area of interest, for example, the Niagara region in Ontario.

![image](https://github.com/user-attachments/assets/ff8273df-5de0-4dbe-9f67-7eb883bf04ea)

## Add the lidar tile index

The lidar tile index is accessible via the following URL:
https://canelevation-lidar-point-clouds.s3-ca-central-1.amazonaws.com/pointclouds_nuagespoints/Index_LiDARtiles_tuileslidar.gpkg

It can be loaded in the same way as the project index using the *Datasource Manager*.

After adjusting the style, here is the map showing the lidar tiles available for the Niagara region.

![image](https://github.com/user-attachments/assets/ea5e6945-276a-41a0-b0ba-e98de9670c21)


## Open a lidar tile in 2D

Each polygon has an attribute containing the URL of the lidar file in [COPC format](https://copc.io/).

![image](https://github.com/user-attachments/assets/7a833d78-0923-43d0-9172-7b9fc40be7f9)

This URL can then be used to load the point cloud on the map using the *Datasource Manager*.

![image](https://github.com/user-attachments/assets/973ddf55-e929-4078-9411-aa0dbe1a0b7a)

The points are now displayed on the 2D map.

![image](https://github.com/user-attachments/assets/d0d16af4-2e1a-44c8-8628-b87a0522df88)

## Open a 3D view of the tile

To fully benefit from the dataset, we will now open a 3D view. The cloud contains points of different classes such as ground (class 2), building (class 5), etc. For the 3D view, we recommend keeping the ground, buildings, and bridge classes. Disable all others in the layer panel on the left.

![image](https://github.com/user-attachments/assets/62cf1f91-fd73-4137-a84b-5e8000865bb1)

The 3D view can now be created by clicking on *View* > *3D Map views* > *New 3D Map View*.

![image](https://github.com/user-attachments/assets/ba2a1fae-68e9-4114-aa59-c575adc60a42)

There are many 3D view settings available; however, since this is not the topic of this demonstration, we suggest you consult the 
[QGIS documentation on the 3D view](https://docs.qgis.org/3.40/en/docs/user_manual/map_views/3d_map_view.html).

![image](https://github.com/user-attachments/assets/b0c193ba-45a8-426e-9e9c-b96c9b56ca12)

