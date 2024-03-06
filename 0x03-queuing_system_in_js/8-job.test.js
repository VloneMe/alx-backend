#!/usr/bin/yarn test
// Import sinon for mocking and chai for assertions
import sinon from 'sinon';
import { expect } from 'chai';
// Import createQueue function from kue module and the function to be tested
import { createQueue } from 'kue';
import createPushNotificationsJobs from './8-job.js';

// Describe block for testing createPushNotificationsJobs function
describe('createPushNotificationsJobs', () => {
  // Spy on console.log
  const BIG_BROTHER = sinon.spy(console);
  // Create a queue instance for testing
  const QUEUE = createQueue({ name: 'push_notification_code_test' });

  // Before hook to enter test mode
  before(() => {
    QUEUE.testMode.enter(true);
  });

  // After hook to clear test mode
  after(() => {
    QUEUE.testMode.clear();
    QUEUE.testMode.exit();
  });

  // After each hook to reset spy history
  afterEach(() => {
    BIG_BROTHER.log.resetHistory();
  });

  // Test case for throwing an error if jobs is not an array
  it('displays an error message if jobs is not an array', () => {
    expect(
      createPushNotificationsJobs.bind(createPushNotificationsJobs, {}, QUEUE)
    ).to.throw('Jobs is not an array');
  });

  // Test case for adding jobs to the queue with correct type and data
  it('adds jobs to the queue with the correct type', (done) => {
    expect(QUEUE.testMode.jobs.length).to.equal(0);
    // Define job information
    const jobInfos = [
      {
        phoneNumber: '44556677889',
        message: 'Use the code 1982 to verify your account',
      },
      {
        phoneNumber: '98877665544',
        message: 'Use the code 1738 to verify your account',
      },
    ];
    // Call the function under test
    createPushNotificationsJobs(jobInfos, QUEUE);
    // Assert that jobs are added to the queue
    expect(QUEUE.testMode.jobs.length).to.equal(2);
    expect(QUEUE.testMode.jobs[0].data).to.deep.equal(jobInfos[0]);
    expect(QUEUE.testMode.jobs[0].type).to.equal('push_notification_code_3');
    // Process the added jobs
    QUEUE.process('push_notification_code_3', () => {
      // Assert that the 'enqueue' event is logged
      expect(
        BIG_BROTHER.log
          .calledWith('Notification job created:', QUEUE.testMode.jobs[0].id)
      ).to.be.true;
      done();
    });
  });

  // Test case for registering the progress event handler for a job
  it('registers the progress event handler for a job', (done) => {
    QUEUE.testMode.jobs[0].addListener('progress', () => {
      expect(
        BIG_BROTHER.log
          .calledWith('Notification job', QUEUE.testMode.jobs[0].id, '25% complete')
      ).to.be.true;
      done();
    });
    QUEUE.testMode.jobs[0].emit('progress', 25);
  });

  // Test case for registering the failed event handler for a job
  it('registers the failed event handler for a job', (done) => {
    QUEUE.testMode.jobs[0].addListener('failed', () => {
      expect(
        BIG_BROTHER.log
          .calledWith('Notification job', QUEUE.testMode.jobs[0].id, 'failed:', 'Failed to send')
      ).to.be.true;
      done();
    });
    QUEUE.testMode.jobs[0].emit('failed', new Error('Failed to send'));
  });

  // Test case for registering the complete event handler for a job
  it('registers the complete event handler for a job', (done) => {
    QUEUE.testMode.jobs[0].addListener('complete', () => {
      expect(
        BIG_BROTHER.log
          .calledWith('Notification job', QUEUE.testMode.jobs[0].id, 'completed')
      ).to.be.true;
      done();
    });
    QUEUE.testMode.jobs[0].emit('complete');
  });
});
