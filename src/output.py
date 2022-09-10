def assemble_zip(title):
    import pathlib
    import zipfile
    from stqdm import stqdm

    directory = pathlib.Path("outputs/")
    zip_name = f"outputs/{title}.zip"

    with zipfile.ZipFile(zip_name, mode="w") as archive:
        for file_path in stqdm(directory.iterdir()):
            archive.write(file_path, arcname=file_path.name)

    return zip_name