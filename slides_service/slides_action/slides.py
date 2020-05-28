# Riley and Tristan
# 5/2/2020
# 
# The Main Slide Actions. Here we will define functions as actions
#   the server can take with the slides files
#
# We will also provide an entry function "onStart" which will be used for general
#   use and a function for the processes in the background. 
#   (We could populate a global credentials variable here)

# API-Related
import googleapiclient.discovery as discovery
import requests

# Other
import datetime

# The ID of a sample presentation.
PRESENTATION_ID = '15axIfyoPF1zDV4VbcQzceM6DNnvbloHX2lXX07fcaZY'

##### PREPERATION ####
now = datetime.datetime.now()
today = now.strftime("%d %B, %Y")

# -------------------------------------------------------------------------------
##### ALL THE API CODE MANIPULATION GOES HERE!!! #####
def on_start(creds, log):

    service = discovery.build('slides', 'v1', credentials=creds)

    # Call the Slides API
    presentation = service.presentations().get(
        presentationId=PRESENTATION_ID)

    presentation = presentation.execute()

    # execute()
    slides = presentation.get('slides')

    print('The presentation contains {} slides:'.format(len(slides)))
    for i, slide in enumerate(slides):
        if(slide.get("pageElements") != None):
            print('- Slide #{} contains {} elements.'.format(
                i + 1, len(slide.get('pageElements'))))
        else:
            print('- Slide #{} contains 0 elements.'.format(i + 1))
    
    # Reads a Presentation and its objects

    r = presentation.get('https://slides.googleapis.com/v1/presentations/{}?fields=slides.objectId'.format(PRESENTATION_ID))

    # Writes the selected slide information to a .json file
    file = open("sideInfo.json","w") 
    file.write(str(slides) + ".json")
    file.close()

# -------------------------------------------------------------------------------

    
    # Grab a presnentation
    # And do stuff with it

# Creates a text box 

    pt100 = {
        'magnitude': 100,
        'unit': 'PT'
    }
    req_body = {
        "requests": [
            {   # Changes Slide background
                "updatePageProperties": {
                    "objectId": "g75387addb7_1_5",  # The Slide ID 
                    "pageProperties": {
                        "pageBackgroundFill": {
                            "stretchedPictureFill": {
                                "contentUrl": "https://images.unsplash.com/photo-1533907650686-70576141c030?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80"   # URL of the new background image
                            }
                        }   
                    },
                    "fields": "pageBackgroundFill"
                }
            },
            {   # Replaces all instances of this text
                "replaceAllText": {
                    "containsText": {
                        "text": "%7Bdate%7D", # Text to replace
                        "matchCase": False
                    },
                    "replaceText": str(today)  # What it should be replaced with
                }
            },
            {  
                "replaceAllText": {
                    "containsText": {
                        "text": "color",  # Text to replace
                        "matchCase": False
                    },
                    "replaceText": "colorHere"  # What it should be replaced with
                }
            }
        ] } 

    service.presentations().batchUpdate(presentationId=PRESENTATION_ID, body=req_body).execute()     
