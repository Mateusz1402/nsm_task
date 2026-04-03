import hashlib
import sys

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

    temp_dir1 = "tests/plik ze spacja.txt"
    temp_dir2 = "tests/data.txt"
    temp_dir3 = "tests/subfolder/plik ze spacja.txt"
    temp_dir4 = "tests/subfolder/data.txt"
    temp_dir = temp_dir3

    checksum = get_hash(temp_dir)

    temp_space = False
    for char in temp_dir:
        if char == ' ':
            temp_space = True

    if temp_space:
        temp_dir = f'"{temp_dir}"'

    print(f"{temp_dir} {checksum}")

    


if __name__ == "__main__":
    main()