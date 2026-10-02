import {extendedSlices,chapters} from './chapters.js';
import * as skin from './slices/slice0.js';import * as bone from './slices/slice1.js';import * as lung from './slices/slice2.js';
export const slices={S1:skin,S2:bone,S6:lung,...extendedSlices};
export const start=id=>({id,step:0,clean:0,swab:0,dots:0,wrap:0,count:0,cards:0,xray:false,tool:'',mistakes:0});
export function dispatch(s,a,now){const before=s.step;const tip=slices[s.id].act(s,a,now);if(tip)s.mistakes++;return {tip,changed:s.step!==before}}
export const observed=s=>s.step===slices[s.id].spec.steps.length-2;
export function journalValid(s,answers){if(!observed(s))return false;if(answers.filter(x=>x.trim().length>=2).length<2)return false;if(chapters[s.id]?.safetyAnswer!==undefined)return /adult|grown.?up|help|clinical|emergency|call|parent|teacher|professional/i.test(answers[chapters[s.id].safetyAnswer]||'');if(s.id==='S6')return /adult|grown.?up|help|clinical|emergency|call|parent|teacher/i.test(answers[1]||'');return true}
