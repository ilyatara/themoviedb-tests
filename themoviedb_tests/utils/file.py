from os.path import abspath, dirname, join


def get_abs_path(relative_path):
    project_root = abspath(dirname(dirname(dirname(__file__))))
    return abspath(join(project_root, relative_path))
