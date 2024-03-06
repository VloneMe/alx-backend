#!/usr/bin/yarn dev
// Import createQueue function from kue module
import { createQueue } from 'kue';

// Create a queue instance with name 'push_notification_code'
const queue = createQueue({name: 'push_notification_code'});

// Create a job for pushing a notification with specified phone number and message
const job = queue.create('push_notification_code', {
  phoneNumber: '07045679939',
  message: 'Account registered',
});

// Event listeners for job events
job
  .on('enqueue', () => {
    console.log('Notification job created:', job.id);
  })
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed attempt', () => {
    console.log('Notification job failed');
  });

// Save the job to the queue
job.save();
