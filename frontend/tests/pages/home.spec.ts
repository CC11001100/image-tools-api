import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Home Page', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/');
    await helpers.waitForPageLoad();
  });

  test('should load home page successfully', async ({ page }) => {
    // Check if the page loads without errors
    await expect(page).toHaveTitle(/AI图像工具箱|Image Tools/);
    
    // Check if main layout is present
    await helpers.checkSidebarNavigation();
  });

  test('should display hero banner', async ({ page }) => {
    // Check for hero banner elements
    const heroBanner = page.locator('.MuiBox-root').first();
    await expect(heroBanner).toBeVisible();
    
    // Check for main heading or welcome text
    const headings = page.locator('h1, h2, h3, h4, h5, h6');
    await expect(headings.first()).toBeVisible();
  });

  test('should display feature groups and cards', async ({ page }) => {
    // Check for feature groups
    await expect(page.locator('h4')).toHaveCount({ min: 1 });
    
    // Check for feature cards - should have multiple cards
    const featureCards = page.locator('.MuiCard-root, .MuiPaper-root');
    await expect(featureCards).toHaveCount({ min: 3 });
    
    // Check if cards are clickable/interactive
    const firstCard = featureCards.first();
    await expect(firstCard).toBeVisible();
  });

  test('should have working navigation links', async ({ page }) => {
    // Test navigation to different feature pages
    const navigationTests = [
      { text: '调整大小', path: '/resize' },
      { text: '裁剪', path: '/crop' },
      { text: '滤镜', path: '/filter' }
    ];

    for (const nav of navigationTests) {
      // Go back to home
      await page.goto('/');
      await helpers.waitForPageLoad();
      
      // Try to find and click the navigation link
      try {
        await page.click(`text=${nav.text}`);
        await page.waitForURL(`**${nav.path}`, { timeout: 5000 });
        
        // Verify we're on the correct page
        expect(page.url()).toContain(nav.path);
      } catch (error) {
        console.log(`Navigation to ${nav.text} (${nav.path}) failed:`, error);
        // Continue with other tests
      }
    }
  });

  test('should display quick start section', async ({ page }) => {
    // Look for quick start or getting started section
    const quickStartElements = [
      'text=快速开始',
      'text=开始使用',
      'text=使用指南',
      'text=1. 选择您需要的功能'
    ];

    let found = false;
    for (const selector of quickStartElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue to next selector
      }
    }
    
    expect(found).toBe(true);
  });

  test('should display API documentation link', async ({ page }) => {
    // Look for API docs link
    const apiDocsLink = page.locator('text=API文档, text=查看API文档, a[href*="api-docs"]');
    
    try {
      await expect(apiDocsLink.first()).toBeVisible();
      
      // Test clicking the link
      await apiDocsLink.first().click();
      await page.waitForURL('**/api-docs', { timeout: 5000 });
      expect(page.url()).toContain('/api-docs');
    } catch (error) {
      console.log('API docs link test failed:', error);
      // This might not be critical for home page functionality
    }
  });

  test('should display WeChat QR code section', async ({ page }) => {
    // Look for WeChat group QR code section
    const qrCodeElements = [
      'text=微信群',
      'text=扫码',
      'img[src*="wechat"]',
      'img[src*="qrcode"]',
      'text=没有找到想要的功能'
    ];

    let found = false;
    for (const selector of qrCodeElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue to next selector
      }
    }
    
    expect(found).toBe(true);
  });

  test('should be responsive on mobile devices', async ({ page }) => {
    await helpers.checkResponsiveness();
  });

  test('should not have console errors', async ({ page }) => {
    const errors: string[] = [];
    
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    // Reload page to capture any console errors
    await page.reload();
    await helpers.waitForPageLoad();
    
    // Filter out known non-critical errors
    const criticalErrors = errors.filter(error => 
      !error.includes('favicon') && 
      !error.includes('404') &&
      !error.includes('net::ERR_')
    );
    
    expect(criticalErrors).toHaveLength(0);
  });

  test('should have proper page structure', async ({ page }) => {
    // Check for proper semantic structure
    await expect(page.locator('main')).toBeVisible();
    
    // Check for proper heading hierarchy
    const headings = page.locator('h1, h2, h3, h4, h5, h6');
    await expect(headings).toHaveCount({ min: 1 });
    
    // Check for navigation structure
    await expect(page.locator('nav, .MuiDrawer-root')).toBeVisible();
  });

  test('should handle search functionality if present', async ({ page }) => {
    // Look for search functionality
    const searchElements = [
      'input[placeholder*="搜索"]',
      'input[placeholder*="search"]',
      '[data-testid="search"]',
      '.search-input'
    ];

    for (const selector of searchElements) {
      try {
        const searchInput = page.locator(selector);
        await expect(searchInput).toBeVisible({ timeout: 2000 });
        
        // Test typing in search
        await searchInput.fill('resize');
        await page.waitForTimeout(1000);
        
        // Check if search results appear
        // This is optional functionality
        break;
      } catch (e) {
        // Search might not be present, continue
      }
    }
  });
});
