import os
import shutil


source_folder = input("Enter the path of the folder you want to organize: ")
destination_folder = input("Enter the path of the folder you want to move the files to: ")

file_types = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".tiff", ".psd", ".ai", ".raw"],
    "videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".vob", ".mng", ".qt"],
    "documents": [".doc", ".docx", ".pdf", ".txt", ".rtf", ".tex", ".wpd", ".odt", ".ppt", ".pptx", ".xls", ".xlsx", ".ods", ".csv", ".xml"],
    "audio": [".mp3", ".wav", ".wma", ".aac", ".flac", ".alac", ".aiff", ".dsd", ".pcm", ".ogg", ".oga", ".m4a", ".m4p", ".m4b", ".m4r", ".3ga", ".mid", ".midi", ".amr", ".mp2"],
    "compressed": [".zip", ".rar", ".7z", ".arj", ".deb", ".pkg", ".rpm", ".tar.gz", ".z", ".gz", ".lz", ".lzma", ".lzo", ".xz", ".bz2", ".bz", ".tbz2", ".tbz", ".tz", ".z", ".Z", ".cpio", ".lz4", ".lzf", ".lha", ".lzh", ".rz", ".sfark", ".sz", ".zoo"],
}

for folder_name in set(file_types.values()):
    folder_path = os.path.join(destination_folder, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    while True:
        files = os.listdir(source_folder)
        for file in files:
            file_path = os.path.join(source_folder, file)

            if os.path.isfile(file_path):
                file_ext = os.path.splitext(file)[1][1:].lower()

                if file_ext in file_types:
                    folder_name = file_types[file_ext]
                    folder_path = os.path.join(destination_folder, folder_name)
                    new_file_path = os.path.join(folder_path, file)

                    shutil.move(file_path, new_file_path)
                    print(f"Moved {file} to {folder_name} folder.")