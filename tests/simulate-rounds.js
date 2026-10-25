const { chromium } = require('playwright');
const path = require('path');
const FILE = 'file://' + path.resolve(__dirname, '../desk-league.html');
const plan = [];
const strategies = ['random','random','random','random','random','random','random','random','longest','longest','longest','longest','longest','longest','perfect','perfect','perfect','wrong','wrong','wrong'];
const lens = [10,15,20,25];
strategies.forEach((s,i)=>plan.push({s,len:lens[i%4]}));
(async()=>{
  const browser = await chromium.launch();
  const out = [];
  for (let r=0;r<plan.length;r++){
    const {s,len}=plan[r];
    const page = await browser.newPage({viewport:{width:1280,height:900}});
    const errors=[];
    page.on('pageerror',e=>errors.push(String(e)));
    page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
    await page.route(/fonts\.(googleapis|gstatic)/,r=>r.abort());
    await page.goto(FILE);
    await page.fill('#name','Sim'+r);
    await page.click(`.len[data-n="${len}"]`);
    await page.click('#go');
    const qs=[];
    for(let q=0;q<len;q++){
      const st=await page.evaluate(()=>{const c=CASES[S.cur];return {cur:S.cur,ref:c.ref,ch:c.ch,d:c.d,level:S.level,perm:S.perm.slice(),ans:c.ans,lens:c.opts.map(o=>o.length),
        btnTexts:[...document.querySelectorAll('.opt span')].map(x=>x.textContent)};});
      // display order lengths
      const dispLens=st.perm.map(k=>st.lens[k]);
      const ansPos=st.perm.indexOf(st.ans);
      const longestPos=dispLens.indexOf(Math.max(...dispLens));
      let j;
      if(s==='random')j=Math.floor(Math.random()*4);
      else if(s==='longest')j=longestPos;
      else if(s==='perfect')j=ansPos;
      else j=(ansPos+1)%4;
      await page.click('#opt'+j);
      const chk=await page.evaluate(([j,ansPos])=>{
        const btns=[...document.querySelectorAll('.opt')];
        const rightIdx=btns.findIndex(b=>b.classList.contains('right'));
        const h4=document.querySelector('.verdict h4').textContent;
        const items=document.querySelectorAll('.whynot li').length;
        const mine=document.querySelectorAll('.whynot li.mine').length;
        return {rightIdx,h4,items,mine,score:S.score,level:S.level};
      },[j,ansPos]);
      const ok=j===ansPos;
      const issues=[];
      if(chk.rightIdx!==ansPos)issues.push('right-class mismatch');
      if(!chk.h4.includes('option '+(ansPos+1)))issues.push('heading position wrong: '+chk.h4);
      if(chk.items!==3)issues.push('whynot count '+chk.items);
      if(ok&&chk.mine!==0)issues.push('mine shown on correct');
      if(!ok&&chk.mine!==1)issues.push('mine missing on wrong');
      qs.push({ref:st.ref,ch:st.ch,d:st.d,levelBefore:st.level,levelAfter:chk.level,ok,ansPos,longestPos,ansIsLongest:longestPos===ansPos,issues});
      await page.click('#next');
    }
    const end=await page.evaluate(()=>({screen:S.screen,score:S.score,correct:S.correct,text:document.querySelector('.end')?.innerText.slice(0,300)}));
    if(r===0||r===14){await page.screenshot({path:path.join(__dirname,'end'+r+'.png'),fullPage:true});}
    out.push({r,s,len,qs,end,errors});
    await page.close();
  }
  // one mid-question screenshot on mobile
  const p=await browser.newPage({viewport:{width:390,height:844}});
  await p.route(/fonts\.(googleapis|gstatic)/,r=>r.abort());
  await p.goto(FILE);await p.fill('#name','Phone');await p.click('#go');await p.click('#opt0');
  await p.screenshot({path:path.join(__dirname,'phone.png'),fullPage:true});
  const ow=await p.evaluate(()=>document.documentElement.scrollWidth);
  out.push({phoneScrollWidth:ow});
  await browser.close();
  require('fs').writeFileSync(path.join(__dirname,'results.json'),JSON.stringify(out,null,1));
  console.log('done');
})();
