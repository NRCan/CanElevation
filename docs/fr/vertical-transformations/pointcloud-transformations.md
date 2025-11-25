# Transformations verticales de nuages de points

Ce guide explique comment effectuer des transformations verticales et d'époques sur des données de nuages de points. Comprendre la relation entre les systèmes altimétriques et les époques est crucial pour des transformations précises. Les données lidar aériennes atteignent souvent une précision de l'ordre du centimètre, rendant ces considérations essentielles.

## Comprendre les systèmes altimétriques et les époques

### CGVD28 - Convention sans époque
Les hauteurs CGVD28 sont considérées **sans époque** par convention. Cela signifie :

- Les hauteurs orthométriques en CGVD28 ne changent pas avec le temps
- Le CGVD28 est basé sur des décennies de données de nivellement
- Les hauteurs restent constantes indépendamment du mouvement de la croûte terrestre

Cependant, puisque les hauteurs ellipsoïdales des GNSS **changent** avec le temps, différentes versions du modèle de géoïde HT2 ont été créées pour convertir entre les hauteurs ellipsoïdales à des époques spécifiques et les hauteurs orthométriques CGVD28 :

- **HT2_1997** – convertit les hauteurs ellipsoïdales NAD83(SCRS) à l'époque 1997 en hauteurs orthométriques CGVD28
- **HT2_2002** – convertit les hauteurs ellipsoïdales NAD83(SCRS) à l'époque 2002 en hauteurs orthométriques CGVD28  
- **HT2_2010** – convertit les hauteurs ellipsoïdales NAD83(SCRS) à l'époque 2010 en hauteurs orthométriques CGVD28

### CGVD2013 - Hauteurs variables selon l'époque
Les hauteurs CGVD2013 **changent avec le temps** car elles suivent le mouvement de la croûte terrestre :

- Les hauteurs de géoïde (CGG2013a) sont considérées statiques dans NAD83(SCRS) par convention
- Les hauteurs orthométriques CGVD2013 changent au même rythme que les hauteurs ellipsoïdales (H = h - N)
- La transformation verticale entre CGVD28 et CGVD2013 change avec le temps

## Scénarios de transformation

Nous démontrons les scénarios de transformation suivants :

1. **UTM 17N NAD83(SCRS) époque 2010 CGVD28 → UTM 17N NAD83(SCRS) époque 2010 CGVD2013** (transformation de datum vertical seulement)
2. **MTM 7 NAD83(SCRS) époque 1997 CGVD28 → MTM 7 NAD83(SCRS) époque 2010 CGVD2013** (transformation de datum vertical avec conversion d'époque)
3. **UTM 10N NAD83(SCRS) époque 2002 CGVD28 → UTM 10N NAD83(SCRS) époque 2010 CGVD2013** (transformation de datum vertical avec conversion d'époque)

Chaque scénario est illustré avec des exemples utilisant la notation PROJ string et la notation URN NRCAN. Les formats de notation sont expliqués dans la section suivante.

## Formats de notation pour les transformations verticales

Avant d'effectuer les transformations, il est important de comprendre les deux notations utilisées dans ce tutoriel pour spécifier les systèmes de référence de coordonnées et les systèmes altimétriques dans PDAL et PROJ. Veuillez noter qu'il existe de nombreuses façons d'effectuer des transformations en utilisant les définitions PROJ. Les utilisateurs avancés peuvent consulter la [documentation PROJ en ligne](https://proj.org/en/stable/usage/index.html).

### Notation PROJ string

La notation PROJ string utilise une combinaison de codes EPSG et de fichiers de grille de géoïde pour définir à la fois le système de référence horizontal et vertical. Par exemple :

```bash
+init=EPSG:2958 +geoidgrids=ca_nrc_HT2_2010v70.tif
```

- `+init=EPSG:xxxx` spécifie le système de coordonnées horizontal (ex. : zone UTM, MTM).
- `+geoidgrids=...` pointe vers le fichier de grille de géoïde qui définit le datum vertical.

Cette notation est largement supportée et permet un contrôle précis des paramètres de transformation. Pour ce tutoriel, **nous l'utilisons uniquement pour les transformations de datum verticaux**. Pour les transformations qui incluent les époques, nous utilisons la notation URN.

### Notation URN NRCAN PROJ

RNCan a collaboré avec l'équipe de développement PROJ pour faciliter les conversions d'époques et de datum verticaux. Depuis PROJ 9.6, des définitions spécifiques `CoordinateMetadata` ont été ajoutées à PROJ, permettant aux utilisateurs de référencer des systèmes de coordonnées canadiens complexes et des systèmes altimétriques à l'aide d'un nom de ressource uniforme (URN).

La liste complète des définitions NRCAN disponibles peut être obtenue avec :
```bash
sqlite3 %PROJ_DATA%/proj.db "select code from coordinate_metadata where auth_name = 'NRCAN';"
```

Le format du URN doit être :
```
urn:ogc:def:coordinateMetadata:NRCAN::<code>
```
où `<code>` est l'identifiant issu de la base de données.

!!! warning "Définitions manquantes"
    Pour l'instant, certaines définitions sont manquantes de l'installation PROJ par défaut. Vous devrez les installer localement afin que les prochaines transformations fonctionnent.

Ces définitions peuvent être ajoutées à votre installation PROJ locale en exécutant la commande suivante :

!!! info "Fichiers"
    [📄 Télécharger nrcan_additional_coordinate_metadata.sql](../assets/scripts/nrcan_additional_coordinate_metadata.sql){ .md-button .md-button--primary }

```bash
sqlite3 %PROJ_DATA%\proj.db ".read D:/dev/CanElevation/docs/assets/scripts/nrcan_additional_coordinate_metadata.sql"
```

Cette notation simplifie la définition des systèmes de coordonnées canadiens courants, **incluant l'époque et le datum vertical**, et assure la cohérence avec les définitions officielles de RNCan.

---

## Réaliser les transformations avec PDAL

[PDAL (Point Data Abstraction Library)](https://pdal.io/) est un outil puissant pour le traitement des nuages de points. Nous utilisons sa commande `translate` avec le filtre `filters.reprojection` pour effectuer les transformations.

### Transformation de système altimétrique : Même époque horizontale

Pour les transformations au sein de la même époque horizontale, les notations PROJ String et URN peuvent être utilisées.
Nous montrerons comment appliquer une transformation de système altimétrique vertical de **UTM 17N NAD83(SCRS) époque 2010 CGVD28** vers **UTM 17N NAD83(SCRS) époque 2010 CGVD2013**. Puisque CGVD28 est sans époque, nous spécifions la grille HT2 appropriée (HT2_2010) pour convertir vers CGVD2013.

<!-- Validated using gps-h 
input coordinates: 673375.980 4891478.970 263.760
output coordinates: 673375.980 4891478.970 263.409-->
!!! info "Fichiers"
    [📄 Télécharger input_utm17n_nad83csrs2010_cgvd28.laz](../assets/sample_data/pointcloud/input_utm17n_nad83csrs2010_cgvd28.laz){ .md-button .md-button--primary }

**Notation PROJ string :**

```bash
pdal translate ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\input_utm17n_nad83csrs2010_cgvd28.laz ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\output_utm17n_nad83csrs2010_cgvd2013.laz ^
--filters.reprojection.in_srs="+init=EPSG:2958 +geoidgrids=ca_nrc_HT2_2010v70.tif" ^
--filters.reprojection.out_srs="+init=EPSG:2958 +geoidgrids=ca_nrc_CGG2013an83.tif" ^
filters.reprojection
```

**Notation URN NRCAN :**
```bash
pdal translate ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\input_utm17n_nad83csrs2010_cgvd28.laz ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\output_utm17n_nad83csrs2010_cgvd2013.laz ^
--filters.reprojection.in_srs="urn:ogc:def:coordinateMetadata:NRCAN::NAD83_CSRS_2010_UTM17_HT2_2010" ^
--filters.reprojection.out_srs="urn:ogc:def:coordinateMetadata:NRCAN::NAD83_CSRS_2010_UTM17_CGVD2013_2010" ^
filters.reprojection
```

### Travailler avec différentes époques horizontales

Pour les nuages de points avec une précision centimétrique, la prise en compte des différences d'époques horizontales est importante lors de la conversion de CGVD28 vers CGVD2013. La notation PROJ String utilisée dans l'exemple précédent ne peut pas gérer la conversion d'époque. Par conséquent, les scénarios de transformation suivants utilisent **uniquement** la notation **URN NRCAN**.

### MTM 7 NAD83(SCRS) époque 1997 CGVD28 → MTM 7 NAD83(SCRS) époque 2010 CGVD2013

Cette transformation traite les données pour lesquelles les coordonnées horizontales ont été acquises à l'époque 1997. La grille HT2_1997 appropriée est utilisée pour la conversion CGVD28, et la sortie convertit à la fois les coordonnées horizontales vers l'époque 2010 et verticales vers CGVD2013.

<!-- Validated using both TRX and gps-h 
Conversion du vertical dans gps-h en utilisant HT2_1997_TO_CGG2013a. 71.525 -> 71.192.
Utilisation de la valeur 71.192 dans TRX afin d'appliquer la transformation d'époque.
input coordinates: 259800.461 5359998.81 71.525
output coordinates:   259800.494 5359998.810 71.25-->

!!! info "Fichiers"
    [📄 Télécharger input_mtm7_nad83csrs1997_cgvd28.laz](../assets/sample_data/pointcloud/input_mtm7_nad83csrs1997_cgvd28.laz){ .md-button .md-button--primary }

```bash
pdal translate ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\input_mtm7_nad83csrs1997_cgvd28.laz ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\output_mtm7_nad83csrs2010_cgvd2013.laz ^
--filters.reprojection.in_srs="urn:ogc:def:coordinateMetadata:NRCAN::NAD83_CSRS_1997_MTM7_HT2_1997" ^
--filters.reprojection.out_srs="urn:ogc:def:coordinateMetadata:NRCAN::NAD83_CSRS_2010_MTM7_CGVD2013_2010" ^
filters.reprojection
```

### UTM 10N NAD83(SCRS) époque 2002 CGVD28 → UTM 10N NAD83(SCRS) époque 2010 CGVD2013

Cette transformation traite les données d'entrée où les coordonnées horizontales ont été acquises à l'époque 2002. La grille HT2_2002 appropriée est utilisée pour la conversion CGVD28, et la sortie convertit à la fois les coordonnées horizontales vers l'époque 2010 et verticales vers CGVD2013.

<!-- Validated using both TRX and gps-h 
Conversion du vertical dans gps-h en utilisant HT2_2002_TO_CGG2013a. 1808.58 -> 1808.876.
Utilisation de la valeur 1808.876 dans TRX afin d'appliquer la transformation d'époque.
input coordinates: 550723.16 5659804.74 1808.58
output coordinates: 550723.19 5659804.76 1808.89-->

!!! info "Fichiers"
    [📄 Télécharger input_utm10n_nad83csrs2002_cgvd28.laz](../assets/sample_data/pointcloud/input_utm10n_nad83csrs2002_cgvd28.laz){ .md-button .md-button--primary }

```bash
pdal translate ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\input_utm10n_nad83csrs2002_cgvd28.laz ^
D:\dev\CanElevation\docs\assets\sample_data\pointcloud\output_utm10n_nad83csrs2010_cgvd2013.laz ^
--filters.reprojection.in_srs="urn:ogc:def:coordinateMetadata:NRCAN::NAD83_CSRS_2002_UTM10_HT2_2002" ^
--filters.reprojection.out_srs="urn:ogc:def:coordinateMetadata:NRCAN::NAD83_CSRS_2010_UTM10_CGVD2013_2010" ^
filters.reprojection
```

## Vérification des résultats de transformation

Une fois le nuage de points transformé, il est recommandé d'effectuer une vérification indépendante pour s'assurer que la transformation verticale a été correctement appliquée. Voici deux méthodes de validation complémentaires : l'inspection dans QGIS et la comparaison avec les valeurs calculées à l'aide des outils [GPS.H](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/gpsh.php?locale=fr) et [TRX](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/trx.php?locale=fr) fournis par les [Levés géodésiques du Canada](https://ressources-naturelles.canada.ca/science-donnees/science-recherche/geomatique/science-recherche-systemes-reference-geodesique).

### Étapes de validation dans QGIS

Ces étapes peuvent être utilisées pour valider uniquement les transformations de datums verticaux. **Pour valider la conversion d'époque, veuillez utiliser les instructions de la section suivante.**

1. Ouvrir le nuage de points d'entrée (en CGVD28) et le nuage de points converti (en CGVD2013) dans QGIS.
2. Ajouter la grille de conversion correspondant à la transformation que vous avez effectuée (voir le tableau ci-dessous).
3. Utiliser l'outil 'Identifier les entités' ou l'outil de profil de nuage de points pour interroger les valeurs d'élévation au même emplacement.
4. Comparer les valeurs obtenues : elles devraient présenter une différence correspondant à la variation entre les deux géoïdes à cet emplacement, selon les grilles utilisées dans la transformation.

La capture suivante illustre le résultat obtenu. La valeur de la grille de séparation (HT2_2010_CGG2013a_tif) est de 35 cm ce qui correspond à la différence entre l'élévation du point en CGVD28 et en CGVD2013 au même endroit soit respectivement, 266.57 m et 266.22 m.

![image](../assets/images/QGIS_validation.png)

**Grilles de conversion pour la conversion de système altimétrique CGVD28 vers CGVD2013**

La grille de conversion à utiliser dépend de **l'époque cible** de votre sortie CGVD2013, puisque les hauteurs CGVD2013 changent avec le temps tandis que les hauteurs CGVD28 restent constantes.

| Époque CGVD2013 cible | Lien vers la grille |
| ----- | --------- |
| 1997 | [HT2_1997_CGG2013a_tif](https://cdn.proj.org/ca_nrc_HT2_1997_CGG2013a.tif) |
| 2002 | [HT2_2002_CGG2013a_tif](https://cdn.proj.org/ca_nrc_HT2_2002v70_CGG2013a.tif) |
| 2010 | [HT2_2010_CGG2013a_tif](https://cdn.proj.org/ca_nrc_HT2_2010v70_CGG2013a.tif) |

### Validation avec les outils GPS.H et TRX

#### GPS.H

Après avoir complété l'analyse dans QGIS, vous pouvez confirmer la validité des élévations converties en interrogeant la même coordonnée XY dans l'[outil GPS.H](https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/gpsh.php?locale=fr) des [Levés géodésiques du Canada](https://ressources-naturelles.canada.ca/science-donnees/science-recherche/geomatique/science-recherche-systemes-reference-geodesique). Cela confirmera que la transformation verticale du nuage de points a été appliquée correctement.

Ici, nous utilisons le fichier résultant de la dernière conversion (UTM 10N NAD83(SCRS) époque 2002 CGVD28 → UTM 10N NAD83(SCRS) époque 2010 CGVD2013). Nous testons la coordonnée d'entrée suivante :

|| X | Y | Z |
|| --- | ----| ----|
| entrée | 550723.16 | 5659804.74 | 1808.58 |
| sortie | 550723.19 | 5659804.76 | 1808.89 |

La commande suivante est utile pour obtenir les détails d'un point unique à l'aide de PDAL. En l'utilisant à la fois sur les fichiers d'entrée et de sortie pour le même identifiant de point, vous obtenez les coordonnées d'un point avant et après la transformation.

```bash
cd docs\assets\sample_data\pointcloud
pdal info output_utm10n_nad83csrs2010_cgvd2013.laz -p 0
```

Dans GPS.H, nous choisissons le mode approprié (Convert) et la grille correspondant à la transformation que nous avons effectuée. Encore une fois, puisque les hauteurs CGVD28 sont statiques, nous utilisons la grille de conversion correspondant à **l'époque cible**, qui est **HT2_2010_to_CGG2013a**. Nous ajoutons ensuite les coordonnées d'entrée et calculons la hauteur CGVD2013 correspondante.

![image](../assets/images/gps-h_scenario3.png)


#### TRX

En utilisant TRX, nous pouvons valider les coordonnées X et Y que nous avons obtenues pour nous assurer que la conversion d'époque a été effectuée correctement.
Nous utiliserons les mêmes valeurs d'entrée que nous avons utilisées dans la dernière section. Nous pouvons ignorer la valeur Z puisque GPS.H a déjà fourni une valeur qui incluait la conversion d'époque.

![image](../assets/images/TRX_scenario3.png)

La valeur h résultante représente la différence de hauteur causée par le changement d'époque (2002 à 2010) aux coordonnées X et Y données. Encore une fois, ce changement d'époque a été pris en compte pour la conversion Z en utilisant GPS.H, donc nous n'avons pas à le traiter séparément.

**Vous devriez** vous assurer que les coordonnées X et Y résultantes correspondent à celles des fichiers résultants. Si ce n'est pas le cas, veuillez réviser les coordonnées et paramètres que vous avez utilisés pour vous assurer qu'ils sont corrects.
