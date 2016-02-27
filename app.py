from flask import Flask, request
import ast
from parse_rest.connection import register #Connects to the PArse Database. Format: <application_id>, <rest_api_key>[, master_key=None]
register("HW8S7gMIafiQQszmJme2IS4Be7jFlRHnE0izdtLs", "D0lEeiwQ62X6POKXJ1RTxbHuDPX91aUvditAIjxC", master_key="fDtm8fpoHSxbeH3iUGaEexoRgsSdiBh2MvYGDjej")

#File Handling
import os
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug import secure_filename
import json,httplib

UPLOAD_FOLDER = '/Users/Steven-PC/Desktop/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bin'])


#Parse handling
from parse_rest.datatypes import Object

from PIL import Image
import urllib, cStringIO

def imagesRetrieve():
   class ImageStorageDev(Object):
       pass

   #Get data from parse by objectId
   #dataRow = ImageStorageDev.Query.get(objectId="uqA3Ycyqnq")

   imageDict = {}
   dataRows = ImageStorageDev.Query.filter(processed=False)
   #print dataRows
   for dataRow in dataRows:
       #Get data column (image) for that record
       image = dataRow.image
       print type(image)
       imageList = []
       #Get image URL
       imageURL = image.url
       category = dataRow.category
       if category not in imageDict:
           imageList.append(imageURL)
           imageDict[category] = imageList
       else:
          imageDict[category].append(imageURL)
   return imageDict

#Get image (We don't actually need the file, URL should be enough)
#Get image from image URL
#imageFile = cStringIO.StringIO(urllib.urlopen(imageURL).read())
#pic = Image.open(imageFile)
#pic.show()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    #pic = Image.open(image)
    #image.show()
    #picTag = '<img src="' + imageURL + '" alt="' + imageURL + '">'
    #print picTag
    #return "Hello World" + picTag
    return "Welcome to The Adherence Pill Image Processing Server"

#In the future, we may want to change this method to POST.
# @app.route('/update/<objectID>')
# def getResult(objectID):
#     pill = request.args.get('pill','')
#     result = {}
#     if pill is not None:
#         result[objectID] = pill
#         updateImages(result)
#         return 'ObjectID: {0}, Pill: {1}'.format(objectID,pill)
#     return 'Pill not found for ObjectID %s' % objectID

@app.route('/getImages')
def getData():
    dic = imagesRetrieve()

    return jsonify(dic)


#Sample Request
# r = requests.post('http://httpbin.org/post', files={'report.xls': open('report.xls', 'rb')})
#r = requests.post('http://localhost:5000', files={'test.txt': open('test.txt', 'rb')})
#r = requests.post('http://localhost:5000/addModel', files={'test.txt': open('test.txt', 'rb')})
# r = requests.post("http://localhost:5000/addModel", files={'test.bin': open('test.bin', 'rb')})
@app.route('/addModel', methods=['POST'])
def insertModel():

    if request.method == 'POST':
        for filename, file in request.files.iteritems():
            name = request.files[filename].name
    file1 = request.files[name] #Grabs the file that was uploaded

#### Uploads File to Parse ####

    connection = httplib.HTTPSConnection('api.parse.com', 443) #Will need to be changed later to wherever we offload parse api
    connection.connect()
    connection.request('POST', '/1/files/' + name, file1.read(),
                   {
           "X-Parse-Application-Id": "HW8S7gMIafiQQszmJme2IS4Be7jFlRHnE0izdtLs",
           "X-Parse-REST-API-Key": "D0lEeiwQ62X6POKXJ1RTxbHuDPX91aUvditAIjxC",
           "Content-Type": "application/octet-stream"
         })

    res = connection.getresponse().read()
    res = str(res)
    res = ast.literal_eval(res) #converts the response into a JSON so we can index it by strings
    # res["name"] #Grab the link that parse stored in the files class so we can associate the file with ModelStorage

#### Adds Recently Uploaded File to Parse to Class: Model Storage ####

    connection.request('POST', '/1/classes/ModelStorage', json.dumps({
       "model": {
         "name": res["name"],
         "__type": "File"
       }
     }), {
       "X-Parse-Application-Id": "HW8S7gMIafiQQszmJme2IS4Be7jFlRHnE0izdtLs",
       "X-Parse-REST-API-Key": "D0lEeiwQ62X6POKXJ1RTxbHuDPX91aUvditAIjxC",
       "Content-Type": "application/json"
     })
    result = json.loads(connection.getresponse().read())
    print result
    return "Successfully inserted model"

@app.route('/getModels', methods=['GET'])
def fetchModel():
    class ModelStorage(Object):
       pass

    modelDict = {}
    dataRows =  ModelStorage.Query.all()
    for dataRow in dataRows:
       #Get data column (file) for that record
       model = dataRow.model
       id = dataRow.objectId
       modelDict[id] = model.url

    return jsonify(modelDict)

if __name__ == '__main__':
    #app.debug = True
    app.run(debug = 'True')