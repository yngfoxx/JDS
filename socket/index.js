const app = require('express')()
const http = require('http').createServer(app)
const port = process.env.PORT || 8000;
var io = require('socket.io')(http, { serveClient: false });


app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "http://localhost:8000");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.get('/', (req, res) => {
   // res.sendFile(__dirname + '/index.html');
   res.json('Running');
})


// SOCKET SECTION ------------------------------------------------------------->
io.on("connection", (socket) => {
  // GET SOCKET DATA
  console.log(`New user connected: ${socket.id}`);

  // SOCKET HANDLING
  socket.on('message', (msg) => {
    io.emit('message', msg);
  });

  // handle basic socket commands
  socket.on('disconnect', function () {
      io.emit('message', 'A user disconnected');
      console.log('A user disconnected');
   });
});
// ---------------------------------------------------------------------------->

http.listen(port, () => console.log(`Listening on port ${port}`));
