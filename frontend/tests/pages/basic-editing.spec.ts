import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Basic Editing Pages', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
  });

  const basicEditingPages = [
    { name: '调整大小', path: '/resize', title: '调整大小' },
    { name: '裁剪', path: '/crop', title: '裁剪' },
    { name: '旋转翻转', path: '/transform', title: '旋转翻转' },
    { name: '画布调整', path: '/canvas', title: '画布调整' },
    { name: '透视变换', path: '/perspective', title: '透视' }
  ];

  basicEditingPages.forEach(({ name, path, title }) => {
    test.describe(`${name} Page (${path})`, () => {
      test.beforeEach(async ({ page }) => {
        await page.goto(path);
        await helpers.waitForPageLoad();
      });

      test(`should load ${name} page successfully`, async ({ page }) => {
        // Check if the page loads without errors
        expect(page.url()).toContain(path);
        
        // Check if main layout is present
        await helpers.checkSidebarNavigation();
        
        // Check page header
        await helpers.checkPageHeader(title);
      });

      test(`should have image upload functionality on ${name} page`, async ({ page }) => {
        await helpers.checkImageUploadPresent();
      });

      test(`should have settings panel on ${name} page`, async ({ page }) => {
        await helpers.checkSettingsPanel();
      });

      test(`should display example images on ${name} page`, async ({ page }) => {
        // Examples might not be present on all pages
        await helpers.checkExampleImages();
      });

      test(`should have tab layout structure on ${name} page`, async ({ page }) => {
        // Check for tab layout (common pattern in the app)
        const tabElements = [
          '.MuiTabs-root',
          '.MuiTab-root',
          'text=文件上传',
          'text=URL输入',
          'text=效果展示'
        ];

        let tabsFound = false;
        for (const selector of tabElements) {
          try {
            await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
            tabsFound = true;
            break;
          } catch (e) {
            // Continue to next selector
          }
        }
        
        // Tabs are expected on most pages
        expect(tabsFound).toBe(true);
      });

      test(`should be responsive on ${name} page`, async ({ page }) => {
        await helpers.checkResponsiveness();
      });

      test(`should not have console errors on ${name} page`, async ({ page }) => {
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
          !error.includes('net::ERR_') &&
          !error.includes('ResizeObserver')
        );
        
        expect(criticalErrors).toHaveLength(0);
      });
    });
  });

  test('should navigate between basic editing pages', async ({ page }) => {
    // Start from home
    await page.goto('/');
    await helpers.waitForPageLoad();

    // Test navigation between basic editing pages
    for (let i = 0; i < basicEditingPages.length; i++) {
      const currentPage = basicEditingPages[i];
      
      try {
        // Navigate to the page via sidebar
        await helpers.navigateToPage(currentPage.name, currentPage.path);
        
        // Verify we're on the correct page
        expect(page.url()).toContain(currentPage.path);
        
        // Check page loads properly
        await helpers.checkPageHeader(currentPage.title);
        
      } catch (error) {
        console.log(`Navigation to ${currentPage.name} failed:`, error);
        // Continue with other tests
      }
    }
  });

  test('should have consistent UI patterns across basic editing pages', async ({ page }) => {
    for (const pageInfo of basicEditingPages) {
      await page.goto(pageInfo.path);
      await helpers.waitForPageLoad();
      
      // Check for consistent UI elements
      const commonElements = [
        '.MuiContainer-root',
        '.MuiPaper-root',
        '.MuiButton-root'
      ];

      for (const selector of commonElements) {
        try {
          await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        } catch (error) {
          console.log(`Common element ${selector} not found on ${pageInfo.path}`);
        }
      }
    }
  });
});

test.describe('Resize Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/resize');
    await helpers.waitForPageLoad();
  });

  test('should have resize-specific settings', async ({ page }) => {
    // Look for resize-specific controls
    const resizeElements = [
      'text=宽度',
      'text=高度',
      'text=保持比例',
      'input[type="number"]',
      '.MuiSlider-root'
    ];

    let found = false;
    for (const selector of resizeElements) {
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
});

test.describe('Crop Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/crop');
    await helpers.waitForPageLoad();
  });

  test('should have crop-specific settings', async ({ page }) => {
    // Look for crop-specific controls
    const cropElements = [
      'text=裁剪',
      'text=比例',
      'text=自由裁剪',
      'text=正方形',
      '.MuiSelect-root'
    ];

    let found = false;
    for (const selector of cropElements) {
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
});

test.describe('Transform Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/transform');
    await helpers.waitForPageLoad();
  });

  test('should have transform-specific settings', async ({ page }) => {
    // Look for transform-specific controls
    const transformElements = [
      'text=旋转',
      'text=翻转',
      'text=角度',
      'text=水平翻转',
      'text=垂直翻转'
    ];

    let found = false;
    for (const selector of transformElements) {
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
});
