#This program is to help find the script files and any files that contains certain words so I don't have to search millions of files. 

import os

#path for your unload files
ROM_PATH = r"E:\Xenosaga_project\Extracted\NDS_UNPACK"

#these are for xenosaga, but can be changed for what ever game.
TARGET_WORDS = [
    "エーテル",              # example: ether
    "スキル",       # example: "skill"
    "アイテム",     # example: "item"
    "U.M.N."
]

# How many characters to show as a sample around the match, so we can verify what it is.
SAMPLE_CHARS = 50

#saves the output files
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "found_texts.txt")


def bytes_for_shiftjis(text):
    """Convert a Japanese string to bytes using Shift-JIS encoding"""
    try:
        return text.encode("shift_jis")
    except:
        return None

def search_file_for_words(file_path, target_bytes_list):
    matches = []
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            
            # Check if EVERY word is in the data (The AND logic)
            if all(target_bytes in data for target_bytes in target_bytes_list):
                # If they all exist, collect samples for each
                for target_bytes in target_bytes_list:
                    index = data.find(target_bytes)
                    # Extract a sample around the match
                    start = max(index - 10, 0)
                    end = min(index + len(target_bytes) + 40, len(data))
                    sample = data[start:end].decode("shift_jis", errors="replace")
                    matches.append(sample)
                return matches
            
        return None
    except Exception as e:

        return None

def scan_folder_for_words(folder_path, target_words):
    # convert words to Shift-JIS bytes
    target_bytes_list = [bytes_for_shiftjis(w) for w in target_words]
    results = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            path = os.path.join(root, file)
            matches = search_file_for_words(path, target_bytes_list)
            if matches:
                results.append((path, matches))
    return results

if __name__ == "__main__":
    print("Scanning ROM for specific words...")
    results = scan_folder_for_words(ROM_PATH, TARGET_WORDS)
    
    if results:
        print(f"\nFound {len(results)} files containing target words.\nSaving results to text file...")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file:
            for f, samples in results:
                out_file.write(f"File: {f}\n")
                for s in samples:
                    out_file.write(f"Sample: {s}\n")
                out_file.write("\n" + "-"*50 + "\n\n")
        print(f"Results saved to: {OUTPUT_FILE}")
    else:
        print("No target words found.")