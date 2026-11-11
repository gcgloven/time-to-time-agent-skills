/* Run: npm install --no-save playwright; node tests/reader.spec.cjs
   Uses CHROMIUM_PATH or Playwright's installed browser. No live web requests. */
const {chromium}=require('playwright');
const http=require('node:http'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const screenshotDir=process.env.READER_SCREENSHOTS; if(screenshotDir) fs.mkdirSync(screenshotDir,{recursive:true});
const server=http.createServer((req,res)=>{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  const file=path.resolve(root,pathname.replace(/^\/nested\/course\//,''));
  if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
  fs.readFile(file,(error,body)=>{if(error){res.writeHead(404);res.end();return;}res.setHeader('Content-Type',({'.js':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.html':'text/html'})[path.extname(file)]||'text/plain');res.end(body);});
});
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base=`http://127.0.0.1:${server.address().port}/nested/course/`;
 const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{})});
 const page=await browser.newPage({viewport:{width:1280,height:900},reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',error=>errors.push(error.message));
 async function selected(id){await page.waitForFunction(id=>document.querySelector('#reader').dataset.selected===id,id);}
 async function scrollPane(pane,index){await page.evaluate(({pane,index})=>{const p=document.getElementById(pane),n=p.children[index];p.scrollTop=n.offsetTop;},{pane,index});}
 try{
 await page.goto(base+'index.html');await selected('queue-1');assert(await page.locator('#previous').isDisabled());
 if(screenshotDir) await page.screenshot({path:path.join(screenshotDir,'reader-desktop.png'),fullPage:true});
 await page.waitForFunction(()=>{const img=document.querySelector('#slides img');return img.complete&&img.naturalWidth>0;});
 await scrollPane('slides',1);await selected('queue-2');await page.waitForTimeout(100);assert(await page.locator('#notes').evaluate(p=>Math.abs(p.scrollTop-p.children[1].offsetTop)<3));
 await scrollPane('notes',2);await selected('queue-3');assert(await page.locator('#next').isDisabled());
 await page.locator('#slide-index').selectOption('0');await selected('queue-1');
 await page.locator('#next').click();await selected('queue-2');await page.goBack();await selected('queue-1');await page.goForward();await selected('queue-2');
 await page.reload();await selected('queue-2');
 await page.locator('#slides').focus();await page.keyboard.press('End');await selected('queue-3');await page.keyboard.press('Home');await selected('queue-1');
 for(let i=0;i<8;i++){await page.locator('#slide-index').selectOption(String(i%3));}await selected('queue-2');
 await page.setViewportSize({width:390,height:844});await selected('queue-2');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 if(screenshotDir) await page.screenshot({path:path.join(screenshotDir,'reader-mobile.png'),fullPage:true});
 await scrollPane('slides',2);await selected('queue-3');await scrollPane('notes',0);await selected('queue-1');
 await page.goto(base+'index.html#slide=invalid');await selected('queue-1');
 await page.route('**/media/queue-1.svg',route=>route.abort());await page.reload();await selected('queue-1');await page.waitForFunction(()=>document.querySelector('#slides .media-fallback'));await page.locator('#next').click();await selected('queue-2');await page.unroute('**/media/queue-1.svg');
 await page.route('**/demo-data.json',route=>route.fulfill({status:200,contentType:'application/json',body:'{"slides":[]}'}));await page.reload();await page.locator('#error:not([hidden])').waitFor();assert(await page.locator('#next').isDisabled());await page.unroute('**/demo-data.json');
 await page.route('**/demo-data.json',route=>route.fulfill({status:404,body:'Not found'}));await page.reload();await page.locator('#error:not([hidden])').waitFor();
 assert.deepEqual(errors,[]);console.log('PASS: nested assets; source→notes and notes→source scroll; boundaries; selector; keyboard; Back/Forward; reload; rapid navigation; mobile resize/overflow/scroll; invalid hash; missing image; empty data; fetch failure; no uncaught errors.');
 }finally{await browser.close();server.close();}
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
