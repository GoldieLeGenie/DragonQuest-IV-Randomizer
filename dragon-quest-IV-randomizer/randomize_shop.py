import struct
import random
import utils
import json

def randomize_shop_price_and_items(file_path,json_file,nds_file,start_offsets,price=False,items=False):
    try:
        with open(json_file, 'r') as file:
            shop_item_ids = json.load(file)
        
        
        ids = shop_item_ids["ids"]

        with open(file_path, "r+b") as f:
            header = f.read(12)
            f.seek(12)  

            modified_data = bytearray()
            modified_data.extend(header)

            while True:
                data = f.read(0X4)
                if len(data) != 0X4:
                    break

                unpacked = struct.unpack("<HH", data)
                shop_price = {
                    "item": unpacked[0].to_bytes(2, 'little')[:1].hex().upper(),
                    "price": unpacked[1],
                }

                if price and items:
                    if shop_price["price"] != 0 and shop_price["item"] != "00":
                        shop_price["price"] = random.randint(1, 65535)
                        selected_item = random.choice(ids)
                        shop_price['item'] = selected_item
                elif price:
                    if shop_price["price"] != 0:
                        shop_price["price"] = random.randint(1, 65535)
                elif items:
                    if shop_price["item"] != "00":
                        selected_item = random.choice(ids)
                        shop_price['item'] = selected_item

                packed_data = struct.pack("<HH", 
                    int(shop_price["item"], 16), shop_price["price"])
                
                modified_data.extend(packed_data)
            
        for start_offset in start_offsets:
            utils.replace_hex_in_nds(nds_file, start_offset, modified_data)

    except Exception as e:
        print(f"Erreur : {e}")


# json_path = "./data/shop_items.json"
# filepaths = {
#     "./param/param_map_shop_first.dat": [0x9A964, 0x5474C00],
#     "./param/param_map_shop_second.dat": [0x9FD9C, 0x5475C00]
# }
# nds_file = "./dq4.nds"

# for filepath, offsets in filepaths.items():
#     randomize_shop_price_and_items(filepath, json_path, nds_file, offsets)





















