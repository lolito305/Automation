# File Organization by Type

This Python script automates the process of organizing files based on their types. It prompts the user to enter the source folder containing the files to be organized and the destination folder where the files will be moved.

## Features

- Organizes files based on their types into separate folders.
- Supports various file types, including images, videos, documents, audio, and compressed files.
- Creates destination folders if they don't exist.

## Usage

1. Clone the repository or download the script file.

2. Open the script file in a text editor.

3. Modify the following variables in the script according to your setup:

    - `source_folder`: Enter the path of the folder you want to organize.
    - `destination_folder`: Enter the path of the folder where you want to move the files.

4. Save the script file.

5. Open a terminal or command prompt and navigate to the directory where the script file is located.

6. Run the script by executing the following command:

    ```shell
    python file_organization.py
    ```

7. The script will prompt you to enter the path of the source folder and the destination folder.

8. Once you provide the paths, the script will start organizing the files into separate folders based on their types.

9. The script will continuously run and organize any new files added to the source folder.

10. Press `Ctrl + C` to stop the script.

## Customization

- The script supports the following file types and organizes them into their respective folders:

    - Images: .jpg, .jpeg, .png, .gif, .tiff, .psd, .ai, .raw
    - Videos: .mp4, .mov, .avi, .mkv, .wmv, .flv, .webm, .vob, .mng, .qt
    - Documents: .doc, .docx, .pdf, .txt, .rtf, .tex, .wpd, .odt, .ppt, .pptx, .xls, .xlsx, .ods, .csv, .xml
    - Audio: .mp3, .wav, .wma, .aac, .flac, .alac, .aiff, .dsd, .pcm, .ogg, .oga, .m4a, .m4p, .m4b, .m4r, .3ga, .mid, .midi, .amr, .mp2
    - Compressed: .zip, .rar, .7z, .arj, .deb, .pkg, .rpm, .tar.gz, .z, .gz, .lz, .lzma, .lzo, .xz, .bz2, .bz, .tbz2, .tbz, .tz, .z, .Z, .cpio, .lz4, .lzf, .lha, .lzh, .rz, .sfark, .sz, .zoo

- You can modify the `file_types` dictionary in the script to add or remove file types as needed.

## Notes

- Make sure you have Python installed on your system.
- The script uses the `os` and `shutil` modules, which are part of the Python Standard Library and do not require any additional installation.
