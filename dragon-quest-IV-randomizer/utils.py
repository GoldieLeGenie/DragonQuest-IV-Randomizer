import os
import mmap

def replace_hex_in_nds(nds_file, start_offset, new_hex_data):
    try:
        with open(nds_file, "r+b") as f:
            f.seek(start_offset)
            f.write(new_hex_data)
    except Exception as e:
        print(f"Erreur lors du remplacement des données : {e}")


def find_offset(nds_file, pattern):
    with open(nds_file, "rb") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            offset = mm.find(pattern) 
            
            if offset != -1:
                return offset
            else:
                return None

def extract_pattern_from_files(directory):
    file_list_and_pattern = []
    for file in os.listdir(directory):
        if file.startswith("param_item_"):
            filepath = os.path.join(directory, file)
            with open(filepath, "rb") as f:
                data = f.read(10)  
                if len(data) == 10:  
                    file_list_and_pattern.append((filepath, data))
    return file_list_and_pattern

