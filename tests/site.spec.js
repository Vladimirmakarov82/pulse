const { test, expect } = require('@playwright/test');

const BASE = 'https://vladimirmakarov82.github.io/pulse';

// ── ГЛАВНАЯ СТРАНИЦА ──────────────────────────────────────────
test('Главная: открывается', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Pulse/);
});

test('Главная: PULSE hero виден', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('#pulse-hero h1')).toBeVisible();
  await expect(page.locator('#pulse-hero h1')).toHaveText('PULSE');
});

test('Главная: стрелка появляется через 1.5s', async ({ page }) => {
  await page.goto('/');
  await page.waitForTimeout(1500);
  await expect(page.locator('#pulse-arrow')).toHaveCSS('opacity', '1');
});

test('Главная: скролл открывает основной контент', async ({ page }) => {
  await page.goto('/');
  await page.waitForTimeout(1000);
  await page.mouse.wheel(0, 300);
  await page.waitForTimeout(1200);
  // Hero должен исчезнуть
  const heroClass = await page.locator('#pulse-hero').getAttribute('class');
  expect(heroClass).toContain('gone');
  // Основной контент виден
  await expect(page.locator('#cta-section')).toBeVisible();
});

test('Главная: кнопка Получить инвайт открывает модал', async ({ page }) => {
  await page.goto('/');
  await page.waitForTimeout(1000);
  await page.mouse.wheel(0, 300);
  await page.waitForTimeout(1200);
  await page.locator('button:has-text("Получить инвайт")').first().click();
  await expect(page.locator('#invite-modal')).toHaveCSS('display', 'flex');
});

test('Главная: крестик инвайт-модала закрывает его', async ({ page }) => {
  await page.goto('/');
  await page.waitForTimeout(1000);
  await page.mouse.wheel(0, 300);
  await page.waitForTimeout(1200);
  await page.locator('button:has-text("Получить инвайт")').first().click();
  await expect(page.locator('#invite-modal')).toHaveCSS('display', 'flex');
  await page.locator('#invite-close').click();
  await expect(page.locator('#invite-modal')).not.toHaveCSS('display', 'flex');
});

test('Главная: кнопка Скопировать текст работает', async ({ page }) => {
  await page.goto('/');
  await page.waitForTimeout(1000);
  await page.mouse.wheel(0, 300);
  await page.waitForTimeout(1200);
  await page.locator('button:has-text("Получить инвайт")').first().click();
  const copyBtn = page.locator('#copy-btn');
  await expect(copyBtn).toBeVisible();
  await copyBtn.click();
  // Кнопка должна показать "Скопировано"
  await expect(copyBtn).toContainText('Скопировано');
});

test('Главная: кнопка Основателям комьюнити открывает overlay', async ({ page }) => {
  await page.goto('/');
  await page.waitForTimeout(1000);
  await page.mouse.wheel(0, 300);
  await page.waitForTimeout(1200);
  await page.locator('button:has-text("Основателям комьюнити")').click();
  // Founders iframe должен появиться
  await expect(page.locator('iframe[src*="founders"]')).toBeVisible();
});

test('Главная: переключение RU/EN работает', async ({ page }) => {
  await page.goto('/');
  await page.waitForTimeout(1000);
  await page.mouse.wheel(0, 300);
  await page.waitForTimeout(1200);
  // Переключаем на EN
  await page.locator('button:has-text("EN")').click();
  await expect(page.locator('#cta-section')).toContainText('Build your universal profile');
  // Обратно на RU
  await page.locator('button:has-text("RU")').click();
  await expect(page.locator('#cta-section')).toContainText('Создай свой');
});

test('Главная: секция Кто внутри содержит 270+', async ({ page }) => {
  await page.goto('/');
  await page.waitForTimeout(1000);
  await page.mouse.wheel(0, 300);
  await page.waitForTimeout(1200);
  const section = page.locator('section').nth(1);
  await expect(section).toContainText('+');
  await expect(section).toContainText('предпринимателей');
});

// ── FOUNDERS СТРАНИЦА ─────────────────────────────────────────
test('Founders: открывается', async ({ page }) => {
  await page.goto('/founders.html');
  await expect(page).toHaveTitle(/основател/i);
});

test('Founders: кнопка Подать заявку (nav) открывает форму', async ({ page }) => {
  await page.goto('/founders.html');
  await page.locator('.cta-nav').click();
  await expect(page.locator('#apply-overlay')).toHaveCSS('display', 'flex');
});

test('Founders: крестик формы закрывает её', async ({ page }) => {
  await page.goto('/founders.html');
  await page.locator('.cta-nav').click();
  await expect(page.locator('#apply-overlay')).toHaveCSS('display', 'flex');
  await page.locator('#apply-overlay button:has-text("Закрыть")').click();
  await expect(page.locator('#apply-overlay')).toHaveCSS('display', 'none');
});

test('Founders: 2 карточки (Макаров и Козлова)', async ({ page }) => {
  await page.goto('/founders.html');
  const imgs = page.locator('img[alt="Владимир Макаров"], img[alt="Анна Козлова"]');
  await expect(imgs).toHaveCount(2);
});

test('Founders: лого ведёт на главную', async ({ page }) => {
  await page.goto('/founders.html');
  await page.locator('.logo').click();
  await expect(page).toHaveURL(/index\.html|\/pulse\/?$/);
});

test('Founders: НЕТ 3-й карточки', async ({ page }) => {
  await page.goto('/founders.html');
  const allImgs = page.locator('img');
  await expect(allImgs).toHaveCount(2);
});

test('Founders: нет дублирующегося "Для основателей комьюнити"', async ({ page }) => {
  await page.goto('/founders.html');
  const text = await page.locator('body').innerText();
  const count = (text.match(/для основателей комьюнити/gi) || []).length;
  expect(count).toBeLessThanOrEqual(1);
});

// ── APPLY ФОРМА ───────────────────────────────────────────────
test('Apply: форма открывается в iframe', async ({ page }) => {
  await page.goto('/founders.html');
  await page.locator('.cta-nav').click();
  const iframe = page.frameLocator('#apply-iframe');
  await expect(iframe.locator('h1')).toBeVisible();
});

test('Apply: все поля формы видны без скролла', async ({ page }) => {
  await page.goto('/founders.html');
  await page.locator('.cta-nav').click();
  const iframe = page.frameLocator('#apply-iframe');
  await expect(iframe.locator('#club-name')).toBeVisible();
  await expect(iframe.locator('#role')).toBeVisible();
  await expect(iframe.locator('#full-name')).toBeVisible();
  await expect(iframe.locator('#telegram')).toBeVisible();
  await expect(iframe.locator('#submit-btn')).toBeVisible();
});
