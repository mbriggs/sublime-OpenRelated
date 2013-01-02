import os


def find(directories, file_matcher):
    return (os.path.join(dirname, file)
        for directory in directories
        for dirname, _, files in walk(directory)
        for file in filter(file_matcher, files))


def walk(directory, ignored_directories=['.git', 'vendor']):
    ignore = lambda dirname: dirname not in ignored_directories
    for dir, dirnames, files in os.walk(directory):
        dirnames[:] = [dirname for dirname in filter(ignore, dirnames)]
        yield dir, dirnames, files
