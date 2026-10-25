const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];const p=await b.newPage({viewport:{width:1280,height:900}});p.on('pageerror',e=>errs.push(String(e)));
 await p.route(/supabase\.co|fonts\./,r=>r.abort());
 await p.goto('http://localhost:8770/');await p.waitForTimeout(1000);await p.fill('#name','T');await p.click('#go');
 const st=()=>p.evaluate(()=>JSON.stringify({score:S.score,correct:S.correct,hist:S.hist.map(h=>[h.k,h.picked]),cur:S.cur,perm:S.perm,picked:S.picked,view:S.view,level:S.level}));
 for(let i=0;i<3;i++){const a=await p.evaluate(()=>S.perm.indexOf(CASES[S.cur].ans));await p.click('#opt'+(i===1?(a+1)%4:a));await p.click('#next');}
 const before=await st();
 console.log('segments clickable:',await p.evaluate(()=>document.querySelectorAll('.progress .seg').length),'| previous link:',!!(await p.$('#toReview')));
 await p.click('.progress .seg[data-i="1"]');
 console.log('locked label:',await p.evaluate(()=>document.querySelector('.lockbar span').textContent));
 console.log('option buttons disabled:',await p.evaluate(()=>[...document.querySelectorAll('.opt')].every(b=>b.disabled)),'| your-answer tag shown:',await p.evaluate(()=>document.querySelectorAll('.yours').length));
 await p.click('.opt >> nth=0',{force:true}).catch(()=>{});for(const k of ['1','2','3','4','Enter'])await p.keyboard.press(k);
 await p.keyboard.press('ArrowLeft');console.log('arrow left ->',await p.evaluate(()=>S.view));await p.keyboard.press('ArrowRight');await p.keyboard.press('ArrowRight');console.log('arrow right x2 ->',await p.evaluate(()=>S.view));
 await p.click('#revBack');
 const after=await st();console.log('state unchanged after review + clicks + keys:',before===after);
 console.log('back on live question, unanswered:',await p.evaluate(()=>S.view===null&&S.picked===null&&document.querySelectorAll('.opt:not(:disabled)').length===4));
 // answer current, then review while verdict open
 const a=await p.evaluate(()=>S.perm.indexOf(CASES[S.cur].ans));await p.click('#opt'+a);
 const mid=await st();await p.click('#toReview');console.log('review from answered state opens q',await p.evaluate(()=>S.view+1),'of reviewable',await p.evaluate(()=>reviewableCount()));
 await p.keyboard.press('Escape');console.log('escape returns with verdict still shown:',await p.evaluate(()=>S.view===null&&!!document.getElementById('next')),'| unchanged:',mid===(await st()));
 await p.click('.progress .seg[data-i="0"]');await p.screenshot({path:'sim/lock_desk.png',fullPage:false});await p.click('#revBack');
 for(let i=0;i<6;i++){await p.click('#next');const x=await p.evaluate(()=>S.perm.indexOf(CASES[S.cur].ans));await p.click('#opt'+x);}
 await p.click('#next');await p.waitForTimeout(300);console.log('round finished, end screen:',await p.evaluate(()=>S.screen),'score',await p.evaluate(()=>S.score+' '+S.correct+'/'+S.hist.length));
 const ph=await b.newPage({viewport:{width:390,height:844}});ph.on('pageerror',e=>errs.push(String(e)));await ph.route(/supabase\.co|fonts\./,r=>r.abort());
 await ph.goto('http://localhost:8770/');await ph.waitForTimeout(800);await ph.fill('#name','P');await ph.click('#go');
 for(let i=0;i<2;i++){const y=await ph.evaluate(()=>S.perm.indexOf(CASES[S.cur].ans));await ph.click('#opt'+y);await ph.click('#next');}
 await ph.click('#toReview');console.log('phone scrollWidth in review:',await ph.evaluate(()=>document.documentElement.scrollWidth));await ph.screenshot({path:'sim/lock_phone.png',fullPage:true});
 console.log('errors',errs);await b.close();})();
