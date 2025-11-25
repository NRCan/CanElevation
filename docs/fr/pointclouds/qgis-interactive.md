# Utilisation du produit [Nuages de points lidar - Série CanÉlévation](https://ouvert.canada.ca/data/fr/dataset/7069387e-9986-4297-9f55-0288e9676947) dans QGIS

Ce tutoriel montre comment trouver et charger les nuages de points à l'aide du logiciel [QGIS](https://qgis.org/).

Les instructions sont compatibles avec la version **QGIS 3.40**

Étapes:

* [Ajouter l'index des projets lidar](#ajouter-lindex-des-projets-lidar)
* [Agrandir la carte sur une région d'intérêt](#agrandir-la-carte-sur-une-r%C3%A9gion-dint%C3%A9r%C3%AAt)
* [Ajouter l'index des tuiles lidar](#ajouter-lindex-des-tuiles-lidar)
* [Ouvrir une tuile lidar en 2D](#ouvrir-une-tuile-lidar-en-2d)
* [Ouvrir une vue 3D sur la tuile](#ouvrir-une-vue-3d-sur-la-tuile)

## Ajouter l'index des projets lidar
Cliquer sur l'icône afin d'accéder au *Datasource Manager*.
<kbd><img src= "https://github.com/user-attachments/assets/c7fb6e3e-785f-48da-935a-63da70953ccd" alt="your-image-description"></kbd>

Sélectionner ensuite le type *Vector*. Pour cet exemple, nous utiliserons l'index directement à partir du bucket s3. 
Voici l'url de l'index des projets: 
https://canelevation-lidar-point-clouds.s3-ca-central-1.amazonaws.com/pointclouds_nuagespoints/Index_LiDARprojects_projetslidar.gpkg

![image](https://github.com/user-attachments/assets/83d8dace-4b82-4855-a572-72d86f4b49fa)

## Agrandir la carte sur une région d'intérêt
À ce point, il peut être utile d'agrandir la carte sur une région d'intérêt. Dans le panneau *Browser* situé à gauche, vous pouvez charger le fond de carte *OpenStreetMap* afin d'avoir un fond cartographique permettant de vous localiser.

![image](https://github.com/user-attachments/assets/6820f0d3-3134-4287-9be0-608c946172a4)

Si le fond de carte ne charge pas, changer la projection de la carte pour *Web mercator*. Il suffit de cliquer sur l'icône située en bas à droite de la carte.

![image](https://github.com/user-attachments/assets/2de5dfdf-5cac-470a-afcd-b3b752f6211b)

Vous pouvez maintenant agrandir la carte sur une zone d'intérêt, par exemple, sur la région de Niagara en Ontario.

![image](https://github.com/user-attachments/assets/ff8273df-5de0-4dbe-9f67-7eb883bf04ea)


## Ajouter l'index des tuiles lidar

L'index des tuiles lidar est accessible via l'url suivant:
https://canelevation-lidar-point-clouds.s3-ca-central-1.amazonaws.com/pointclouds_nuagespoints/Index_LiDARtiles_tuileslidar.gpkg

Il peut être chargé de la même façon que pour l'index des projets en utilisant le *Datasource Manager*.

Après ajustement du style, voici la carte représentant les tuiles lidars disponibles pour la région de Niagara.

![image](https://github.com/user-attachments/assets/ea5e6945-276a-41a0-b0ba-e98de9670c21)

## Ouvrir une tuile lidar en 2D

Chaque polygone a un attribut contenant l'URL du fichier lidar en format COPC.

![image](https://github.com/user-attachments/assets/7a833d78-0923-43d0-9172-7b9fc40be7f9)

Cet URL peut alors être utilisé pour charger le nuage de point dans la carte à l'aide du *Datasource Manager*.

![image](https://github.com/user-attachments/assets/973ddf55-e929-4078-9411-aa0dbe1a0b7a)

Les points s'affichent maintenant dans la carte en 2D.
![image](https://github.com/user-attachments/assets/d0d16af4-2e1a-44c8-8628-b87a0522df88)


## Ouvrir une vue 3D sur la tuile

Afin de profiter pleinement du jeu de données, nous allons maintenant ouvrir une vue 3D. Le nuage contient des points de différentes classes tels que sol (classe 2), bâtiments (classe 5), etc. Pour la vue 3D, nous vous recommandons de conserver les classes sol, bâtiments et pont. Désactiver toutes les autres dans le panneau *layer* situé à la gauche.

![image](https://github.com/user-attachments/assets/62cf1f91-fd73-4137-a84b-5e8000865bb1)

La vue 3D peut maintenant être créée en cliquant dans *View* > *3d Map views* > *New 3D Map View*.

![image](https://github.com/user-attachments/assets/ba2a1fae-68e9-4114-aa59-c575adc60a42)

Les paramètres de la vue 3D sont nombreux et ne sont pas l'objet de la présente démonstration. Nous vous suggérons de consulter la [documentation de QGIS portant sur la vue 3D](https://docs.qgis.org/3.40/en/docs/user_manual/map_views/3d_map_view.html).





![image](https://github.com/user-attachments/assets/b0c193ba-45a8-426e-9e9c-b96c9b56ca12)










