const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
 // desktop round with the real CSV (68 live)
 let p=await b.newPage({viewport:{width:1280,height:900}});p.on('pageerror',e=>errs.push(String(e)));
 await p.route(/supabase\.co/,r=>r.abort());
 await p.goto('http://localhost:8767/');await p.waitForTimeout(1500);
 console.log('bank:',await p.evaluate(()=>document.getElementById('bankNote').textContent));
 await p.screenshot({path:'sim/n_intro.png'});
 await p.fill('#name','Kishan');await p.click('#go');await p.waitForTimeout(300);
 await p.screenshot({path:'sim/n_case.png',fullPage:true});
 const j=await p.evaluate(()=>S.perm.indexOf(CASES[S.cur].ans));await p.click('#opt'+((j+1)%4));await p.waitForTimeout(500);
 await p.screenshot({path:'sim/n_answer.png',fullPage:true});
 const lawCount=await p.evaluate(()=>document.querySelectorAll('.law blockquote').length);console.log('law blocks on first answer',lawCount);
 for(let i=1;i<10;i++){await p.click('#next');const k=await p.evaluate(()=>S.perm.indexOf(CASES[S.cur].ans));await p.click('#opt'+k);}
 await p.click('#next');await p.waitForTimeout(300);await p.screenshot({path:'sim/n_end.png',fullPage:true});
 await p.close();
 // all 175 live: check every case renders its law block
 p=await b.newPage({viewport:{width:1280,height:900}});p.on('pageerror',e=>errs.push(String(e)));
 await p.route(/supabase\.co/,r=>r.abort());
 await p.route('**/questions.csv',r=>r.fulfill({path:'srv3/all.csv',contentType:'text/csv'}));
 await p.goto('http://localhost:8767/');await p.waitForTimeout(1500);
 const stats=await p.evaluate(()=>({n:CASES.length,withLaw:CASES.filter(c=>c.law&&c.law.length).length,two:CASES.filter(c=>c.law&&c.law.length>1).length,noLaw:CASES.filter(c=>!c.law||!c.law.length).map(c=>c.ref)}));
 console.log('all-live bank',JSON.stringify(stats));
 await p.close();
 // phone
 p=await b.newPage({viewport:{width:390,height:844}});p.on('pageerror',e=>errs.push(String(e)));
 await p.route(/supabase\.co/,r=>r.abort());
 await p.goto('http://localhost:8767/');await p.waitForTimeout(1200);await p.fill('#name','Phone');await p.click('#go');
 const jj=await p.evaluate(()=>S.perm.indexOf(CASES[S.cur].ans));await p.click('#opt'+jj);await p.waitForTimeout(400);
 console.log('phone scrollWidth',await p.evaluate(()=>document.documentElement.scrollWidth));
 await p.screenshot({path:'sim/n_phone.png',fullPage:true});
 console.log('errors',errs);await b.close();})();
