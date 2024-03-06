#!/usr/bin/yarn dev
// Import createQueue and Job from kue module
import { createQueue, Job } from 'kue';

// Define an array of blacklisted phone numbers
const BLACKLISTED_NUMBERS = ['4153518780', '4153518781'];

// Create a queue instance
const queue = createQueue();

/**
 * Sends a push notification to a user.
 * @param {String} phoneNumber
 * @param {String} message
 * @param {Job} job
 * @param {*} done
 */
const sendNotification = (phoneNumber, message, job, done) => {
  // Initialize counters for total and pending notifications
  let total = 2, pending = 2;
  // Set an interval to simulate sending notifications
  let sendInterval = setInterval(() => {
    // Update job progress
    if (total - pending <= total / 2) {
      job.progress(total - pending, total);
    }
    // Check if the phone number is blacklisted
    if (BLACKLISTED_NUMBERS.includes(phoneNumber)) {
      // If blacklisted, mark job as failed with an error
      done(new Error(`Phone number ${phoneNumber} is blacklisted`));
      // Clear the interval and return
      clearInterval(sendInterval);
      return;
    }
    // Log the notification being sent when all notifications are pending
    if (total === pending) {
      console.log(
        `Sending notification to ${phoneNumber},`,
        `with message: ${message}`,
      );
    }
    // Decrement pending count, and if it reaches 0, call done to indicate job completion
    --pending || done();
    // Clear the interval if all notifications are sent
    pending || clearInterval(sendInterval);
  }, 1000);
};

// Process jobs with type 'push_notification_code_2', allowing 2 concurrent jobs
queue.process('push_notification_code_2', 2, (job, done) => {
  // Call sendNotification function to handle each job
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
