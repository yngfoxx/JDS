const app = require('express')()
const http = require('http').createServer(app)
var io = require('socket.io')(http)

app.get('/', (req, res) => {
   res.sendFile(__dirname + '/index.html');
})

// SOCKET SECTION ------------------------------------------------------------->
io.on("connection", (socket) => {
  // SOCKET HANDLING
  socket.on('message', (msg) => {
    io.emit('message', msg);
  });

  // handle basic socket commands
  socket.on('disconnect', function () {
      console.log('A user disconnected');
   });
});
// ---------------------------------------------------------------------------->

// http.listen(8000)

http.listen(process.env.PORT)
