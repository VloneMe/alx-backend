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
  console.error(`Redis client not connected to the server: ${err}`);
});

// Function to set a new school name and its value in the Redis database
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

// Function to asynchronously display the value associated with a given school name from the Redis database
async function displaySchoolValue(schoolName) {
  // Promisify the Redis get method to enable asynchronous behavior
  const getAsync = promisify(client.get).bind(client);
  // Retrieve the value associated with the schoolName asynchronously
  const value = await getAsync(schoolName);
  // Log the retrieved value
  console.log(value);
}

// Display the value associated with the school name 'Holberton' from the Redis database
displaySchoolValue('Holberton');

// Set a new school name 'HolbertonSanFrancisco' with a value of '100' in the Redis database
setNewSchool('HolbertonSanFrancisco', '100');

// Display the updated value associated with the school name 'HolbertonSanFrancisco' from the Redis database
displaySchoolValue('HolbertonSanFrancisco');
