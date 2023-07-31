import os
import struct
import sys
from io import BytesIO
from pathlib import Path

EXTENSIONS = {
    b"RSSA": "rssa",
    b"MIG.": "gim",
    b"OMG.": "gmo",
    b"EFCT": "efp",
}

def insert_rssa_files(chain_file, rssa_directory, output_directory):
    original_chain_name = os.path.basename(chain_file)
    with open(chain_file, 'rb') as original_f:
        temp_f = BytesIO(original_f.read())

    header = temp_f.read(0x10)
    print('header=', header.hex())
    entry_count = struct.unpack_from('<I', header)[0]
    print('entry count=', entry_count)

    # Read the structures from the binary file
    structures = []
    for _ in range(entry_count):
        structure = struct.unpack('<II', temp_f.read(8))
        structures.append(structure)

    rssa_dir = Path(rssa_directory)
    for (i, structure) in enumerate(structures):
        # Read the file offset and size from the table
        file_offset = structure[0]
        file_size = structure[1]

        # Extract the file data
        temp_f.seek(file_offset)
        file_data = temp_f.read(file_size)

        # Get file extension
        ext = EXTENSIONS.get(file_data[:4], "bin")

        file_name = ""
        # If it is an RSSA then extract the file name from the chain file
        if ext == "rssa":
            for x in file_data[4:0x30]:
                if x == 0:
                    break
                file_name += chr(x)
            file_name = f"{file_name}.{ext}"
        else:
            # No name for us, use the index
            file_name = f"{i:03d}.{ext}"

        structure = (*structure, file_name)
        print('structure=', structure)

        file_path = rssa_dir / structure[2]
        if not file_path.exists() and not file_path.is_file():
            continue

        with open(file_path, "rb") as tf:
            temp_f.seek(file_offset)
            temp_f.write(tf.read())

    output_file = os.path.join(output_directory, f"{original_chain_name}")
    with open(output_file, 'w+b') as new_f:
        new_f.write(temp_f.getbuffer())

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python chain_insertion.py <chain_file> <rssa_directory> <output_directory>")
    else:
        chain_file = sys.argv[1]
        rssa_directory = sys.argv[2]
        output_directory = sys.argv[3]
        insert_rssa_files(chain_file, rssa_directory, output_directory)
