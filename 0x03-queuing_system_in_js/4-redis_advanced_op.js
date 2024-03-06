// Import the Redis library
import redis from 'redis';

// Create a Redis client instance
const client = redis.createClient();

// Set values for different Holberton schools using hset command
client.hset("HolbertonSchools", "Portland", 50, redis.print);
client.hset("HolbertonSchools", "Seattle", 80, redis.print);
client.hset("HolbertonSchools", "New York", 20, redis.print);
client.hset("HolbertonSchools", "Bogota", 20, redis.print);
client.hset("HolbertonSchools", "Cali", 40, redis.print);
client.hset("HolbertonSchools", "Paris", 2, redis.print);

// Retrieve all the values associated with keys in a hash with hgetall command
client.hgetall("HolbertonSchools", function(err, reply) {
  console.log(reply);
});
