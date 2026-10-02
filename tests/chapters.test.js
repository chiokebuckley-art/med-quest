import test from 'node:test';import assert from 'node:assert/strict';
import {start,dispatch,observed,journalValid} from '../src/game/learnEngine.js';
import {chapters} from '../src/game/chapters.js';import {load} from '../src/game/state.js';
const flows={
 S3:['Muscle','Rest and ask an adult',[0,1,2,3],'wait',50,'snap'],
 S4:['Inside vessels','A steady pad','wait',75,'wait','snap'],
 S5:['Heart','A connected outward and return loop','Heart','snap',['Pulse 1','Pulse 2','Pulse 3'],['Enjoy active play','Get enough sleep']],
 S7:['Mouth','Stomach',['Mouth','Esophagus','Stomach','Intestines'],'Pipe bend',['Guide 1','Guide 2','Guide 3'],['Drink water when thirsty','Tell an adult about pain']],
 S8:['Kidneys','Useful oxygen and nutrients','sort','Drink water',['Kidneys','Ureters','Bladder']],
 S9:['Brain','Stop play and tell an adult','Quiet space','I bumped my head and do not feel right','wait','Nerves'],
 S10:['White blood cells','Wash hands',[0,1,2,3,4],'snap',['Zone 1','Zone 2','Zone 3'],['Get enough sleep','Enjoy varied food']],
 E1:['Serious trouble breathing','Stay safe and get adult / emergency help',['Tell a trusted adult','Describe the problem and location','Get urgent emergency help'],'It helps me practice asking for help'],
 E2:['Dizzy after a head bump','Stop play and tell a trusted adult',['Tell a trusted adult','Describe the problem and location','Get professional advice; keep play paused'],'It helps me practice asking for help'],
 E3:['An accident near a busy road','Stay safe and get adult / emergency help',['Tell a trusted adult','Describe the problem and location','Call local emergency services when urgent'],'It helps me practice asking for help']
};
for(const [id,flow] of Object.entries(flows))test(`${id} completes its own curriculum, blocks skipping, and requires observation before journaling`,()=>{
 const s=start(id);assert.equal(journalValid(s,['science','adult help']),false);
 const act=(value,extra={},now=10000)=>dispatch(s,{type:'chapter',step:s.step,value,...extra},now);
 assert.ok(dispatch(s,{type:'chapter',step:flow.length-1,value:'skip'}).tip);assert.equal(s.step,0);
 for(let step=0;step<flow.length;step++){
  const def=chapters[id].steps[step],value=flow[step];assert.equal(s.step,step);
  if(def.tool){assert.ok(act(value).tip,'Tool-less action must not advance');s.tool=def.tool;}
  if(value==='wait'){assert.ok(act('finish').tip);act('start',{},10000);assert.ok(act('finish',{},10000+def.duration-1).tip);act('finish',{},10000+def.duration);}
  else if(value==='snap'){assert.ok(act('snap',{distance:def.tolerance+1}).tip);act('snap',{distance:def.tolerance});}
  else if(value==='sort'){assert.ok(act('keep').tip);for(let i=0;i<4;i++){act('select',{item:i});const correct=i%2===0?'waste':'keep';assert.ok(act(correct==='keep'?'waste':'keep').tip);act(correct);}}
  else if(Array.isArray(value)){
   if(def.kind==='sequence'){assert.ok(act(value[value.length-1]).tip);}
   if(def.kind==='cards'){assert.ok(act('Skip sleep').tip);}
   for(let i=0;i<value.length;i++){act(value[i]);if(i===0&&def.kind==='coverage'){const count=s.hits.length;act(value[i]);assert.equal(s.hits.length,count,'Duplicate zone cannot add progress');}}
  }else {assert.ok(act('incorrect').tip);act(value);}
  assert.equal(s.step,step+1);
 }
 assert.ok(observed(s));assert.ok(journalValid(s,['body science','get a trusted adult and professional help']));
 if(id==='S9'||id.startsWith('E'))assert.equal(journalValid(s,['science','keep playing alone']),false);
});
test('All ten Learn and three Emergency completions survive loading; arbitrary IDs are excluded',()=>{
 const completed=[...Object.keys(flows),'S1','S2','S6','S11','bad'];const state=load({getItem:()=>JSON.stringify({completed})});assert.equal(state.completed.length,13);assert.ok(state.completed.includes('S10'));assert.ok(state.completed.includes('E3'));assert.ok(!state.completed.includes('S11'));
});
