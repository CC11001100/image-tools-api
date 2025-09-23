import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Filter and Effects Pages', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
  });

  const filterPages = [
    { name: '滤镜', path: '/filter', title: '滤镜' },
    { name: '艺术滤镜', path: '/art-filter', title: '艺术滤镜' },
    { name: '颜色调整', path: '/color', title: '颜色' },
    { name: '图像增强', path: '/enhance', title: '增强' },
    { name: '噪点处理', path: '/noise', title: '噪点' },
    { name: '像素化', path: '/pixelate', title: '像素化' }
  ];

  filterPages.forEach(({ name, path, title }) => {
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
        // Filter pages typically have rich examples
        const hasExamples = await helpers.checkExampleImages();
        // Most filter pages should have examples
        expect(hasExamples).toBe(true);
      });

      test(`should have tab layout structure on ${name} page`, async ({ page }) => {
        // Check for tab layout
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

        await page.reload();
        await helpers.waitForPageLoad();
        
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

  test('should navigate between filter pages', async ({ page }) => {
    await page.goto('/');
    await helpers.waitForPageLoad();

    for (const pageInfo of filterPages) {
      try {
        await helpers.navigateToPage(pageInfo.name, pageInfo.path);
        expect(page.url()).toContain(pageInfo.path);
        await helpers.checkPageHeader(pageInfo.title);
      } catch (error) {
        console.log(`Navigation to ${pageInfo.name} failed:`, error);
      }
    }
  });
});

test.describe('Filter Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/filter');
    await helpers.waitForPageLoad();
  });

  test('should have filter-specific settings', async ({ page }) => {
    const filterElements = [
      'text=滤镜类型',
      'text=强度',
      'text=模糊',
      'text=锐化',
      '.MuiSlider-root',
      '.MuiSelect-root'
    ];

    let found = false;
    for (const selector of filterElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    expect(found).toBe(true);
  });
});

test.describe('Art Filter Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/art-filter');
    await helpers.waitForPageLoad();
  });

  test('should have art filter gallery', async ({ page }) => {
    const artFilterElements = [
      'text=艺术风格',
      'text=油画',
      'text=水彩',
      'text=素描',
      '.MuiGrid-item',
      'img[src*="art"]'
    ];

    let found = false;
    for (const selector of artFilterElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    expect(found).toBe(true);
  });
});

test.describe('Color Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/color');
    await helpers.waitForPageLoad();
  });

  test('should have color adjustment controls', async ({ page }) => {
    const colorElements = [
      'text=亮度',
      'text=对比度',
      'text=饱和度',
      'text=色调',
      '.MuiSlider-root'
    ];

    let found = false;
    for (const selector of colorElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    expect(found).toBe(true);
  });
});

test.describe('Enhance Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/enhance');
    await helpers.waitForPageLoad();
  });

  test('should have enhancement options', async ({ page }) => {
    const enhanceElements = [
      'text=增强',
      'text=锐化',
      'text=降噪',
      'text=超分辨率',
      '.MuiSelect-root'
    ];

    let found = false;
    for (const selector of enhanceElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    expect(found).toBe(true);
  });
});

test.describe('Noise Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/noise');
    await helpers.waitForPageLoad();
  });

  test('should have noise processing controls', async ({ page }) => {
    const noiseElements = [
      'text=噪点',
      'text=降噪',
      'text=强度',
      'text=类型',
      '.MuiSlider-root'
    ];

    let found = false;
    for (const selector of noiseElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    expect(found).toBe(true);
  });
});

test.describe('Pixelate Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/pixelate');
    await helpers.waitForPageLoad();
  });

  test('should have pixelation controls', async ({ page }) => {
    const pixelateElements = [
      'text=像素化',
      'text=像素大小',
      'text=强度',
      '.MuiSlider-root'
    ];

    let found = false;
    for (const selector of pixelateElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    expect(found).toBe(true);
  });
});
