from flask import Flask

from parse_rest.connection import register #Connects to the PArse Database. Format: <application_id>, <rest_api_key>[, master_key=None]
register("HW8S7gMIafiQQszmJme2IS4Be7jFlRHnE0izdtLs", "D0lEeiwQ62X6POKXJ1RTxbHuDPX91aUvditAIjxC", master_key="fDtm8fpoHSxbeH3iUGaEexoRgsSdiBh2MvYGDjej")

from parse_rest.datatypes import Object

class GameScore(Object): #Declare the class you want to access in the parse database
    pass
gameScore = GameScore(score=1337, player_name='John Doe', cheat_mode=False)
gameScore.cheat_mode = True
gameScore.level = 20
gameScore.save()


gameScore = GameScore.Query.get(objectId="xxwXx9eOec")
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
