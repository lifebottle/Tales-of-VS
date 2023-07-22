import argparse
import zlib
import shutil
import struct

def uncompress_custom_zlib_file(input_file, output_file):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        magic = f_in.read(4)
        if magic != b'SIZE':
            raise ValueError('Invalid file format')

        # Read the uncompressed size
        usize = struct.unpack('<I', f_in.read(4))[0]

        # Read the zlib compressed data
        compressed_data = f_in.read()

        # Decompress the zlib compressed data
        decompressed_data = zlib.decompress(compressed_data)

        # Verify the decompressed size matches the expected uncompressed size
        if len(decompressed_data) != usize:
            raise ValueError('Decompressed data size mismatch')

        # Write the decompressed data to the output file
        f_out.write(decompressed_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Uncompress a custom zlib-compressed file')
    parser.add_argument('input_file', help='Path to the input custom zlib-compressed file')
    parser.add_argument('output_file', help='Path to save the uncompressed file')
    args = parser.parse_args()

    uncompress_custom_zlib_file(args.input_file, args.output_file)