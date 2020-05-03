# Riley and Tristan
# 5/2/2020
# 
# The Main Slide Actions. Here we will define functions as actions
#   the server can take with the slides files
#
# We will also provide an entry function "onStart" which will be used for general
#   use and a function for the processes in the background. 
#   (We could populate a global credentials variable here)

import googleapiclient.discovery as discovery

# The ID of a sample presentation.
PRESENTATION_ID = '1LZ4ZzKeAMbCVxB0MUiVyI3fddqjBKJaKp_6ZRDF-Rwc'


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
    
    # Other Stuff
    body = {
        'title': "This is a title!"
    }
    presentation = service.presentations() \
        .create(body=body).execute()
    
    print('Created presentation with ID: {0}'.format(
        presentation.get('presentationId')))