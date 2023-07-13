::Download the CSV from the GoogleSheets
::Sheets with <space> in the name should be replaced with %20. 
::Using BAT file, escape an extra % like this %%20 instead.
if not exist "2_translated" mkdir 2_translated
curl -L "https://docs.google.com/spreadsheets/d/1fYuy52kEaBRSI5-GOqvuJNegd3w4O75ixesAI7vPAiA/gviz/tq?tqx=out:csv&sheet=Menu&range=A:F" > 2_translated/USRDIR/MESSAGE/tod_msg_menu.csv
curl -L "https://docs.google.com/spreadsheets/d/1fYuy52kEaBRSI5-GOqvuJNegd3w4O75ixesAI7vPAiA/gviz/tq?tqx=out:csv&sheet=Skit&range=A:E" > 2_translated/USRDIR/MESSAGE/tod_msg_skit.csv
curl -L "https://docs.google.com/spreadsheets/d/1fYuy52kEaBRSI5-GOqvuJNegd3w4O75ixesAI7vPAiA/gviz/tq?tqx=out:csv&sheet=Skit_Sub&range=A:E" > 2_translated/USRDIR/MESSAGE/tod_msg_skit_sub.csv

if not exist "3_patched" mkdir 3_patched
::python script.py "path/to/input.csv" "path/to/original.bin" "path/to/output.bin"
python tools/CodeBase/insertionscript.py "2_translated/USRDIR/MESSAGE/tod_msg_menu.csv" "0_data/USRDIR/MESSAGE/tod_msg_menu.msd" "3_patched/USRDIR/MESSAGE/tod_msg_menu.msd"
python tools/CodeBase/insertionscript.py "2_translated/USRDIR/MESSAGE/tod_msg_skit.csv" "0_data/USRDIR/MESSAGE/tod_msg_skit.msd" "3_patched/USRDIR/MESSAGE/tod_msg_skit.msd"
python tools/CodeBase/insertionscript.py "2_translated/USRDIR/MESSAGE/tod_msg_skit_sub.csv" "0_data/USRDIR/MESSAGE/tod_msg_skit_sub.msd" "3_patched/USRDIR/MESSAGE/tod_msg_skit_sub.msd"


::use this to reduce to 8bpp the images so that index8 of gimconv work proprely
::pngquant.exe --force --verbose 256 title.png

::Build command for the gim conversion
pushd "tools/GimConv/"
gimconv ../../2_translated/USRDIR/CLIMAX/data/bg/title.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/bg/title.gim
popd

::Build command for the asm hacks
pushd "tools/Asm/"
armips.exe eboot.asm
armips.exe font.asm
popd

Pause