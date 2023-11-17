import { Browser, BrowserContext, Page, devices, firefox } from 'playwright';
import { readFileSync, writeFileSync, readdirSync, rm } from 'fs';

rm(__dirname + '/cntx/re50er500/sessionstore-backups', () => {});
rm(__dirname + '/cntx/re50er500/sessionCheckpoints.json', () => {});
rm(__dirname + '/cntx/re50er500/sessionstore.jsonlz4', () => {});

const users: [] = JSON.parse(
  readFileSync(__dirname + '/users.json', { encoding: 'utf8' })
);

describe('CONTX', () => {
  let browser: Browser;
  let context: BrowserContext;
  let page: Page;
  let topUsers: string[] = [];

  beforeAll(async () => {
    context = await firefox.launchPersistentContext(
      __dirname + '/cntx/re50er500',
      { headless: false }
    );
    page = context.pages()[0];
    await page.goto('https://www.tiktok.com/login/phone-or-email/email', {
      waitUntil: 'load',
    });
    await page.waitForSelector(`input`);
    await page.click(`input[placeholder~='Email']`);
    await page.waitForTimeout(500);
    await page.fill(`input[placeholder~='Email']`, 'yungbezo');

    await page.click(`input[type='password']`);
    await page.waitForTimeout(500);
    await page.fill(`input[type='password']`, 'abc123!@#');

    await page.click(`button[type='submit']`);
    await page.waitForSelector(`h3[data-e2e="video-author-uniqueid"]`);
    /* await page.goto('https://www.tiktok.com/following', {
      waitUntil: 'domcontentloaded',
    }); */
  });

  test('GET USERS', async () => {
    //await page.waitForTimeout(30000000);
    const getUsers = new Promise(async (res, rej) => {
      const scrollInt = setInterval(async () => {
        await page.evaluate(() => {
          const h: any = document.querySelector('html')?.scrollHeight;
          document.querySelector('html')?.scroll(0, h - 100);
        });

        topUsers = await page
          .locator(`h3[data-e2e="video-author-uniqueid"]`)
          .allInnerTexts();

        if (topUsers.length > 4) {
          clearInterval(scrollInt);
          topUsers = Array.from(new Set(topUsers));
          res(true);
        }
      }, 1000);
    });
    await getUsers;
    topUsers.length = 4;
    console.log(topUsers);
  });

  test('CHECK VIDS', async () => {
    for (const user of topUsers) {
      let hasComment = false;
      const visit = new Promise(async (res, rej) => {
        await page.goto(`https://www.tiktok.com/@${user}`, {
          waitUntil: 'load',
        });
        await page.click('video');
        const comNumber = await page
          .locator(`strong[data-e2e="browse-comment-count"]`)
          .innerText();
        try {
          await page.waitForSelector(`div[class*="DivCommentItemContainer"]`, {
            timeout: 5000,
          });
        } catch (error) {}
        const coms = await page
          .locator(`div[class*="DivCommentItemContainer"]`)
          .allInnerTexts();
        coms.map(async (c) => {
          if (c.toLowerCase().includes('ihptto')) {
            hasComment = true;
            topUsers = topUsers.filter((u) => {
              return u !== user;
            });
          }
        });
        if (hasComment === false && comNumber !== '0') {
          await context.newPage();
          const cntxL = context.pages().length;
          page = context.pages()[cntxL - 1];
        }
        res(true);
      });
      await visit;
      //await page.goto('https://www.tiktok.com', { waitUntil: 'load' });
    }
  });

  test('COMMENT', async () => {
    const comL = context.pages().length - 1;
    for (let i = 0; i < comL; i++) {
      const comment = new Promise(async (res, rej) => {
        page = context.pages()[i];
        //await page.bringToFront();
        await page.click(`div[class*="DivEmojiButton"]`);
        await page.keyboard.type('I LIKE THAT THING');
        await page.keyboard.press('Enter');
        await page.waitForSelector('text=Comment posted');
        await page.click(`div[data-e2e="comment-like-icon"]`);
        await page.waitForSelector(
          `div[class*="DivCommentItemContainer"] svg[fill="rgba(254, 44, 85, 1.0)"]`
        );
        await page.evaluate(() => {
          document
            .querySelector(`div[class*="DivCommentItemContainer"]`)
            ?.setAttribute('playwright', 'true');
          document.querySelectorAll('video').forEach((v) => {
            v.pause();
            v.remove();
            v.innerHTML = '';
          });
          document
            .querySelectorAll(`div[class*=DivItemContainerV2]`)
            .forEach((v) => {
              v.innerHTML = '';
            });
          document.querySelectorAll(`img`).forEach((img) => {
            img.remove();
          });
        });
        res(true);
      });
      await comment;
    }
    console.log('done commenting');
  });

  test('CHANGE USERS', async () => {
    //FIX ME!!!
    const logIndex = context.pages().length - 1;
    page = context.pages()[logIndex];
    for (const user of users) {
      console.log(user['u']);

      //await page.bringToFront();
      await page.goto('https://www.tiktok.com/logout', {
        waitUntil: 'domcontentloaded',
      });
      await page.goto('https://www.tiktok.com/login/phone-or-email/email', {
        waitUntil: 'load',
      });
      await page.waitForSelector(`input`);
      await page.click(`input[placeholder~='Email']`);
      await page.waitForTimeout(500);
      await page.fill(`input[placeholder~='Email']`, user['u']);

      await page.click(`input[type='password']`);
      await page.waitForTimeout(500);
      await page.fill(`input[type='password']`, user['p']);

      await page.click(`button[type='submit']`);
      try {
        page
          .waitForSelector(`h3[data-e2e="video-author-uniqueid"]`, {
            timeout: 10000,
          })
          .then(() => {
            context.pages().forEach(async (p, i) => {
              if (i !== logIndex) {
                //await p.bringToFront();
                await p.click(
                  `div[playwright="true"] div[data-e2e="comment-like-icon"] svg`
                );
                console.log('liked');
              }
            });
          });
        await page.evaluate(() => {
          document.querySelectorAll('video').forEach((v) => {
            v.pause();
            v.innerHTML = '';
          });
        });
      } catch (error) {
        console.log('error while logging in');
      }
    }
  });

  afterAll(async () => {
    console.log('done');
    await page.waitForTimeout(1033000);
    await page.close();
    await context.close();
    await browser.close();
  });
});
