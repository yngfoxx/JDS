const app = require('express')()
const server = require('http').createServer(app)
const port = process.env.PORT || 8000;
const io = require('socket.io')(server, {
  cors: {
    origin: '*',
  },
  serveClient: false,
  // below are engine.IO options
  pingInterval: 10000,
  pingTimeout: 5000,
  cookie: false
});


app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.get('/', (req, res) => { // SERVER OUTPUT
   res.sendFile(__dirname + '/index.html');
   // res.json('Running');
});

const sukey = [
  'FMZur70PbXcT7dYOFdOuzjSpC4xdduMD',
  'u0xx53YtRC77iH1ROnIZSivPeKr2XzzP',
];

const usrkey = [
  'Aj6dN8WfWbPq1HdnHJFXwsXV7MDRrCCU'
];

const pykey = [
  'qPyFMKAdjtfL3Gq5pk2xDgy0SKMpEmLz'
];

// SOCKET SECTION ============================================================================================================================================================>
const admin_server_nsp = io.of(/^\/su_\d+$/);
const user_nsp = io.of(/^\/usr_\d+$/);
const cookie = require('cookie');

let user_array = [];


// ADMIN SOCKET NAMESPACE/CHANNELS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\/
admin_server_nsp.use((socket, next) => { // Authenticate admin channel
  let handshake = socket.handshake;
  if (sukey.includes(handshake.auth.token)) return next(); // check authenticity of key
    admin_server_nsp.emit('msg', {socket_type: 'admin', socket_data: '{ADMIN} => ['+socket.id+'] ACCESS DENIED (Invalid key)'}); // send message direct to the admin namespace
  return next(new Error('Authentication error'));
});

admin_server_nsp.on('connection', (socket) => {
  const admin_channel = socket.nsp; // newNamespace.name === '/su_123456'
  let handshake = socket.handshake;

  admin_server_nsp.emit('msg', {socket_type: 'admin', socket_data: '{ADMIN} => ['+socket.id+'] NEW CONNECTION TO '+admin_channel.name}); // send message direct to the admin namespace

  // SOCKET EVENT PROCESSING
  socket.on('msg', (data) => {
    console.log('ADMIN_MSG => '+JSON.stringify(data)); // data received
    admin_server_nsp.emit('msg', {socket_type: 'admin', socket_data: data}); // send message direct to the admin namespace
  });

  // BASIC SOCKET COMMANDS
  socket.on('disconnect', function () {
    admin_server_nsp.emit('msg', {socket_type: 'admin', socket_data: `ADMIN [${socket.id}] DISCONNECTED`}); // send message direct to the admin namespace
  });
});
// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>/\



// USER SOCKET NAMESPACE/CHANNEL>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\/
user_nsp.use((socket, next) => { // Authenticate admin channel
  let handshake = socket.handshake;
  if (usrkey.includes(handshake.auth.token)) return next(); // check authenticity of key
  admin_server_nsp.emit('msg', {socket_type: 'user', socket_data: '{USER} => ['+socket.id+'] ACCESS DENIED (Invalid key)'}); // send message direct to the admin namespace
  return next(new Error('authentication error'));
});

user_nsp.on('connection', (socket) => {
  const user_channel = socket.nsp; // newNamespace.name === '/usr_123456
  let handshake = socket.handshake;
  // console.log(handshake.query);
  // console.log(handshake.auth);

  // Announce user connection
  admin_server_nsp.emit('msg', {socket_type: 'user', socket_data: '{USER} => ['+socket.id+'] NEW CONNECTION TO '+user_channel.name}); // send message direct to the admin namespace

  // GET DEVICE KEY
  const cookies = cookie.parse(socket.request.headers.cookie || '');
  const device_key = (cookies.dKEY || '');

  // SOCKET EVENT PROCESSING
  socket.on('msg', (data) => {
    user_channel.emit('msg', data); // send message direct to the namespace
    admin_server_nsp.emit('msg', {socket_type: 'user', socket_data: data}); // send message direct to the admin namespace
  });

  // BASIC SOCKET COMMANDS
  socket.on('disconnect', function () {
    admin_server_nsp.emit('msg', {socket_type: 'user', socket_data: `USER [${socket.id}] DISCONNECTED`}); // send message direct to the admin namespace
  });
});
// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>/\

























// PYTHON API SOCKET NAMESPACE/CHANNELS =====================================================================================================================================\/
  const python_server_nsp = io.of(/^\/py_\d+$/);
  let pyClients = [];

  python_server_nsp.on('connection', (socket) => {
    const python_channel = socket.nsp;
    let handshake = socket.handshake;
    let socketGC = (handshake.auth.gc) ? handshake.auth.gc : ((handshake.room) ? handshake.room : 'general');
    if (socketGC != 'general') socket.join(socketGC); // add only users to rooms
    let uData = {
      uuid: handshake.auth.uid,
      room: socketGC
    };
    if (socketGC != 'general') pyClients.push(uData);

    // SOCKET ON DISCONNECT EVENT
    socket.on('disconnect', () => {
      if (socketGC != 'general') pyClients.splice(pyClients.indexOf(uData), 1); // remove user from client list
      admin_server_nsp.emit('msg', {socket_type: 'python', socket_data: `[-] PYTHON SOCKET [${socket.id}] DISCONNECTED`}); // send message direct to the admin namespace
      admin_server_nsp.emit('msg', {socket_type: 'admin', socket_data: '{USERS} =>'+JSON.stringify(pyClients)});
    });

    // python_server_nsp.to(socketGC).emit('msg', 'Welcome to Joint Downloading System'); // send status of all users in the channel
    admin_server_nsp.emit('msg', {socket_type: 'python', socket_data: `[+] PYTHON SOCKET [${socket.id}] CONNECTED`}); // send message direct to the admin namespace
    admin_server_nsp.emit('msg', {socket_type: 'admin', socket_data: '{USERS} =>'+JSON.stringify(pyClients)}); // Notify admin

    // SOCKET { EVENT } PROCESSING
    socket.on('event', (data) => { // File download event
      data.channel = python_channel.name;
      python_server_nsp.to(data.namespace).emit('msg', data); // send message direct to the namespace
      admin_server_nsp.emit('msg', {socket_type: 'python', socket_data: data}); // send message direct to the admin namespace
      if (data.file_data.progress) console.log(data.file_data.progress);
    });

    // SOCKET { MSG } PROCESSING
    socket.on('msg', (data) => {
      data.sid = socket.id;
      admin_server_nsp.emit('msg', {socket_type: 'admin', socket_data: data}); // send message direct to the admin namespace

      if (data.hasOwnProperty('action')) {
        switch (data.action) {
          case 'user_status': // get user status in specified room
             if (data.hasOwnProperty('gc') && data.hasOwnProperty('uid')) {
               let t_gc = data.gc;
               let t_uid = data.uid;
               let inList = false;
               let index;
               pyClients.forEach((item, i) => {
                if (getKeyByValue(item, t_uid) == 'uuid' && pyClients[i].room == t_gc) {
                  inList = true;
                  index = i;
                }
               });
               let arr = (inList) ? {gc: pyClients[index].room, uid: pyClients[index].uuid, status: 'connected'} : {gc: t_gc, uid: t_uid, status: 'disconnected'};
               python_server_nsp.to(t_gc).emit('msg', {response: 'user_status', data: arr}); // send status of all users in the channel
             }
            break;

          default:
            break;
        }
      }

    });
  });
// ==========================================================================================================================================================================/\



function getKeyByValue(object, value) {
  return Object.keys(object).find(key => object[key] === value);
}


















// ===========================================================================================================================================================================>

server.listen(port, () => console.log(`Listening on port ${port}`));
