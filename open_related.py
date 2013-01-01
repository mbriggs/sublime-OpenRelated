import sublime
import sublime_plugin
import os.path
import converter


class RelatedFiles(object):
    window = None
    paths = None
    root = None

    def __init__(self, window):
        self.window = window
        self.paths = []
        self.root = window.folders()[0]

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


class OpenRelatedCommand(sublime_plugin.WindowCommand):
    def run(self):
        related_files = RelatedFiles(self.window)
        view = self.window.active_view()
        current_file = view.file_name()

        for patterns in view.settings().get('open_related_patterns', []):
            paths = converter.create(patterns, sublime.platform()).convert(current_file)

            for path in paths:
                if os.path.exists(path):
                    related_files.append(path)

        related_files.choose_path()

    def is_enabled(self):
        return self.window.active_view() != None

    def description(self):
        return "Open related file."
