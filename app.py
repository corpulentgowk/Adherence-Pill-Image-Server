from flask import Flask, request

from parse_rest.connection import register #Connects to the PArse Database. Format: <application_id>, <rest_api_key>[, master_key=None]
register("HW8S7gMIafiQQszmJme2IS4Be7jFlRHnE0izdtLs", "D0lEeiwQ62X6POKXJ1RTxbHuDPX91aUvditAIjxC", master_key="fDtm8fpoHSxbeH3iUGaEexoRgsSdiBh2MvYGDjej")

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
    for dataRow in dataRows:
        #Get data column (image) for that record
        image = dataRow.image
        #Get image URL
        imageURL = image.url
        imageDict[dataRow.objectId] = imageURL
    return imageDict

def updateImages(result):
    class ImageStorageDev(Object):
        pass
    for key in result:
        dataRow = ImageStorageDev.Query.get(objectId=key)
        dataRow.processed=True
        print result[key]
        dataRow.pill = result[key]
        dataRow.save()


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
    #picTag = '<img src="' + imageURL + '" alt="' + imageURL + '">'
    #print picTag
    #return "Hello World" + picTag
    return "Hello World"

#In the future, we may want to change this method to POST.
@app.route('/update/<objectID>')
def getResult(objectID):
    pill = request.args.get('pill','')
    result = {}
    if pill is not None:
        result[objectID] = pill
        updateImages(result)
        return 'ObjectID: {0}, Pill: {1}'.format(objectID,pill)
    return 'Pill not found for ObjectID %s' % objectID

@app.route('/getData')
def getData():
    dic = imagesRetrieve()
    result = ""
    # These results may look bad on browser, but by using telnet, it actually
    # starts a new line.
    for key, value in dic.iteritems():
        result = result + key + ":" + value + "\n"
    return result


#Sample Request
# r = requests.post('http://httpbin.org/post', files={'report.xls': open('report.xls', 'rb')})
#r = requests.post('http://localhost:5000', files={'test.txt': open('test.txt', 'rb')})

@app.route('/addModel/<param>', methods=['POST'])
def insertModel(param):
    param = str(param)
    dat = ast.literal_eval(param)
    dat = ast.literal_eval(dat)

    if request.method == 'POST':
        file = request.files['file']
    class ModelStorage(Object):
        pass
    modelStorage = ModelStorage(patientID=dat['patientID'], model=file)

    return "Successfully inserted model"


@requires_auth
def update_task(param):
    param = str(param)
    dat = ast.literal_eval(param)
    dat = ast.literal_eval(dat)
    cur.execute("select exists(select 1 from utiltrack where jobid='%s');" % (dat['jobid']))
if __name__ == '__main__':
    #app.debug = True
    app.run()
