#!/usr/bin/yarn dev
// Import Queue and Job from kue module
import { Queue, Job } from 'kue';

/**
 * Creates push notification jobs from the array of job info.
 * @param {Job[]} jobs
 * @param {Queue} queue
 */
export const createPushNotificationsJobs = (jobs, queue) => {
  // Check if jobs is an array
  if (!(jobs instanceof Array)) {
    throw new Error('Jobs is not an array');
  }
  // Process each job in the jobs array
  for (const jobInfo of jobs) {
    // Create a new job for each jobInfo object
    const job = queue.create('push_notification_code_3', jobInfo);

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
};

// Export the createPushNotificationsJobs function as the default export
export default createPushNotificationsJobs;
