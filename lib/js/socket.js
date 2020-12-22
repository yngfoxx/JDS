// code to connect to SOCKET from external site
// const io = require('socket.io-client');
const socket = io.connect('http://localhost:8000');

socket.on('connect', () => {
  console.log('Successfully connected!');
});
