/**
 * UMS Mobile E2E Tests
 * Comprehensive end-to-end tests for critical workflows
 */

import { expect, by } from 'detox';


describe('Student Registration Flow', () => {
  
  beforeAll(async () => {
    await device.launchApp();
    await device.reloadReactNative();
  });

  it('should login successfully', async () => {
    await element(by.id('emailInput')).typeText('student@university.edu.ng');
    await element(by.id('passwordInput')).typeText('SecurePass123!');
    await element(by.id('loginButton')).tap();
    
    // Wait for home screen
    await expect(element(by.id('homeScreen'))).toBeVisible();
  });

  it('should view available courses', async () => {
    await element(by.id('coursesTab')).tap();
    await expect(element(by.id('courseList'))).toBeVisible();
    
    // Check courses load
    const courses = element(by.id('courseItem'));
    await expect(courses).toBeVisible();
  });

  it('should register for a course', async () => {
    await element(by.id('registerButton')).tap();
    
    // Confirm registration
    await element(by.id('confirmButton')).tap();
    
    // Verify success message
    await expect(element(by.text('Registration Successful'))).toBeVisible();
  });

  it('should view results', async () => {
    await element(by.id('resultsTab')).tap();
    await expect(element(by.id('resultsList'))).toBeVisible();
  });
});


describe('Offline Flow', () => {
  
  it('should work offline', async () => {
    // Enable airplane mode
    await device.setHardwareKeyboardIO(true);
    
    // App should still load cached data
    await expect(element(by.id('homeScreen'))).toBeVisible();
    
    // Should show offline indicator
    await expect(element(by.id('offlineIndicator'))).toBeVisible();
  });

  it('should sync when back online', async () => {
    // Disable airplane mode (simulate)
    await device.reloadReactNative();
    
    // Wait for sync
    await waitFor(element(by.id('syncComplete')))
      .toBeVisible()
      .withTimeout(5000);
  });
});


describe('Payment Flow', () => {
  
  it('should process payment', async () => {
    await element(by.id('paymentsTab')).tap();
    await element(by.id('payFeesButton')).tap();
    
    // Select amount
    await element(by.id('amountInput')).typeText('50000');
    
    // Select payment method
    await element(by.id('cardPayment')).tap();
    
    // Process payment
    await element(by.id('payButton')).tap();
    
    // Verify success
    await expect(element(by.text('Payment Successful'))).toBeVisible();
  });
});


describe('Hostel Allocation Flow', () => {
  
  it('should request hostel', async () => {
    await element(by.id('hostelTab')).tap();
    await element(by.id('requestHostel')).tap();
    
    // Select hostel preferences
    await element(by.id('hostelType')).tap();
    await element(by.text('Single Room')).tap();
    
    // Submit request
    await element(by.id('submitButton')).tap();
    
    // Verify confirmation
    await expect(element(by.text('Request Submitted'))).toBeVisible();
  });
});


describe('Performance', () => {
  
  it('should load within 3 seconds', async () => {
    const startTime = Date.now();
    
    await element(by.id('coursesTab')).tap();
    await expect(element(by.id('courseList'))).toBeVisible();
    
    const loadTime = Date.now() - startTime;
    expect(loadTime).toBeLessThan(3000);
  });
});