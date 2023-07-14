import os
import struct
import sys

def extract_gim_files(rssa_file):
    # Create a directory with the same name as the chain file
    output_directory = os.path.splitext(rssa_file)[0]
    os.makedirs(output_directory, exist_ok=True)
    
    with open(rssa_file, 'rb') as file:
        header = file.read(0x60) #read 50 bytes header
        print('header=', header.hex())
        magic = struct.unpack_from('=4s', header,0)[0]
        fname = struct.unpack_from('=28s', header,0x4)[0]
        ssad_count = struct.unpack_from('<H', header,0x2C)[0]
        gim_count = struct.unpack_from('<H', header,0x2E)[0]
        ssad_pos_foffset = struct.unpack_from('<I', header,0x30)[0]
        ssad_pos_fsize = struct.unpack_from('<I', header,0x34)[0]
        gim_pos_foffset = struct.unpack_from('<I', header,0x38)[0]
        gim_pos_fsize = struct.unpack_from('<I', header,0x3C)[0]
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
        file.seek(gim_pos_foffset)
        for _ in range(gim_count):
            structure_pos = struct.unpack('<I', file.read(4))
            structures_pos.append(structure_pos)
            print('structure_pos=',hex(structure_pos[0]))
            
        structures_size = []
        file.seek(gim_pos_fsize)
        for _ in range(gim_count):
            structure_size = struct.unpack('<I', file.read(4))
            structures_size.append(structure_size)
            print('structure_size=',hex(structure_size[0]))
           
       
        for (i, structures_pos) in enumerate(structures_pos):
            # Read the file offset and size from the table
            file_offset = structure_pos[0]
            file_size   = structure_size[0]
            print("File offset:", file_offset)
            print("File size:", file_size)
            
            #name the file
            file_name = str(i) + '.gim'
            
            # Extract the file data
            file.seek(file_offset)
            file_data = file.read(file_size)
            
            # Write the file data to the output directory
            output_file_path = os.path.join(output_directory, file_name)
            with open(output_file_path, 'wb') as output_file:
                output_file.write(file_data)
                
    print(f"All .gim files extracted to {output_directory}.")       
            
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python gimtools.py <rssa_file> <output_dir>")
    else:
        rssa_file = sys.argv[1]
        extract_gim_files(rssa_file)