/**
 * Peer 1 (Sender)
 * Peer 2 (Receiver)
 * This example has both the peers in the same browser window.
 * In a real application, the peers would exchange their signaling data for a proper connection.
 * The signaling server part is omitted for simplicity
 */
const peer1 = new SimplePeer({ initiator: true });
const peer2 = new SimplePeer();

/**
 * Implementing the WebRTC connection between the nodes
 */

// Share the signalling data of sender with the receivers
peer1.on('signal', data => {
  peer2.signal(data);
});

// Share the signalling data of receiver with the sender
peer2.on('signal', data => {
  peer1.signal(data);
});


/**
 * Connection established, now sender can send files to other peers
 */
peer1.on('connect', () => {
  const input = document.getElementById('file-input');

  // Event listener on the file input
  input.addEventListener('change', () => {
    const file = input.files[0];
    console.log('Sending', file)

    // We convert the file from Blob to ArrayBuffer, since some browsers don't work with blobs
    file.arrayBuffer()
    .then(buffer => {
      // Off goes the file!
      peer1.send(buffer);
    });

  });
});


/**
 * Receiver receives the files
 */
peer2.on('data', data => {
  // Convert the file back to Blob
  const file = new Blob([ data ]);

  console.log('Received', file);
  // Download the received file using downloadjs
  download(file, 'test.png');
});
