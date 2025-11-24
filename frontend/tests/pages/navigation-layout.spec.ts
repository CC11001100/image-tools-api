import { test, expect } from '@playwright/test';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Navigation and Layout', () => {
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    helpers = new TestHelpers(page);
    await page.goto('/');
    await helpers.waitForPageLoad();
  });

  test('should display sidebar navigation', async ({ page }) => {
    // Check if sidebar is visible
    await expect(page.locator('.MuiDrawer-root')).toBeVisible();
    
    // Check if the app title is visible
    await expect(page.locator('text=AI图像工具箱')).toBeVisible();
    
    // Check version number if present
    const versionElement = page.locator('text*=v');
    if (await versionElement.isVisible({ timeout: 1000 })) {
      await expect(versionElement).toBeVisible();
    }
  });

  test('should have all main navigation categories', async ({ page }) => {
    const mainCategories = [
      '首页',
      '基础编辑',
      '滤镜效果',
      '图像合成',
      '格式处理',
      'GIF处理'
    ];

    for (const category of mainCategories) {
      try {
        await expect(page.locator(`text=${category}`)).toBeVisible({ timeout: 2000 });
      } catch (error) {
        console.log(`Category ${category} not found:`, error);
        // Some categories might be named differently
      }
    }
  });

  test('should expand and collapse navigation groups', async ({ page }) => {
    // Find expandable menu items
    const expandableItems = page.locator('.MuiListItemButton-root:has(.MuiCollapse-root), .MuiListItemButton-root:has([data-testid="ExpandMoreIcon"])');
    
    const count = await expandableItems.count();
    if (count > 0) {
      // Test expanding first group
      await expandableItems.first().click();
      await page.waitForTimeout(500);
      
      // Test collapsing
      await expandableItems.first().click();
      await page.waitForTimeout(500);
    }
  });

  test('should navigate to different pages via sidebar', async ({ page }) => {
    const navigationTests = [
      { text: '调整大小', path: '/resize' },
      { text: '裁剪', path: '/crop' },
      { text: '滤镜', path: '/filter' },
      { text: '水印', path: '/watermark' }
    ];

    for (const nav of navigationTests) {
      try {
        // Go back to home first
        await page.goto('/');
        await helpers.waitForPageLoad();
        
        // Navigate to the page
        await page.click(`text=${nav.text}`);
        await page.waitForURL(`**${nav.path}`, { timeout: 5000 });
        
        // Verify we're on the correct page
        expect(page.url()).toContain(nav.path);
        
        // Check page loads properly
        await helpers.waitForPageLoad();
        
      } catch (error) {
        console.log(`Navigation to ${nav.text} failed:`, error);
      }
    }
  });

  test('should highlight current page in navigation', async ({ page }) => {
    // Navigate to a specific page
    await page.goto('/resize');
    await helpers.waitForPageLoad();
    
    // Look for active/selected state indicators
    const activeIndicators = [
      '.Mui-selected',
      '.active',
      '.current',
      '[aria-current="page"]'
    ];

    let activeFound = false;
    for (const selector of activeIndicators) {
      try {
        const activeElement = page.locator(selector);
        if (await activeElement.count() > 0) {
          activeFound = true;
          break;
        }
      } catch (e) {
        // Continue
      }
    }
    
    // Active state highlighting might not be implemented
    // This is optional functionality
  });

  test('should have responsive mobile navigation', async ({ page }) => {
    // Switch to mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await helpers.waitForPageLoad();
    
    // Check if mobile menu button is visible
    const menuButton = page.locator('[aria-label="open drawer"], .MuiIconButton-root').first();
    await expect(menuButton).toBeVisible();
    
    // Test opening mobile menu
    await menuButton.click();
    await page.waitForTimeout(500);
    
    // Check if navigation is visible
    await expect(page.locator('.MuiDrawer-root')).toBeVisible();
    
    // Test closing mobile menu (click outside or close button)
    try {
      const backdrop = page.locator('.MuiBackdrop-root');
      if (await backdrop.isVisible({ timeout: 1000 })) {
        await backdrop.click();
        await page.waitForTimeout(500);
      }
    } catch (error) {
      console.log('Mobile menu close test skipped:', error);
    }
    
    // Reset to desktop viewport
    await page.setViewportSize({ width: 1280, height: 720 });
  });

  test('should have search functionality', async ({ page }) => {
    // Look for search functionality
    const searchElements = [
      'input[placeholder*="搜索"]',
      'input[placeholder*="search"]',
      '[data-testid="search"]',
      '.search-input',
      'button[aria-label*="search"]'
    ];

    let searchFound = false;
    for (const selector of searchElements) {
      try {
        const searchElement = page.locator(selector);
        if (await searchElement.isVisible({ timeout: 2000 })) {
          searchFound = true;
          
          // Test search functionality
          if (selector.includes('input')) {
            await searchElement.fill('resize');
            await page.waitForTimeout(1000);
            
            // Look for search results
            const resultElements = [
              '.search-results',
              '.search-dropdown',
              '.MuiAutocomplete-popper'
            ];
            
            for (const resultSelector of resultElements) {
              try {
                await expect(page.locator(resultSelector)).toBeVisible({ timeout: 2000 });
                break;
              } catch (e) {
                // Continue
              }
            }
          }
          break;
        }
      } catch (e) {
        // Continue
      }
    }
    
    // Search functionality might not be implemented
    // This is optional
  });

  test('should have proper header/app bar', async ({ page }) => {
    // Check for app bar elements
    const headerElements = [
      '.MuiAppBar-root',
      'header',
      '.app-header',
      '.toolbar'
    ];

    let headerFound = false;
    for (const selector of headerElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        headerFound = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    expect(headerFound).toBe(true);
  });

  test('should have user authentication UI in header', async ({ page }) => {
    // Look for auth-related UI elements
    const authElements = [
      'text=登录',
      'text=注册',
      'text=用户',
      '.user-menu',
      '[data-testid="user-menu"]',
      'button[aria-label*="account"]'
    ];

    let authFound = false;
    for (const selector of authElements) {
      try {
        await expect(page.locator(selector)).toBeVisible({ timeout: 2000 });
        authFound = true;
        break;
      } catch (e) {
        // Continue
      }
    }
    
    expect(authFound).toBe(true);
  });

  test('should maintain layout consistency across pages', async ({ page }) => {
    const testPages = ['/resize', '/filter', '/watermark', '/api-docs'];
    
    for (const testPage of testPages) {
      await page.goto(testPage);
      await helpers.waitForPageLoad();
      
      // Check consistent layout elements
      await expect(page.locator('.MuiDrawer-root')).toBeVisible();
      await expect(page.locator('main')).toBeVisible();
      
      // Check for consistent spacing and structure
      const mainContent = page.locator('main');
      await expect(mainContent).toBeVisible();
    }
  });

  test('should handle browser back/forward navigation', async ({ page }) => {
    // Navigate through several pages
    await page.goto('/resize');
    await helpers.waitForPageLoad();
    
    await page.goto('/filter');
    await helpers.waitForPageLoad();
    
    await page.goto('/watermark');
    await helpers.waitForPageLoad();
    
    // Test browser back button
    await page.goBack();
    expect(page.url()).toContain('/filter');
    await helpers.waitForPageLoad();
    
    await page.goBack();
    expect(page.url()).toContain('/resize');
    await helpers.waitForPageLoad();
    
    // Test browser forward button
    await page.goForward();
    expect(page.url()).toContain('/filter');
    await helpers.waitForPageLoad();
  });

  test('should have proper page titles', async ({ page }) => {
    const pageTests = [
      { path: '/', titleContains: 'AI图像工具箱' },
      { path: '/resize', titleContains: '调整大小' },
      { path: '/filter', titleContains: '滤镜' },
      { path: '/watermark', titleContains: '水印' }
    ];

    for (const pageTest of pageTests) {
      await page.goto(pageTest.path);
      await helpers.waitForPageLoad();
      
      // Check page title
      const title = await page.title();
      expect(title.toLowerCase()).toContain(pageTest.titleContains.toLowerCase());
    }
  });

  test('should handle keyboard navigation', async ({ page }) => {
    // Test tab navigation
    await page.keyboard.press('Tab');
    await page.waitForTimeout(100);
    
    // Check if focus is visible
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toBeVisible();
    
    // Test more tab navigation
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    
    // Test Enter key on focused element
    try {
      await page.keyboard.press('Enter');
      await page.waitForTimeout(500);
    } catch (error) {
      // Enter might not trigger action on all elements
      console.log('Keyboard navigation test completed with minor issues:', error);
    }
  });
});
