def assemble_zip(title):
    import pathlib
    import zipfile
    from stqdm import stqdm

    directory = pathlib.Path("outputs/")
    zip_name = f"outputs/{title}.zip"

    with zipfile.ZipFile(zip_name, mode="w") as archive:
        for file_path in stqdm(directory.iterdir()):
            print(f'Current path: {file_path}')
            if pathlib.Path(file_path).suffix == '.wav':
                print(f'Archiving {file_path}')
                archive.write(file_path, arcname=file_path.name)
                print(f'Archived {file_path}')

    return zip_name