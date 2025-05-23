from PIL import Image
import imagehash
import os
import csv

def generate_hashes(image_folder, hashfunc=imagehash.phash):
    """
    Generate perceptual hashes for all images in the folder.

    Args:
        image_folder (str): Path to folder with images.
        hashfunc (function): Hash function from imagehash library (default: phash).

    Returns:
        dict: filename -> hash value
    """
    hashes = {}
    supported_exts = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")

    for filename in sorted(os.listdir(image_folder)):
        if filename.lower().endswith(supported_exts):
            img_path = os.path.join(image_folder, filename)
            try:
                with Image.open(img_path) as img:
                    hash_val = hashfunc(img)
                hashes[filename] = hash_val
            except Exception as e:
                print(f"[WARN] Failed to process {filename}: {e}")
    return hashes


def detect_duplicates(hashes, max_distance=5):
    """
    Detect duplicates or near-duplicates based on hash distance threshold.

    Args:
        hashes (dict): filename -> imagehash object
        max_distance (int): max Hamming distance to consider images duplicates

    Returns:
        list of tuples: (filename1, filename2, distance)
    """
    duplicates = []
    checked = set()
    files = list(hashes.keys())

    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            file1, file2 = files[i], files[j]
            if (file1, file2) in checked or (file2, file1) in checked:
                continue
            dist = hashes[file1] - hashes[file2]
            if dist <= max_distance:
                duplicates.append((file1, file2, dist))
            checked.add((file1, file2))
    return duplicates


def save_duplicates_to_csv(duplicates, output_file="duplicates_report.csv"):
    """
    Save duplicates list to a CSV file.

    Args:
        duplicates (list): list of (file1, file2, distance) tuples
        output_file (str): CSV filename
    """
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["File 1", "File 2", "Hamming Distance"])
        for row in duplicates:
            writer.writerow(row)
    print(f"[INFO] Duplicates report saved to {output_file}")


if __name__ == "__main__":
    folder_path = r"C:/Users/Sathwik/myprojects/frames"
    print(f"Scanning images in: {folder_path}")

    hashes = generate_hashes(folder_path)
    print(f"Total images processed: {len(hashes)}")

    duplicates = detect_duplicates(hashes)
    if duplicates:
        print(f"Found {len(duplicates)} duplicates or near-duplicates:")
        for dup in duplicates:
            print(f"  {dup[0]} <-> {dup[1]} (distance: {dup[2]})")
        save_duplicates_to_csv(duplicates)
    else:
        print("No duplicates found.")
