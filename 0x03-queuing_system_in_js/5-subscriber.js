// Import the Redis library
import redis from 'redis';
// Import the promisify function from the util module
import { promisify } from 'util';

// Create a Redis client instance
const client = redis.createClient();

// Event listener for successful connection to the Redis server
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Event listener for connection error with the Redis server
client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Subscribe to a specific Redis channel
client.subscribe('holberton school channel');

// Event listener for messages received on the subscribed channel
client.on('message', (channel, message) => {
  console.log(message);
  // Check if the received message is 'KILL_SERVER'
  if (message === 'KILL_SERVER') {
    // Unsubscribe from the channel and quit the client
    client.unsubscribe();
    client.quit();
  }
});

// Function to publish a message to a Redis channel after a certain delay
async function publishMessage(message, time) {
  // Set a timeout to publish the message after a specified delay
  setTimeout(() => {
    console.log(`About to send ${message}`);
    // Publish the message to the Redis channel
    client.publish('holberton school channel', message);
  }, time);
}

// Publish messages with specified delays
publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400);
