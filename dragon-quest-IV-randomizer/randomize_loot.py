
import struct
import utils
import random

def randomize_all_loot(file_path,nds_file,start_offset):
    try:
        all_items = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "0A", "0B", "0C", "0D", "0E", "0F", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "1A", "1B", "1C", "1D", "1E", "1F", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "2A", "2B", "2C", "2D", "2E", "2F", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "3A", "3B", "3C", "3D", "3E", "3F", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "4A", "4B", "4C", "4D", "4E", "4F", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "5A", "5B", "5C", "5D", "5E", "5F", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "6A", "6B", "6C", "6D", "6E", "6F", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "7A", "7E", "7F", "80", "81", "82", "83", "84", "89", "8C", "8D", "8E", "97", "98", "99", "9E"]
        important_item = ["9D", "7C", "86", "8F", "8A", "9B", "87", "90", "8B", "91", "95", "94", "88", "85", "7B", "93", "9A", "92", "7D", "96", "9C"]
        with open(file_path, "r+b") as f:
            header = f.read(4)
            f.seek(4)  

            modified_data = bytearray()
            modified_data.extend(header)

            while True:
                data = f.read(0x18) 
                if len(data) != 0x18:
                    break  

                unpacked = struct.unpack("<I8H3Bc", data)  
                furniture = {
                    "message": unpacked[0],
                    "uid": unpacked[1],
                    "item": unpacked[2].to_bytes(2, 'little')[:1].hex().upper(),
                    "gold": unpacked[3],
                    "monster": unpacked[4],
                    "encount": unpacked[5],
                    "uidReplace": unpacked[6],
                    "openIndex": unpacked[7],
                    "flagIndex": unpacked[8],
                    "type": unpacked[9],
                    "furnIndex": unpacked[10],
                    "ListSize": unpacked[11],
                    "byte_1": unpacked[12].hex(),
                }

                if furniture['item'] != "00" and furniture["item"] not in important_item and furniture["gold"] == 0:
                    selected_item = random.choice(all_items)
                    furniture['item'] = selected_item
                
                if furniture["gold"] != 0 and furniture['item'] == "00":
                    furniture["gold"] = random.randint(1, 65535)
                
                packed_data = struct.pack("<I8H3Bc", 
                    furniture["message"], furniture["uid"], 
                    int(furniture['item'], 16), furniture["gold"],furniture["monster"],
                    furniture["encount"], furniture["uidReplace"], furniture["openIndex"], 
                    furniture["flagIndex"], furniture["type"], 
                    furniture["furnIndex"], furniture["ListSize"], 
                    bytes.fromhex(furniture["byte_1"]))
                
                modified_data.extend(packed_data)
            
            utils.replace_hex_in_nds(nds_file, start_offset, modified_data)
            
    except Exception as e:
        print("Erreur :", str(e))


# nds_file = "./dq4.nds"
# directory = "./param/"

# file_list_and_pattern = utils.extract_pattern_from_files(directory)
# for filepath, pattern in file_list_and_pattern:
#     start_offset = utils.find_offset(nds_file, pattern)
#     randomize_all_loot(filepath,nds_file,start_offset)


