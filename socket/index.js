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

// SOCKET SECTION ------------------------------------------------------------->
const admin_server_nsp = io.of(/^\/su_\d+$/);
const python_server_nsp = io.of(/^\/py_\d+$/);
const user_nsp = io.of(/^\/usr_\d+$/);
const cookie = require('cookie');


// ADMIN SOCKET NAMESPACE/CHANNELS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
admin_server_nsp.use((socket, next) => { // Authenticate admin channel
  if (sukey.includes(socket.handshake.query.auth)) return next(); // check authenticity of key
  admin_server_nsp.emit('msg', '{ADMIN} => ['+socket.id+'] ACCESS DENIED (Invalid key)');
  return next(new Error('authentication error'));
});

admin_server_nsp.on('connection', (socket) => {
  const admin_channel = socket.nsp; // newNamespace.name === '/su_123456'

  admin_server_nsp.emit('msg', '{ADMIN} => ['+socket.id+'] NEW CONNECTION TO '+admin_channel.name);
  console.log('{ADMIN} => ['+socket.id+'] NEW CONNECTION TO '+admin_channel.name);

  // SOCKET EVENT PROCESSING
  socket.on('msg', (data) => {
    console.log('ADMIN_MSG => '+JSON.stringify(data)); // data received
    admin_server_nsp.emit('msg', data); // send message direct to the namespace
  });

  // BASIC SOCKET COMMANDS
  socket.on('disconnect', function () {
    admin_server_nsp.emit('msg', `ADMIN [${socket.id}] DISCONNECTED`);
  });
});
// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



// USER SOCKET NAMESPACE/CHANNEL>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
user_nsp.use((socket, next) => { // Authenticate admin channel
  if (usrkey.includes(socket.handshake.query.auth)) return next(); // check authenticity of key
  user_nsp.emit('msg', '{USER} => ['+socket.id+'] ACCESS DENIED (Invalid key)');
  return next(new Error('authentication error'));
});

user_nsp.on('connection', (socket) => {
  const user_channel = socket.nsp; // newNamespace.name === '/usr_123456

  // Announce user connection
  user_nsp.emit('msg', '{USER} => ['+socket.id+'] NEW CONNECTION TO '+user_channel.name);
  console.log('{USER} => ['+socket.id+'] NEW CONNECTION TO '+user_channel.name);

  // GET DEVICE KEY
  const cookies = cookie.parse(socket.request.headers.cookie || '');
  const device_key = (cookies.dKEY || '');
  //if (device_key != '') console.log("DEVICE_KEY: "+device_key); // user device key from cookie (used to identify users)

  // SOCKET EVENT PROCESSING
  socket.on('msg', (data) => {
    console.log('USER_MSG => '+JSON.stringify(data)); // data received
    user_channel.emit('msg', data); // send message direct to the namespace
  });

  // BASIC SOCKET COMMANDS
  socket.on('disconnect', function () {
    console.log(`{USER} => [${socket.id}] DISCONNECTED`);
    user_nsp.emit('msg', `USER [${socket.id}] DISCONNECTED`);
  });
});
// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



// PYTHON API SOCKET NAMESPACE/CHANNELS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
// python_server_nsp.use((socket, next) => { // Authenticate admin channel
//   if (pykey.includes(socket.handshake.query.auth)) return next(); // check authenticity of key
//   python_server_nsp.emit('msg', '{PYTHON} => ['+socket.id+'] ACCESS DENIED (Invalid key)');
//   return next(new Error('authentication error'));
// });

python_server_nsp.on('connection', (socket) => {
  const python_channel = socket.nsp; // newNamespace.name === '/python

  // GET SOCKET DATA
  python_server_nsp.emit('msg', '{PYTHON} => ['+socket.id+'] NEW CONNECTION TO '+python_channel.name);
  console.log('{PYTHON} => ['+socket.id+'] NEW CONNECTION TO '+python_channel.name);

  // SOCKET EVENT PROCESSING
  socket.on('msg', (data) => {
    python_server_nsp.emit('msg', data); // send message direct to the namespace
  });

  // BASIC SOCKET COMMANDS
  socket.on('disconnect', function () {
    python_server_nsp.emit('msg', `PYTHON SOCKET [${socket.id}] DISCONNECTED`);
  });
});
// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

// ---------------------------------------------------------------------------->

server.listen(port, () => console.log(`Listening on port ${port}`));
