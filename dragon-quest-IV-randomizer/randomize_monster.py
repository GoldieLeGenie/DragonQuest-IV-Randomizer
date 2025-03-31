import json
import struct
import random
import utils

def randomize_monsters(file_path,json_file,nds_file,start_offsets):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        monsters_values = {v for entry in data for k, v in entry.items() if k.startswith("monster") and v != 0}
        monsters_list = sorted(monsters_values)

        with open(file_path, "r+b") as f:
            header = f.read(4)
            f.seek(4)  

            modified_data = bytearray()
            modified_data.extend(header)

            while True:
                data = f.read(0x28)  

                if len(data) != 0x28:
                    break  

                unpacked = struct.unpack("<15H10B", data)

                encount_entry = {
                    "sound":unpacked[0],
                    "monsterA":unpacked[1],
                    "monsterB":unpacked[2],
                    "monsterC":unpacked[3],
                    "monsterD":unpacked[4],
                    "monsterE":unpacked[5],
                    "monsterF":unpacked[6],
                    "monsterG":unpacked[7],
                    "monsterH":unpacked[8],
                    "monsterI":unpacked[9],
                    "monsterJ":unpacked[10],
                    "monsterK":unpacked[11],
                    "monsterL":unpacked[12],
                    "specialM":unpacked[13],
                    "specialN":unpacked[14],
                    "tileLevel":unpacked[15],
                    "ratio":unpacked[16],
                    "formation":unpacked[17],
                    "firstattack":unpacked[18],
                    "invite":unpacked[19],
                    "escape":unpacked[20],
                    "event":unpacked[21],
                    "dmmy0":unpacked[22],
                    "dmmy1":unpacked[23],
                    "dmmy2":unpacked[24]
                }

                monsters = [encount_entry[f"monster{chr(i)}"] for i in range(ord('A'), ord('L')+1)]

                for i in range(len(monsters)):
                    if monsters[i] != 0:
                        encount_entry[f"monster{chr(i + ord('A'))}"] = random.choice(monsters_list)

                packed_data = struct.pack("<15H10B", 
                    encount_entry["sound"], encount_entry["monsterA"], encount_entry["monsterB"], 
                    encount_entry["monsterC"], encount_entry["monsterD"], encount_entry["monsterE"], 
                    encount_entry["monsterF"], encount_entry["monsterG"], encount_entry["monsterH"], 
                    encount_entry["monsterI"], encount_entry["monsterJ"],encount_entry["monsterK"],encount_entry["monsterL"],encount_entry["specialM"], 
                    encount_entry["specialN"], encount_entry["tileLevel"], encount_entry["ratio"], 
                    encount_entry["formation"], encount_entry["firstattack"], encount_entry["invite"], 
                    encount_entry["escape"], encount_entry["event"], encount_entry["dmmy0"], 
                    encount_entry["dmmy1"], encount_entry["dmmy2"]
                    )

                modified_data.extend(packed_data)
            
            utils.replace_hex_in_nds(nds_file, start_offsets, modified_data)

    except Exception as e:
        print("Erreur :", str(e))


def randomize_monster_drop(file_path,json_file,nds_file,start_offsets):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        items = []
        for item in data:
            if isinstance(item, dict) and "item" in item and item["item"] != 0:
                items.append(item["item"])
        
        with open(file_path, "r+b") as f:
            header = f.read(4)
            f.seek(4)  

            modified_data = bytearray()
            modified_data.extend(header)

            while True:
                data = f.read(0x3C)  

                if len(data) != 0x3C:
                    break  

                unpacked = struct.unpack("<15H17B10c3B", data)

                monster_data_entry = {
                    "name": unpacked[0],
                    "level": unpacked[1],
                    "exp": unpacked[2],
                    "MP": unpacked[3],
                    "HP": unpacked[4],
                    "attack": unpacked[5],
                    "defence": unpacked[6],
                    "money": unpacked[7],
                    "item": unpacked[8].to_bytes(2, 'little')[:1].hex().upper(),
                    "action1": unpacked[9],
                    "action2": unpacked[10],
                    "action3": unpacked[11],
                    "action4": unpacked[12],
                    "action5": unpacked[13],
                    "action6": unpacked[14],
                    "agility": unpacked[15],
                    "itemRatio": unpacked[16],
                    "integer": unpacked[17],
                    "focus": unpacked[18],
                    "times": unpacked[19],
                    "heal": unpacked[20],
                    "avoid": unpacked[21],
                    "init": unpacked[22],
                    "initRatio": unpacked[23],
                    "pattern": unpacked[24],
                    "animation1": unpacked[25],
                    "animation2": unpacked[26],
                    "animation3": unpacked[27],
                    "animation4": unpacked[28],
                    "animation5": unpacked[29],
                    "animation6": unpacked[30],
                    "animationMulti": unpacked[31],
                    "byte_1": unpacked[32].hex(),
                    "byte_2": unpacked[33].hex(),
                    "byte_3": unpacked[34].hex(),
                    "byte_4": unpacked[35].hex(),
                    "byte_5": unpacked[36].hex(),
                    "byte_6": unpacked[37].hex(),
                    "byte_7": unpacked[38].hex(),
                    "byte_8": unpacked[39].hex(),
                    "byte_9": unpacked[40].hex(),
                    "byte_10": unpacked[41].hex(),
                    "dmmy0": unpacked[42],
                    "dmmy1": unpacked[43],
                    "dmmy2": unpacked[44]
                }

                if monster_data_entry['item'] != "00":
                    selected_item = random.choice(items)
                    monster_data_entry['item'] = selected_item

                packed_data = struct.pack("<15H17B10c3B",monster_data_entry["name"],
                    monster_data_entry["level"],
                    monster_data_entry["exp"],
                    monster_data_entry["MP"],
                    monster_data_entry["HP"],
                    monster_data_entry["attack"],
                    monster_data_entry["defence"],
                    monster_data_entry["money"],
                    int(monster_data_entry['item'], 16),
                    monster_data_entry["action1"],
                    monster_data_entry["action2"],
                    monster_data_entry["action3"],
                    monster_data_entry["action4"],
                    monster_data_entry["action5"],
                    monster_data_entry["action6"],
                    monster_data_entry["agility"],
                    monster_data_entry["itemRatio"],
                    monster_data_entry["integer"],
                    monster_data_entry["focus"],
                    monster_data_entry["times"],
                    monster_data_entry["heal"],
                    monster_data_entry["avoid"],
                    monster_data_entry["init"],
                    monster_data_entry["initRatio"],
                    monster_data_entry["pattern"],
                    monster_data_entry["animation1"],
                    monster_data_entry["animation2"],
                    monster_data_entry["animation3"],
                    monster_data_entry["animation4"],
                    monster_data_entry["animation5"],
                    monster_data_entry["animation6"],
                    monster_data_entry["animationMulti"],
                    bytes.fromhex(monster_data_entry["byte_1"]),
                    bytes.fromhex(monster_data_entry["byte_2"]),
                    bytes.fromhex(monster_data_entry["byte_3"]),
                    bytes.fromhex(monster_data_entry["byte_4"]),
                    bytes.fromhex(monster_data_entry["byte_5"]),
                    bytes.fromhex(monster_data_entry["byte_6"]),
                    bytes.fromhex(monster_data_entry["byte_7"]),
                    bytes.fromhex(monster_data_entry["byte_8"]),
                    bytes.fromhex(monster_data_entry["byte_9"]),
                    bytes.fromhex(monster_data_entry["byte_10"]),
                    monster_data_entry["dmmy0"],
                    monster_data_entry["dmmy1"],
                    monster_data_entry["dmmy2"])

                modified_data.extend(packed_data)
            
            utils.replace_hex_in_nds(nds_file, start_offsets, modified_data)

    except Exception as e:
        print("Erreur :", str(e))


# file_path = "./param/param_encount_data.dat"
# json_file = './data/param_encount_data.json'
# nds_file = "./dq4.nds"
# start_offsets = 0xA1AE0
# randomize_monsters(file_path,json_file,nds_file,start_offsets)

# file_path = "./param/param_monster_monster.dat"
# json_file = './data/param_monster_monster.json'

# start_offsets = 0xA42E4
# randomize_monster_drop(file_path,json_file,nds_file,start_offsets)
# start_offsets = 0x5478200
# randomize_monster_drop(file_path,json_file,nds_file,start_offsets)


