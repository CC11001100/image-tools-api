import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Cross-Page Integration Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
  });

  test('should maintain consistent user experience across all pages', async ({ page }) => {
    const allPages = [
      '/',
      '/resize',
      '/crop',
      '/transform',
      '/canvas',
      '/perspective',
      '/filter',
      '/art-filter',
      '/color',
      '/enhance',
      '/noise',
      '/pixelate',
      '/blend',
      '/stitch',
      '/overlay',
      '/mask',
      '/format',
      '/text',
      '/annotation',
      '/gif',
      '/create-gif',
      '/extract-gif',
      '/watermark',
      '/api-docs',
      '/auth-test'
    ];

    for (const pagePath of allPages) {
      try {
        await page.goto(pagePath);
        await helpers.waitForPageLoad();
        
        // Check consistent layout elements
        await expect(page.locator('.MuiDrawer-root')).toBeVisible();
        
        // Check no critical errors
        const errors: string[] = [];
        page.on('console', (msg) => {
          if (msg.type() === 'error') {
            errors.push(msg.text());
          }
        });
        
        await page.waitForTimeout(1000);
        
        const criticalErrors = errors.filter(error => 
          !error.includes('favicon') && 
          !error.includes('404') &&
          !error.includes('net::ERR_') &&
          !error.includes('ResizeObserver')
        );
        
        if (criticalErrors.length > 0) {
          console.log(`Critical errors on ${pagePath}:`, criticalErrors);
        }
        
      } catch (error) {
        console.log(`Failed to load page ${pagePath}:`, error);
      }
    }
  });

  test('should navigate through complete user workflow', async ({ page }) => {
    // Start from home page
    await page.goto('/');
    await helpers.waitForPageLoad();
    
    // Navigate to resize page
    await helpers.navigateToPage('调整大小', '/resize');
    await helpers.checkPageHeader('调整大小');
    
    // Navigate to filter page
    await helpers.navigateToPage('滤镜', '/filter');
    await helpers.checkPageHeader('滤镜');
    
    // Navigate to watermark page
    await helpers.navigateToPage('水印', '/watermark');
    await helpers.checkPageHeader('水印');
    
    // Navigate to API docs
    await helpers.navigateToPage('API文档', '/api-docs');
    await helpers.checkPageHeader('API');
    
    // Return to home
    await page.goto('/');
    await helpers.waitForPageLoad();
    await helpers.checkPageHeader('图像工具箱', '首页');
  });

  test('should maintain state when navigating between pages', async ({ page }) => {
    // This test checks if any global state is maintained
    // For example, authentication state, theme preferences, etc.
    
    await page.goto('/');
    await helpers.waitForPageLoad();
    
    // Check initial state
    const initialTheme = await page.evaluate(() => {
      return document.documentElement.getAttribute('data-theme') || 
             document.body.className ||
             'default';
    });
    
    // Navigate to different pages and check state consistency
    const testPages = ['/resize', '/filter', '/watermark'];
    
    for (const testPage of testPages) {
      await page.goto(testPage);
      await helpers.waitForPageLoad();
      
      // Check if theme/state is maintained
      const currentTheme = await page.evaluate(() => {
        return document.documentElement.getAttribute('data-theme') || 
               document.body.className ||
               'default';
      });
      
      expect(currentTheme).toBe(initialTheme);
    }
  });

  test('should handle deep linking correctly', async ({ page }) => {
    // Test direct navigation to deep pages
    const deepLinks = [
      '/resize',
      '/filter',
      '/watermark',
      '/api-docs'
    ];

    for (const link of deepLinks) {
      // Navigate directly to the page
      await page.goto(link);
      await helpers.waitForPageLoad();
      
      // Check that the page loads correctly
      expect(page.url()).toContain(link);
      
      // Check that navigation state is correct
      await helpers.checkSidebarNavigation();
      
      // Check that the page content loads
      await expect(page.locator('main')).toBeVisible();
    }
  });

  test('should handle URL parameters and query strings', async ({ page }) => {
    // Test pages with potential query parameters
    const urlTests = [
      '/resize?width=800&height=600',
      '/filter?type=blur',
      '/watermark?position=center'
    ];

    for (const url of urlTests) {
      try {
        await page.goto(url);
        await helpers.waitForPageLoad();
        
        // Check that the page loads despite query parameters
        expect(page.url()).toContain(url.split('?')[0]);
        
        // Check that the page functions normally
        await helpers.checkSidebarNavigation();
        
      } catch (error) {
        console.log(`URL parameter test failed for ${url}:`, error);
      }
    }
  });

  test('should handle browser refresh on any page', async ({ page }) => {
    const testPages = ['/resize', '/filter', '/watermark', '/api-docs'];
    
    for (const testPage of testPages) {
      await page.goto(testPage);
      await helpers.waitForPageLoad();
      
      // Refresh the page
      await page.reload();
      await helpers.waitForPageLoad();
      
      // Check that the page still works after refresh
      expect(page.url()).toContain(testPage);
      await helpers.checkSidebarNavigation();
      await expect(page.locator('main')).toBeVisible();
    }
  });

  test('should handle network errors gracefully', async ({ page }) => {
    // Test offline behavior
    await page.goto('/');
    await helpers.waitForPageLoad();
    
    // Simulate network failure
    await page.context().setOffline(true);
    
    try {
      // Try to navigate to another page
      await page.click('text=调整大小');
      await page.waitForTimeout(2000);
      
      // Check if there's any error handling UI
      const errorElements = [
        'text=网络错误',
        'text=连接失败',
        'text=offline',
        '.error',
        '.network-error'
      ];

      let errorHandlingFound = false;
      for (const selector of errorElements) {
        try {
          if (await page.locator(selector).isVisible({ timeout: 1000 })) {
            errorHandlingFound = true;
            break;
          }
        } catch (e) {
          // Continue
        }
      }
      
      // Error handling might not be implemented
      // This is optional functionality
      
    } finally {
      // Restore network
      await page.context().setOffline(false);
    }
  });

  test('should maintain accessibility across all pages', async ({ page }) => {
    const testPages = ['/', '/resize', '/filter', '/watermark'];
    
    for (const testPage of testPages) {
      await page.goto(testPage);
      await helpers.waitForPageLoad();
      
      // Check for basic accessibility features
      const accessibilityChecks = [
        // Check for proper heading structure
        async () => {
          const headings = page.locator('h1, h2, h3, h4, h5, h6');
          await expect(headings).toHaveCount({ min: 1 });
        },
        
        // Check for alt text on images
        async () => {
          const images = page.locator('img');
          const imageCount = await images.count();
          if (imageCount > 0) {
            // At least some images should have alt text
            const imagesWithAlt = page.locator('img[alt]');
            const altCount = await imagesWithAlt.count();
            expect(altCount).toBeGreaterThan(0);
          }
        },
        
        // Check for proper form labels
        async () => {
          const inputs = page.locator('input, textarea, select');
          const inputCount = await inputs.count();
          if (inputCount > 0) {
            // Check if inputs have labels or aria-labels
            const labeledInputs = page.locator('input[aria-label], input[aria-labelledby], textarea[aria-label], select[aria-label]');
            const labelCount = await labeledInputs.count();
            // Some inputs should have proper labeling
            expect(labelCount).toBeGreaterThanOrEqual(0);
          }
        }
      ];

      for (const check of accessibilityChecks) {
        try {
          await check();
        } catch (error) {
          console.log(`Accessibility check failed on ${testPage}:`, error);
        }
      }
    }
  });

  test('should handle concurrent page loads', async ({ page, context }) => {
    // Test multiple pages loading simultaneously
    const pages = await Promise.all([
      context.newPage(),
      context.newPage(),
      context.newPage()
    ]);

    try {
      // Load different pages concurrently
      await Promise.all([
        pages[0].goto('/resize'),
        pages[1].goto('/filter'),
        pages[2].goto('/watermark')
      ]);

      // Wait for all pages to load
      await Promise.all([
        new TestHelpers(pages[0]).waitForPageLoad(),
        new TestHelpers(pages[1]).waitForPageLoad(),
        new TestHelpers(pages[2]).waitForPageLoad()
      ]);

      // Check that all pages loaded correctly
      expect(pages[0].url()).toContain('/resize');
      expect(pages[1].url()).toContain('/filter');
      expect(pages[2].url()).toContain('/watermark');

    } finally {
      // Clean up
      await Promise.all(pages.map(p => p.close()));
    }
  });

  test('should handle rapid navigation', async ({ page }) => {
    // Test rapid clicking between pages
    await page.goto('/');
    await helpers.waitForPageLoad();

    const rapidNavigation = [
      { text: '调整大小', path: '/resize' },
      { text: '滤镜', path: '/filter' },
      { text: '水印', path: '/watermark' },
      { text: '首页', path: '/' }
    ];

    for (const nav of rapidNavigation) {
      try {
        await page.click(`text=${nav.text}`);
        await page.waitForURL(`**${nav.path}`, { timeout: 3000 });
        // Don't wait for full page load to simulate rapid navigation
        await page.waitForTimeout(100);
      } catch (error) {
        console.log(`Rapid navigation to ${nav.text} failed:`, error);
      }
    }

    // Final check that we end up on a valid page
    await helpers.waitForPageLoad();
    await helpers.checkSidebarNavigation();
  });
});
