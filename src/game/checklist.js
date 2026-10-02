import {slices} from './learnEngine.js';
export const checklist=s=>slices[s.id].spec.steps.map((v,i)=>`<li class="${i<s.step?'done':i===s.step?'current':''}"><span>${i<s.step?'✓':i+1}</span>${v}</li>`).join('');
