
::Decompress the mgz archive into chain files
::python tools/CodeBase/zlibtools.py 0_data/tod.fat.mgz 1_extracted/tod.fat
python tools/CodeBase/zlibtools.py 0_data/USRDIR/2D/chara_intro_00.chain.mgz 1_extracted/USRDIR/2D/chara_intro_00.chain
::python tools/CodeBase/zlibtools.py 0_data/2D/chara_intro_01.chain.mgz 1_extracted/2D/chara_intro_01.chain
::python tools/CodeBase/zlibtools.py 0_data/USRDIR/2D/c028_00_00.chain.mgz 1_extracted/USRDIR/2D/c028_00_00.chain

::extract the rssa file from the chain file
::python tools/CodeBase/rssatools.py 1_extracted/2D/chara_intro_00.chain
::python tools/CodeBase/rssatools.py 1_extracted/2D/chara_intro_01.chain


::extract the gim files from a rssa file
python tools/CodeBase/gimtools.py 0_data/USRDIR/2D/copyright.rssa 1_extracted/USRDIR/2D/


::This was used to decompress the altered tod.fat from the patch
::python tools/zlibtools.py 0_data/tod.fat.altered.mgz 1_extracted/tod.fat.altered.bin
pause
