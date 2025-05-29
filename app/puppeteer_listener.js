const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // 监听WebSocket事件
  page.on('websocket', (ws) => {
    ws.on('framesent', (event) => {
      console.log('发送消息:', event.payload);
    });
    ws.on('framereceived', (event) => {
      console.log('收到消息:', event.payload);
    });
  });

  await page.goto('https://www.websocket.org/echo.html');
  await page.waitForTimeout(5000);  // 等待消息
  await browser.close();
})();