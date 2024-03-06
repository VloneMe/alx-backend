// Import the Redis library
import redis from 'redis';

// Create a Redis client instance
const client = redis.createClient();

// Event listener for successful connection to the Redis server
client.on('connect', function() {
  console.log('Redis client connected to the server');
});

// Event listener for connection error with the Redis server
client.on('error', function(err) {
  console.log('Redis client not connected to the server: ' + err);
});

// Subscribe to a specific Redis channel
client.subscribe('holberton school channel');

// Event listener for messages received on the subscribed channel
client.on('message', function(channel, message) {
  console.log('Message received on channel ' + channel + ': ' + message);
  // Check if the received message is 'KILL_SERVER'
  if (message === 'KILL_SERVER') {
    // Unsubscribe from the channel and quit the client
    client.unsubscribe();
    client.quit();
  }
});
