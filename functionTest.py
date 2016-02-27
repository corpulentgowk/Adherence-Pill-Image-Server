import ast
from parse_rest.connection import register #Connects to the PArse Database. Format: <application_id>, <rest_api_key>[, master_key=None]
register("HW8S7gMIafiQQszmJme2IS4Be7jFlRHnE0izdtLs", "D0lEeiwQ62X6POKXJ1RTxbHuDPX91aUvditAIjxC", master_key="fDtm8fpoHSxbeH3iUGaEexoRgsSdiBh2MvYGDjej")

#File Handling
import os
from flask import Flask, request, redirect, url_for
#from werkzeug import secure_filename

UPLOAD_FOLDER = '/Users/Steven-PC/Desktop/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bin'])


#Parse handling
from parse_rest.datatypes import Object

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

val = imagesRetrieve()
print val['Tivicay']