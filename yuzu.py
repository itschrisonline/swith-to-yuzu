import os
import re

def sanitize_for_filename(input_string):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        input_string = input_string.replace(char, '-')
    # Replace sequences of dots at the end of a string
    input_string = re.sub(r'\.{2,}$', '', input_string)
    return input_string.strip()

def normalize_string(s):
    s = re.sub(r'[^\x00-\x7F]+', '_', s)
    s = s.replace("]", "_")
    s = s.replace("[", "_")
    s = s.replace("\t", " ")
    s = sanitize_for_filename(s)
    return s

# The source directory where the cheats are located
src_dir = r"D:\AAC"

# The destination directory where the cheats will be sorted
dst_base_dir = r"D:\AAB"

MAX_TITLE_LENGTH = 100

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".txt"):
            with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Extract the title ID from the path
            title_id = root.split("\\")[-2]

            # Process each cheat
            for index, line in enumerate(lines):
                if line.startswith("[") and "]" in line:
                    cheat_title = line.strip()[1:-1]
                    sanitized_title = normalize_string(cheat_title)

                    # Truncate the title if it's too long
                    if len(sanitized_title) > MAX_TITLE_LENGTH:
                        sanitized_title = sanitized_title[:MAX_TITLE_LENGTH].rstrip('.-_ ')

                    new_dir = os.path.join(dst_base_dir, title_id, sanitized_title, "cheats")
                    os.makedirs(new_dir, exist_ok=True)

                    cheat_code = []
                    cheat_code.append("[" + sanitized_title + "]\n")
                    index += 1
                    while index < len(lines) and not lines[index].startswith("["):
                        cheat_code.append(lines[index])
                        index += 1

                    # Convert filename to uppercase
                    upper_file = file.upper()
                    
                    with open(os.path.join(new_dir, upper_file), 'w', encoding='utf-8') as cheat_file:
                        cheat_file.writelines(cheat_code)
                        

print("Finished organizing cheats!")
