# Joint Downloading System (JDS)
Joint Downloading System (JDS) is an online content downloader that eases file downloading over the internet and solves downloading problems such as poor internet connection, limited network bandwidth and limited download speeds by utilizing technologies such as PHP, Python, Node.js and MySQL.

## Installation
### Requirements
* XAMPP
* Python 3.7^
* npm
* pip
* php 7

### Setup and usage
#### 1. Pull the repository into your preferred web host root folder, by default it is *C:/xampp/htdocs* for Windows

#### 2. Start apache and MySQL service in XAMPP

#### 3. Run the following in CMD to activate the flask downloader API:
    $ cd c:/xampp/htdocs/JDS/api/
    $ fetch\Scripts\activate
    $ python fetch.py


#### 4. Run the following in CMD to run the Desktop client:
    $ cd c:/xampp/htdocs/JDS/application/
    $ venv\Scripts\activate
    $ python app.py
    or run with debugger:
    $ python app.py --remote-debugging-port=1231


#### 5. Run the following in CMD to run the JDS socket server locally:
     $ cd c:/xampp/htdocs/JDS/socket/
     $ npm start dev


### Ports
* 8000 - JDS socket server (Alternative is live at https://ws-jds-eu.herokuapp.com/)
* 5000 - JDS flask downloader API
* 8000 - Desktop LAN HTTP server for client application
* 5678 - Desktop WEBSOCKET SERVER for client application
* 1231 - Desktop client application debugger (Inspect element)
