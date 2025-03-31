import struct
import random
import utils

def randomize_medal_prize(file_path,nds_file,start_offsets):
    try:
        all_items = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "0A", "0B", "0C", "0D", "0E", "0F", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "1A", "1B", "1C", "1D", "1E", "1F", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "2A", "2B", "2C", "2D", "2E", "2F", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "3A", "3B", "3C", "3D", "3E", "3F", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "4A", "4B", "4C", "4D", "4E", "4F", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "5A", "5B", "5C", "5D", "5E", "5F", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "6A", "6B", "6C", "6D", "6E", "6F", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "7A", "7E", "7F", "80", "81", "82", "83", "84", "89", "8C", "8D", "8E", "97", "98", "99", "9E"]

        with open(file_path, "r+b") as f:
            header = f.read(4)
            f.seek(4)  

            modified_data = bytearray()
            modified_data.extend(header)

            while True:
                data = f.read(0x4)  

                if len(data) != 0x4:
                    break  
                unpacked = struct.unpack("<HH", data)

                medal_prize_entry = {
                    "item": unpacked[0].to_bytes(2, 'little')[:1].hex().upper(),
                    "price": unpacked[1],
                }

                medal_prize_entry['item'] = random.choice(all_items)

                packed_data = struct.pack("<HH", 
                int(medal_prize_entry['item'], 16), medal_prize_entry["price"])
                
                modified_data.extend(packed_data)
                
  
            utils.replace_hex_in_nds(nds_file, start_offsets, modified_data)


    except Exception as e:
        print("Erreur :", str(e))

# file_path = "./param/param_map_medal.dat"
# nds_file = "./dq4.nds"
# start_offsets = 0x5474800
# randomize_medal_prize(file_path,nds_file,start_offsets)