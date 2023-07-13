::python tools/gziptools.py uncompress 0_data/tod.fat.mgz 1_extracted/tod.fat.txt
::python tools/CodeBase/zlibtools.py 0_data/tod.fat.mgz 1_extracted/tod.fat
::python tools/CodeBase/zlibtools.py 0_data/2D/chara_intro_00.chain.mgz 1_extracted/2D/chara_intro_00.chain
::python tools/CodeBase/zlibtools.py 0_data/2D/chara_intro_01.chain.mgz 1_extracted/2D/chara_intro_01.chain
python tools/CodeBase/zlibtools.py 0_data/2D/c028_00_00.chain.mgz 1_extracted/2D/c028_00_00.chain


::python tools/CodeBase/rssatools.py 1_extracted/2D/chara_intro_00.chain
::python tools/CodeBase/rssatools.py 1_extracted/2D/chara_intro_01.chain



::python tools/zlibtools.py 0_data/tod.fat.altered.mgz 1_extracted/tod.fat.altered.bin
pause
