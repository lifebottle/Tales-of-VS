import os
import struct
import sys

EXTENSIONS = {
    b"RSSA": "rssa",
    b"MIG.": "gim",
    b"OMG.": "gmo",
    b"EFCT": "efp",
}


def extract_rssa_files(chain_file):
    # Create a directory with the same name as the chain file
    output_directory = os.path.splitext(chain_file)[0]
    os.makedirs(output_directory, exist_ok=True)

    with open(chain_file, 'rb') as file:
        header = file.read(0x10)
        print('header=', header.hex())
        entry_count = struct.unpack_from('<I', header,0)[0]
        print('entry count=', entry_count)

        # Read the structures from the binary file
        structures = []
        for _ in range(entry_count):
            structure = struct.unpack('<II', file.read(8))
            structures.append(structure)
            print('structure=',structure)

        for (i, structure) in enumerate(structures):
            # Read the file offset and size from the table
            file_offset = structure[0]
            file_size   = structure[1]
            print("File offset:", file_offset)
            print("File size:", file_size)



            # Extract the file data
            file.seek(file_offset)
            file_data = file.read(file_size)

            # Get file extension
            ext = EXTENSIONS.get(file_data[:4], "bin")
            
            file_name = ""
            # If it is an RSSA then extract the file name from the chain file
            if ext == "rssa":
                for x in file_data[4:0x30]:
                    if x == 0: break
                    file_name += chr(x)
                file_name = f"{file_name}.{ext}"
            else:
                # No name for us, use the index
                file_name = f"{i:03d}.{ext}"
            
            # Write the file data to the output directory
            output_file_path = os.path.join(output_directory, file_name)
            with open(output_file_path, 'wb') as output_file:
                output_file.write(file_data)


    print(f"All .rssa files extracted to {output_directory}.")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python rssatools.py <chain_file>")
    else:
        chain_file = sys.argv[1]
        extract_rssa_files(chain_file)