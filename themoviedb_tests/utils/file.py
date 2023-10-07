from os.path import abspath, dirname, join


def get_path(*segments):
    project_root = abspath(dirname(dirname(dirname(__file__))))
    return abspath(join(project_root, *segments))
