import csv
import struct
import sys

def update_text_strings(csv_file, binary_file, output_file):
    # Read the existing text offset pointer from the binary file
    with open(binary_file, "rb") as f:
        f.seek(0x18)
        text_offset = struct.unpack("<I", f.read(4))[0]

    # Open the binary file in binary mode for updating
    with open(binary_file, "r+b") as f:
        # Move to the position of the text offset pointer
        f.seek(text_offset)

        # Open the CSV file and update the text strings
        with open(csv_file, "r", encoding="utf-8-sig") as csv_file:
            csv_reader = csv.reader(csv_file)
            
            # Skip the header row
            #next(csv_reader)
            
            for row in csv_reader:
                english_text = row[1].strip()
                japanese_text = row[0].strip()

                # Choose the text string to insert
                text_string = english_text if english_text else japanese_text
                text_string = text_string.replace("`","　").encode("utf-16-le")
                text_length = len(text_string) + 4

                # Write the updated text string
                f.write(text_string)
                f.write(b"\x00\x00\x00\x00")  # End of string marker

                # Update the text offset pointer
                text_offset += text_length

        # Update the text offset pointer in the binary file header
        f.seek(0x18)
        f.write(struct.pack("<I", text_offset))

    # Save the updated binary file to the output file path
    with open(binary_file, "rb") as f_in, open(output_file, "wb") as f_out:
        f_out.write(f_in.read())

if __name__ == "__main__":
    # Check if the required arguments are provided
    if len(sys.argv) < 4:
        print("Usage: python script.py <csv_file> <binary_file> <output_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    binary_file = sys.argv[2]
    output_file = sys.argv[3]
    
    update_text_strings(csv_file, binary_file, output_file)
    print("Text strings and offset pointer updated successfully.")
