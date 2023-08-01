import os
import subprocess

# Path to the gimconv.exe executable (assuming it is located in 'tools/GimConv/')
gimconv_path = os.path.join('tools', 'GimConv')

# Path to the folder containing the .gim files
input_folder = '1_extracted'

for root, _, files in os.walk(input_folder):
    for file in files:
        if file.endswith('.gim'):
            # Construct the full path of the .gim file
            gim_file = os.path.join(root, file)

            # Construct the full path of the corresponding .png file
            png_file = os.path.splitext(gim_file)[0] + '.png'

            # Convert paths to be relative to the gimconv.exe location
            relative_gim_file = os.path.relpath(gim_file, start=gimconv_path)
            relative_png_file = os.path.relpath(png_file, start=gimconv_path)

            # Execute the gimconv.exe tool to convert the .gim file to .png
            subprocess.run([os.path.join(gimconv_path, 'gimconv.exe'), relative_gim_file, '-o', relative_png_file], cwd=gimconv_path)
