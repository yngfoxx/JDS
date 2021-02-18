// SOCKET MANAGER ------------------------------------------------------------->
let USID;
let UUID = rand(1000000000, 9999999999);

// SOCKET MANAGER
const manager = io('ws://ws-jds-eu.herokuapp.com', {
// const manager = io('ws://localhost:8000', {
  reconnectionDelayMax: 10000,
  query: { uChannel: UUID }
});

const user_socket = manager.connect('/usr_'+UUID, {
    auth: { token: 'Aj6dN8WfWbPq1HdnHJFXwsXV7MDRrCCU' }
  }
);


user_socket.on('connect', ()=>{
  console.log("connected");
});
// ---------------------------------------------------------------------------->
