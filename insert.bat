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

::Reduce Png to 8bpp in 2D folder
@echo off
setlocal enabledelayedexpansion
set "pngquant= tools\Pngquant\pngquant.exe"

for /r "2_translated/USRDIR/2D" %%F in (*.png) do (
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

::Insert gim in Rssa file (need to be looped eventually)
python tools/CodeBase/gim_insertionv2.py 0_data/USRDIR/2D/copyright.rssa 2_translated/USRDIR/2D/copyright 3_patched/USRDIR/2D

::Build command for the gim conversion for climax need --images_format index8 for this
pushd "tools/GimConv/"
gimconv ../../2_translated/USRDIR/CLIMAX/data/bg/title.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/bg/title.gim
popd

::Compress the file back to mgz
python tools/CodeBase/zlibtools.py -c 2_translated/USRDIR/tod.fat 3_patched/USRDIR/tod.fat.mgz

::Build command for the asm hacks
pushd "tools/Asm/"
armips.exe eboot.asm
armips.exe font.asm
popd

Pause