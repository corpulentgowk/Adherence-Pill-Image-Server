from flask import Flask

from parse_rest.connection import register #Connects to the PArse Database. Format: <application_id>, <rest_api_key>[, master_key=None]
register("HW8S7gMIafiQQszmJme2IS4Be7jFlRHnE0izdtLs", "D0lEeiwQ62X6POKXJ1RTxbHuDPX91aUvditAIjxC", master_key="fDtm8fpoHSxbeH3iUGaEexoRgsSdiBh2MvYGDjej")

from parse_rest.datatypes import Object

from PIL import Image
import urllib, cStringIO

class ImageStorageDev(Object):
    pass

#Get data from parse by objectId
dataRow = ImageStorageDev.Query.get(objectId="uqA3Ycyqnq")
#Get data column (image) for that record
image = dataRow.image
#Get image URL
imageURL = image.url
print imageURL

#Get image (We don't actually need the file, URL should be enough)
#Get image from image URL
#imageFile = cStringIO.StringIO(urllib.urlopen(imageURL).read())
#pic = Image.open(imageFile)
#pic.show()

app = Flask(__name__)
@app.route('/')
def hello_world():
    #pic = Image.open(image)
    #image.show()
    picTag = '<img src="' + imageURL + '" alt="' + imageURL + '">'
    print picTag
    return "Hello World" + picTag


if __name__ == '__main__':
    app.run()
