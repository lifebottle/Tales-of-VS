::python tools/gziptools.py uncompress 0_data/tod.fat.mgz 1_extracted/tod.fat.txt
python tools/zlibtools.py 0_data/tod.fat.mgz 1_extracted/tod.fat.bin
::python tools/zlibtools.py 0_data/tod.fat.altered.mgz 1_extracted/tod.fat.altered.bin
pause
