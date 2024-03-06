// Import the Redis library
import redis from 'redis';

// Create a Redis client instance
const client = redis.createClient();

// Event listener for successful connection to the Redis server
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Event listener for connection error with the Redis server
client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});
