#!/usr/bin/yarn dev
// Import createQueue function from kue module
import { createQueue } from 'kue';

// Create a queue instance
const queue = createQueue();

// Function to send a notification with specified phone number and message
const sendNotification = (phoneNumber, message) => {
  console.log(
    `Sending notification to ${phoneNumber},`,
    'with message:',
    message,
  );
};

// Process jobs with type 'push_notification_code'
queue.process('push_notification_code', (job, done) => {
  // Extract phone number and message from the job data and send notification
  sendNotification(job.data.phoneNumber, job.data.message);
  // Notify the queue that processing of the job is complete
  done();
});
