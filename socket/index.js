const app = require('express')()
const http = require('http').createServer(app)
var io = require('socket.io')(http)

app.get('/', (req, res) => {
   res.sendFile(__dirname + '/index.html');
})

// SOCKET SECTION ------------------------------------------------------------->
io.on("connection", (socket) => {
  io.emit('message', 'A user has connected');
  // SOCKET HANDLING
  socket.on('message', (msg) => {
    io.emit('message', msg);
  });

  // handle basic socket commands
  socket.on('disconnect', function () {
      io.emit('message', 'A user disconnected');
      // console.log('A user disconnected');
   });
});

// const dynamicNsp = io.of(/^\/dynamic-\d+$/).on('connection', (socket) => {
//   const newNSP = socket.nsp; // newNamespace.name === '/dynamic-101'
//
//   // broadcast to all clients in the given sub-namespace
//   newNSP.emit('hello');
// });
// ---------------------------------------------------------------------------->

// http.listen(8000)

http.listen(process.env.PORT)
