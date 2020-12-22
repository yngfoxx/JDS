// code to connect to SOCKET from external site
const socket = io.connect('http://ws-jds-eu.herokuapp.com');
// const socket = io.connect('http://localhost:8000');

socket.on('connect', () => {
  console.log('Successfully connected!');
});
