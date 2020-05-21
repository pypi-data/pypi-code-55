import asyncio
import websockets
import json
import traceback

async def handler(ai, id, game):
    uri = "ws://34.70.80.81:80"
    async with websockets.connect(uri) as websocket:
        #send hello with array of AI IDs
        data = {
            "status":"hello",
            "payload":{
                "aiIDs":[(id, game)]
            }
        }
        await websocket.send(json.dumps(data))

        #listen for updates
        try:
            async for message in websocket:
                data = json.loads(message)
                status = data["status"]
                payload = data["payload"]
                #print(status, payload)

                #switch response based on status
                if status == "state":
                    gameID = payload["gameID"]
                    state = payload["state"]
                    aiID = payload["aiID"]

                    #make move
                    move = ai.makeMove(state)

                    response = {
                        "status":"move",
                        "payload":{
                            "gameID":gameID,
                            "aiID":aiID,
                            "move":move
                        }
                    }
                    #send move
                    await websocket.send(json.dumps(response))

                elif status == "message":
                    print(f'{payload}')

                elif status == "game created":
                    gameID = payload["gameID"]
                    gameType = payload["gameType"]
                    aiID = payload["aiID"]
                    print(f'A new game was created. Type:{gameType}, AI:{aiID}')

                elif status == "game deleted":
                    gameID = payload["gameID"]
                    result = payload["result"]
                    aiID = payload["aiID"]
                    print(f'A game completed. Result:{result}')
        except Exception as e:
            print("Server disconnected")
            t=traceback.format_exc()
            print(t)
            #print(str(e))
        finally:
            pass



def enterMatchMaker(ai, id, game):
    asyncio.get_event_loop().run_until_complete(handler(ai, id, game))
