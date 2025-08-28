import os

from src.resources.controls.filters.filters import Filter

directory_path = './demo-images/'
output_path = './filtered_images/'

def main():
    FILTERA = Filter()
    
    entries = os.listdir(directory_path)
    print(f"Found {len(entries)} files in {directory_path}")

    for file_name in entries:
        print(f"Processing file: {file_name}")
        FILTERA.crop_center_object(
            image_path=os.path.join(directory_path, file_name),
            width=1000,
            height=1000,
            output_path=os.path.join(output_path, f"cropped_{file_name}"),
            margin=10
        )
        print(f"Finished processing file: {file_name}")

    return

if __name__=="__main__":
    main()