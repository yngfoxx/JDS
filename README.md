## About Joint Downloading System (JDS)
Joint Downloading System (JDS) is an online content downloader that eases file downloading over the internet and solves downloading problems such as poor internet connection, limited network bandwidth and limited download speeds by utilizing technologies such as PHP, Python, Node.js and MySQL.

## How to setup JDS locally
#### Requirements
* XAMPP
* PyCharm (optional: you will need to install all the modules manually)
* Python
* npm

#### Installation
1. Copy all files to *c:/xampp/htdocs/JDS*
2. Start apache and mysql service in xampp
3. Run *c:/xampp/htdocs/JDS/api/fetch.py* in PyCharm or run *python c:/xampp/htdocs/JDS/api/fetch.py* in a command prompt to start the python flask server on port 5000
4. Run *npm start dev* in *c:/xampp/htdocs/JDS/socket* to start the socket server on port 8000
