import hashlib
import sys
import argparse
import os

def get_hash(file_path):
    # Generating a unique SHA256 hash code for entry file.
    hash = hashlib.sha256();
    try:
        with open(file_path, "rb") as bin_file:
            while True:
                #Reading a 4096 bytes-portion blocks of entry file.
                byte_block = bin_file.read(4096)
                #When block is empty -> break the loop. 
                if not byte_block:
                    break

                hash.update(byte_block)
        return hash.hexdigest()

    except Exception as e:
        print(f"Generating a SHA256 hash from the file {file_path} occurs an error: {e}")
        sys.exit(1)





def main():
    parser = argparse.ArgumentParser(description="NMS directory manifest tool")
    #Input:
    parser.add_argument("-input_dir", required=True, help="Directory to scan")
    #Output:
    parser.add_argument("-output", required=True, help="Output manifest file")

    args = parser.parse_args()
    #Take absolute input directory (if symlink)
    input_dir = os.path.abspath(args.input_dir)
    #Secure input from hazardous
    if not os.path.isdir(input_dir):
        print(f"Error: {input_dir} is not a directory!")
        sys.exit(1)

    output_file = args.output

    manifest_list = []


    #explore the whole directory tree, starting from input_dir point.
    for root, dirs, files in os.walk(input_dir):
        for name in files:
            full_path = os.path.join(root, name)

            #Checking for regular file type or symlink 
            if not (os.path.isfile(full_path) or os.path.islink(full_path)):
                print(f"Error: Unsupported file type found at {full_path}")
                sys.exit(1)
            
            if os.path.islink(full_path):
                target_path = os.path.realpath(full_path)
                #Checking whether the symlink points the file in target directory.
                if not target_path.startswith(input_dir):
                    print(f"Error: Symlink {full_path} points outside the target directory!")
                    sys.exit(1)
            
            #Generating the SHA256 hash
            checksum = get_hash(full_path)


            #Cut the absolute directory to be started from target directory.
            rel_path = os.path.relpath(full_path, input_dir)

            #Spaces case
            if " " in rel_path:
                formatted_path = f'"{rel_path}"'
            else:
                #Non spaces case
                formatted_path = rel_path

            manifest_list.append(f"{formatted_path} {checksum}")
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write("\n".join(manifest_list) + "\n")
        print(f"Manifest file successfully saved to {output_file}")
    except Exception as e:
        print(f"Error while writing manifest: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()