#!/usr/bin/yarn dev
// Import necessary modules
import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';

// Create an Express application
const app = express();
// Create a Redis client
const client = createClient({ name: 'reserve_seat' });
// Create a Kue queue instance
const queue = createQueue();
// Define the initial number of seats
const INITIAL_SEATS_COUNT = 50;
// Flag to indicate whether reservations are enabled or not
let reservationEnabled = false;
// Define the port number
const PORT = 1245;

// Function to modify the number of available seats
const reserveSeat = async (number) => {
  return promisify(client.SET).bind(client)('available_seats', number);
};

// Function to retrieve the number of available seats
const getCurrentAvailableSeats = async () => {
  return promisify(client.GET).bind(client)('available_seats');
};

// Route to get the number of available seats
app.get('/available_seats', (_, res) => {
  getCurrentAvailableSeats()
    .then((numberOfAvailableSeats) => {
      res.json({ numberOfAvailableSeats })
    });
});

// Route to reserve a seat
app.get('/reserve_seat', (_req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation is blocked' });
    return;
  }
  try {
    const job = queue.create('reserve_seat');

    job.on('failed', (err) => {
      console.log(
        'Seat reservation job',
        job.id,
        'failed:',
        err.message || err.toString(),
      );
    });
    job.on('complete', () => {
      console.log(
        'Seat reservation job',
        job.id,
        'completed'
      );
    });
    job.save();
    res.json({ status: 'Reservation in process' });
  } catch {
    res.json({ status: 'Reservation failed' });
  }
});

// Route to start processing the queue
app.get('/process', (_req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', (_job, done) => {
    getCurrentAvailableSeats()
      .then((result) => Number.parseInt(result || 0))
      .then((availableSeats) => {
        // Disable reservations if there's only one seat left
        reservationEnabled = availableSeats <= 1 ? false : reservationEnabled;
        if (availableSeats >= 1) {
          // Reserve one seat
          reserveSeat(availableSeats - 1)
            .then(() => done());
        } else {
          // If no seats are available, mark the job as failed
          done(new Error('Not enough seats available'));
        }
      });
  });
});

// Function to reset the available seats count
const resetAvailableSeats = async (initialSeatsCount) => {
  return promisify(client.SET)
    .bind(client)('available_seats', Number.parseInt(initialSeatsCount));
};

// Start the server
app.listen(PORT, () => {
  // Reset the available seats count and enable reservations
  resetAvailableSeats(process.env.INITIAL_SEATS_COUNT || INITIAL_SEATS_COUNT)
    .then(() => {
      reservationEnabled = true;
      console.log(`API available on localhost port ${PORT}`);
    });
});

// Export the Express app
export default app;
