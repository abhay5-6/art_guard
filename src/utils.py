#fetches hidden files
def is_hidden(path):
    return path.name.startswith(".")

#checks if file is a supported image type(not to convert)
def is_supported_image(path):
    return path.suffix.lower() in [".jpg", ".jpeg"]

#checks if file is a krita file
def is_kra_file(path):
    return path.suffix.lower() == ".kra"
