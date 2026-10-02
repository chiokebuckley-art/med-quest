import {anatomyScenes,anatomyImage,anatomyMotion} from './livingAnatomy.js';
import {layers,mountLab} from './freeLab.js';

// The part list drives both the illustration and its explanation.
export function layerScene(layer,index){
 const [name,,system]=layers[layer][index];
 const id=layer==='Pipes'?'S4':system;
 const focus={Tendons:'270 150 200 245',Joints:'385 80 250 300',Stomach:'260 90 240 230',Intestines:'230 185 260 225',Brain:'110 10 250 230',Nerves:'170 190 510 240'}[name]||'0 0 700 430';
 return {id,name,focus,reverse:name==='Veins'};
}
export function layerExhibit(){return `<section class="layer-exhibit" aria-label="Animated anatomy layer"><div class="layer-view-switch" role="group" aria-label="Anatomy presentation"><button data-exhibit-mode="detail" aria-pressed="true">Animated detail</button><button data-exhibit-mode="body" aria-pressed="false">3D body</button></div><div class="layer-display"></div><div class="layer-animation-controls living-controls"><button data-layer-pause>Pause animation</button><button data-layer-slow aria-pressed="false">Slow motion</button><button data-layer-wide aria-pressed="false">See surrounding anatomy</button></div><p class="layer-motion-description" aria-live="polite"></p><p class="living-caption">Detailed anatomy illustrations with animated teaching overlays. Flow, signals, and tissue motion are enlarged for visibility.</p></section>`}
export function mountLayerExhibit(host,layer,onPart){
 let selected=0,mode='detail',wide=false,paused=matchMedia('(prefers-reduced-motion: reduce)').matches,slow=false,stopBody=()=>{};
 const display=host.querySelector('.layer-display');
 const sync=()=>{
  for(const a of display.getAnimations({subtree:true})){a.playbackRate=slow?.35:1;paused?a.pause():a.play()}
  host.querySelector('[data-layer-pause]').textContent=paused?'Play animation':'Pause animation';
  host.querySelector('[data-layer-pause]').setAttribute('aria-pressed',String(paused));
  host.querySelector('[data-layer-slow]').setAttribute('aria-pressed',String(slow));
  host.querySelector('[data-layer-wide]').setAttribute('aria-pressed',String(wide));
  host.dataset.animationState=paused?'paused':'playing';host.dataset.speed=slow?'slow':'normal';
 };
 const draw=()=>{
  stopBody();stopBody=()=>{};
  const s=layerScene(layer,selected),scene=anatomyScenes[s.id];
  host.dataset.selectedPart=s.name;host.dataset.mode=mode;
  host.querySelectorAll('[data-exhibit-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.exhibitMode===mode)));
  host.querySelector('.layer-animation-controls').hidden=mode==='body';
  host.querySelector('.living-caption').hidden=mode==='body';
  host.querySelector('.layer-motion-description').textContent=mode==='body'?'Drag to turn the body. Use the controls to watch movement and circulation.':layer==='Pipes'?`${s.name}: ${s.reverse?'blood returns toward the heart':'blood travels away from the heart'}. Watch red blood cells move through the vessel.`:scene.motion;
  if(mode==='body'){
   display.innerHTML=`<div id="anatomy-3d"><span class="exhibit-label">${layer.toUpperCase()} / INTERACTIVE 3D EXHIBIT</span></div>`;
   stopBody=mountLab(display.firstElementChild,layer,onPart);return;
  }
  // Namespace SVG clips: the upper laboratory may show the same organ.
  const motion=anatomyMotion(s.id).replaceAll('-tissue-clip','-layer-tissue-clip');
  display.innerHTML=`<div class="living-view layer-detail ${s.reverse?'layer-return-flow':''}"><svg viewBox="${wide?'0 0 700 430':s.focus}" role="img" aria-label="${s.name}, animated detailed anatomy"><title>${s.name}</title>${anatomyImage(s.id)}<g class="motion-overlay">${motion}</g></svg><span class="living-view-label">${s.name.toUpperCase()} · ANIMATED DETAIL</span></div>`;
  host.querySelector('[data-layer-wide]').disabled=s.focus==='0 0 700 430';sync();
 };
 const click=e=>{const b=e.target.closest('button');if(!b)return;
  if(b.dataset.exhibitMode){mode=b.dataset.exhibitMode;draw()}
  else if(b.hasAttribute('data-layer-pause')){paused=!paused;sync()}
  else if(b.hasAttribute('data-layer-slow')){slow=!slow;sync()}
  else if(b.hasAttribute('data-layer-wide')){wide=!wide;draw()}
 };
 host.addEventListener('click',click);draw();
 return {select(index){if(index===selected)return;selected=index;wide=false;if(mode==='detail')draw()},dispose(){stopBody();host.removeEventListener('click',click);for(const a of display.getAnimations({subtree:true}))a.cancel()}};
}
