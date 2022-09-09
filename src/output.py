def assemble_zip(title):
    # import streamlit as st
    # from shutil import make_archive

    # directory = "outputs"
    # book_title = f'outputs/{title}'
    # zip_file = make_archive(book_title, "zip", directory)  # zipping the directory

    # return zip_file

    import pathlib
    import zipfile
    from stqdm import stqdm

    directory = pathlib.Path("outputs/")
    zip_name = f'outputs/{title}.zip'

    with zipfile.ZipFile(zip_name, mode="w") as archive:
        for file_path in stqdm(directory.iterdir()):
            archive.write(file_path, arcname=file_path.name)

    return zip_name