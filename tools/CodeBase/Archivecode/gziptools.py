import argparse
import gzip
import shutil

def compress_file(input_file, output_file):
    with open(input_file, 'rb') as f_in, gzip.open(output_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def uncompress_file(input_file, output_file):
    with gzip.open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compress or uncompress a file using gzip.')
    parser.add_argument('mode', choices=['compress', 'uncompress'], help='Mode: compress or uncompress')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('output_file', help='Path to save the result')
    args = parser.parse_args()

    if args.mode == 'compress':
        compress_file(args.input_file, args.output_file)
    elif args.mode == 'uncompress':
        uncompress_file(args.input_file, args.output_file)