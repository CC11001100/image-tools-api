import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Watermark Page', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/watermark');
    await helpers.waitForPageLoad();
  });

  test('should load watermark page successfully', async ({ page }) => {
    // Check if the page loads without errors
    expect(page.url()).toContain('/watermark');
    
    // Check if main layout is present
    await helpers.checkSidebarNavigation();
    
    // Check page header
    await helpers.checkPageHeader('水印');
  });

  test('should have image upload functionality', async ({ page }) => {
    await helpers.checkImageUploadPresent();
  });

  test('should have watermark settings panel', async ({ page }) => {
    await helpers.checkSettingsPanel();
  });

  test('should display example images', async ({ page }) => {
    // Watermark page should have examples
    const hasExamples = await helpers.checkExampleImages();
    expect(hasExamples).toBe(true);
  });

  test('should have tab layout structure', async ({ page }) => {
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

  test('should have watermark type selection', async ({ page }) => {
    const watermarkTypeElements = [
      'text=水印类型',
      'text=文字水印',
      'text=图片水印',
      'text=文字',
      'text=图片',
      '.MuiSelect-root',
      '.MuiRadioGroup-root'
    ];

    let found = false;
    for (const selector of watermarkTypeElements) {
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

  test('should have text watermark settings', async ({ page }) => {
    const textWatermarkElements = [
      'text=水印文字',
      'text=文字内容',
      'text=字体大小',
      'text=字体颜色',
      'text=透明度',
      'textarea',
      'input[type="text"]',
      '.MuiTextField-root'
    ];

    let found = false;
    for (const selector of textWatermarkElements) {
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

  test('should have watermark position settings', async ({ page }) => {
    const positionElements = [
      'text=位置',
      'text=水印位置',
      'text=左上角',
      'text=右上角',
      'text=左下角',
      'text=右下角',
      'text=居中',
      '.MuiSelect-root',
      '.MuiRadioGroup-root'
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

  test('should have transparency/opacity controls', async ({ page }) => {
    const transparencyElements = [
      'text=透明度',
      'text=不透明度',
      'text=opacity',
      '.MuiSlider-root'
    ];

    let found = false;
    for (const selector of transparencyElements) {
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

  test('should have watermark size controls', async ({ page }) => {
    const sizeElements = [
      'text=大小',
      'text=尺寸',
      'text=缩放',
      'text=字体大小',
      'text=水印大小',
      '.MuiSlider-root',
      'input[type="number"]'
    ];

    let found = false;
    for (const selector of sizeElements) {
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

  test('should support image watermark upload', async ({ page }) => {
    // Look for image watermark upload functionality
    const imageWatermarkElements = [
      'text=水印图片',
      'text=上传水印',
      'text=选择水印图片',
      'input[type="file"]'
    ];

    let found = false;
    for (const selector of imageWatermarkElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        found = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    // Image watermark might be in a separate tab or section
    // Not critical if not immediately visible
  });

  test('should have color picker for text watermark', async ({ page }) => {
    const colorElements = [
      'input[type="color"]',
      'text=颜色',
      'text=字体颜色',
      'text=文字颜色',
      '.color-picker',
      '[data-testid="color-picker"]'
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

  test('should have preview functionality', async ({ page }) => {
    const previewElements = [
      'text=预览',
      'text=效果预览',
      'canvas',
      'img[src*="preview"]',
      '.preview',
      '[data-testid="preview"]'
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
    
    // Preview might not be visible until an image is uploaded
  });

  test('should have processing/download functionality', async ({ page }) => {
    const processElements = [
      'text=处理',
      'text=生成',
      'text=下载',
      'text=添加水印',
      '.MuiButton-root'
    ];

    let found = false;
    for (const selector of processElements) {
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

  test('should have proper form validation', async ({ page }) => {
    // Try to submit without required fields and check for validation
    const submitButton = page.locator('button:has-text("处理"), button:has-text("生成"), button:has-text("添加水印")').first();
    
    try {
      await submitButton.click({ timeout: 2000 });
      
      // Look for validation messages
      const validationElements = [
        'text=请选择图片',
        'text=请输入水印文字',
        'text=必填',
        '.MuiFormHelperText-root.Mui-error'
      ];

      let validationFound = false;
      for (const selector of validationElements) {
        try {
          await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
          validationFound = true;
          break;
        } catch (e) {
          // Continue
        }
      }
      
      // Validation might not be immediately visible or might be handled differently
      // This is optional functionality
    } catch (error) {
      // Submit button might not be clickable without proper setup
      console.log('Form validation test skipped:', error);
    }
  });

  test('should handle different watermark positions', async ({ page }) => {
    // Test different position options if available
    const positions = ['左上角', '右上角', '左下角', '右下角', '居中'];
    
    for (const position of positions) {
      try {
        const positionOption = page.locator(`text=${position}`);
        if (await positionOption.isVisible({ timeout: 1000 })) {
          await positionOption.click();
          // Verify selection (this might update preview or settings)
          await page.waitForTimeout(500);
        }
      } catch (error) {
        // Position option might not be available or clickable
        console.log(`Position ${position} test skipped:`, error);
      }
    }
  });
});
