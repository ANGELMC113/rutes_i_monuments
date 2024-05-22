# generics.py

"""Contains defined exceptions and generic transversal funcions."""



def check_file_extension(filename: str, extension: str) -> None:
    """Checks if filename is of the desired extension.
    Raises IOError if it's incorrect."""
    if filename[-4:] != extension:
        raise IOError(f"The format of the given file is incorrect. Filename should finish in {extension}")