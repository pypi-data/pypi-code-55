""""A small sphinx extension to add a ``panels`` directive.

This directive creates panels of content in an M x N layout.
The panels are separated by `---`::

    .. panels::

        Content of the top-left panel

        ---

        Content of the top-right panel

        ---

        Content of the bottom-left panel

        ---

        Content of the bottom-right panel

The content can be any valid rST.
"""
import os
import re
from urllib.parse import unquote

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.util.docutils import SphinxDirective

__version__ = "0.3.2"

DEFAULT_CONTAINER = "container pb-4"
DEFAULT_COLUMN = "col-lg-6 col-md-6 col-sm-6 col-xs-12 p-2"
DEFAULT_CARD = "shadow"

RE_OPTIONS = re.compile(
    r"\:(column|card|body|header|footer|"
    r"img-top|img-bottom|img-top-cls|img-bottom-cls)\:\s*(\+?)\s*(.*)"
)

LOCAL_FOLDER = os.path.dirname(os.path.abspath(__file__))


def parse_panels(
    content,
    content_offset,
    default_classes,
    panel_regex=None,
    head_regex=None,
    foot_regex=None,
):
    """split a block of content into panels.

    example::

        ---
        header
        ===
        body
        ...
        footer
        ---
        next panel

    """
    panel_regex = panel_regex or re.compile(r"^\-{3,}$")
    head_regex = head_regex or re.compile(r"^\^{3,}$")
    foot_regex = foot_regex or re.compile(r"^\+{3,}$")

    if isinstance(content, str):
        content = content.splitlines()

    panel_blocks = []
    start_line = 0
    header_split = footer_split = None
    for i, line in enumerate(content):
        if panel_regex.match(line.strip()):
            if i != 0:
                panel_blocks.append(
                    parse_single_panel(
                        content[start_line:i],
                        start_line,
                        header_split,
                        footer_split,
                        content_offset,
                        default_classes,
                    )
                )
            start_line = i + 1
            header_split = footer_split = None
        if head_regex.match(line.strip()) and footer_split is None:
            header_split = i - start_line
        if foot_regex.match(line.strip()):
            footer_split = i - start_line
        # TODO warn if multiple header_split or footer_split
        # TODO assert header_split is before footer_split
    try:
        panel_blocks.append(
            parse_single_panel(
                content[start_line:],
                start_line,
                header_split,
                footer_split,
                content_offset,
                default_classes,
            )
        )
    except IndexError:
        pass
    return panel_blocks


def parse_single_panel(
    content, offset, header_split, footer_split, content_offset, default_classes
):
    """parse each panel data to dict."""
    output = {}
    body_start = 0
    body_end = len(content)

    # parse the classes required for this panel, and top/bottom images
    classes = default_classes.copy()
    for opt_offset, line in enumerate(content):
        opt_match = RE_OPTIONS.match(line)
        if not opt_match:
            break
        body_start += 1
        if opt_match.group(1) in ["img-top", "img-bottom"]:
            output[opt_match.group(1)] = opt_match.group(3)
            continue
        if opt_match.group(2) == "+":
            classes[opt_match.group(1)] = (
                classes.get(opt_match.group(1), []) + opt_match.group(3).split()
            )
        else:
            classes[opt_match.group(1)] = opt_match.group(3).split()

    if classes:
        output["classes"] = classes

    if header_split is not None:
        header_content = content[opt_offset:header_split]
        header_offset = content_offset + offset + opt_offset
        body_start = header_split + 1
        output["header"] = (header_content, header_offset)

    if footer_split is not None:
        footer_content = content[footer_split + 1 :]
        footer_offset = content_offset + offset + footer_split
        body_end = footer_split
        output["footer"] = (footer_content, footer_offset)

    body_content = content[body_start:body_end]
    body_offset = content_offset + offset + body_start
    output["body"] = (body_content, body_offset)
    return output


def add_child_classes(node):
    """Add classes to specific child nodes."""
    for para in node.traverse(nodes.paragraph):
        para["classes"] = ([] if "classes" in para else para["classes"]) + ["card-text"]
    for title in node.traverse(nodes.title):
        title["classes"] = ([] if "classes" in title else title["classes"]) + [
            "card-title"
        ]


class Panels(SphinxDirective):
    """Two Column Panels."""

    has_content = True
    option_spec = {
        "container": directives.unchanged,
        "column": directives.unchanged,
        "card": directives.unchanged,
        "body": directives.unchanged,
        "header": directives.unchanged,
        "footer": directives.unchanged,
        "img-top-cls": directives.unchanged,
        "img-bottom-cls": directives.unchanged,
    }

    def run(self):
        default_classes = {
            "container": DEFAULT_CONTAINER.split(),
            "column": DEFAULT_COLUMN.split(),
            "card": DEFAULT_CARD.split(),
            "body": [],
            "header": [],
            "footer": [],
            "img-top-cls": [],
            "img-bottom-cls": [],
        }

        # set classes from the directive options
        for key, value in default_classes.items():
            if key not in self.options:
                continue
            option_value = self.options[key].strip()
            if option_value.startswith("+"):
                default_classes[key] += option_value[1:].split()
            else:
                default_classes[key] = option_value.split()

        # split the block into panels
        panel_blocks = parse_panels(
            self.content,
            self.content_offset,
            default_classes,
            panel_regex=self.env.app.config.panels_delimiters[0],
            head_regex=self.env.app.config.panels_delimiters[1],
            foot_regex=self.env.app.config.panels_delimiters[2],
        )

        # set the top-level containers
        parent = nodes.container(in_panel=True, classes=default_classes["container"])
        rows = nodes.container(in_panel=True, classes=["row"])
        parent += rows

        for data in panel_blocks:

            classes = data["classes"]

            column = nodes.container(
                in_panel=True, classes=["d-flex"] + classes["column"]
            )
            rows += column
            card = nodes.container(
                in_panel=True, classes=["card", "w-100"] + classes["card"]
            )
            column += card

            if "img-top" in data:
                image_top = nodes.image(
                    "",
                    uri=directives.uri(data["img-top"]),
                    alt="img-top",
                    classes=["card-img-top"] + classes["img-top-cls"],
                )
                self.add_name(image_top)
                card += image_top

            if "header" in data:
                header = nodes.container(
                    in_panel=True, classes=["card-header"] + classes["header"]
                )
                card += header

                header_content, header_offset = data["header"]
                self.state.nested_parse(header_content, header_offset, header)
                add_child_classes(header)

            body = nodes.container(
                in_panel=True, classes=["card-body"] + classes["body"]
            )
            card += body

            body_content, body_offset = data["body"]
            self.state.nested_parse(body_content, body_offset, body)
            add_child_classes(body)

            if "footer" in data:
                footer = nodes.container(
                    in_panel=True, classes=["card-footer"] + classes["footer"]
                )
                card += footer

                footer_content, footer_offset = data["footer"]
                self.state.nested_parse(footer_content, footer_offset, footer)
                add_child_classes(footer)

            if "img-bottom" in data:
                image_top = nodes.image(
                    "",
                    uri=directives.uri(data["img-bottom"]),
                    alt="img-bottom",
                    classes=["card-img-bottom"] + classes["img-bottom-cls"],
                )
                self.add_name(image_top)
                card += image_top

        return [parent]


def validate_config(app, config):
    if len(app.config.panels_delimiters) != 3:
        raise AssertionError(
            "panels_delimiters config must be of form: (header, body, footer)"
        )
    if len(set(app.config.panels_delimiters)) != 3:
        raise AssertionError("panels_delimiters config must contain unique values")
    try:
        app.config.panels_delimiters = tuple(
            [re.compile(s) for s in app.config.panels_delimiters]
        )
    except Exception as err:
        raise AssertionError(
            "panels_delimiters config must contain only compilable regexes: {}".format(
                err
            )
        )


def add_static_paths(app):
    if app.config.panels_add_boostrap_css:
        app.config.html_static_path.append(os.path.join(LOCAL_FOLDER, "css"))
        app.add_css_file("bs-grids.css")
        app.add_css_file("bs-cards.css")
        app.add_css_file("bs-borders.css")
        app.add_css_file("bs-buttons.css")


def visit_container(self, node):
    classes = "docutils container"
    if node.get("in_panel", False):
        # we don't want the CSS for container for these nodes
        classes = "docutils"
    self.body.append(self.starttag(node, "div", CLASS=classes))


def depart_container(self, node):
    self.body.append("</div>\n")


class LinkButton(SphinxDirective):
    """A directive to turn a link into a button."""

    has_content = False
    required_arguments = 1
    option_spec = {
        "type": lambda arg: directives.choice(arg, ("url", "ref")),
        "text": directives.unchanged,
        "tooltip": directives.unchanged,
        "classes": directives.unchanged,
    }

    def run(self):

        uri = self.arguments[0]
        link_type = self.options.get("type", "url")

        text = self.options.get("text", uri)
        innernode = nodes.inline("", text)

        if link_type == "ref":
            ref_node = addnodes.pending_xref(
                reftarget=unquote(uri),
                reftype="any",
                # refdoc=self.env.docname,
                refdomain="",
                refexplicit=True,
                refwarn=True,
            )
            innernode["classes"] = ["xref", "any"]
            if "tooltip" in self.options:
                ref_node["title"] = self.options["tooltip"]
        else:
            ref_node = nodes.reference()
            ref_node["refuri"] = uri
            if "tooltip" in self.options:
                ref_node["reftitle"] = self.options["tooltip"]

        self.set_source_info(ref_node)

        ref_node["classes"] = ["btn"] + self.options.get("classes", "").split()
        ref_node += innernode
        # sphinx requires that a reference be inside a block element
        container = nodes.paragraph()
        container += ref_node

        return [container]


def setup(app):
    app.add_directive("panels", Panels)
    app.add_config_value(
        "panels_delimiters", (r"^\-{3,}$", r"^\^{3,}$", r"^\+{3,}$"), "env"
    )
    app.connect("config-inited", validate_config)
    app.add_config_value("panels_add_boostrap_css", True, "env")
    app.connect("builder-inited", add_static_paths)
    # we override container html visitors,
    # to stop the default behaviour of adding the `container` class to all nodes
    app.add_node(
        nodes.container, override=True, html=(visit_container, depart_container)
    )
    app.add_directive("link-button", LinkButton)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
