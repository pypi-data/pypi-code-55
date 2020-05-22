import requests
import json
import logging
import uuid
import base64
from urllib.parse import urljoin
from pathlib import Path
import os
import re
from xml.dom import minidom
from string import Template, Formatter

cwdPath = Path.cwd()
thisPath = Path(__file__).parent

#from robot.api import logger
#from robot.libraries.BuiltIn import BuiltIn
#from robot.utils.asserts import assert_equal
#from robot.api.deco import keyword

"""
ATP Keywords Library for RobotFramework
"""
class ATPKeywords(object):
    ROBOT_LIBRARY_SCOPE = 'Global'

    ATP_DEFAULT_IMAGEPROCESSOR = 'local'
    ATP_DEFAULT_RELAYATPURL = 'http://localhost:9090/'
    ATP_DEFAULT_KEYMAP = "USKeyboard"

    def __init__(self, atpUrl, imageProcessor=ATP_DEFAULT_IMAGEPROCESSOR, relayAtpUrl=ATP_DEFAULT_RELAYATPURL, keyMap=ATP_DEFAULT_KEYMAP):

        self._atpUrl = atpUrl
        self._imageProcessor = imageProcessor
        self._relayAtpUrl = relayAtpUrl
        self._keyMapName = keyMap
        self._keyMapDoc = minidom.parse(str(thisPath.joinpath("KeyMappings.xml")))
        self._keyMap = self._getKeyMapping(self._keyMapName)

        if self._imageProcessor == 'relay':
            pingResponse = self._call(self._getRelayAtpUrl('v3'), 'performPing')
            if pingResponse['Successful'] == False:
                raise Exception('Relay ATP instance not available!')

        if self._keyMap:
            keyMapResponse = self._call(self._getAtpUrl('v2'), 'setKeyMappings', [self._keyMap])
            if keyMapResponse['Successful'] == False:
                raise Exception('Unable to set ATP KeyMapping!')

    # Gets the ATP Url endpoint based on version (default v3)
    def _getAtpUrl(self, version='v3'):
        return urljoin(self._atpUrl, 'ATP/' + version)

    # Gets the ATP Relay Url endpoint based on version (default v3)
    def _getRelayAtpUrl(self, version='v3'):
        return urljoin(self._relayAtpUrl, 'ATP/' + version)

    def _getKeyMapping(self, name):
        items = self._keyMapDoc.getElementsByTagName('KeyMapping')
        i = None
        for item in items:
            if item.attributes['name'].value == self._keyMapName:
                i = item
                break

        keyMapping = {
                "keyMappings": []
        }

        if i != None:
            keys = i.getElementsByTagName('Key')
            for key in keys:
                keyMapping['keyMappings'].append({ 
                    "id": key.attributes['id'].value,
                    "keyCode": key.attributes['keycode'].value,
                    "name": key.attributes['name'].value
                })

        return keyMapping

    def _getKeyByName(self, name):
        for key in self._keyMap['keyMappings']:
            if key['name'] == name:
                return key
        return None

    def _getKeyById(self, id):
        for key in self._keyMap['keyMappings']:
            if key['id'] == id:
                return key
        return None

    def _getKeyByCode(self, code):
        for key in self._keyMap['keyMappings']:
            if key['keyCode'] == code:
                return key
        return None

    def _getKeySequenceFromString(self, keys):
        keySeq = []
        tokens = [el[1] for el in Formatter().parse(keys) if el[1] is not None]
        
        inToken = False
        tokenAdded = False

        for i in range(len(keys)):
            c = keys[i]

            #Start of a token
            if not inToken and c == "{":
                inToken = True
                tokenAdded = False

                for token in tokens:
                    if keys[i+1:i+1+len(token)] == token:
                        k = self._getKeyByName(token)
                        if k is not None:
                            keySeq.append(k)
                            tokenAdded=True
                            i+=len(token)
                        k = self._getKeyByCode(token)
                        if k is not None:
                            keySeq.append(k)
                            tokenAdded=True
                            i+=len(token)
                        k = self._getKeyById(token)
                        if k is not None:
                            keySeq.append(k)
                            tokenAdded=True
                            i+=len(token)

            if inToken and c == "}":
                inToken = False

            if not tokenAdded:
                k = self._getKeyByName(c)
                if k is not None:
                    keySeq.append(k)

        return keySeq


    # Validates an ATPResponse object.
    # If result = True - Validate a 'result' object was returned in the ATP Response, and that response was successful
    # If errors = True - Validate response does not have errors reported aswell
    def _validateResponse(self, response, result=True, errors=True):

        try:
            logging.debug('ATP:validateResponse')
            logging.debug(json.dumps(response, indent=4))

            if result == True:
                if response['result']:
                    assert response['result'], 'Invalid ATP Response'
                    assert response['result']['Successful'] == True, 'ATP Response was not successful'
                    #assert response['result']['Result'], 'ATP Response has no result'
                    if errors == True:
                        assert len(response['result']['Errors']) == 0, 'ATP Response contains errors'
                else:
                    assert response != None, 'Invalid ATP Response'
            if response['result']:        
                return response['result']
            else:
                return response
        except Exception as error:
            logging.error(error)
            assert error, error

    def _call(self, url, method, params=[{}], validateResult=True, validateErrors=True):
        try:
            logging.debug('ATP:call ' + method + ' @ ' + url)

            payload = {
                "method": method,
                "params": params,
                "jsonrpc": "2.0",
                "id": str(uuid.uuid4())
            }

            response = requests.post(url, json=payload)

            logging.debug(response.text)
            
            return self._validateResponse(response.json(), validateResult, validateErrors)
        except Exception as error:
            logging.error(error)

    def atp_ping(self):
        """ ATP Ping: Pings ATP server """
        return self._call(self._getAtpUrl('v3'), 'performPing',[{}], True)

    def atp_kill(self):
        """ ATP Kill: Kills ATP server """
        return self._call(self._getAtpUrl('v2'), 'kill', [], False)

    def atp_delay(self, duration):
        """ ATP Delay: Delays X milliseconds """
        return self._call(self._getAtpUrl('v2'), 'delay', [duration], False)

    def atp_take_screen_capture(self):
        """ ATP Take Screen Capture: Takes Screen capture on ATP server """
        return self._call(self._getAtpUrl('v2'), 'takeScreenCapture',[], True)

    def atp_save_screen_capture(self, filename):
        """ ATP Save Screen Capture: Takes and Saves screen capture from ATP server to file """
        response = self.atp_take_screen_capture()
        data = base64.b64decode(response['Result'])
        with open(filename, 'wb') as f:
            f.write(data)

    def _read_image(self, filename):
        filepath = self._parse_filepath(filename)

        with open(filepath.absolute(), "rb") as imgFile:
            imgBytes = imgFile.read()

        base64Bytes = base64.b64encode(imgBytes).decode('utf-8')
        return str(base64Bytes)

    def _parse_filepath(self, filepath):
        filepath = Path(filepath)
        if not filepath.is_absolute() and not filepath.exists():
            filepath = cwdPath.joinpath(filepath)
        return filepath.absolute()


    # check if a string is base64 encoded.
    def _is_base64(self, s):
        pattern = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$")
        if not s or len(s) < 1:
            return False
        else:
            return pattern.match(s)

    def atp_find_image_in(self, findImage, targetImage, findText=None, tolerance=0.95):
        """ ATP Find Image In: Finds image inside another image """

        findInPayload = {
            "tolerance": tolerance,
            "findText": findText,
            "findImage": findImage,
            "targetImage": targetImage
        }

        if self._imageProcessor == 'relay':
            return self._call(self._getRelayAtpUrl('v3'), 'performFindImageIn',[findInPayload], True)
        else:
            return self._call(self._getAtpUrl('v3'), 'performFindImageIn', [findInPayload], True)

    def atp_click(self, type='LEFTSINGLE', image=None, offset=None, highlight=True, preDelay=0, postDelay=0, tolerance=0.95):
        """ ATP Click: Mouse moves and clicks where an image is found """

        calcOffset = None
        clickPayload = {
            "clickType": type,
            "highlight": highlight,
            "preDelay": preDelay,
            "postDelay": postDelay
        }

        if image is not None:
            if self._imageProcessor == "relay":
                
                imageData = self._read_image(image)
                logging.debug('Find: ' + imageData)

                findImage = {
                    "imageData": imageData,
                    "imagePath": image
                }

                targetResponse = self.atp_take_screen_capture()
                logging.debug('Target: ' + targetResponse['Result'])

                targetImage = {
                    "imageData": targetResponse['Result']
                }

                findImageInResponse = self.atp_find_image_in(findImage, targetImage, tolerance=tolerance)

                #need to validate response matches

                match = findImageInResponse['Result']['Matches'][0]

                if offset is not None:
                    #Offset the found image location
                    offsetSplit = offset.split(",")
                    offsetX = offsetSplit[0].trim()
                    offsetY = offsetSplit[1].trim()
                    calcOffset = str(match['x'] + int(offsetX)) + ',' + str(match['y'] + int(offsetY))
                else:
                    #Calc middle of found region
                    calcOffset = str(match['x'] + int(match['width'] / 2)) + ',' + str(match['y'] + int(match['height'] / 2))

            else:
                if self._is_base64(image):
                    clickPayload['image'] = {
                        "imageData": image
                    }
                else:
                    clickPayload['image'] = {
                        "imageData": self._read_image(image),
                        "imagePath": image
                    }

                calcOffset = offset
        else:
            calcOffset = offset
            
        clickPayload['clickOffset'] = calcOffset
        
        try:
            clickResponse = self._call(self._getAtpUrl('v3'), 'performClick', [clickPayload], True)
        except Exception as err:
            print(err)
        
        return clickResponse

    def atp_keyPress(self, key, release=True, preDelay=0, postDelay=0):
        """ ATP KeyPress: Press a single key (default to not release) """

        if isinstance(key, str):
            key = self._getKeySequenceFromString(key)

        payload = {
            "key": key,
            "press": True,
            "release": release,
            "preDelay": preDelay,
            "postDelay": postDelay,
            "returnScreenBuffer": False
        }
        
        try:
            response = self._call(self._getAtpUrl('v3'), 'keyPress', [payload], True)
        except Exception as err:
            print(err)
        
        return response

    def atp_keyRelease(self, key, preDelay=0, postDelay=0):
        """ ATP KeyRelease: Release previously pressed key """

        if isinstance(key, str):
            key = self._getKeySequenceFromString(key)

        payload = {
            "key": key,
            "press": False,
            "release": True,
            "preDelay": preDelay,
            "postDelay": postDelay,
            "returnScreenBuffer": False
        }
        
        try:
            response = self._call(self._getAtpUrl('v3'), 'keyRelease', [payload], True)
        except Exception as err:
            print(err)
        
        return response

    def atp_keyPressSequence(self, keys, preDelay=0, postDelay=0):
        """ ATP KeyPressSequence: Press and release numerious keys """


        if isinstance(keys, str):
            keys = self._getKeySequenceFromString(keys)

        payload = {
            "sequence": keys,
            "preDelay": preDelay,
            "postDelay": postDelay,
            "detectScreenChange": False,
            "screenChangeTimeout": 30000,
            "screenChangeArea": "0,0,*,*",
            "actionDelay": 250,
            "returnScreenBuffer": False
        }
        
        try:
            response = self._call(self._getAtpUrl('v3'), 'keyPressSequence', [payload], True)
        except Exception as err:
            print(err)
        
        return response
