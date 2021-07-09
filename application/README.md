## Desktop Application

Firstly move the application folder to wherever you wish to put it on your local machine. 
It is not needed on the server!
```
$ cd venv/Scripts
$ activate
$ cd ../../
$ python app.py --remote-debugging-port=1231
```
the debugger will be live on http://127.0.0.1:1231
```
$ cd application/venv/scripts && activate && cd ../../ && python app.py --remote-debugging-port=1231
```
## tools

downloader
```
$ python downloader.py -u "URL_SOURCE" -d "LOCAL_DESTINATION"
```
