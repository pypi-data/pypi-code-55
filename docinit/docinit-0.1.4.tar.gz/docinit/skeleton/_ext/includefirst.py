from docutils.parsers.rst.directives.misc import Include


class IncludeFirst(Include):

    def run(self):
        files = self.arguments[0].split(',')
        for file in files:
            self.arguments[0] = file.strip()
            try:
                nodes = super().run()
            except:
                continue
            else:
                return nodes
        raise self.severe('Could not include any file.')


def setup(app):
    app.add_directive('includefirst', IncludeFirst)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }