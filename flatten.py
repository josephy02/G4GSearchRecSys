# function for flatten
import os
import shutil

def flatten_folder(root_folder):
    # Loop through all files and subdirectories in the root folder
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Skip the root folder itself
        if dirpath == root_folder:
            continue

        # Move each file to the root folder
        for file in filenames:
            if file.lower().endswith(('.html', '.htm', '.pdf')):
                src = os.path.join(dirpath, file)
                dest = os.path.join(root_folder, file)

                # Handle duplicate file names
                if os.path.exists(dest):
                    base, ext = os.path.splitext(file)
                    dest = os.path.join(root_folder, f"{base}_copy{ext}")

                shutil.move(src, dest)

        # Remove empty subdirectory
        if not os.listdir(dirpath):
            os.rmdir(dirpath)

# Replace with the path to your main folder
root_folder = "/Users/joeyared/Desktop/INFO_376/geek"
flatten_folder(root_folder)
print("Folder flattened successfully!")