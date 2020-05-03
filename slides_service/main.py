# Sour_Tooth and TFlexSoom
# 4/30/2020
# Entry Script For Application

"""
Later on we should create files for these processes but for now I will
post them underneath commented sections to allow for seperation
"""


### First Start a Flask Server to Handle OAuth so we can snag crednetials

from multiprocessing import Process, Pipe
from time import sleep
from web_auth_server.web_server import run_server
from slides_action.slides import on_start

### Run it all
def main():
    
    webPipe = Pipe(True)

    webProc = Process(target=run_server, args=[webPipe[0]])
    webProc.start()

    # Wait till authentication is complete
    webPipe[1].poll(None)

    # Create credentials
    cred = webPipe[1].recv()

    print(cred)

    # Close process
    webPipe[1].close()
    webProc.terminate()
    webProc.join()
    

    print("Gathered Credentials!")

    log = open("log.txt", "w")
    log.write("Success!\n")
    log.write(repr(cred))

    on_start(cred, log)
    


if __name__ == "__main__":
    main()
