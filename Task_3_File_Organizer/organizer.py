import os
import shutil
import logging
from pathlib import Path

# Logging configuration
logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# File extension categories
FILE_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json"]
}


def get_category(extension):
    """Return the category for a file extension."""
    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category

    return "Others"


def get_unique_path(destination):
    """Generate a unique filename if a file already exists."""
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_destination = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )

        if not new_destination.exists():
            return new_destination

        counter += 1


def organize_files(folder_path):
    """Organize files into category folders."""

    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        print("Error: The provided folder does not exist.")
        return

    moved = 0
    skipped = 0
    failed = 0

    print("\nStarting file organization...\n")

    try:
        entries = list(os.scandir(folder))

        for entry in entries:

            if not entry.is_file(follow_symlinks=False):
                continue

            source = Path(entry.path)
            category = get_category(source.suffix)

            destination_folder = folder / category

            try:
                destination_folder.mkdir(exist_ok=True)

                destination = get_unique_path(
                    destination_folder / source.name
                )

                shutil.move(str(source), str(destination))

                moved += 1
                logging.info("Moved %s to %s", source, destination)

                print(f"Moved: {source.name} -> {category}")

            except FileExistsError as error:
                skipped += 1
                logging.warning("File collision: %s", error)
                print(f"Skipped: {source.name} (file already exists)")

            except PermissionError as error:
                failed += 1
                logging.error("Permission denied: %s", error)
                print(f"Permission denied: {source.name}")

            except OSError as error:
                failed += 1
                logging.error("Could not move %s: %s", source, error)
                print(f"Could not move {source.name}: {error}")

    except PermissionError as error:
        print(f"Cannot access folder: {error}")
        logging.error("Cannot access folder: %s", error)
        return

    print("\n" + "=" * 45)
    print("       FILE ORGANIZATION SUMMARY")
    print("=" * 45)
    print(f"Total files moved : {moved}")
    print(f"Files skipped     : {skipped}")
    print(f"Files failed      : {failed}")
    print("=" * 45)

    logging.info(
        "Organization completed. Moved=%s, Skipped=%s, Failed=%s",
        moved, skipped, failed
    )


def main():
    print("=" * 45)
    print("       AUTOMATED FILE ORGANIZER")
    print("=" * 45)

    folder_path = input(
        "\nEnter folder path to organize: "
    ).strip().strip('"')

    organize_files(folder_path)


if __name__ == "__main__":
    main()
