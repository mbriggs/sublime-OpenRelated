import sublime_plugin
import related_files


class OpenRelatedCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()
        related = related_files.by_path_patterns(view)

        if (not related.paths):
            related = related_files.by_filename_patterns(view)

        related.choose_path()

    def is_enabled(self):
        return self.window.active_view() != None

    def description(self):
        return "Open related file."
