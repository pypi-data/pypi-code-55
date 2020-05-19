"""
Module for a Jira Textile like to Markdown parser
"""
import random
import re
import string

from rich.syntax import Syntax


class JiraDocument:
    """
    Class wich represent a Jira Rich text field such as an Issue Description or comment
    It provides methods to convert it to Markdown and prepare it for rendering through Rich
    """

    HEAD_COLORS = [
        "dodger_blue3",
        "dodger_blue2",
        "dodger_blue1",
        "deep_sky_blue3",
        "deep_sky_blue2",
        "deep_sky_blue1",
        "bright_blue",
    ]

    def __init__(self, raw: str):
        """
        Init a JiraDocument object

        Args:
            raw (str): The Jira rich text content
        """
        # Convert \n into \r\n to fulfill Jira's behaviour
        if raw:
            if "\n" in raw and "\r\n" not in raw:
                raw = raw.replace("\n", "\r\n")

            self.raw = raw
            self.elements = self._parse()
        else:
            self.raw = ""
            self.elements = []
            self.markdown = ""
            self.rendered = ""

    def _parse(self):
        """
        Parse the raw content line by line into cutom JiraElement objects
        It will groups block lines into BlockElement and create a list of all elements
        presents into the document
        """
        elements = []

        in_block = False
        block = ""
        block_type = ""
        block_style = ""

        for line in self.raw.split("\r\n"):
            # if line starts with {code}, {quote}, {panel} or {color}
            if (
                line.startswith("{quote")
                or line.startswith("{code")
                or line.startswith("{panel")
                or line.startswith("{color")
            ) and not in_block:
                if self.isoneline(line):
                    search = re.search(r"{(.*?)(:(.*?))?}(.*){.*}", line)
                    elements.append(
                        BlockElement(
                            search.string,
                            content=search[4],
                            content_type=search[1],
                            content_style=search[3],
                            oneline=True,
                        )
                    )
                    continue
                else:
                    in_block = True
                    search = re.search(r"\{(.*?)(:(.*?))?\}", line)
                    block_type = search[1]
                    if search[3]:
                        block_style = search[3]
                # Get the content existing after the block element to put back into block
                if re.search(r"\{.*\}(.*)", line):
                    block = re.search(r"\{.*\}(.*)", line)[1] + "\n"
            elif ("{quote" in line or "{code" in line or "{panel" in line or "{color" in line) and in_block:
                in_block = False
                # Get content esisting before the block element and put it back into block
                if re.search(r"\{.*\}(.*)", line):
                    block = block + re.search(r"(.*)\{.*\}.*", line)[1]
                elements.append(BlockElement(block, content=block, content_type=block_type, content_style=block_style,))
                block = ""
                block_style = ""
            else:
                if in_block:
                    block = block + line + "\n"
                else:
                    # Head Element
                    search = re.search(r"^h([0-9])\. (.*)$", line)
                    if search:
                        elements.append(HeadElement(search[0], content=search[2], level=int(search[1])))
                        continue
                    # List Item Element
                    search = re.search(r"^(\*+) (.*)$", line)
                    if search:
                        elements.append(
                            ListItemElement(search[0], content=search[2], level=len(search[1]), item_type="*",)
                        )
                        continue
                    search = re.search(r"^(#+) (.*)$", line)
                    if search:
                        elements.append(
                            ListItemElement(search[0], content=search[2], level=len(search[1]), item_type="#",)
                        )
                        continue
                    # Quote Element
                    search = re.search(r"^bq. (.*)$", line)
                    if search:
                        elements.append(QuoteElement(search[0], content=search[1]))
                        continue
                    # Table Element
                    # Text line
                    # New Line
                    if line == "":
                        elements.append(NewLineElement())
                        continue
                    elements.append(TextElement(line))
        return elements

    def isoneline(self, line: str):
        """
        Check if the given line is a oneline block
        With a pair of {quote|code|etc...} tags

        Args:
            line (str): The line to check
        """
        search = re.search(r"^\{(.*?)(:(.*?))?\}(.*)\{.*$", line)
        if search:
            block_type = search[1]
            if re.findall(rf"{{{block_type}", line):
                return True
        return False


class JiraElement:
    """
    A root custom JiraElement
    It represent any kind of element
    """

    def __init__(self):
        """
        Init the object
        """
        pass

    def _parse(self):
        """
        Convert the element into markdown
        """
        pass


class TextElement:
    def __init__(self, raw: str):
        """
        Init the object

        Args:
            raw (str): The raw element
        """
        self.raw = raw
        self.content = raw
        self.rendered = raw
        self.markdown = raw
        self._parse()

    def _parse(self):
        """
        Convert the element into markdown
        It will parse and convert syntax such bold, italic, quotes etc...
        """

        # Users references
        matches = re.findall(r"(\[~(.*?)\])", self.markdown)
        for match in matches:
            self.markdown = self.markdown.replace(match[0], f"**@{match[1]}**")
            self.rendered = self.rendered.replace(match[0], f"[bold]@{match[1]}[/bold]")

        # Get links which should be protected
        links = []
        for match in re.findall(r"(\[(.*?)\])", self.markdown):
            link_anchor = f"[{''.join(random.choice(string.ascii_lowercase) for i in range(10))}]"
            title = ""
            url = match[1]
            rendered = f"[grey70]{url}[/grey70]"
            if "|" in match[1]:
                title = match[1].split("|")[0]
                url = match[1].split("|")[1]
                rendered = f"[blue]{title}[/blue] | [grey70]{url}[/grey70]"
            link_value = f"[{title}]({url})" if "|" in match[1] else f"[{url}]"

            links.append({"key": link_anchor, "value": link_value, "rendered": rendered})
            self.markdown = self.markdown.replace(match[0], link_anchor)
            self.rendered = self.rendered.replace(match[0], link_anchor)

        monospaceds = []
        for match in re.findall(r"({{(.*?)}})", self.markdown):
            monospaced_anchor = f"[{''.join(random.choice(string.ascii_lowercase) for i in range(10))}]"
            monospaceds.append(
                {"key": monospaced_anchor, "value": f"`{match[1]}`", "rendered": f"[dim]{match[1]}[/dim]"}
            )
            self.markdown = self.markdown.replace(match[0], monospaced_anchor)
            self.rendered = self.rendered.replace(match[0], monospaced_anchor)

        # *strong*
        matches = re.findall(r"( |^)(\*(.*?)\*)( |$)", self.markdown)
        for match in matches:
            self.markdown = self.markdown.replace(match[1], f"*{match[2]}*")
            self.rendered = self.rendered.replace(match[1], f"[bold]{match[2]}[/bold]")
        # _emphasis_
        matches = re.findall(r"( |^)(_(.*?)_)( |$)", self.markdown)
        for match in matches:
            self.markdown = self.markdown.replace(match[1], f"_{match[2]}_")
            self.rendered = self.rendered.replace(match[1], f"[italic]{match[2]}[/italic]")
        # ??citation??
        matches = re.findall(r"( |^)(\?\?(.*?)\?\?)( |$)", self.markdown)
        for match in matches:
            self.markdown = self.markdown.replace(match[1], f"*{match[2]}*")
            self.rendered = self.rendered.replace(match[1], f"[underline]{match[2]}[/underline]")
        # -deleted- / +inserted+ / ^superscript^ / ~subscript~
        matches = re.findall(r"( |^)(-(.*?)-)( |$)", self.markdown)
        for match in matches:
            self.markdown = self.markdown.replace(match[1], f"*{match[2]}*")
            self.rendered = self.rendered.replace(match[1], f"[underline]{match[2]}[/underline]")

        matches = re.findall(r"( |^)(\+(.*?)\+)( |$)", self.markdown)
        for match in matches:
            self.markdown = self.markdown.replace(match[1], f"*{match[2]}*")
            self.rendered = self.rendered.replace(match[1], f"[underline]{match[2]}[/underline]")

        matches = re.findall(r"( |^)(\^(.*?)\^)( |$)", self.markdown)
        for match in matches:
            self.markdown = self.markdown.replace(match[1], f"*{match[2]}*")
            self.rendered = self.rendered.replace(match[1], f"[underline]{match[2]}[/underline]")

        matches = re.findall(r"( |^)(~(.*?)~)( |$)", self.markdown)
        for match in matches:
            self.markdown = self.markdown.replace(match[1], f"*{match[2]}*")
            self.rendered = self.rendered.replace(match[1], f"[underline]{match[2]}[/underline]")

        # Put back protected links and monospaced strings
        for link in links:
            self.markdown = self.markdown.replace(link["key"], link["value"])
            self.rendered = self.rendered.replace(link["key"], link["rendered"])

        for monospaced in monospaceds:
            self.markdown = self.markdown.replace(monospaced["key"], monospaced["value"])
            self.rendered = self.rendered.replace(monospaced["key"], monospaced["rendered"])

    def __repr__(self):
        """
        Representation method of the object
        """
        return f"<Text Element: content='{self.content}'>"


class BlockElement(JiraElement):
    """
    This class represent block part element such as code snippets
    They could be multiline or note
    """

    def __init__(
        self, raw: str, content: str = "", content_type: str = None, content_style: str = None, oneline: bool = False,
    ):
        """
        Init the object

        Args:
            raw (str): The raw element
            content (str): The content of the element without the {block} tags
            content_type (str): The type of content extracted from the taf (example: python, bash etc...)
            content_style (str): The content style if it exists (For panel)
            oneline (bool): True if the block element is represented in oneline only
        """
        self.raw = raw
        self.content = content
        self.type = content_type
        self.style = content_style
        self.oneline = oneline
        self.renderer = ""
        self.markdown = ""
        self._parse()

    def _parse(self):
        """
        Convert the element into markdown
        It will convert different kind of block part:
        - {quote}
        - {code}
        - {color}
        - {panel}
        - {etc}
        """
        if self.oneline:
            self.rendered = f"[bold blue]|[italic] Quote: [/blue bold]{self.content}[/italic]"
            self.markdown = f"> {self.content}"
        else:
            if self.type == "quote":
                self.rendered = f"[bold blue]|[italic] Quote: [/blue bold]{self.content}[/italic]"
            else:
                self.rendered = Syntax(self.content, self.style, line_numbers=False)
            self.markdown = f"```{self.style if self.style else ''}\n{self.content}\n```"

    def __repr__(self):
        """
        Representation method of the element
        """
        repr_content = self.content.replace("\n", "\\n")
        return f"<Block Element: content='{repr_content}'>"


class HeadElement(JiraElement):
    """
    This class represents Header element
    """

    def __init__(self, raw, content: str = None, level: int = 1):
        """
        Init the object

        Args:
            raw (str): The raw element
            content (str): The content of the element without the 'h[0-9].' tag
            level (int): The value of the header level (example: h3. => 3)
        """
        self.raw = raw
        self.content = content
        self.level = level
        self.markdown = ""
        self.rendered = ""
        self._parse()

    def _parse(self):
        """
        Convert the element into markdown
        """
        self.rendered = f"[bold {JiraDocument.HEAD_COLORS[self.level - 1]}]{self.content}[/]"
        self.markdown = f"{'#' * self.level} {self.content}"

    def __repr__(self):
        """
        Representation method of the element
        """
        return f"<Head Element: level='{self.level}' content='{self.content}'>"


class QuoteElement(JiraElement):
    """
    Class representing a quote (tag bq. in Jira)
    """

    def __init__(self, raw, content: str = None):
        """
        Init the object

        Args:
            raw (str): The raw element
            content (str): The content of the element without the 'bq.' tag
        """
        self.raw = raw
        self.content = TextElement(content)
        self.markdown = ""
        self.rendered = ""
        self._parse()

    def _parse(self):
        """
        Convert the element into markdown
        """
        self.rendered = f"[bold blue]|[italic] Quote: [/blue bold]{self.content.rendered}[/italic]"
        self.markdown = f"> {self.content.markdown}"

    def __repr__(self):
        """
        Representation method of the element
        """
        return f"<Quote Element: content='{self.content}'>"


class ListItemElement(JiraElement):
    """
    Class representing a list item such as:
    * item
    """

    def __init__(self, raw: str, content: str = "", level: int = 1, item_type: str = "*"):
        """
        Init the object

        Args:
            raw (str): The raw element
            content (str): The content element without the '*' tag
            level (str): The level of the element inside the list
            item_type (str): The kind of list (Support only : '*')
        """
        self.raw = raw
        self.content = TextElement(content)
        self.level = level
        self.item_type = item_type
        self.rendered = ""
        self.markdown = ""
        self._parse()

    def _parse(self):
        """
        Convert the element into markdown
        """
        self.rendered = f"{' ' * 2 *(self.level - 1)}• {self.content.rendered}"
        self.markdown = f"{' ' * 2 *(self.level - 1)}{self.item_type} {self.content.markdown}"

    def __repr__(self):
        """
        Representation method of the element
        """
        return f"<ListItem Element: level='{self.level}' content='{self.content}' item_type='{self.item_type}'>"


class NewLineElement(JiraElement):
    """
    Class representing an emtpy line
    """

    def __init__(self):
        """
        Init the object
        """
        self.raw = ""
        self.content = ""
        self.markdown = ""
        self.rendered = ""

    def __repr__(self):
        """
        Representation method of the element
        """
        return "<NewLine Element: >"
