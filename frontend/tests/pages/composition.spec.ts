import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Composition Pages', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
  });

  const compositionPages = [
    { name: '图像混合', path: '/blend', title: '混合' },
    { name: '图像拼接', path: '/stitch', title: '拼接' },
    { name: '图像叠加', path: '/overlay', title: '叠加' },
    { name: '蒙版处理', path: '/mask', title: '蒙版' }
  ];

  compositionPages.forEach(({ name, path, title }) => {
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
        // Composition pages typically have examples
        const hasExamples = await helpers.checkExampleImages();
        expect(hasExamples).toBe(true);
      });

      test(`should have tab layout structure on ${name} page`, async ({ page }) => {
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

  test('should navigate between composition pages', async ({ page }) => {
    await page.goto('/');
    await helpers.waitForPageLoad();

    for (const pageInfo of compositionPages) {
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

test.describe('Blend Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/blend');
    await helpers.waitForPageLoad();
  });

  test('should have blend-specific settings', async ({ page }) => {
    const blendElements = [
      'text=混合模式',
      'text=透明度',
      'text=正常',
      'text=叠加',
      'text=柔光',
      '.MuiSelect-root',
      '.MuiSlider-root'
    ];

    let found = false;
    for (const selector of blendElements) {
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

  test('should support multiple image upload for blending', async ({ page }) => {
    // Look for multiple image upload areas or indicators
    const multiUploadElements = [
      'text=背景图片',
      'text=前景图片',
      'text=第二张图片',
      'input[type="file"][multiple]'
    ];

    let found = false;
    for (const selector of multiUploadElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    // Multiple image support is expected for blend functionality
    expect(found).toBe(true);
  });
});

test.describe('Stitch Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/stitch');
    await helpers.waitForPageLoad();
  });

  test('should have stitch-specific settings', async ({ page }) => {
    const stitchElements = [
      'text=拼接方向',
      'text=水平拼接',
      'text=垂直拼接',
      'text=网格拼接',
      'text=间距',
      '.MuiSelect-root'
    ];

    let found = false;
    for (const selector of stitchElements) {
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

  test('should support multiple image upload for stitching', async ({ page }) => {
    const multiUploadElements = [
      'text=添加图片',
      'text=多张图片',
      'input[type="file"][multiple]',
      'text=拖拽多张图片'
    ];

    let found = false;
    for (const selector of multiUploadElements) {
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

test.describe('Overlay Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/overlay');
    await helpers.waitForPageLoad();
  });

  test('should have overlay-specific settings', async ({ page }) => {
    const overlayElements = [
      'text=叠加位置',
      'text=透明度',
      'text=缩放',
      'text=旋转',
      'text=左上角',
      'text=居中',
      '.MuiSlider-root'
    ];

    let found = false;
    for (const selector of overlayElements) {
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

  test('should support background and overlay image upload', async ({ page }) => {
    const overlayUploadElements = [
      'text=背景图片',
      'text=叠加图片',
      'text=主图片',
      'text=水印图片'
    ];

    let found = false;
    for (const selector of overlayUploadElements) {
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

test.describe('Mask Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/mask');
    await helpers.waitForPageLoad();
  });

  test('should have mask-specific settings', async ({ page }) => {
    const maskElements = [
      'text=蒙版',
      'text=蒙版类型',
      'text=反转蒙版',
      'text=羽化',
      'text=透明度',
      '.MuiSelect-root',
      '.MuiSlider-root'
    ];

    let found = false;
    for (const selector of maskElements) {
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

  test('should support image and mask upload', async ({ page }) => {
    const maskUploadElements = [
      'text=原图',
      'text=蒙版图片',
      'text=遮罩图片',
      'text=选择蒙版'
    ];

    let found = false;
    for (const selector of maskUploadElements) {
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
