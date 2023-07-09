import csv
import struct
import sys

def truncate_string(text):
    if len(text) > 0x66:
        text = text[:0x66]
    
    return text


def write_binary_from_csv(csv_file, binary_file, output_file):
    # Read the header from the binary file
    with open(binary_file, 'rb') as f:
        header = f.read(0x10)
        entry_count = struct.unpack_from('<I', header, 0x8)[0]

        # Read the structures from the binary file
        structures = []
        for _ in range(entry_count):
            structure = f.read(0xC)
            structures.append(structure)

    # Read the CSV file
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        entries = list(reader)

    # Create a new binary file
    with open(output_file, 'wb') as f:
        # Write the header
        f.write(header)

        # Write the structures
        for structure in structures:
            f.write(structure)

        # Write the text strings and update the pointers
        current_offset = 0x10 + entry_count * 0xC
        for i in range(entry_count):
            english_short_text = entries[i][2]
            english_text = entries[i][1]
            japanese_text = entries[i][0]
            #text = english_text if english_text else japanese_text
            text = english_short_text if english_short_text else (english_text if english_text else japanese_text)

            # Write the text string
            text_bytes = text.encode("utf-16-le")
            truncated_text_bytes = text_bytes[:0x66]  # Truncate if longer than 0x66
            f.write(truncated_text_bytes)

            # Write four 00 bytes
            f.write(b'\x00\x00\x00\x00')

            # Update the corresponding pointer in the previous structure
            structure_offset = 0x10 + i * 0xC
            f.seek(structure_offset + 0x8)
            f.write(struct.pack('<I', current_offset))

            # Update the current offset
            current_offset += len(text_bytes) + 4

            # Seek back to the end of the current string
            f.seek(current_offset)

    print("Binary file created successfully.")

if __name__ == "__main__":
    # Check if the required arguments are provided
    if len(sys.argv) < 4:
        print("Usage: python script.py <csv_file> <binary_file> <output_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    binary_file = sys.argv[2]
    output_file = sys.argv[3]
    
    write_binary_from_csv(csv_file, binary_file, output_file)
    print("Text strings and offset pointer updated successfully.")
