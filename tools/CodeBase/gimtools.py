import os
import struct
import sys

def extract_gim_files(rssa_file, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    with open(rssa_file, 'rb') as rssa_f:
        header = rssa_f.read(0x60)  # read 50 bytes header
        print('header=', header.hex())
        magic = struct.unpack_from('=4s', header, 0)[0]
        fname = struct.unpack_from('=28s', header, 0x4)[0]
        ssad_count = struct.unpack_from('<H', header, 0x2C)[0]
        gim_count = struct.unpack_from('<H', header, 0x2E)[0]
        ssad_pos_foffset = struct.unpack_from('<I', header, 0x30)[0]
        ssad_pos_fsize = struct.unpack_from('<I', header, 0x34)[0]
        gim_pos_foffset = struct.unpack_from('<I', header, 0x38)[0]
        gim_pos_fsize = struct.unpack_from('<I', header, 0x3C)[0]
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
        rssa_f.seek(gim_pos_foffset)
        for _ in range(gim_count):
            structure_pos = struct.unpack('<I', rssa_f.read(4))
            structures_pos.append(structure_pos)
            print('structure_pos=', hex(structure_pos[0]))

        structures_size = []
        rssa_f.seek(gim_pos_fsize)
        for _ in range(gim_count):
            structure_size = struct.unpack('<I', rssa_f.read(4))
            structures_size.append(structure_size)
            print('structure_size=', hex(structure_size[0]))

        for (i, structure_pos) in enumerate(structures_pos):
            # Read the file offset and size from the table
            file_offset = structure_pos[0]
            file_size = structures_size[i][0]
            print("File offset:", file_offset)
            print("File size:", file_size)

            # Name the file
            file_name = str(i) + '.gim'

            # Extract the file data
            rssa_f.seek(file_offset)
            file_data = rssa_f.read(file_size)

            # Write the file data to the specified output directory
            output_file_path = os.path.join(output_directory, file_name)
            with open(output_file_path, 'wb') as output_f:
                output_f.write(file_data)

    print(f"All .gim files extracted to {output_directory}.")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python gimtools.py <rssa_file> <output_dir>")
    else:
        rssa_file = sys.argv[1]
        output_directory = sys.argv[2]
        extract_gim_files(rssa_file, output_directory)
