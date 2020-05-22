import pytest
from ctypes import windll, Structure, c_long, byref
import base64
import os
import pathlib

thisDir = pathlib.Path(__file__).parent

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def getMousePos():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}

def readImage(filename):
    filepath = pathlib.Path(filename)
    if not filepath.is_absolute() and not filepath.exists():
        filepath = thisDir.joinpath(filename)

    with open(filepath.absolute(), "rb") as imgFile:
        imgBytes = imgFile.read()

    base64Bytes = base64.b64encode(imgBytes).decode('utf-8')
    return str(base64Bytes)

@pytest.fixture
def keywords():
    from ATPLibrary.ATPKeywords import ATPKeywords
    return ATPKeywords('http://localhost:9090/', 'local')

def test_atp_ping(keywords):
    response = keywords.atp_ping()
    assert response, 'Invalid Response'

def test_atp_click_offset(keywords):
    response = keywords.atp_click(offset="0,0")
    assert response, 'Invalid Response'
    mouse = getMousePos()
    print(mouse)
    assert mouse['x'] == 0, 'Mouse X not at 0'
    assert mouse['y'] == 0, 'Mouse Y not at 0'

    response = keywords.atp_click(offset="100,50")
    assert response, 'Invalid Response'
    mouse = getMousePos()
    print(mouse)
    assert mouse['x'] == 100, 'Mouse X not at 100'
    assert mouse['y'] == 50, 'Mouse Y not at 50'

    response = keywords.atp_click(offset="2*,2*")
    assert response, 'Invalid Response'
    mouse = getMousePos()
    print(mouse)
    #assert mouse['x'] == 100, 'Mouse X not at 100'
    #assert mouse['y'] == 50, 'Mouse Y not at 50'

def test_atp_click_image(keywords):
    #make sure mouse is at 0,0
    response = keywords.atp_click(offset="0,0")
    assert response, 'Invalid Response'

    #Click based on image LEFTSINGLE
    response = keywords.atp_click(image="tests/start.png")
    assert response, 'Invalid Response'

    keywords.atp_keyPress(key='{Escape}')

    response = keywords.atp_click(image="tests/start.png", type="LEFTDOUBLE")
    assert response, 'Invalid Response'

    mouse = getMousePos()
    assert mouse['x']>0, 'Mouse X invalid position'
    assert mouse['y']>0, 'Mouse Y invalid position'
    