import os
import types
from collections import namedtuple

from ..parameters import DOWNLOADS, SERVER_DISPLAY, SERVER_DISPLAY_BASE
from ..core.text import DEFAULT_FORMAT
from ..core.helpers import mdEsc, htmlEsc, flattenToSet, console
from .helpers import tupleEnum, RESULT, dh, NB
from .condense import condense, condenseSet
from .highlight import getTupleHighlights, getHlAtt
from .displaysettings import DisplaySettings
from .settings import ORIG

LIMIT_SHOW = 100
LIMIT_TABLE = 2000
LIMIT_DISPLAY_DEPTH = 100

QUAD = "  "

__pdoc__ = {}

OuterContext = namedtuple(
    "OuterContext",
    """
    ltr
    textCls
    slots
    inTuple
    explain
""".strip().split(),
)
OuterContext.__doc__ = (
    "Outer node properties during plain() and pretty(). "
    "Only the properties of the node for which the outer call"
    " plain() or pretty() has been made, not the nodes encountered"
    " during recursion."
)
__pdoc__["OuterContext.ltr"] = "writing direction."
__pdoc__["OuterContext.textCls"] = "Css class for full text."
__pdoc__["OuterContext.slots"] = "Set of slots under the outer node."
__pdoc__[
    "OuterContext.inTuple"
] = "Whether the outer node is displayed as part of a tuple of nodes."

NodeContext = namedtuple(
    "NodeContext",
    """
    slotType
    nType
    isSlot
    isSlotOrDescend
    descend
    isBaseNonSlot
    hasChunks
    children
    boundaryCls
    textCls
    hlCls
    hlStyle
    nodePart
    cls
    slots
    hidden
""".strip().split(),
)
NodeContext.__doc__ = "Node properties during plain() or pretty()."
__pdoc__["NodeContext.slotType"] = "The slot type of the data set."
__pdoc__["NodeContext.nType"] = "The node type of the current node."
__pdoc__["NodeContext.isSlot"] = "Whether the current node is a slot node."
__pdoc__["NodeContext.isSlotOrDescend"] = (
    "Whether the current node is a slot node or"
    " has a type to which the current text format should descend."
    " This type is determined by the current text format."
)
__pdoc__["NodeContext.descend"] = (
    "When calling T.text(n, descend=??) for this node, what should we"
    " substitute for the ?? ?"
)
__pdoc__["NodeContext.isBaseNonSlot"] = (
    "Whether the current node has a type that is currently a baseType,"
    " i.e. a type where a pretty display should stop unfolding."
    " No need to put the slot type in this set."
)
__pdoc__["NodeContext.hasChunks"] = (
    "Whether the current node has a type that has a related type that"
    " corresponds to contiguous chunks that build it. "
    " E.g. in the BHSA the type phrase has a chunk type phrase_atom."
)
__pdoc__["NodeContext.children"] = "The children of the current node."
__pdoc__["NodeContext.boundaryCls"] = (
    "Css class that represent the kinds of boundaries for this node."
    " Nodes can have a firm of dotted left/right boundary, or no boundary at all."
)
__pdoc__["NodeContext.textCls"] = "The text Css class of the current node."
__pdoc__["NodeContext.hlCls"] = "The highlight Css class of the current node."
__pdoc__["NodeContext.hlStyle"] = "The highlight style attribute of the current node."
__pdoc__[
    "NodeContext.nodePart"
] = "The node type/number insofar it has to be displayed for the current node"
__pdoc__["NodeContext.cls"] = (
    "A dict of several classes for the display of the node:"
    " for the container, the label, and the children of the node;"
    " might be set by prettyCustom"
)
__pdoc__["NodeContext.slots"] = "Set of slots that must be displayed for this node"
__pdoc__["NodeContext.hidden"] = (
    "Whether the outer container and label of the current node"
    " should be hidden."
    " This is used to reduce displays by hiding the chunk types of types"
    " that have chunks. E.g. in the BHSA: the phrase_atoms can be hidden."
)


def displayApi(app, silent):
    """Produce the display API.

    The display API provides methods to generate styled representations
    of pieces of corpus texts in their relevant structures.
    The main end-user functions are `plain(node)` and `pretty(node)`.

    `plain()` focuses on the plain text, `pretty()` focuses on structure
    and feature display.

    Related are `plainTuple()` and `prettyTuple()` that work for tuples
    instead of nodes.

    And further there are `show()` and `table()`, that work
    with iterables of tuples of nodes (e.g. query results).

    Parameters
    ----------
    app: obj
        The high-level API object
    silent:
        The verbosity mode to perform this operation in.
        Normally it is the same as for the app, but when we do an `A.reuse()`
        we force `silent=True`.
    """

    app.export = types.MethodType(export, app)
    app.table = types.MethodType(table, app)
    app.plainTuple = types.MethodType(plainTuple, app)
    app.plain = types.MethodType(plain, app)
    app.show = types.MethodType(show, app)
    app.prettyTuple = types.MethodType(prettyTuple, app)
    app.pretty = types.MethodType(pretty, app)
    app.loadCss = types.MethodType(loadCss, app)
    app.displaySetup = types.MethodType(displaySetup, app)
    app.displayReset = types.MethodType(displayReset, app)

    app.display = DisplaySettings(app)
    if not app._browse:
        app.loadCss()


def displaySetup(app, **options):
    """Set up all display parameters.

    The display parameters are given default values, unless they are overriden
    by `options`.

    !!! hint "corpus settings"
        The defaults themselves come from the corpus settings, which are influenced
        by the `config.yaml` file, if it exists.

    Parameters
    ----------
    options: dict
        Explicit values for selected options that act as overrides of the defaults.
    """

    display = app.display

    display.setup(**options)


def displayReset(app, *options):
    """Restore display parameters to their defaults.

    Parameters
    ----------
    options: list, optional `[]`
        If present, only restore these options to their defaults.
    """

    display = app.display

    display.reset(*options)
    # if not app._browse:
    #    app.loadCss()


def export(app, tuples, toDir=None, toFile="results.tsv", **options):
    display = app.display

    if not display.check("table", options):
        return ""

    dContext = display.get(options)
    fmt = dContext.fmt
    condenseType = dContext.condenseType
    tupleFeatures = dContext.tupleFeatures

    if toDir is None:
        toDir = os.path.expanduser(DOWNLOADS)
        if not os.path.exists(toDir):
            os.makedirs(toDir, exist_ok=True)
    toPath = f"{toDir}/{toFile}"

    resultsX = getResultsX(app, tuples, tupleFeatures, condenseType, fmt=fmt,)

    with open(toPath, "w", encoding="utf_16_le") as fh:
        fh.write(
            "\ufeff"
            + "".join(
                ("\t".join("" if t is None else str(t) for t in tup) + "\n")
                for tup in resultsX
            )
        )


# PLAIN and FRIENDS


def table(app, tuples, _asString=False, **options):
    display = app.display

    if not display.check("table", options):
        return ""

    api = app.api
    F = api.F
    fOtype = F.otype.v

    dContext = display.get(options)
    end = dContext.end
    start = dContext.start
    withPassage = dContext.withPassage
    condensed = dContext.condensed
    condenseType = dContext.condenseType
    skipCols = dContext.skipCols

    if skipCols:
        tuples = tuple(
            tuple(x for (i, x) in enumerate(tup) if i + 1 not in skipCols)
            for tup in tuples
        )

    item = condenseType if condensed else RESULT

    if condensed:
        tuples = condense(api, tuples, condenseType, multiple=True)

    passageHead = '</th><th class="tf">p' if withPassage is True else ""

    html = []
    one = True

    newOptions = display.consume(options, "skipCols")

    for (i, tup) in tupleEnum(tuples, start, end, LIMIT_TABLE, item):
        if one:
            heads = '</th><th class="tf">'.join(fOtype(n) for n in tup)
            html.append(
                f'<tr class="tf">'
                f'<th class="tf">n{passageHead}</th>'
                f'<th class="tf">{heads}</th>'
                f"</tr>"
            )
            one = False
        html.append(
            plainTuple(
                app,
                tup,
                i,
                item=item,
                position=None,
                opened=False,
                _asString=True,
                skipCols=set(),
                **newOptions,
            )
        )
    html = "<table>" + "\n".join(html) + "</table>"
    if _asString:
        return html
    dh(html)


def plainTuple(
    app, tup, seq, item=RESULT, position=None, opened=False, _asString=False, **options
):
    display = app.display

    if not display.check("plainTuple", options):
        return ""

    api = app.api
    F = api.F
    T = api.T
    fOtype = F.otype.v
    _browse = app._browse

    dContext = display.get(options)
    condenseType = dContext.condenseType
    colorMap = dContext.colorMap
    highlights = dContext.highlights
    withPassage = dContext.withPassage
    skipCols = dContext.skipCols

    if skipCols:
        tup = tuple(x for (i, x) in enumerate(tup) if i + 1 not in skipCols)

    if withPassage is True:
        passageNode = getRefMember(app, tup, dContext)
        passageRef = (
            ""
            if passageNode is None
            else app._sectionLink(passageNode)
            if _browse
            else app.webLink(passageNode, _asString=True)
        )
        passageRef = f'<span class="section ltr">{passageRef}</span>'
    else:
        passageRef = ""

    newOptions = display.consume(options, "withPassage")
    newOptionsH = display.consume(options, "withPassage", "highlights")

    highlights = getTupleHighlights(api, tup, highlights, colorMap, condenseType)

    if _browse:
        prettyRep = (
            prettyTuple(app, tup, seq, withPassage=False, **newOptions)
            if opened
            else ""
        )
        current = "focus" if seq == position else ""
        attOpen = "open " if opened else ""
        tupSeq = ",".join(str(n) for n in tup)
        if withPassage is True:
            sparts = T.sectionFromNode(passageNode, fillup=True)
            passageAtt = " ".join(
                f'sec{i}="{sparts[i] if i < len(sparts) else ""}"' for i in range(3)
            )
        else:
            passageAtt = ""

        plainRep = "".join(
            "<span>"
            + mdEsc(
                app.plain(
                    n,
                    _inTuple=True,
                    withPassage=doPassage(dContext, i),
                    highlights=highlights,
                    **newOptionsH,
                )
            )
            + "</span>"
            for (i, n) in enumerate(tup)
        )
        html = (
            f'<details class="pretty dtrow {current}" seq="{seq}" {attOpen}>'
            f"<summary>"
            f'<a href="#" class="pq fa fa-solar-panel fa-xs"'
            f' title="show in context" {passageAtt}></a>'
            f'<a href="#" class="sq" tup="{tupSeq}">{seq}</a>'
            f" {passageRef} {plainRep}"
            f"</summary>"
            f'<div class="pretty">{prettyRep}</div>'
            f"</details>"
        )
        return html

    html = [str(seq)]
    if withPassage is True:
        html.append(passageRef)
    for (i, n) in enumerate(tup):
        html.append(
            app.plain(
                n,
                _inTuple=True,
                _asString=True,
                withPassage=doPassage(dContext, i),
                highlights=highlights,
                **newOptionsH,
            )
        )
    html = (
        f'<tr class="tf"><td class="tf">'
        + '</td><td class="tf">'.join(html)
        + "</td></tr>"
    )
    if _asString:
        return html

    passageHead = '</th><th class="tf">p' if withPassage is True else ""
    head = (
        f'<tr class="tf"><th class="tf">n{passageHead}</th><th class="tf">'
        + '</th><th class="tf">'.join(fOtype(n) for n in tup)
        + f"</th></tr>"
    )
    html = f"<table>" + head + "".join(html) + "</table>"

    dh(html)


def plain(app, n, _inTuple=False, _asString=False, explain=False, **options):
    display = app.display

    if not display.check("plain", options):
        return ""

    aContext = app.context
    formatHtml = aContext.formatHtml

    dContext = display.get(options)
    fmt = dContext.fmt

    dContext.isHtml = fmt in formatHtml

    _browse = app._browse
    api = app.api

    ltr = getLtr(app, dContext)
    textCls = getTextCls(app, fmt)
    slots = getSlots(api, n)

    oContext = OuterContext(ltr, textCls, slots, _inTuple, not not explain)
    passage = getPassage(app, True, dContext, oContext, n)
    rep = _doPlain(
        app, dContext, oContext, None, n, True, True, True, 0, passage, [], {}, {}
    )
    sep = " " if passage and rep else ""

    result = passage + sep + rep

    if _browse or _asString:
        return result
    dh(result)


def note(isPretty, oContext, n, nType, first, last, level, *labels, **info):
    if not oContext.explain:
        return
    block = QUAD * level
    kindRep = "pretty" if isPretty else "plain"
    labelRep = " ".join(str(lab) for lab in labels)
    console(f"{block}<{level}>{kindRep}({nType} {n}): {labelRep}", error=True)
    for (k, v) in info.items():
        console(f"{block}<{level}>      {k:<10} = {repr(v)}", error=True)


def depthExceeded(level):
    if level > LIMIT_DISPLAY_DEPTH:
        console("DISPLAY: maximal depth exceeded: {LIMIT_DISPLAY_DEPTH}", error=True)
        return True
    return False


def _doPlain(
    app,
    dContext,
    oContext,
    pContext,
    n,
    outer,
    first,
    last,
    level,
    passage,
    html,
    done,
    called,
):
    if depthExceeded(level):
        return

    origOuter = outer
    if outer is None:
        outer = True

    nContext = _prepareDisplay(
        app, False, dContext, oContext, pContext, n, origOuter, done=done,
    )
    if type(nContext) is str:
        note(False, oContext, n, nContext, first, last, level, "nothing to do")
        return "".join(html) if outer else None

    nDone = done.setdefault(n, set())
    nCalled = called.setdefault(n, set())

    slots = nContext.slots

    finished = slots <= nDone
    calledBefore = slots <= nCalled
    if finished or calledBefore:
        note(
            False,
            oContext,
            n,
            nContext.nType,
            first,
            last,
            level,
            "already " + ("finished" if finished else "called"),
            task=slots,
            done=nDone,
            called=nCalled,
        )
        return "".join(html) if outer else None

    aContext = app.context
    chunkedTypes = aContext.chunkedTypes

    ltr = oContext.ltr

    nType = nContext.nType
    hlCls = nContext.hlCls
    hlStyle = nContext.hlStyle
    boundaryCls = nContext.boundaryCls
    nodePart = nContext.nodePart
    children = nContext.children

    outerCls = f"outer" if outer else ""

    didChunkedType = False

    sdone = {}
    if not (outer and nType in chunkedTypes):
        snodeInfo = getChunkedType(app, nContext, n, outer)
        if snodeInfo:
            (sn, spContext) = snodeInfo
            snContext = _prepareDisplay(
                app,
                False,
                dContext,
                oContext,
                spContext,
                sn,
                False,
                chunk=n,
                done=sdone,
            )
            shlCls = snContext.hlCls
            shlStyle = snContext.hlStyle
            snodePart = snContext.nodePart
            sboundaryCls = snContext.boundaryCls

            if (type(snContext) is not str) and shlCls:
                sclses = f"plain {sboundaryCls} {shlCls}"
                html.append(f'<span class="{sclses}" {shlStyle}>')
                if snodePart:
                    html.append(snodePart)
                didChunkedType = True

        clses = (
            f"plain {'' if didChunkedType else outerCls} {ltr} {boundaryCls} {hlCls}"
        )
        html.append(f'<span class="{clses}" {hlStyle}>')

        if nodePart:
            html.append(nodePart)

        html.append(
            _doPlainNode(
                app,
                dContext,
                oContext,
                nContext,
                n,
                outer,
                first,
                last,
                level,
                passage,
                done=done,
            )
        )

    nCalled.update(nContext.slots)

    lastCh = len(children) - 1

    note(
        False,
        oContext,
        n,
        nContext.nType,
        first,
        last,
        level,
        "start children" if children else "bottom node",
        children=children,
        task=slots,
        done=nDone,
        called=nCalled,
    )

    for (i, ch) in enumerate(children):
        thisFirst = first and i == 0
        thisLast = last and i == lastCh
        _doPlain(
            app,
            dContext,
            oContext,
            nContext,
            ch,
            False,
            thisFirst,
            thisLast,
            level + 1,
            "",
            html,
            done,
            called,
        )
    if not (outer and nType in chunkedTypes):
        html.append("</span>")
        if didChunkedType:
            html.append("</span>")

    nDone = done.setdefault(n, set())
    nDone |= slots

    if children:
        note(
            False,
            oContext,
            n,
            nContext.nType,
            first,
            last,
            level,
            "end children",
            done=nDone,
        )

    return "".join(html) if outer else None


def _doPlainNode(
    app, dContext, oContext, nContext, n, outer, first, last, level, passage, done={}
):
    api = app.api
    T = api.T

    aContext = app.context
    plainCustom = aContext.plainCustom

    isHtml = dContext.isHtml
    fmt = dContext.fmt

    ltr = oContext.ltr
    textCls = nContext.textCls

    nType = nContext.nType

    isSlotOrDescend = nContext.isSlotOrDescend
    descend = nContext.descend

    if nType in plainCustom:
        method = plainCustom[nType]
        contrib = method(app, dContext, oContext, nContext, n, outer, done=done)
        return contrib
    if isSlotOrDescend:
        text = htmlSafe(
            T.text(
                n,
                fmt=fmt,
                descend=descend,
                outer=outer,
                first=first,
                last=last,
                level=level,
            ),
            isHtml,
        )
        contrib = f'<span class="{textCls}">{text}</span>'
    else:
        tplFilled = getText(
            app,
            False,
            n,
            nType,
            outer,
            first,
            last,
            level,
            passage if outer else "",
            descend,
            dContext=dContext,
        )
        contrib = f'<span class="plain {textCls} {ltr}">{tplFilled}</span>'

    return contrib


# PRETTY and FRIENDS


def show(app, tuples, **options):
    display = app.display

    if not display.check("show", options):
        return ""

    dContext = display.get(options)
    end = dContext.end
    start = dContext.start
    condensed = dContext.condensed
    condenseType = dContext.condenseType
    skipCols = dContext.skipCols

    if skipCols:
        tuples = tuple(
            tuple(x for (i, x) in enumerate(tup) if i + 1 not in skipCols)
            for tup in tuples
        )

    api = app.api
    F = api.F

    item = condenseType if condensed else RESULT

    if condensed:
        tuples = condense(api, tuples, condenseType, multiple=True)

    newOptions = display.consume(options, "skipCols")

    for (i, tup) in tupleEnum(tuples, start, end, LIMIT_SHOW, item):
        item = F.otype.v(tup[0]) if condensed and condenseType else RESULT
        prettyTuple(app, tup, i, item=item, skipCols=set(), **newOptions)


def prettyTuple(app, tup, seq, item=RESULT, **options):
    display = app.display

    if not display.check("prettyTuple", options):
        return ""

    dContext = display.get(options)
    colorMap = dContext.colorMap
    highlights = dContext.highlights
    condenseType = dContext.condenseType
    condensed = dContext.condensed
    skipCols = dContext.skipCols

    _browse = app._browse

    if skipCols:
        tup = tuple(x for (i, x) in enumerate(tup) if i + 1 not in skipCols)

    if len(tup) == 0:
        if _browse:
            return ""
        else:
            return

    api = app.api
    sortKey = api.sortKey

    containers = {tup[0]} if condensed else condenseSet(api, tup, condenseType)
    highlights = getTupleHighlights(api, tup, highlights, colorMap, condenseType)

    if not _browse:
        dh(f"<p><b>{item}</b> <i>{seq}</i></p>")
    if _browse:
        html = []
    for t in sorted(containers, key=sortKey):
        h = app.pretty(
            t, highlights=highlights, **display.consume(options, "highlights"),
        )
        if _browse:
            html.append(h)
    if _browse:
        return "".join(html)


def pretty(app, n, explain=False, **options):
    display = app.display

    if not display.check("pretty", options):
        return ""

    _browse = app._browse

    aContext = app.context
    formatHtml = aContext.formatHtml

    dContext = display.get(options)
    condenseType = dContext.condenseType
    condensed = dContext.condensed
    tupleFeatures = dContext.tupleFeatures
    extraFeatures = dContext.extraFeatures
    fmt = dContext.fmt

    dContext.isHtml = fmt in formatHtml
    dContext.features = sorted(
        flattenToSet(extraFeatures[0]) | flattenToSet(tupleFeatures)
    )
    dContext.featuresIndirect = extraFeatures[1]

    api = app.api
    F = api.F
    L = api.L
    otypeRank = api.otypeRank

    ltr = getLtr(app, dContext)
    textCls = getTextCls(app, fmt)

    containerN = None

    nType = F.otype.v(n)
    if condensed and condenseType:
        if nType == condenseType:
            containerN = n
        elif otypeRank[nType] < otypeRank[condenseType]:
            ups = L.u(n, otype=condenseType)
            if ups:
                containerN = ups[0]

    slots = (
        getSlots(api, n)
        if not condensed or not condenseType or containerN is None
        else getSlots(api, containerN)
    )

    oContext = OuterContext(ltr, textCls, slots, False, not not explain)
    passage = getPassage(app, False, dContext, oContext, n)

    html = []

    _doPretty(app, dContext, oContext, None, n, True, True, True, 0, html, {}, {})

    htmlStr = passage + "".join(html)
    if _browse:
        return htmlStr
    dh(htmlStr)


def _doPretty(
    app, dContext, oContext, pContext, n, outer, first, last, level, html, done, called,
):
    if depthExceeded(level):
        return

    nContext = _prepareDisplay(
        app, True, dContext, oContext, pContext, n, outer, done=done
    )
    if type(nContext) is str:
        note(True, oContext, n, nContext, first, last, level, "nothing to do")
        return "".join(html) if outer else None

    nDone = done.setdefault(n, set())
    nCalled = called.setdefault(n, set())

    slots = nContext.slots

    finished = slots <= nDone
    calledBefore = slots <= nCalled
    if finished or calledBefore:
        note(
            True,
            oContext,
            n,
            nContext.nType,
            first,
            last,
            level,
            "already " + ("finished" if finished else "called"),
            task=slots,
            done=nDone,
            called=nCalled,
        )
        return "".join(html) if outer else None

    aContext = app.context
    afterChild = aContext.afterChild
    hasGraphics = aContext.hasGraphics

    showGraphics = dContext.showGraphics

    ltr = oContext.ltr

    isBaseNonSlot = nContext.isBaseNonSlot
    nType = nContext.nType
    hasChunks = nContext.hasChunks
    children = nContext.children
    cls = nContext.cls
    childCls = cls["children"]

    nodePlain = None
    if isBaseNonSlot:
        nodePlain = _doPlain(
            app,
            dContext,
            oContext,
            nContext,
            n,
            None,
            first,
            last,
            level,
            "",
            [],
            done,
            called,
        )

    didChunkedType = False

    snodeInfo = getChunkedType(app, nContext, n, outer)
    if snodeInfo:
        (sn, spContext) = snodeInfo
        snContext = _prepareDisplay(
            app, True, dContext, oContext, spContext, sn, False, chunk=n, done=done,
        )
        if type(snContext) is not str:
            sisBaseNonSlot = snContext.isBaseNonSlot
            scls = snContext.cls
            schildCls = scls["children"]
            sslots = snContext.slots

            snodePlain = None
            if sisBaseNonSlot:
                snodePlain = _doPlain(
                    app,
                    dContext,
                    oContext,
                    spContext,
                    sn,
                    None,
                    first,
                    last,
                    level,
                    "",
                    [],
                    done,
                    called,
                )
            (slabel, sfeaturePart) = _doPrettyNode(
                app,
                dContext,
                oContext,
                snContext,
                sn,
                False,
                first,
                last,
                level,
                snodePlain,
            )
            (scontainerB, scontainerE) = _doPrettyWrapPre(
                app,
                sn,
                False,
                slabel,
                sfeaturePart,
                html,
                snContext,
                showGraphics,
                hasGraphics,
                ltr,
            )
            done.setdefault(sn, set()).add(sslots)
            nDone = done.setdefault(sn, set())
            nDone |= sslots
            html.append(f'<div class="{schildCls} {ltr}">')

            didChunkedType = True

    if not hasChunks or isBaseNonSlot:
        (label, featurePart) = _doPrettyNode(
            app, dContext, oContext, nContext, n, outer, first, last, level, nodePlain
        )
        (containerB, containerE) = _doPrettyWrapPre(
            app,
            n,
            outer,
            label,
            featurePart,
            html,
            nContext,
            showGraphics,
            hasGraphics,
            ltr,
        )

    nCalled.update(nContext.slots)

    if children:
        html.append(f'<div class="{childCls} {ltr}">')

    lastCh = len(children) - 1

    note(
        True,
        oContext,
        n,
        nContext.nType,
        first,
        last,
        level,
        "start children" if children else "bottom node",
        children=children,
        task=slots,
        done=nDone,
        called=nCalled,
    )

    for (i, ch) in enumerate(children):
        thisFirst = first and i == 0
        thisLast = last and i == lastCh
        _doPretty(
            app,
            dContext,
            oContext,
            nContext,
            ch,
            False,
            thisFirst,
            thisLast,
            level + 1,
            html,
            done,
            called,
        )
        after = afterChild.get(nType, None)
        if after:
            html.append(after(ch))

    nDone = done.setdefault(n, set())
    nDone |= slots

    if children:
        note(
            True,
            oContext,
            n,
            nContext.nType,
            first,
            last,
            level,
            "end children",
            task=slots,
        )

    if children:
        html.append("</div>")

    if not hasChunks or isBaseNonSlot:
        _doPrettyWrapPost(label, featurePart, html, containerB, containerE)

    if didChunkedType:
        _doPrettyWrapPost(slabel, sfeaturePart, html, scontainerB, scontainerE)
        html.append("</div>")

    return "".join(html) if outer else None


def _doPrettyWrapPre(
    app, n, outer, label, featurePart, html, nContext, showGraphics, hasGraphics, ltr,
):
    nType = nContext.nType
    hidden = nContext.hidden
    cls = nContext.cls
    contCls = "contnr cnul" if hidden else cls["container"]
    hlCls = nContext.hlCls
    hlStyle = nContext.hlStyle
    boundaryCls = nContext.boundaryCls
    children = nContext.children
    label0 = label.get("", None)
    labelB = label.get("b", None)

    containerB = f'<div class="{contCls} {{}} {ltr} {boundaryCls} {hlCls}" {hlStyle}>'
    containerE = f"</div>"

    terminalCls = "trm"
    # if hidden:
    #    html.append(containerB.format(terminalCls))
    # else:
    material = "" if hidden else f" {featurePart}"
    if labelB is not None:
        trm = terminalCls
        html.append(f"{containerB.format(trm)}{labelB}{material}{containerE}")
    if label0 is not None:
        trm = "" if children and not hidden else terminalCls
        html.append(f"{containerB.format(trm)}{label0}{material}")

    if showGraphics and nType in hasGraphics:
        html.append(app.getGraphics(n, nType, outer))

    return (containerB, containerE)


def _doPrettyWrapPost(label, featurePart, html, containerB, containerE):
    label0 = label.get("", None)
    labelE = label.get("e", None)

    if label0 is not None:
        html.append(containerE)
    if labelE is not None:
        html.append(f"{containerB}{labelE} {featurePart}{containerE}")


def _doPrettyNode(
    app, dContext, oContext, nContext, n, outer, first, last, level, nodePlain
):
    api = app.api
    L = api.L

    aContext = app.context
    lexTypes = aContext.lexTypes
    lexMap = aContext.lexMap

    textCls = nContext.textCls
    hidden = nContext.hidden

    nType = nContext.nType
    cls = nContext.cls
    hlCls = nContext.hlCls
    hlStyle = nContext.hlStyle
    descend = nContext.descend
    isBaseNonSlot = nContext.isBaseNonSlot
    children = nContext.children
    nodePart = nContext.nodePart

    labelHlCls = ""
    labelHlStyle = ""

    if isBaseNonSlot:
        heading = nodePlain
    else:
        labelHlCls = hlCls
        labelHlStyle = hlStyle
        heading = getText(
            app,
            True,
            n,
            nType,
            outer,
            first,
            last,
            level,
            "",
            descend,
            dContext=dContext,
        )

    heading = f'<span class="{textCls}">{heading}</span>' if heading else ""

    featurePart = getFeatures(app, dContext, n, nType)

    if nType in lexTypes:
        slots = getSlots(api, n)
        extremeOccs = (slots[0],) if len(slots) == 1 else (slots[0], slots[-1])
        linkOccs = " - ".join(app.webLink(lo, _asString=True) for lo in extremeOccs)
        featurePart += f'<div class="occs">{linkOccs}</div>'
    if nType in lexMap:
        lx = L.u(n, otype=lexMap[nType])
        if lx:
            heading = app.webLink(lx[0], heading, _asString=True)

    label = {}
    for x in ("", "b", "e"):
        key = f"label{x}"
        if key in cls:
            val = cls[key]
            terminalCls = "trm" if x or not children else ""
            sep = " " if nodePart and heading else ""
            material = (
                (heading if nodePlain else "")
                if hidden
                else f"{nodePart}{sep}{heading}"
                if nodePart or heading
                else ""
            )
            label[x] = (
                f'<div class="{val} {terminalCls} {labelHlCls}" {labelHlStyle}>'
                f"{material}</div>"
                if material
                else ""
            )

    return (label, featurePart)


def _prepareDisplay(
    app, isPretty, dContext, oContext, pContext, n, outer, chunk=None, done=set(),
):
    api = app.api
    F = api.F
    T = api.T
    slotType = F.otype.slotType
    nType = F.otype.v(n)

    aContext = app.context
    levelCls = aContext.levelCls
    noChildren = aContext.noChildren
    prettyCustom = aContext.prettyCustom
    isChunkOf = aContext.isChunkOf
    chunkedTypes = aContext.chunkedTypes
    lexTypes = aContext.lexTypes
    styles = aContext.styles

    fmt = dContext.fmt
    baseTypes = dContext.baseTypes
    setSubBaseTypes(aContext, dContext, slotType)

    highlights = dContext.highlights
    showChunks = dContext.showChunks

    descendType = T.formats.get(fmt, slotType)
    bottomTypes = baseTypes if isPretty else {descendType}

    isSlot = nType == slotType
    hasChunks = nType in chunkedTypes
    isHidden = not showChunks and nType in isChunkOf

    slots = (
        oContext.slots
        if pContext is None
        else frozenset()
        if type(pContext) is str
        else pContext.slots
    )
    nDone = done.get(n, set())
    slots -= nDone

    isBaseNonSlot = nType != slotType and nType in baseTypes

    children = (
        ()
        if isSlot
        or nType in bottomTypes
        or isChunkOf.get(nType, None) in bottomTypes
        or nType in lexTypes
        or (not isPretty and nType in noChildren)
        else getChildren(app, isPretty, dContext, oContext, n, nType)
    )

    boundaryResult = getBoundaryResult(
        isPretty, api, oContext, slots, n, nType, chunk=chunk
    )
    if boundaryResult is None:
        return nType

    (boundaryCls, slots) = boundaryResult
    if not slots:
        return nType

    (hlCls, hlStyle) = getHlAtt(app, n, highlights, baseTypes, not isPretty)

    isSlotOrDescend = isSlot or nType == descendType
    descend = False if descendType == slotType else None

    nodePart = getNodePart(
        app, isPretty, dContext, n, nType, isSlot, outer, hlCls != ""
    )
    cls = {}
    if isPretty:
        if nType in levelCls:
            cls.update(levelCls[nType])
        if nType in prettyCustom:
            prettyCustom[nType](app, n, nType, cls)

    textCls = styles.get(nType, oContext.textCls)

    return NodeContext(
        slotType,
        nType,
        isSlot,
        isSlotOrDescend,
        descend,
        isBaseNonSlot,
        hasChunks,
        children,
        boundaryCls,
        textCls,
        hlCls,
        hlStyle,
        nodePart,
        cls,
        slots,
        isHidden,
    )


def setSubBaseTypes(aContext, dContext, slotType):
    descendantType = aContext.descendantType
    isChunkOf = aContext.isChunkOf
    baseTypes = dContext.baseTypes

    chunkBaseTypes = {ct for (ct, t) in isChunkOf.items() if t in baseTypes}
    subBaseTypes = set()

    if baseTypes and baseTypes != {slotType}:
        for bt in baseTypes:
            if bt in descendantType:
                subBaseTypes |= descendantType[bt]
    dContext.subBaseTypes = subBaseTypes - baseTypes - chunkBaseTypes


def doPassage(dContext, i):
    withPassage = dContext.withPassage
    return withPassage is not True and withPassage and i + 1 in withPassage


def getPassage(app, isPretty, dContext, oContext, n):
    withPassage = dContext.withPassage

    if not withPassage:
        return ""

    passage = app.webLink(n, _asString=True)
    return f'<span class="section ltr">{passage}{NB}</span>'


def getText(
    app, isPretty, n, nType, outer, first, last, level, passage, descend, dContext=None
):
    T = app.api.T
    sectionTypeSet = T.sectionTypeSet
    structureTypeSet = T.structureTypeSet

    aContext = app.context
    templates = aContext.labels if isPretty else aContext.templates

    fmt = None if dContext is None else dContext.fmt
    standardFeatures = True if dContext is None else dContext.standardFeatures
    isHtml = False if dContext is None else dContext.isHtml
    suppress = set() if dContext is None else dContext.suppress

    (tpl, feats) = templates[nType]

    tplFilled = (
        (
            (
                '<span class="section">'
                + (NB if passage else app.sectionStrFromNode(n))
                + "</span>"
            )
            if nType in sectionTypeSet
            else f'<span class="structure">{app.structureStrFromNode(n)}</span>'
            if nType in structureTypeSet
            else htmlSafe(
                T.text(
                    n,
                    fmt=fmt,
                    descend=descend,
                    outer=outer,
                    first=first,
                    last=last,
                    level=level,
                ),
                isHtml,
            )
        )
        if tpl is True
        else (
            tpl.format(
                **{feat: getValue(app, n, nType, feat, suppress) for feat in feats}
            )
            if standardFeatures
            else ""
        )
    )
    return tplFilled


def htmlSafe(text, isHtml):
    return text if isHtml else htmlEsc(text)


def getTextCls(app, fmt):
    aContext = app.context
    formatCls = aContext.formatCls
    defaultClsOrig = aContext.defaultClsOrig

    return formatCls.get(fmt or DEFAULT_FORMAT, defaultClsOrig)


def getValue(app, n, nType, feat, suppress):
    F = app.api.F
    Fs = app.api.Fs

    aContext = app.context
    transform = aContext.transform
    if feat in suppress:
        val = ""
    else:
        featObj = Fs(feat) if hasattr(F, feat) else None
        val = htmlEsc(featObj.v(n)) if featObj else None
        modifier = transform.get(nType, {}).get(feat, None)
        if modifier:
            val = modifier(n, val)
    return f'<span title="{feat}">{val}</span>'


def getLtr(app, dContext):
    aContext = app.context
    direction = aContext.direction

    fmt = dContext.fmt or DEFAULT_FORMAT

    return (
        "rtl"
        if direction == "rtl" and (f"{ORIG}-" in fmt or f"-{ORIG}" in fmt)
        else ("" if direction == "ltr" else "ltr")
    )


def getBigType(app, dContext, nType, otypeRank):
    api = app.api
    T = api.T

    sectionTypeSet = T.sectionTypeSet
    structureTypeSet = T.structureTypeSet

    full = dContext.full
    condenseType = dContext.condenseType

    isBig = False
    if not full:
        if sectionTypeSet and nType in sectionTypeSet | structureTypeSet:
            if condenseType is None or otypeRank[nType] > otypeRank[condenseType]:
                isBig = True
        elif condenseType is not None and otypeRank[nType] > otypeRank[condenseType]:
            isBig = True
    return isBig


def getBoundaryResult(isPretty, api, oContext, inSlots, n, nType, chunk=None):
    ltr = oContext.ltr
    startCls = "r" if ltr == "rtl" else "l"
    endCls = "l" if ltr == "rtl" else "r"

    boundaryCls = ""

    nSlots = getSlots(api, n)

    chunkSlots = getSlots(api, chunk) & nSlots if chunk else None

    slots = inSlots & (chunkSlots if chunk else nSlots)

    if not slots:
        return None

    nStart = min(nSlots)
    nEnd = max(nSlots)
    tStart = min(slots)
    tEnd = max(slots)

    boundaryCls = ""

    if chunk:
        chStart = min(chunkSlots)
        chEnd = max(chunkSlots)

    kind = ""
    if nStart < tStart:
        kind = (
            ""
            if ((tStart - 1 not in nSlots) or (chunk and chStart == tStart))
            else "no"
        )
        boundaryCls += f" {startCls}{kind}"
    if nEnd > tEnd:
        kind = "" if ((tEnd + 1 not in nSlots) or (chunk and chEnd == tEnd)) else "no"
        boundaryCls += f" {endCls}{kind}"

    return (boundaryCls, slots)


def getChunkedType(app, nContext, n, outer):

    aContext = app.context
    isChunkOf = aContext.isChunkOf
    chunkedTypes = aContext.chunkedTypes

    nType = nContext.nType

    if not outer and nType not in chunkedTypes and nType in isChunkOf:
        api = app.api
        L = api.L
        chunkedType = isChunkOf[nType]
        sn = L.u(n, otype=chunkedType)
        if sn:
            E = api.E
            nSlots = nContext.slots
            sownSlots = frozenset(E.oslots.s(sn[0]))
            return (
                sn[0],
                nContext._replace(slots=nSlots & sownSlots),
            )

    return None


def getChildren(app, isPretty, dContext, oContext, n, nType):
    api = app.api
    L = api.L
    F = api.F
    otypeRank = api.otypeRank
    sortNodes = api.sortNodes
    slotType = F.otype.slotType
    fOtypev = F.otype.v

    aContext = app.context
    verseTypes = aContext.verseTypes
    childType = aContext.childType
    baseTypes = dContext.baseTypes
    subBaseTypes = dContext.subBaseTypes
    childrenCustom = aContext.childrenCustom
    showVerseInTuple = aContext.showVerseInTuple

    inTuple = oContext.inTuple

    full = dContext.full

    isBigType = (
        inTuple
        if not isPretty and nType in verseTypes and not showVerseInTuple
        else getBigType(app, dContext, nType, otypeRank)
    )

    if isBigType and not full:
        children = ()
    elif nType in childType:
        childType = childType[nType]
        children = L.i(n, otype=childType)
        if nType in childrenCustom:
            (condition, method, add) = childrenCustom[nType]
            if condition(n):
                others = method(n)
                if add:
                    children += others
                else:
                    children = others

            children = sortNodes(set(children) - {n})
    else:
        children = L.i(n)
    if isPretty and baseTypes and baseTypes != {slotType}:
        refSet = set(children)
        children = tuple(
            ch
            for ch in children
            if (fOtypev(ch) not in subBaseTypes)
            and not (set(L.u(ch, otype=baseTypes)) & refSet)
        )
    return children


def getNodePart(app, isPretty, dContext, n, nType, isSlot, outer, isHl):
    _browse = app._browse

    Fs = app.api.Fs

    aContext = app.context
    lineNumberFeature = aContext.lineNumberFeature
    allowInfo = isPretty or outer is None or outer or isHl

    withNodes = dContext.withNodes and outer is not None
    withTypes = dContext.withTypes and outer is not None
    prettyTypes = dContext.prettyTypes and outer is not None
    lineNumbers = dContext.lineNumbers and outer is not None

    num = ""
    if withNodes and allowInfo:
        num = n

    ntp = ""
    if (withTypes or isPretty and prettyTypes) and not isSlot and allowInfo:
        ntp = nType

    line = ""
    if lineNumbers and allowInfo:
        feat = lineNumberFeature.get(nType, None)
        if feat:
            line = Fs(feat).v(n)
        if line:
            line = f"@{line}" if line else ""

    elemb = 'a href="#"' if _browse else "span"
    eleme = "a" if _browse else "span"
    sep = ":" if ntp and num else ""

    return (
        f'<{elemb} class="nd">{ntp}{sep}{num}{line}</{eleme}>'
        if ntp or num or line
        else ""
    )


# COMPOSE TABLES FOR CSV EXPORT


def getResultsX(app, results, features, condenseType, fmt=None):
    api = app.api
    F = api.F
    Fs = api.Fs
    T = api.T
    fOtype = F.otype.v
    otypeRank = api.otypeRank
    sectionTypeSet = T.sectionTypeSet

    aContext = app.context
    noDescendTypes = aContext.noDescendTypes

    sectionDepth = len(sectionTypeSet)
    if len(results) == 0:
        return ()
    firstResult = results[0]
    nTuple = len(firstResult)
    refColumns = [
        i for (i, n) in enumerate(firstResult) if fOtype(n) not in sectionTypeSet
    ]
    refColumn = refColumns[0] if refColumns else nTuple - 1
    header = ["R"] + [f"S{i}" for i in range(1, sectionDepth + 1)]
    emptyA = []

    featureDict = {i: tuple(f.split()) if type(f) is str else f for (i, f) in features}

    def withText(nodeType):
        return (
            condenseType is None
            and nodeType not in sectionTypeSet
            or otypeRank[nodeType] <= otypeRank[condenseType]
        )

    noDescendTypes = noDescendTypes

    for j in range(nTuple):
        i = j + 1
        n = firstResult[j]
        nType = fOtype(n)
        header.extend([f"NODE{i}", f"TYPE{i}"])
        if withText(nType):
            header.append(f"TEXT{i}")
        header.extend(f"{feature}{i}" for feature in featureDict.get(j, emptyA))
    rows = [tuple(header)]
    for (rm, r) in enumerate(results):
        rn = rm + 1
        row = [rn]
        refN = r[refColumn]
        sparts = T.sectionFromNode(refN)
        nParts = len(sparts)
        section = sparts + ((None,) * (sectionDepth - nParts))
        row.extend(section)
        for j in range(nTuple):
            n = r[j]
            nType = fOtype(n)
            row.extend((n, nType))
            if withText(nType):
                text = T.text(n, fmt=fmt, descend=nType not in noDescendTypes)
                row.append(text)
            row.extend(Fs(feature).v(n) for feature in featureDict.get(j, emptyA))
        rows.append(tuple(row))
    return tuple(rows)


def getSlots(api, n):
    F = api.F
    fOtype = F.otype.v
    slotType = F.otype.slotType
    if fOtype(n) == slotType:
        return frozenset((n,))
    E = api.E
    maxSlot = F.otype.maxSlot
    return frozenset(E.oslots.data[n - maxSlot - 1])


def getFeatures(app, dContext, n, nType):
    api = app.api
    L = api.L
    Fs = api.Fs

    aContext = app.context
    featuresBare = aContext.featuresBare
    features = aContext.features

    dFeatures = dContext.features
    dFeaturesIndirect = dContext.featuresIndirect
    queryFeatures = dContext.queryFeatures
    standardFeatures = dContext.standardFeatures
    suppress = dContext.suppress
    noneValues = dContext.noneValues

    (theseFeatures, indirect) = features.get(nType, ((), {}))
    (theseFeaturesBare, indirectBare) = featuresBare.get(nType, ((), {}))

    # a feature can be nType:feature
    # do a L.u(n, otype=nType)[0] and take the feature from there

    givenFeatureSet = set(theseFeatures) | set(theseFeaturesBare)
    xFeatures = tuple(
        f for f in dFeatures if not standardFeatures or f not in givenFeatureSet
    )
    featureList = tuple(theseFeaturesBare + theseFeatures) + xFeatures
    bFeatures = len(theseFeaturesBare)
    nbFeatures = len(theseFeaturesBare) + len(theseFeatures)

    featurePart = ""

    if standardFeatures or queryFeatures:
        for (i, name) in enumerate(featureList):
            if name not in suppress:
                fsName = Fs(name)
                if fsName is None:
                    continue
                fsNamev = fsName.v

                value = None
                if (
                    name in dFeaturesIndirect
                    or name in indirectBare
                    or name in indirect
                ):
                    refType = (
                        dFeaturesIndirect[name]
                        if name in dFeaturesIndirect
                        else indirectBare[name]
                        if name in indirectBare
                        else indirect[name]
                    )
                    refNode = L.u(n, otype=refType)
                    refNode = refNode[0] if refNode else None
                else:
                    refNode = n
                if refNode is not None:
                    value = fsNamev(refNode)

                value = None if value in noneValues else htmlEsc(value or "")
                if value is not None:
                    value = value.replace("\n", "<br/>")
                    isBare = i < bFeatures
                    isExtra = i >= nbFeatures
                    if (
                        isExtra
                        and not queryFeatures
                        or not isExtra
                        and not standardFeatures
                    ):
                        continue
                    nameRep = "" if isBare else f'<span class="f">{name}=</span>'
                    titleRep = f'title="{name}"' if isBare else ""
                    xCls = "xft" if isExtra else ""
                    featurePart += (
                        f'<span class="{name.lower()} {xCls}" {titleRep}>'
                        f"{nameRep}{value}</span>"
                    )
    if not featurePart:
        return ""

    return f"<div class='features'>{featurePart}</div>"


def loadCss(app):
    """The CSS is looked up and then loaded into a notebook if we are not
    running in the TF browser,
    else the CSS is returned.
    """

    _browse = app._browse
    aContext = app.context
    css = aContext.css

    if _browse:
        return css

    cssPath = (
        f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}"
        f"{SERVER_DISPLAY_BASE}"
    )
    genericCss = ""
    for cssFile in SERVER_DISPLAY:
        with open(f"{cssPath}/{cssFile}", encoding="utf8") as fh:
            genericCss += fh.read()

    tableCss = "tr.tf, td.tf, th.tf { text-align: left ! important;}"
    dh(f"<style>" + tableCss + genericCss + css + "</style>")


def getRefMember(app, tup, dContext):
    api = app.api
    otypeRank = api.otypeRank
    fOtypev = api.F.otype.v

    minRank = None
    minN = None
    for n in tup:
        nType = fOtypev(n)
        rank = otypeRank[nType]
        if minRank is None or rank < minRank:
            minRank = rank
            minN = n
            if minRank == 0:
                break

    return (tup[0] if tup else None) if minN is None else minN
