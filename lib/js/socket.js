// code to connect to SOCKET from external site
let USER_SOCKET_ID;
let USER_CHANNEL_ID = rand(1000000000, 9999999999);

// const user_socket = io('ws://localhost:8000'+USER_CHANNEL_ID, {
const user_socket = io('ws://ws-jds-eu.herokuapp.com/usr_'+USER_CHANNEL_ID, {
  query: { auth: 'Aj6dN8WfWbPq1HdnHJFXwsXV7MDRrCCU' },
  reconnectionDelayMax: 10000,
  // forceNew: true
});

user_socket.on('connect', () => {
  USER_SOCKET_ID = user_socket.id;
  console.log('{USER} => ['+USER_SOCKET_ID+'] NOW LISTENING TO '+USER_CHANNEL_ID);
  // TODO: update socket id in database
});

user_socket.on('msg', (data) => {
  // TODO: Process incoming messages
});

user_socket.on("connect_error", err => {
  if (err instanceof Error) {
    console.error(err.message); // not authorized
    console.log(err.data); // { content: "Please retry later" }
  }
});
