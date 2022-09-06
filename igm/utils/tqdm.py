import shutil


def tqdm_ncols(maxwidth: int = 80):
    width, _ = shutil.get_terminal_size()
    return min(maxwidth, width)
