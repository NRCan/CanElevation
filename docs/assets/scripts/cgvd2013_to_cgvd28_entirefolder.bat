@echo off
setlocal enabledelayedexpansion

set input_folder=D:\tutoriel\sample_data\CGVD2013
set output_folder=D:\tutoriel\sample_data\CGVD28

rem Loop through all tif files in input folder
for %%f in ("%input_folder%\*.tif") do (
    rem Get just the filename (no path)
    set filename=%%~nxf

    rem Build full input and output paths
    set input_file=%%f
    set output_file=%output_folder%\!filename!

    echo Processing !input_file! ...
	gdalwarp -co COMPRESS=LZW -multi -wo NUM_THREADS=4 -s_srs "+init=EPSG:3158 +geoidgrids=ca_nrc_CGG2013an83.tif" -t_srs "+init=EPSG:3158 +geoidgrids=ca_nrc_HT2_2010v70.tif" "!input_file!" "!output_file!"

    echo Done with !filename!
)

echo All done.
pause