import sublime
import os.path
import converter
import project_files


class RelatedFiles(object):
    window = None
    paths = None
    root = None
    from_cache = None

    def __init__(self, window):
        self.window = window
        self.paths = []
        self.root = window.folders()[0]
        self.from_cache = False

    def append(self, path):
        self.paths.append(path)

    def choose_path(self):
        if len(self.paths) > 1:
            choices = [path.replace(self.root + '/', '') for path in self.paths]
            self.window.show_quick_panel(choices, self.open_path)
        elif len(self.paths) == 1:
            self.open_path(0)
        else:
            sublime.status_message("Cannot find related file !")

    def open_path(self, index):
        if index == -1:
            return

        win = self.window
        path = self.paths[index]

        if win.num_groups() > 1:
            win.focus_group((win.active_group() + 1) % win.num_groups())

        win.open_file(path)


class RelatedFileCache(object):
    related_files = {}
    related_file_names = {}

    def get_for_path(self, key, window):
        result = None

        if key in self.related_files:
            result = self.related_files[key]
            result.window = window
            result.from_cache = True
        else:
            result = RelatedFiles(window)
            self.related_files[key] = result

        return result

    def get_for_filename(self, key, window):
        result = None

        if key in self.related_file_names:
            result = self.related_file_names[key]
            result.window = window
            result.from_cache = True
        else:
            result = RelatedFiles(window)
            self.related_file_names[key] = result

        return result


cache = RelatedFileCache()


def by_path_patterns(view):
    related_files = cache.get_for_path(view.file_name(), view.window())

    if not related_files.from_cache:
        print "IS NEW path"
        for paths in paths_for_pattern('open_related_patterns', view):
            for path in paths:
                if os.path.exists(path):
                    related_files.append(path)

    return related_files


def by_filename_patterns(view):
    related_files = cache.get_for_filename(view.file_name(), view.window())

    if not related_files.from_cache:
        print "IS NEW name"
        for patterns in paths_for_pattern('open_related_file_patterns', view):
            for path_pattern in patterns:
                name_pattern = os.path.basename(path_pattern)
                paths = project_files.find(view.window().folders(),
                                           lambda filename: filename == name_pattern)

                for path in paths:
                    related_files.append(path)

    return related_files


def paths_for_pattern(pattern_key, view):
    current_file = view.file_name()

    for patterns in view.settings().get(pattern_key, []):
        yield converter.create(patterns, sublime.platform()).convert(current_file)
