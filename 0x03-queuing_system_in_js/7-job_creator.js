#!/usr/bin/yarn dev
// Import createQueue function from kue module
import { createQueue } from 'kue';

// Define an array of job objects with phone numbers and messages
const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account',
  },
  // Add more job objects as needed...
];

// Create a queue instance with a specific name
const queue = createQueue({ name: 'push_notification_code_2' });

// Process each job in the jobs array
for (const jobInfo of jobs) {
  // Create a new job for each jobInfo object
  const job = queue.create('push_notification_code_2', jobInfo);

  // Event listeners for job lifecycle events
  job
    .on('enqueue', () => {
      console.log('Notification job created:', job.id);
    })
    .on('complete', () => {
      console.log('Notification job', job.id, 'completed');
    })
    .on('failed', (err) => {
      console.log('Notification job', job.id, 'failed:', err.message || err.toString());
    })
    .on('progress', (progress, _data) => {
      console.log('Notification job', job.id, `${progress}% complete`);
    });
  
  // Save the job to the queue
  job.save();
}
