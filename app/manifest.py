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

def verify_manifest(input_dir, manifest_path):
    #Verifying whole manifest list for SHA256 hash mismatches.
    print(f"Veryfing directory against manifest: {manifest_path}")
    mismatches = 0
    try:
        with open(manifest_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                #Spaces case (directory in the " ").
                if line.startswith('"'):
                    #Seraching for second char of " (end of dir).
                    parts = line[1:].split('"', 1)
                    #Left side.
                    rel_path = parts[0]
                    #Right side.
                    expected_hash = parts[1].strip()
                #No spaces case.
                else:
                    parts = line.split(" ", 1)
                    rel_path = parts[0]
                    expected_hash = parts[1].strip()
                
                full_path = os.path.join(input_dir, rel_path)

                #Check whether file exists.
                if not os.path.exists(full_path):
                    print(f"Missing the file: {rel_path}")
                    mismatches += 1
                    continue

                current_hash = get_hash(full_path)
                if current_hash == expected_hash:
                    print(f"OK: {rel_path}")
                else:
                    print(f"Failed: {rel_path} (Hash mismatch)")
                    mismatches += 1
        if mismatches == 0:
            print("\nVerification successful! All files match.")
        else:
            print(f"\nVerification failed! Found {mismatches} mismatches.")
            sys.exit(1)
    except Exception as e:
        print(f"Error during verification: {e}")
        sys.exit(1)
                

def generate_manifest(input_dir):
    #Generating new manifest list.
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
    return manifest_list


def main():
    parser = argparse.ArgumentParser(description="NMS directory manifest tool")
    #Input:
    parser.add_argument("-input_dir", required=True, help="Directory to scan")
    #Output:
    parser.add_argument("-output", required=True, help="Output manifest file")
    # BONUS part:
    parser.add_argument("--check", action="store_true", help="Enable verification mode")


    args = parser.parse_args()
    #Take absolute input directory (if symlink)
    input_dir = os.path.abspath(args.input_dir)
    #Secure input from hazardous
    if not os.path.isdir(input_dir):
        print(f"Error: {input_dir} is not a directory!")
        sys.exit(1)

    output_file = args.output

    #Whether verify function to use.
    if args.check:
        verify_manifest(input_dir, output_file)
    else:
        manifest_list = generate_manifest(input_dir)
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write("\n".join(manifest_list) + "\n")
            print(f"Manifest file successfully saved to {output_file}")
        except Exception as e:
            print(f"Error while writing manifest: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()