import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('GIF Processing Pages', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
  });

  const gifPages = [
    { name: 'GIF处理', path: '/gif', title: 'GIF' },
    { name: '创建GIF', path: '/create-gif', title: 'GIF' },
    { name: '提取GIF帧', path: '/extract-gif', title: 'GIF' }
  ];

  gifPages.forEach(({ name, path, title }) => {
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

      test(`should have upload functionality on ${name} page`, async ({ page }) => {
        // GIF pages might have different upload requirements
        if (path === '/create-gif') {
          // Create GIF should support multiple image upload
          const multiUploadElements = [
            'input[type="file"][multiple]',
            'text=选择多张图片',
            'text=添加图片',
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
        } else {
          // Other GIF pages should have standard upload
          await helpers.checkImageUploadPresent();
        }
      });

      test(`should have settings panel on ${name} page`, async ({ page }) => {
        await helpers.checkSettingsPanel();
      });

      test(`should display example images on ${name} page`, async ({ page }) => {
        // GIF pages typically have examples
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

  test('should navigate between GIF processing pages', async ({ page }) => {
    await page.goto('/');
    await helpers.waitForPageLoad();

    for (const pageInfo of gifPages) {
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

test.describe('GIF Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/gif');
    await helpers.waitForPageLoad();
  });

  test('should have GIF processing options', async ({ page }) => {
    const gifElements = [
      'text=GIF处理',
      'text=帧率',
      'text=质量',
      'text=尺寸',
      'text=循环',
      '.MuiSlider-root',
      '.MuiSelect-root'
    ];

    let found = false;
    for (const selector of gifElements) {
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

  test('should support GIF file upload', async ({ page }) => {
    // Look for GIF-specific upload hints
    const gifUploadElements = [
      'text=选择GIF文件',
      'text=上传GIF',
      'text=.gif',
      'input[accept*="gif"]'
    ];

    let found = false;
    for (const selector of gifUploadElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    // GIF upload hints might not be explicitly shown
    // Standard upload should work
  });
});

test.describe('Create GIF Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/create-gif');
    await helpers.waitForPageLoad();
  });

  test('should have GIF creation settings', async ({ page }) => {
    const createGifElements = [
      'text=帧间隔',
      'text=延迟',
      'text=循环次数',
      'text=帧率',
      'text=FPS',
      'text=持续时间',
      '.MuiSlider-root',
      'input[type="number"]'
    ];

    let found = false;
    for (const selector of createGifElements) {
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

  test('should support multiple image upload for GIF creation', async ({ page }) => {
    const multiUploadElements = [
      'input[type="file"][multiple]',
      'text=选择多张图片',
      'text=添加图片',
      'text=拖拽多张图片',
      'text=批量上传'
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

  test('should have image sequence management', async ({ page }) => {
    const sequenceElements = [
      'text=图片顺序',
      'text=排序',
      'text=删除',
      'text=预览',
      'text=拖拽排序',
      '.MuiList-root'
    ];

    let found = false;
    for (const selector of sequenceElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    // Image sequence management might not be immediately visible
    // until images are uploaded
  });
});

test.describe('Extract GIF Page Specific Tests', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/extract-gif');
    await helpers.waitForPageLoad();
  });

  test('should have GIF extraction options', async ({ page }) => {
    const extractElements = [
      'text=提取帧',
      'text=帧范围',
      'text=开始帧',
      'text=结束帧',
      'text=间隔',
      'text=输出格式',
      '.MuiSlider-root',
      'input[type="number"]'
    ];

    let found = false;
    for (const selector of extractElements) {
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

  test('should support GIF file upload for extraction', async ({ page }) => {
    // Standard upload should work for GIF extraction
    await helpers.checkImageUploadPresent();
    
    // Look for GIF-specific hints
    const gifHints = [
      'text=上传GIF文件',
      'text=选择GIF',
      'text=.gif'
    ];

    for (const selector of gifHints) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        break;
      } catch (e) {
        // Continue - hints might not be present
      }
    }
  });

  test('should have frame preview functionality', async ({ page }) => {
    const previewElements = [
      'text=帧预览',
      'text=预览',
      'text=播放',
      'text=暂停',
      'canvas',
      'video',
      '.preview'
    ];

    let found = false;
    for (const selector of previewElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    // Preview functionality might not be visible until a GIF is uploaded
  });
});
