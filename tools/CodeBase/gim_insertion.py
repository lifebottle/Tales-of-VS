import os
import struct
import sys

def insert_gim_files(rssa_file, gim_directory):
    # Create a temporary output file
    temp_file = "temp.rssa"

    with open(rssa_file, 'rb') as file:
        with open(temp_file, 'wb') as temp:
            header = file.read(0x60)  # Read 60 bytes header
            temp.write(header)

            # Get the original gim_count and update the header
            #gim_count = struct.unpack_from('<H', header, 0x2E)[0]
            #new_gim_count = gim_count + len(os.listdir(gim_directory))
            #temp.seek(0x2E)
            #temp.write(struct.pack('<H', new_gim_count))

            # Get the original gim_pos_foffset and update the header
            gim_pos_foffset = struct.unpack_from('<I', header, 0x38)[0]
            new_gim_pos_foffset = gim_pos_foffset + (8 * len(os.listdir(gim_directory)))
            temp.seek(0x38)
            temp.write(struct.pack('<I', new_gim_pos_foffset))

            # Write the original gim_pos_fsize back to the header
            gim_pos_fsize = struct.unpack_from('<I', header, 0x3C)[0]
            temp.seek(0x3C)
            temp.write(struct.pack('<I', gim_pos_fsize))

            # Write the original ssad_pos_foffset and ssad_pos_fsize back to the header
            ssad_pos_foffset = struct.unpack_from('<I', header, 0x30)[0]
            ssad_pos_fsize = struct.unpack_from('<I', header, 0x34)[0]
            temp.seek(0x30)
            temp.write(struct.pack('<I', ssad_pos_foffset))
            temp.seek(0x34)
            temp.write(struct.pack('<I', ssad_pos_fsize))

            # Write the gim_pos_foffset for each .gim file
            gim_pos_foffset_offset = new_gim_pos_foffset
            for gim_file in sorted(os.listdir(gim_directory)):
                with open(os.path.join(gim_directory, gim_file), 'rb') as gim:
                    gim_data = gim.read()
                    temp.write(struct.pack('<I', gim_pos_foffset_offset))
                    temp.write(struct.pack('<I', len(gim_data)))
                    gim_pos_foffset_offset += len(gim_data)

            # Append the .gim file data
            for gim_file in sorted(os.listdir(gim_directory)):
                with open(os.path.join(gim_directory, gim_file), 'rb') as gim:
                    gim_data = gim.read()
                    temp.write(gim_data)

    # Replace the original RSSA file with the modified temp file
    os.replace(temp_file, rssa_file)

    print(f"All .gim files inserted into {rssa_file}.")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python gim_insertion.py <rssa_file> <gim_directory>")
    else:
        rssa_file = sys.argv[1]
        gim_directory = sys.argv[2]
        insert_gim_files(rssa_file, gim_directory)
