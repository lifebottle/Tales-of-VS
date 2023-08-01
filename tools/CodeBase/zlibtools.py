import argparse
import zlib
import shutil
import struct

def decompress_custom_zlib_file(input_file, output_file):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        magic = f_in.read(4)
        if magic != b'SIZE':
            raise ValueError('Invalid file format')

        # Read the decompressed size
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

def compress_custom_zlib_file(input_file, output_file):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        # Read the uncompressed data
        uncompressed_data = f_in.read()

        # Compress the data using zlib
        compressed_data = zlib.compress(uncompressed_data, level=9)

        # Write the custom header ('SIZE') to indicate the uncompressed size
        f_out.write(b'SIZE')
        
        # Write the uncompressed size as a 4-byte little-endian unsigned integer
        f_out.write(struct.pack('<I', len(uncompressed_data)))

        # Write the zlib compressed data to the output file
        f_out.write(compressed_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compress or decompress a file using custom zlib compression')
    parser.add_argument('-c', '--compress', action='store_true', help='Compress the input file')
    parser.add_argument('-d', '--decompress', action='store_true', help='Decompress the input file')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('output_file', help='Path to the output file')
    args = parser.parse_args()

    if args.compress and args.decompress:
        print('Error: Please choose either -c (compress) or -d (decompress), not both.')
    elif not args.compress and not args.decompress:
        print('Error: Please choose either -c (compress) or -d (decompress).')
    elif args.compress:
        compress_custom_zlib_file(args.input_file, args.output_file)
    elif args.decompress:
        decompress_custom_zlib_file(args.input_file, args.output_file)

#python zlibtools.py -c <inputfile> <outputfile>