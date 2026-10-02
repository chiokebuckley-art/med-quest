import test from 'node:test';
import assert from 'node:assert/strict';
import {existsSync} from 'node:fs';
import {board} from '../src/game/boards.js';
import {anatomyScenes,anatomyImage,anatomyMotion} from '../src/game/livingAnatomy.js';
import {chapters} from '../src/game/chapters.js';

test('Every mission stage and living system references shipped anatomy assets',()=>{
 for(const id of Object.keys(anatomyScenes)){
  const stages=chapters[id]?.steps.length??8;
  for(let step=0;step<=stages;step++){
   const markup=board({id,step,hits:[],sorted:[],chosen:[],dots:0,xray:true});
   assert.ok(markup.includes('<image'),`${id} stage ${step} has detailed artwork`);
   assert.ok(!/undefined|NaN/.test(markup),`${id} stage ${step} is complete`);
   for(const [,href] of markup.matchAll(/href="([^\"]+)"/g))assert.ok(existsSync(new URL('../public'+href,import.meta.url)),`${id}: ${href}`);
  }
  assert.ok(anatomyMotion(id).includes('anatomy-motion'),`${id} has a visible process`);
  for(const [,href] of (anatomyImage(id)+anatomyMotion(id)).matchAll(/href="([^\"]+)"/g))assert.ok(existsSync(new URL('../public'+href,import.meta.url)),href);
 }
});

test('Defense practice uses the human hand for washing and cells for the immune sequence',()=>{
 assert.match(board({id:'S10',step:2,hits:[]}),/MQ_S1_realistic_arm/);
 assert.match(board({id:'S10',step:4,hits:[]}),/MQ_R17_museum/);
 const [x,y]=chapters.S10.steps[3].target;
 assert.ok(x>=440&&x<=610&&y>=160&&y<=235,'patch target stays on the human hand');
});
