# v1.9.5
# Fleasion, open sourced cache modifier made by @cro.p, intended for Phantom Forces. plz dont abuse D:
# discord.gg/v9gXTuCz8B

import os
import sys
import shutil
import time
import json
import webbrowser
import requests
import platform

README_URL = 'https://github.com/standingmcdonalds/Reasion/blob/main/README.md'
FLEASION_URL = 'https://github.com/standingmcdonalds/Reasion/blob/main/fleasion.py'
ASSETS_URL = 'https://github.com/standingmcdonalds/Reasion/blob/main/assets.json'
RUN_URL = 'https://github.com/standingmcdonalds/Reasion/blob/main/run.bat'
RUNSH_URL = 'https://github.com/standingmcdonalds/Reasion/blob/main/run.sh'
README_FILE = 'README.md'
FLEASION_FILE = 'fleasion.py'
ASSETS_FILE = 'assets.json'
RUN_FILE = 'run.bat'
RUNSH_FILE = 'run.sh'
GREEN, RED, BLUE, DEFAULT = '\033[32m', '\033[31m', '\033[34m', '\033[0m'
os_name = platform.system()
clear_command = 'cls' if os_name == 'Windows' else 'clear'
mesh_version = 'v2'


def fetch_lines(url, num_lines=1):
    response = requests.get(url)
    lines = response.text.splitlines()
    return lines[:num_lines], lines


def read_lines(file_name, num_lines=1):
    try:
        with open(file_name, 'r') as file:
            return [file.readline().strip() for _ in range(num_lines)]
    except FileNotFoundError:
        return [''] * num_lines


def update_file(file_name, lines):
    with open(file_name, 'w') as file:
        file.write('\n'.join(lines))


def get_version():
    global presets_file
    readme_first_line, readme_lines = fetch_lines(README_URL)
    fleasion_first_line, fleasion_lines = fetch_lines(FLEASION_URL)
    run_lines, all_run_lines = fetch_lines(RUN_URL, 2)
    runsh_lines, all_runsh_lines = fetch_lines(RUNSH_URL, 2)

    print("Validating file versions...")

    local_readme_first_line = read_lines(README_FILE)[0]
    if readme_first_line[0] == local_readme_first_line:
        print(f"ReadMe   {GREEN}{readme_first_line[0]}{DEFAULT}")
    else:
        update_file(README_FILE, readme_lines)
        print(f"Updated README.md to {BLUE}{readme_first_line[0]}{DEFAULT}")

    local_fleasion_first_line = read_lines(FLEASION_FILE)[0]
    fleasion_display = fleasion_first_line[0][2:]
    if fleasion_first_line[0] == local_fleasion_first_line:
        print(f"Fleasion {GREEN}{fleasion_display}{DEFAULT}")
    else:
        update_file(FLEASION_FILE, fleasion_lines)
        print(f"Updated fleasion.py to {BLUE}{fleasion_display}{DEFAULT}")
        os.execv(sys.executable, ['python'] + sys.argv)

    response_assets = requests.get(ASSETS_URL)
    response_json = response_assets.json()

    try:
        with open(ASSETS_FILE, 'r') as file:
            local_assets = json.load(file)
    except FileNotFoundError:
        local_assets = {}

    if response_json.get('version') == local_assets.get('version'):
        print(f"Assets   {GREEN}{response_json['version']}{DEFAULT}")
    else:
        with open(ASSETS_FILE, 'w') as file:
            json.dump(response_json, file, indent=4)
        print(f"Updated assets.json to {BLUE}{response_json['version']}{DEFAULT}")

    local_run_lines = read_lines(RUN_FILE, 2)
    run_version = run_lines[1][2:]
    if run_version == local_run_lines[1][2:]:
        print(f"Run.bat  {GREEN}{run_version}{DEFAULT}")
    else:
        update_file(RUN_FILE, all_run_lines)
        print(f"Updated run.bat to {BLUE}{run_version}{DEFAULT}")

    local_runsh_lines = read_lines(RUNSH_FILE, 2)
    runsh_version = runsh_lines[1][2:]
    if runsh_version == local_runsh_lines[1][2:]:
        print(f"Run.sh   {GREEN}{runsh_version}{DEFAULT}")
    else:
        update_file(RUNSH_FILE, all_runsh_lines)
        print(f"Updated run.sh to  {BLUE}{runsh_version}{DEFAULT}")

    presets_file = 'presets.json'
    if not os.path.exists(presets_file):
        with open(presets_file, 'w') as file:
            json.dump({
                "replace oled": [
                    '0fd98b21b47dbd948988ec1c67696af8',
                    '5873cfba79134ecfec6658f559d8f320',
                    '009b0b998ae084f23e5c0d7b1f9431b3',
                    '577f6c95249ebea2926892c3f3e8c040'
                ]
            }, file, indent=4)
        print(f"Created {BLUE}{presets_file}{DEFAULT}")

    time.sleep(1)
    os.system(clear_command)


def dlist(area, specific_area=None):
    if specific_area:
        current_level = specific_area
    else:
        current_level = data[area]
    path = [area]

    while isinstance(current_level, dict):
        match = {}
        print(f"\nAvailable keys in {GREEN}{' -> '.join(path)}{DEFAULT}:")
        for j, key in enumerate(current_level):
            match[str(j + 1)] = key
            print(f"{j + 1}: {' ' if j < 9 else ''}{GREEN}{key}{DEFAULT}")

        user_input = input(
            f"Enter the key(name or number) you want to use in {GREEN}{' -> '.join(path)}{DEFAULT}\n(nest in keys with a period, type 'back' to go back, or 'skip' to skip)\n: ").strip().lower()

        if user_input == 'back':
            if len(path) > 1:
                path.pop()
                current_level = data[path[0]]
                for key in path[1:]:
                    current_level = current_level[key]
            else:
                print("You are already at the top level. Cannot go back.")
            continue

        if user_input == 'skip':
            print("Skipping category.")
            return

        if user_input in match.keys():
            selected_keys = [match[user_input]]
        else:
            selected_keys = user_input.split('.')
            selected_keys = [key.strip() for key in selected_keys]

        valid = True
        temp_level = current_level
        for key in selected_keys:
            if key in temp_level:
                temp_level = temp_level[key]
            else:
                print(f"{RED}Key '{key}' does not exist in '{' -> '.join(path)}'. Please try again.{DEFAULT}")
                valid = False
                break

        if valid:
            for key in selected_keys:
                path.append(key)
                current_level = current_level[key]

    return current_level


def bloxstrap():
    base_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Bloxstrap', 'Modifications')
    nested_folders = ["PlatformContent", "pc", "textures", "sky"]

    if not os.path.exists(base_path):
        print(f"{RED}bloxstrap not found{DEFAULT}")
    else:
        path = base_path
        for folder in nested_folders:
            path = os.path.join(path, folder)
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"Created folder: {path}")
            else:
                print(f"Folder already exists: {path}")

        print("All folders created successfully! Import your skyboxes into the opened folder.")
        os.startfile(path)

        replace(data["skyboxes"], 'd625adff6a3d75081d11b3407b0b417c')


def delete_stuff(files_to_delete):
    for file_to_delete in files_to_delete:
        delete_file_path = os.path.join(folder_path, file_to_delete)
        if os.path.exists(delete_file_path):
            os.remove(delete_file_path)  #
            print(f'{file_to_delete} has been deleted.')
        else:
            print(f'{RED}{file_to_delete} not found.{DEFAULT}')


def preset_check():
    print("\nAvailable presets:")
    for idx, key in enumerate(presets.keys(), start=1):
        print(f"{idx}: {GREEN}{key}{DEFAULT}")

    choice = input(": ")

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(presets):
            return list(presets.keys())[choice - 1]
        else:
            print("Invalid number.")
            return None
    else:
        return choice


get_version()

if os_name == "Windows":
    folder_path = os.path.join(os.getenv('TEMP'), 'roblox', 'http')
else:
    print(f"Unsupported OS - {os}")
    exit()

mod_cache = False
pf_cache = False
ar2_cache = False

mod_cache_check_path = os.path.join(folder_path,
                                    '192ce9c124a483a4fa063a1849fcb755') 
pf_cache_check_path = os.path.join(folder_path,
                                   '7b8ca4a4ec7addd0f55179a86e49a5a1')
ar2_cache_check_path = os.path.join(folder_path,
                                   '025c9ff09c0c54793baa59dfa0115401')

if os.path.exists(mod_cache_check_path):
    mod_cache = True
if os.path.exists(pf_cache_check_path):
    pf_cache == True
if os.path.exists(ar2_cache_check_path):
    ar2_cache == True

if not mod_cache or not pf_cache or ar2_cache:
    print(
        f"{RED}Missing cache, join prompted {'experiences' if not mod_cache or not pf_cache else 'experience'}.{DEFAULT}")
if not mod_cache:
    webbrowser.open_new_tab("https://www.roblox.com/games/96564332811680/Asset-loader")
if not pf_cache:
    webbrowser.open_new_tab("https://www.roblox.com/games/292439477/Phantom-Forces")
if not ar2_cache:
    webbrowser.open_new_tab("https://www.roblox.com/games/863266079/Apocalypse-Rising-2")

while not mod_cache or not pf_cache or ar2_cache:
    if os.path.exists(mod_cache_check_path) and not mod_cache:
        print(f"{GREEN}Modding{DEFAULT} cache detected")
        mod_cache = True

    if os.path.exists(pf_cache_check_path) and not pf_cache:
        print(f"{GREEN}PF{DEFAULT} cache detected")
        pf_cache = True

    if os.path.exists(pf_cache_check_path) and not pf_cache:
        print(f"{GREEN}AR2{DEFAULT} cache detected")
        ar2_cache = True

    if mod_cache and pf_cache and ar2_cache:
        time.sleep(1)
        os.system(clear_command)

with open('assets.json', 'r') as file:
    data = json.load(file)

with open('presets.json', 'r') as file:
    presets = json.load(file)


def replace(files_to_delete, file_to_replace):
    try:
        copy_file_path = os.path.join(folder_path, file_to_replace)
        if os.path.exists(copy_file_path):
            for file_to_delete in files_to_delete:
                delete_file_path = os.path.join(folder_path, file_to_delete)
                if os.path.exists(delete_file_path):
                    os.remove(delete_file_path)
                    # print(f'{file_to_delete} has been deleted.')
                else:
                    print(f'{RED}{file_to_delete} not found.{DEFAULT}')

                new_file_path = os.path.join(folder_path, file_to_delete)
                shutil.copy(copy_file_path, new_file_path)
                # print(f'{copy_file_path} has been copied to {new_file_path}.')
                print(f'{BLUE}{file_to_delete} has been replaced with {file_to_replace}.{DEFAULT}')
        else:
            print(f'{RED}{file_to_replace} not found.{DEFAULT}')

    except Exception as e:
        if hasattr(e, 'winerror') and e.winerror == 183:
            pass
        else:
            print(f'{RED}An error occurred: {e}{DEFAULT}\n')


def get_hashes():
    output = []
    print(
        f"\nasset replacements:\n0:  {GREEN}Custom{DEFAULT}\n1:  {GREEN}Sights{DEFAULT}\n2:  {GREEN}Gun sounds{DEFAULT}\n3:  {GREEN}Gun skins{DEFAULT}\n4:  {GREEN}No textures{DEFAULT}\n5: {GREEN}Hit tweaks{DEFAULT}\n6: {GREEN}Misc tweaks{DEFAULT}\n7: )
    options = input(": ")
    try:
        match int(options):
            case 0:
                output.append(([input("\nEnter asset to change: ")], input("Enter replacement: ")))
            case 1:
                sight_option = input(
                    f"\nEnter sight option:\n1: {GREEN}Reticle tweaks{DEFAULT}\n2: {GREEN}Sight model tweaks{DEFAULT}\n3: {GREEN}Ballistics tracker tweaks{DEFAULT}\n: ")
                try:
                    match int(sight_option):
                        case 1:
                            reticle = dlist("reticles")
                            reticle_replacement = dlist("reticle replacement")
                            if reticle and reticle_replacement:
                                output.append(([reticle], reticle_replacement))
                        case _:
                            print("Invalid option")
                except Exception as e:
                    print(f"{RED}Error: {e}{DEFAULT}")
            case 4:
                    output.append(
                        (data["textures"], 'd2dfde24b1e69b530645ac4fe5ef4572'))  # no textures without downside
            case 4:
                    output.append(([dlist("gun skins")], dlist("skins")))
            case 3:
                sound = dlist("gun sounds")
                sound_replacement = dlist("replacement sounds")
                if sound and sound_replacement:
                    output.append(([sound], sound_replacement))
            case 5:  #
                hit_option = input(
                    f"\nEnter hit option:\n1: {GREEN}Headshot sounds{DEFAULT}\n1: {GREEN}Chest/limb sounds{DEFAULT}\n2:")
                match int(hit_option):
                    case 1:
                        output.append((['f18a3d8802af7033d415ee22d9097990'], dlist("replacement sounds")))  # headshot
                    case 2:
                        output.append((['4e8756761c1bfe163a5a03ef5d6b0d56', '489a66f78dd94311b84f9e368db4df82'], dlist("replacement sounds"))) #hit sounds
                    case _:
                        print("Enter a Valid Option!")
            case _:
                print("Invalid number.")
    except Exception as e:
        print(f"{RED}Error: {e}{DEFAULT}")

    return output


print(f"Welcome to: {GREEN}Reasion!{DEFAULT}\n")
start = True
while True:
    if not start:
        print(" ")
    start = False
    menu = input(
        f"Enter the number corresponding to what you'd like to do:\n1: {GREEN}Ingame asset replacements{DEFAULT}\n2: {GREEN}Presets{DEFAULT}\n3: {GREEN}Block (experimental, dont use){DEFAULT}\n4: {GREEN}Cache Settings{DEFAULT}\n5: {GREEN}Settings{DEFAULT}\n6: {GREEN}Exit{DEFAULT}\n: ")
    if menu == '1':
        replacements = get_hashes()
        for replacement in replacements:
            if isinstance(replacement[1], list):
                if len(replacement[0]) == len(replacement[1]):
                    for i, replac in enumerate(replacement[0]):
                        replace([replac], replacement[1][i])
            else:
                replace(replacement[0], replacement[1])

    elif menu == '2':
        preset_option = input(
            f"\nPresets:\n1: {GREEN}Load preset{DEFAULT}\n2: {GREEN}Add preset{DEFAULT}\n3: {GREEN}Delete preset{DEFAULT}\n: ")

        if preset_option == '1':
            if presets:
                name = preset_check()

                n_asset = 0
                r_asset = 1
                loops = 1
                if name:
                    values = int((len(presets[name]) / 2) + 1)
                if name in presets:
                    while loops != values:
                        replace([presets[name][n_asset]], presets[name][r_asset])
                        n_asset += 2
                        r_asset += 2
                        loops += 1
                else:
                    print(f"{RED}{name}{DEFAULT} does not exist.")
            else:
                print("No presets available")

        elif preset_option == '2':
            new_preset = input("\nEnter preset name\n: ")
            if new_preset not in presets:
                presets[new_preset] = []
            while True:
                replacements = get_hashes()
                for replacement in replacements:
                    if isinstance(replacement[1], list):
                        if len(replacement[0]) == len(replacement[1]):
                            for i, replac in enumerate(replacement[0]):
                                presets[new_preset].append(replac)
                                presets[new_preset].append(replacement[1][i])
                                print(f"{BLUE}Added successfully ({replac} -> {replacement[1][i]}){DEFAULT}")
                        else:
                            print(f"{RED}This replacement is not supported, changes not applied{DEFAULT}")
                            presets[new_preset] = []
                    else:
                        for replac in replacement[0]:
                            presets[new_preset].append(replac)
                            presets[new_preset].append(replacement[1])
                            print(f"{BLUE}Added successfully ({replac} -> {replacement[1]}){DEFAULT}")
                with open('presets.json', 'w') as f:
                    json.dump(presets, f, indent=4)
                    print(f"{BLUE}Preset saved{DEFAULT}")
                repeat = input("Continue editing preset? (y/n)\n: ").lower()
                if repeat == 'n':
                    break

        elif preset_option == '3':
            if presets:
                name = preset_check()

                if name in presets:
                    del presets[name]
                    with open("presets.json", 'w') as file:
                        json.dump(presets, file, indent=4)
                    print(f"{GREEN}{name}{DEFAULT} deleted successfully.")
                else:
                    print(f"{RED}{name}{DEFAULT} does not exist.")
            else:
                print("No presets available to delete.")

        else:
            print("Invalid option")

    elif menu == '3':
        blockwarn = input(
            f"\n{RED}Warning: This is highly experimental and volatile to causing errors, requiring run.bat to be ran as admin to use. Only continue if you are aware of what youre doing.\nType 'done' to proceed, anything else will cancel.\n{DEFAULT}")
        if blockwarn == "done":
            file_path = r"C:\Windows\System32\drivers\etc\hosts"
            with open(file_path, "r") as file:
                content = file.read()

            blockedlist = []
            unblockedlist = []

            for i in range(8):
                if f"#127.0.0.1 c{i}.rbxcdn.com" in content:
                    unblockedlist.append(f"c{i}")
                elif f"127.0.0.1 c{i}.rbxcdn.com" in content:
                    blockedlist.append(f"c{i}")

                if f"#127.0.0.1 t{i}.rbxcdn.com" in content:
                    unblockedlist.append(f"t{i}")
                elif f"127.0.0.1 t{i}.rbxcdn.com" in content:
                    blockedlist.append(f"t{i}")

            print("\nCurrently blocked:", " ".join(blockedlist))
            print("Currently unblocked:", " ".join(unblockedlist))


            def website_blocks():
                website_blocklist = []
                print("Enter c(num)/t(num) to block/unblock (type 'done' when finished)")
                while True:
                    website_name = input("Enter string: ")
                    if website_name.lower() == 'done':
                        break
                    website_blocklist.append(website_name)
                return website_blocklist


            website_block = website_blocks()

            try:
                modified_content = content
                for string_thing in website_block:
                    if f"#127.0.0.1 {string_thing}.rbxcdn.com" in content:
                        modified_content = modified_content.replace(f"#127.0.0.1 {string_thing}.rbxcdn.com",
                                                                    f"127.0.0.1 {string_thing}.rbxcdn.com")
                        print("Blocked!")
                    elif f"127.0.0.1 {string_thing}.rbxcdn.com" in content:
                        modified_content = modified_content.replace(f"127.0.0.1 {string_thing}.rbxcdn.com",
                                                                    f"#127.0.0.1 {string_thing}.rbxcdn.com")
                        print("Unblocked!")
                    else:
                        print("No text found, blocking it.")
                        modified_content += f"\n127.0.0.1 {string_thing}.rbxcdn.com"

            except Exception as e:
                print(f"An error occurred: {e}")

            try:
                with open(file_path, "w") as file:
                    file.write(modified_content)
            except Exception as e:
                print(f"{RED}An error occurred: {e}{DEFAULT}")
        else:
            pass

    elif menu == '4':
        menu = input(
            f"\nEnter the number corresponding to what you'd like to do:\n1: {GREEN}Revert replacement{DEFAULT}\n2: {GREEN}Clear full cache{DEFAULT}\n: ")
        if menu == '1':
            replacements = get_hashes()
            for replacement in replacements:
                delete_stuff(replacement[0])

        elif menu == '2':
            resetkwarn = input(
                f"\n{RED}Warning: This will fully reset all tweaks and anything loaded from any game.\nType 'done' to proceed, anything else will cancel.\n{DEFAULT}")
            if resetkwarn == "done":
                def delete_all_in_directory(directory):
                    try:
                        if os.path.exists(directory):
                            for filename in os.listdir(directory):
                                file_path = os.path.join(directory, filename)
                                try:
                                    if os.path.isfile(file_path) or os.path.islink(file_path):
                                        os.unlink(file_path)
                                    elif os.path.isdir(file_path):
                                        shutil.rmtree(file_path)
                                except Exception as e:
                                    print(f'Failed to delete {file_path}. Reason: {e}')
                        else:
                            print(f'{RED}The directory {directory} does not exist.{DEFAULT}')
                    except Exception as e:
                        print(f'{RED}Error: {e}{DEFAULT}')


                delete_all_in_directory(folder_path)
                print("Cleared cache, rejoin relevant experiences")

    elif menu == '5':
        b_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Bloxstrap', 'Modifications')
        Cset = ["ClientSettings", "ClientAppSettings.json"]
        settings_file_path = os.path.join(b_path, *Cset)

        cache_flags = {
            "DFIntNumAssetsMaxToPreload": "9999999",
            "DFIntAssetPreloading": "9999999",
            "DFIntHttpCacheCleanMinFilesRequired": "9999999"
        }

        if not os.path.exists(b_path):
            print(f"{RED}Bloxstrap not found{DEFAULT}")
        else:
            if not os.path.exists(settings_file_path):
                print(f"{RED}Settings file not found: {settings_file_path}{DEFAULT}")
            else:
                with open(settings_file_path, 'r') as file:
                    settings_data = json.load(file)

                cacheclear = "False"
                for key, value in cache_flags.items():
                    if settings_data.get(key) != value:
                        cacheclear = "True"
                        break

                cache_color = RED if cacheclear == "False" else BLUE

                print(
                    f"\nSettings:\n1: {GREEN}Auto Cache Clear : {cache_color}{cacheclear}{DEFAULT}\n"
                )

                settings = input(": ")
                try:
                    match int(settings):
                        case 1:
                            if cacheclear == "False":
                                for key in cache_flags.keys():
                                    settings_data.pop(key, None)
                                cacheclear = "True"
                                val2 = "True"
                                val_color = BLUE
                            else:
                                settings_data.update(cache_flags)
                                cacheclear = "False"
                                val2 = "False"
                                val_color = RED
                            val = "Auto Cache Clear"
                        case _:
                            print("Invalid number.")

                    with open(settings_file_path, 'w') as file:
                        json.dump(settings_data, file, indent=4)

                    print(f"\n{GREEN}Successfully changed {BLUE}{val}{GREEN} to {val_color}{val2}{DEFAULT}!")

                except ValueError:
                    print(f"{RED}Invalid input. Please enter a number.{DEFAULT}")
                except Exception as e:
                    print(f"{RED}Error: {e}{DEFAULT}")

    elif menu == '6':
        print("\nExiting the program.")
        break

    else:
        print("Invalid, type a corresponding number!")
