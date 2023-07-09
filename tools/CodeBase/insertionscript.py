import csv
import struct
import sys

def truncate_text(text):
    lines = text.split('\n')
    truncated_lines = []

    total_length = 0
    for line in lines:
        if len(line) > 0x15:
            truncated_line = line[:0x15]
            print('line got truncated')
        else:
            truncated_line = line

        if total_length + len(truncated_line) > 0x15:
            excess_length = 0x15 - total_length
            truncated_line = truncated_line[:excess_length]
            truncated_lines.append(truncated_line)
            print('cell got truncated')
            break
        else:
            truncated_lines.append(truncated_line)
            total_length += len(truncated_line)

    return '\n'.join(truncated_lines)


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
            english_short_text = entries[i][5]
            english_text = entries[i][4]
            japanese_text = entries[i][3]
            String_Flags = entries[i][1]
            Unique_ID = entries[i][0]
            
            #text = english_text if english_text else japanese_text
            text = english_short_text if english_short_text else (english_text if english_text else japanese_text)
            #text = truncate_text(text)
            

            # Write the text string
            text_bytes = text.encode("utf-16-le")
            f.write(text_bytes)

            # Write four 00 bytes
            f.write(b'\x00\x00\x00\x00')

            # Update the corresponding pointer in the previous structure
            structure_offset = 0x10 + i * 0xC
            #print(hex(structure_offset))
            #write unique id
            f.seek(structure_offset)
            f.write(struct.pack('<I', int(Unique_ID)))
            #write string flags
            f.seek(structure_offset + 0x4)
            f.write(struct.pack('<I', int(String_Flags)))
            #write new adress
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
