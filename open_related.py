import sublime
import sublime_plugin
import related_files


class OpenRelatedCommand(sublime_plugin.WindowCommand):

    def run(self, *args, **kwargs):
        if 'clear_cache' in kwargs and kwargs['clear_cache']:
            related_files.clear_cache()
            sublime.status_message("Cleared related file cache.")
            return

        print args
        print kwargs

        view = self.window.active_view()
        related = related_files.by_path_patterns(view)

        if (not related.paths):
            related = related_files.by_filename_patterns(view)

        related.choose_path()

    def is_enabled(self):
        return self.window.active_view() != None

    def description(self):
        return "Open related file."
