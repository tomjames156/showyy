import re

def get_file_extension(file_name):

    file_extension = re.search(r"\.(jpg|png|jpeg|gif|pdf)", file_name)
    return file_extension.group()
