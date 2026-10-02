export const DISCLAIMER='Med Quest is a game for learning. Not real medical care. For real injuries, tell a grown-up / get clinical care.';
const KEY='medquest.v1.progress';
export const blank=()=>({completed:[],entries:[],stars:{},lastMode:'Learn',settings:{sound:false,pip:true}});
export function load(storage=globalThis.localStorage){try{const p=JSON.parse(storage.getItem(KEY));if(!p)return blank();return {...blank(),...p,completed:Array.isArray(p.completed)?p.completed.filter(x=>/^(S([1-9]|10)|E[1-3])$/.test(x)):[],entries:Array.isArray(p.entries)?p.entries:[],settings:{...blank().settings,...p.settings}}}catch{return blank()}}
export let progress=load();
export function persist(){try{localStorage.setItem(KEY,JSON.stringify(progress));return true}catch{return false}}
export function record(id,answers,mode,stars=3){const previous=progress;progress={...previous,entries:[...previous.entries,{id,answers,mode,date:new Date().toISOString()}],completed:[...previous.completed],stars:{...previous.stars}};if(['Learn','Emergency'].includes(mode)&&!progress.completed.includes(id))progress.completed.push(id);if(mode==='Arcade')progress.stars[id]=Math.max(progress.stars[id]||0,stars);if(persist())return true;progress=previous;return false}
export const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
