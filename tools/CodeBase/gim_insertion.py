import os
import struct
import sys
from io import BytesIO


def insert_gim_files(rssa_file, gim_directory, output_directory):
    original_rssa_name = os.path.basename(rssa_file)
    with open(rssa_file, 'rb') as original_f:
        temp_f = BytesIO(original_f.read())
    
    temp_f.seek(0)    
    header = temp_f.read(0x60)  # read 60 bytes header
    magic = struct.unpack_from('=4s', header, 0)[0]
    fname = struct.unpack_from('=28s', header, 0x4)[0]
    ssad_count = struct.unpack_from('<H', header, 0x2C)[0]
    gim_count = struct.unpack_from('<H', header, 0x2E)[0]
    ssad_pos_foffset = struct.unpack_from('<I', header, 0x30)[0]
    ssad_pos_fsize = struct.unpack_from('<I', header, 0x34)[0]
    gim_pos_foffset = struct.unpack_from('<I', header, 0x38)[0]
    gim_pos_fsize = struct.unpack_from('<I', header, 0x3C)[0]
    print('header=', header.hex())
    print('magic=', magic.decode('utf-8'))
    print('fname=', fname.decode('utf-8'))
    print('ssad_count=', hex(ssad_count))
    print('gim_count=', hex(gim_count))
    print('ssad_pos_foffset=', hex(ssad_pos_foffset))
    print('ssad_pos_fsize=', hex(ssad_pos_fsize))
    print('gim_pos_foffset=', hex(gim_pos_foffset))
    print('gim_pos_fsize=', hex(gim_pos_fsize))
    
    # Read the structures from the binary file
    structures_pos = []
    temp_f.seek(gim_pos_foffset)
    for _ in range(gim_count):
        structure_pos = struct.unpack('<I', temp_f.read(4))[0]
        structures_pos.append(structure_pos)
        #print('structure_pos=', hex(structure_pos[0]))

    structures_size = []
    temp_f.seek(gim_pos_fsize)
    for _ in range(gim_count):
        structure_size = struct.unpack('<I', temp_f.read(4))[0]
        structures_size.append(structure_size)
        #print('structure_size=', hex(structure_size[0]))

    
    
    # insert the gim in the temp_f
    for gim_file in sorted(os.listdir(gim_directory)):
        if gim_file.endswith('.gim'):  # Check if the file has the .gim extension
            with open(os.path.join(gim_directory, gim_file), 'rb') as gim:
                gim_data = gim.read()
                gim_name = os.path.splitext(gim_file)[0]  # Get the gim file name without the .gim extension
                print(gim_name)
                gim_pos = structures_pos[int(gim_name)]  # Retrieve the file offset for this gim file
                print(hex(gim_pos))
                temp_f.seek(gim_pos)  # Move the pointer in temp_f to the specified offset
                temp_f.write(gim_data)  # Write the gim data at the specified position in temp_f
    # Save the modified content to a new file in the output directory

    output_file = os.path.join(output_directory, f"{original_rssa_name}")
    with open(output_file, 'w+b') as new_f:
        new_f.write(temp_f.getbuffer())


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python gim_insertion.py <rssa_file> <gim_directory> <output_directory>")
    else:
        rssa_file = sys.argv[1]
        gim_directory = sys.argv[2]
        output_directory = sys.argv[3]
        insert_gim_files(rssa_file, gim_directory, output_directory)