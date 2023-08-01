::Download the CSV from the GoogleSheets
::Sheets with <space> in the name should be replaced with %20. 
::Using BAT file, escape an extra % like this %%20 instead.
if not exist "2_translated" mkdir 2_translated
curl -L "https://docs.google.com/spreadsheets/d/1fYuy52kEaBRSI5-GOqvuJNegd3w4O75ixesAI7vPAiA/gviz/tq?tqx=out:csv&sheet=Menu&range=A:E" > 2_translated/USRDIR/MESSAGE/tod_msg_menu.csv
curl -L "https://docs.google.com/spreadsheets/d/1fYuy52kEaBRSI5-GOqvuJNegd3w4O75ixesAI7vPAiA/gviz/tq?tqx=out:csv&sheet=Skit&range=A:E" > 2_translated/USRDIR/MESSAGE/tod_msg_skit.csv
curl -L "https://docs.google.com/spreadsheets/d/1fYuy52kEaBRSI5-GOqvuJNegd3w4O75ixesAI7vPAiA/gviz/tq?tqx=out:csv&sheet=Skit_Sub&range=A:E" > 2_translated/USRDIR/MESSAGE/tod_msg_skit_sub.csv

if not exist "3_patched" mkdir 3_patched
::python script.py "path/to/input.csv" "path/to/original.bin" "path/to/output.bin"
python tools/CodeBase/insertionscript.py "2_translated/USRDIR/MESSAGE/tod_msg_menu.csv" "0_data/USRDIR/MESSAGE/tod_msg_menu.msd" "3_patched/USRDIR/MESSAGE/tod_msg_menu.msd"
python tools/CodeBase/insertionscript.py "2_translated/USRDIR/MESSAGE/tod_msg_skit.csv" "0_data/USRDIR/MESSAGE/tod_msg_skit.msd" "3_patched/USRDIR/MESSAGE/tod_msg_skit.msd"
python tools/CodeBase/insertionscript.py "2_translated/USRDIR/MESSAGE/tod_msg_skit_sub.csv" "0_data/USRDIR/MESSAGE/tod_msg_skit_sub.msd" "3_patched/USRDIR/MESSAGE/tod_msg_skit_sub.msd"

::Reduce Png to 8bpp in for the translated folder
@echo off
setlocal enabledelayedexpansion
set "pngquant= tools\Pngquant\pngquant.exe"

for /r "2_translated/USRDIR" %%F in (*.png) do (
    echo Processing: "%%F"
    call %pngquant% --force --verbose 256 --ext .png "%%F"
)

::Convert png to gim for 2d folder need to be --pixel_order faster
@echo off
set "GimConvDir=tools/GimConv"
set "SourceDir=2_translated/USRDIR/2D"

for /r "%SourceDir%" %%F in (*.png) do (
    pushd "%GimConvDir%"
    gimconv.exe "%%F" --pixel_order faster -o "%%~dpF%%~nF.gim"
    popd
)

::::Convert png to gim for CLIMAX folder need to be --image_format index8
::@echo off
::set "GimConvDir=tools/GimConv"
::set "SourceDir=2_translated/USRDIR/CLIMAX"
::
::for /r "%SourceDir%" %%F in (*.png) do (
::    pushd "%GimConvDir%"
::    gimconv.exe "%%F" --image_format index8 -o "%%~dpF%%~nF.gim"
::    popd
::)

::Insert gim in Rssa file (need to be looped eventually)
python tools/CodeBase/gim_insertionv2.py 0_data/USRDIR/2D/copyright.rssa 2_translated/USRDIR/2D/copyright 3_patched/USRDIR/2D

::Build command for the gim conversion for climax need --images_format index8 for this
pushd "tools/GimConv/"
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch001_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch001/ch001_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch002_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch002/ch002_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch003_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch003/ch003_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch004_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch004/ch004_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch005_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch005/ch005_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch006_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch006/ch006_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch007_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch007/ch007_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch008_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch008/ch008_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch009_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch009/ch009_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch010_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch010/ch010_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch011_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch011/ch011_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch012_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch012/ch012_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch013_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch013/ch013_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch014_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch014/ch014_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch015_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch015/ch015_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch016_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch016/ch016_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch017_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch017/ch017_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch018_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch018/ch018_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch019_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch019/ch019_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch020_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch020/ch020_5.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/ch021_5.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch021/ch021_5.gim

gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/vs_ch001.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch001/vs_ch001.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/vs_ch002.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch002/vs_ch002.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/vs_ch003.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch003/vs_ch003.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/vs_ch004.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch004/vs_ch004.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/vs_ch005.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch005/vs_ch005.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/vs_ch006.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch006/vs_ch006.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/_ch/vs_ch007.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/ch007/vs_ch007.gim


gimconv ../../2_translated/USRDIR/CLIMAX/data/bg/title.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/bg/title.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/bg/char_select.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/bg/char_select.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/bg/char_select2.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/bg/char_select2.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/bg/contine.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/bg/contine.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/bg/ranking.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/bg/ranking.gim
gimconv ../../2_translated/USRDIR/CLIMAX/data/bg/ranking2.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/bg/ranking2.gim
popd

::Compress the file back to mgz
python tools/CodeBase/zlibtools.py -c 2_translated/USRDIR/tod.fat 3_patched/USRDIR/tod.fat.mgz

::Build command for the asm hacks
pushd "tools/Asm/"
armips.exe eboot.asm
armips.exe font.asm
popd

Pause