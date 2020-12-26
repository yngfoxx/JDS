// code to connect to SOCKET from external site
// const socket = io.connect('http://ws-jds-eu.herokuapp.com');
// const socket = io.connect('https://ws-jds-eu.herokuapp.com/usr');
let USER_SOCKET_ID;
let USER_CHANNEL_ID = '/usr_'+rand(1000000000, 9999999999);

const user_socket = io('ws://localhost:8000'+USER_CHANNEL_ID, {
  // query: { auth: 'qPyFMKAdjtfL3Gq5pk2xDgy0SKMpEmLz' },
  query: { auth: 'sadrwe234' },
  reconnectionDelayMax: 10000,
  forceNew: true
});

user_socket.on('connect', () => {
  SOCKET_ID = user_socket.id;
  console.log('{USER} => ['+USER_SOCKET_ID+'] NOW CONNECTED TO '+USER_CHANNEL_ID);
  // update socket id in database
});

user_socket.on("connect_error", err => {
  if (err instanceof Error) {
    console.error(err.message); // not authorized
    console.log(err.data); // { content: "Please retry later" }
  }
});
