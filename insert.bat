::Download the CSV from the GoogleSheets
::Sheets with <space> in the name should be replaced with %20. 
::Using BAT file, escape an extra % like this %%20 instead.
if not exist "2_translated" mkdir 2_translated

curl -L "https://docs.google.com/spreadsheets/d/1fYuy52kEaBRSI5-GOqvuJNegd3w4O75ixesAI7vPAiA/gviz/tq?tqx=out:csv&sheet=Menu&range=A:F" > 2_translated/tod_msg_menu.csv

::python script.py "path/to/input.csv" "path/to/original.bin" "path/to/output.bin"
python tools/CodeBase/insertionscript.py "2_translated/tod_msg_menu.csv" "0_data\tod_msg_menu.msd" "3_patched\tod_msg_menu.msd"

Pause