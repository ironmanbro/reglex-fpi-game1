const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
 const ctx=await b.newContext({viewport:{width:1280,height:900},acceptDownloads:true,permissions:['clipboard-read','clipboard-write']});
 const p=await ctx.newPage();p.on('pageerror',e=>errs.push(String(e)));await p.route(/supabase\.co|fonts\./,r=>r.abort());
 await p.goto('http://localhost:8768/');await p.waitForTimeout(1200);
 console.log('bank:',await p.evaluate(()=>document.getElementById('bankNote').textContent.slice(0,60)));
 await p.fill('#name','Kishan');await p.click('.len[data-n="15"]');await p.click('#go');
 const truth=[];
 for(let i=0;i<15;i++){const st=await p.evaluate(()=>({ans:S.perm.indexOf(CASES[S.cur].ans),ref:CASES[S.cur].ref}));
   const j=i%3===0?(st.ans+1)%4:st.ans;truth.push({ref:st.ref,ok:j===st.ans});await p.click('#opt'+j);
   if(i===0){await p.waitForTimeout(300);console.log('quote blocks after answer 1:',await p.evaluate(()=>document.querySelectorAll('.verdict .law blockquote').length));}
   await p.click('#next');}
 await p.waitForTimeout(400);
 const r=await p.evaluate(()=>({items:document.querySelectorAll('.revitem').length,open:document.querySelectorAll('.revitem details[open]').length,
   refs:[...document.querySelectorAll('.revitem .rmeta')].map(e=>e.textContent.split(' · ').pop()),
   marks:[...document.querySelectorAll('.revitem')].map(e=>e.dataset.ok),ansOpts:document.querySelectorAll('.ro.ans').length,picks:document.querySelectorAll('.ro.pick').length}));
 const wrong=truth.filter(t=>!t.ok).length;
 console.log('review items',r.items,'| open (wrong)',r.open,'expected wrong',wrong,'| correct-option rows',r.ansOpts,'| wrong-pick rows',r.picks);
 console.log('order matches play order:',JSON.stringify(r.refs)===JSON.stringify(truth.map(t=>t.ref)),'| right/wrong match:',r.marks.join('')===truth.map(t=>t.ok?1:0).join(''));
 await p.click('.segb[data-f="wrong"]');console.log('wrong filter visible:',await p.evaluate(()=>[...document.querySelectorAll('.revitem')].filter(e=>!e.hidden).length));
 await p.click('.segb[data-f="all"]');
 await p.click('#copyRev');await p.waitForTimeout(200);const clip=await p.evaluate(()=>navigator.clipboard.readText());
 console.log('clipboard lines',clip.split('\n').length,'| starts:',clip.split('\n')[0]);
 const [dl]=await Promise.all([p.waitForEvent('download'),p.click('#dlRev')]);const path=await dl.path();const csv=require('fs').readFileSync(path,'utf8');
 console.log('csv file',dl.suggestedFilename(),'rows',csv.trim().split('\r\n').length-1);
 await p.screenshot({path:'sim/rev_desk.png',fullPage:true});
 const ph=await ctx.newPage();await ph.setViewportSize({width:390,height:844});ph.on('pageerror',e=>errs.push(String(e)));await ph.route(/supabase\.co|fonts\./,r=>r.abort());
 await ph.goto('http://localhost:8768/');await ph.waitForTimeout(1000);await ph.fill('#name','P');await ph.click('#go');
 for(let i=0;i<10;i++){const a=await ph.evaluate(()=>S.perm.indexOf(CASES[S.cur].ans));await ph.click('#opt'+(i%2?a:(a+1)%4));await ph.click('#next');}
 await ph.waitForTimeout(300);console.log('phone scrollWidth',await ph.evaluate(()=>document.documentElement.scrollWidth));
 await ph.screenshot({path:'sim/rev_phone.png',fullPage:true});
 console.log('errors',errs);await b.close();})();
