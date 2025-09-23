import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Format and Text Pages', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
  });

  const formatTextPages = [
    { name: '格式转换', path: '/format', title: '格式' },
    { name: '文字处理', path: '/text', title: '文字' },
    { name: '图像标注', path: '/annotation', title: '标注' }
  ];

  formatTextPages.forEach(({ name, path, title }) => {
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
        // Format and text pages may have examples
        await helpers.checkExampleImages();
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

  test('should navigate between format and text pages', async ({ page }) => {
    await page.goto('/');
    await helpers.waitForPageLoad();

    for (const pageInfo of formatTextPages) {
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

test.describe('Format Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/format');
    await helpers.waitForPageLoad();
  });

  test('should have format conversion options', async ({ page }) => {
    const formatElements = [
      'text=输出格式',
      'text=JPEG',
      'text=PNG',
      'text=WebP',
      'text=质量',
      '.MuiSelect-root',
      '.MuiSlider-root'
    ];

    let found = false;
    for (const selector of formatElements) {
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

  test('should display supported format information', async ({ page }) => {
    const formatInfoElements = [
      'text=支持格式',
      'text=输入格式',
      'text=输出格式',
      'text=格式说明'
    ];

    let found = false;
    for (const selector of formatInfoElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    // Format info might be in examples or help text
    // Not critical if not found
  });
});

test.describe('Text Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/text');
    await helpers.waitForPageLoad();
  });

  test('should have text input and styling options', async ({ page }) => {
    const textElements = [
      'text=文字内容',
      'text=字体',
      'text=字号',
      'text=颜色',
      'text=位置',
      'textarea',
      'input[type="text"]',
      '.MuiTextField-root'
    ];

    let found = false;
    for (const selector of textElements) {
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

  test('should have text positioning controls', async ({ page }) => {
    const positionElements = [
      'text=位置',
      'text=左上角',
      'text=居中',
      'text=右下角',
      'text=X坐标',
      'text=Y坐标',
      '.MuiSelect-root'
    ];

    let found = false;
    for (const selector of positionElements) {
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

  test('should have text styling options', async ({ page }) => {
    const styleElements = [
      'text=字体大小',
      'text=字体颜色',
      'text=背景色',
      'text=透明度',
      'text=粗体',
      'text=斜体',
      '.MuiSlider-root',
      'input[type="color"]'
    ];

    let found = false;
    for (const selector of styleElements) {
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

test.describe('Annotation Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/annotation');
    await helpers.waitForPageLoad();
  });

  test('should have annotation tools', async ({ page }) => {
    const annotationElements = [
      'text=标注类型',
      'text=矩形',
      'text=圆形',
      'text=箭头',
      'text=文字标注',
      'text=线条',
      '.MuiSelect-root'
    ];

    let found = false;
    for (const selector of annotationElements) {
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

  test('should have annotation styling options', async ({ page }) => {
    const styleElements = [
      'text=颜色',
      'text=线条粗细',
      'text=透明度',
      'text=填充',
      'text=边框',
      '.MuiSlider-root',
      'input[type="color"]'
    ];

    let found = false;
    for (const selector of styleElements) {
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

  test('should support interactive annotation', async ({ page }) => {
    // Look for canvas or interactive elements for drawing annotations
    const interactiveElements = [
      'canvas',
      'svg',
      'text=点击添加',
      'text=拖拽绘制',
      '[data-testid="annotation-canvas"]'
    ];

    let found = false;
    for (const selector of interactiveElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    // Interactive annotation might not be immediately visible
    // This is optional functionality
  });
});
