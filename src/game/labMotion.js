import * as THREE from 'three';

// The exhibit uses one shared shoulder/elbow motion for surface and inner layers.
// Coordinates are in the exported human's metre-scale frame, before display rotation.
export const ELBOW = new THREE.Vector3(.275, 1.102, 0);
export const SHOULDER = new THREE.Vector3(.19, 1.395, -.004);
const smooth=(a,b,x)=>{const t=THREE.MathUtils.clamp((x-a)/(b-a),0,1);return t*t*(3-2*t)};
function rotateX(p,pivot,angle,out){const y=p.y-pivot.y,z=p.z-pivot.z,c=Math.cos(angle),s=Math.sin(angle);return out.set(p.x,pivot.y+y*c-z*s,pivot.z+y*s+z*c)}
export function armPose(point,bend,out=new THREE.Vector3(),rig=null){
 const originalX=point.x,originalY=point.y,originalZ=point.z;
 const armEdge=.145+.145*(1-smooth(.92,1.38,point.y));
 const weight=rig?rig.x:smooth(armEdge,armEdge+.03,point.x)*smooth(.50,.61,point.y)*(1-smooth(1.39,1.46,point.y));
 const forearm=rig?rig.y:1-smooth(1.07,1.14,point.y);
 const moved=rotateX(point,ELBOW,-bend*1.2*forearm,out);
 rotateX(moved,SHOULDER,-bend*.12,moved);
 return moved.set(originalX+(moved.x-originalX)*weight,originalY+(moved.y-originalY)*weight,originalZ+(moved.z-originalZ)*weight);
}
export function motionAt(seconds,mode){return mode==='hold'?1:mode==='bend'?(1-Math.cos(seconds*Math.PI/4))*.5:0}
export function heartPulse(seconds){const phase=(seconds*1.1)%1;return Math.exp(-Math.pow((phase-.14)/.075,2))*.034+Math.exp(-Math.pow((phase-.34)/.09,2))*.014}

const poseShader=`
uniform mat4 mqLocalToBody;
uniform mat4 mqBodyToLocal;
uniform float mqBend;
uniform float mqUseRig;
attribute vec3 mqRig;
vec3 mqRotate(vec3 p,vec3 pivot,float a){float c=cos(a),s=sin(a);vec3 d=p-pivot;return pivot+vec3(d.x,d.y*c-d.z*s,d.y*s+d.z*c);}
float mqWeight(vec3 p){if(mqUseRig>.5)return mqRig.x;float edge=.145+.145*(1.-smoothstep(.92,1.38,p.y));return smoothstep(edge,edge+.03,p.x)*smoothstep(.50,.61,p.y)*(1.-smoothstep(1.39,1.46,p.y));}
vec3 mqPose(vec3 p){float f=mqUseRig>.5?mqRig.y:1.-smoothstep(1.07,1.14,p.y);vec3 q=mqRotate(p,vec3(.275,1.102,0.),-mqBend*1.2*f);q=mqRotate(q,vec3(.19,1.395,-.004),-mqBend*.12);return mix(p,q,mqWeight(p));}
`;
export function installArmMotion(mesh,body,bendUniform){
 const toBody=new THREE.Matrix4().copy(body.matrixWorld).invert().multiply(mesh.matrixWorld);
 const toLocal=toBody.clone().invert();
 const rig=mesh.geometry.attributes._mq_arm_weights;if(rig)mesh.geometry.setAttribute('mqRig',rig);mesh.material.defaultAttributeValues={mqRig:[0,0,0]};
 const patch=shader=>{Object.assign(shader.uniforms,{mqLocalToBody:{value:toBody},mqBodyToLocal:{value:toLocal},mqBend:bendUniform,mqUseRig:{value:rig?1:0}});shader.vertexShader=poseShader+shader.vertexShader;
 shader.vertexShader=shader.vertexShader.replace('#include <beginnormal_vertex>', '#include <beginnormal_vertex>\nvec3 mqP=(mqLocalToBody*vec4(position,1.)).xyz;vec3 mqN=mat3(mqLocalToBody)*objectNormal;float mqF=mqUseRig>.5?mqRig.y:1.-smoothstep(1.07,1.14,mqP.y);vec3 mqRotN=mqRotate(mqRotate(mqN,vec3(0.),-mqBend*1.2*mqF),vec3(0.),-mqBend*.12);objectNormal=mat3(mqBodyToLocal)*normalize(mix(mqN,mqRotN,mqWeight(mqP)));');
 shader.vertexShader=shader.vertexShader.replace('#include <displacementmap_vertex>','#include <displacementmap_vertex>\ntransformed=(mqBodyToLocal*vec4(mqPose((mqLocalToBody*vec4(transformed,1.)).xyz),1.)).xyz;');
 };
 mesh.material.onBeforeCompile=patch;mesh.material.customProgramCacheKey=()=> 'mq-arm-motion-v1';
 mesh.customDepthMaterial=new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking});mesh.customDepthMaterial.defaultAttributeValues={mqRig:[0,0,0]};mesh.customDepthMaterial.onBeforeCompile=patch;
 // GPU motion also needs accurate click picking. Bake a temporary pose only at click time.
 const originalRaycast=mesh.raycast;
 mesh.raycast=function(raycaster,hits){
  if(bendUniform.value<.001)return originalRaycast.call(this,raycaster,hits);
  const original=this.geometry,temp=original.clone(),source=original.attributes.position;
  const position=new THREE.BufferAttribute(new Float32Array(source.count*3),3),p=new THREE.Vector3();
  for(let i=0;i<source.count;i++){this.getVertexPosition(i,p);p.applyMatrix4(toBody);armPose(p,bendUniform.value,p,rig?{x:rig.getX(i),y:rig.getY(i)}:null);p.applyMatrix4(toLocal);position.setXYZ(i,p.x,p.y,p.z)}
  temp.setAttribute('position',position);temp.morphAttributes={};temp.computeBoundingBox();temp.computeBoundingSphere();this.geometry=temp;
  try{originalRaycast.call(this,raycaster,hits)}finally{this.geometry=original;temp.dispose()}
 };
 return ()=>mesh.customDepthMaterial.dispose();
}

// Closed loops connect systemic outflow, body return, pulmonary outflow and lung return.
// Cells are red at both oxygen levels; blue is only a vessel diagram convention.
const heart=[.05,1.25,.078],returnHeart=[-.006,1.26,.074];
const lungLoop=[returnHeart,[-.052,1.31,.057],[-.095,1.34,.026],[-.074,1.28,.05],heart];
const routes=[];
for(const sign of [-1,1]){
 routes.push({name:`${sign<0?'Left':'Right'} leg`,body:[heart,[.025*sign,1.34,.042],[.024*sign,.94,.038],[.092*sign,.77,.034],[.106*sign,.48,.036],[.103*sign,.18,.019],[.115*sign,.18,.019],[.118*sign,.48,.036],[.104*sign,.77,.034],[.036*sign,.94,.038],[.03*sign,1.15,.047],returnHeart]});
 routes.push({name:`${sign<0?'Left':'Right'} arm`,body:[heart,[.02*sign,1.37,.045],[.177*sign,1.415,.04],[.246*sign,1.26,.035],[.3*sign,1.075,.027],[.35*sign,.85,.024],[.37*sign,.758,.017],[.382*sign,.758,.017],[.362*sign,.85,.024],[.312*sign,1.075,.027],[.258*sign,1.26,.035],[.189*sign,1.415,.04],returnHeart]});
}
routes.push({name:'Head',body:[heart,[.016,1.36,.042],[.028,1.522,.018],[.037,1.608,.025],[-.037,1.608,.025],[-.028,1.522,.018],[-.016,1.36,.042],returnHeart]});
export function circulationRoutes(){return routes.map((route,index)=>({...route,curve:new THREE.CatmullRomCurve3([...route.body,...lungLoop.slice(1,-1).map(([x,y,z])=>[index%2===0?x:-x,y,z])].map(p=>new THREE.Vector3(...p)),true,'centripetal')}))}
export function createCirculation(){
 const group=new THREE.Group();group.name='Visible closed circulation';const paths=circulationRoutes(),vessels=[],disposables=[];
 for(const {curve,body} of paths){
  const total=body.length+lungLoop.length-2;const cuts=[0,(body.length/2)/total,(body.length-1)/total,(body.length+1)/total,1];
  for(let j=0;j<4;j++){const section=new THREE.Curve();section.getPoint=(t,target=new THREE.Vector3())=>target.copy(curve.getPoint(cuts[j]+t*(cuts[j+1]-cuts[j])));
   const part=j%2===0?'Arteries':'Veins';const geometry=new THREE.TubeGeometry(section,90,.0065,10,false),material=new THREE.MeshStandardMaterial({color:part==='Arteries'?0xd87566:0x5a99b0,transparent:true,opacity:.25,roughness:.3,depthWrite:false,side:THREE.DoubleSide});const mesh=new THREE.Mesh(geometry,material);mesh.userData={layer:'Pipes',part};group.add(mesh);vessels.push(mesh);disposables.push(geometry,material)
  }
 }
 const cellGeometry=new THREE.LatheGeometry([new THREE.Vector2(0,.00065),new THREE.Vector2(.0025,.00075),new THREE.Vector2(.0046,.00165),new THREE.Vector2(.0055,0),new THREE.Vector2(.0046,-.00165),new THREE.Vector2(.0025,-.00075),new THREE.Vector2(0,-.00065)],12);
 const material=new THREE.MeshStandardMaterial({color:0xe04736,roughness:.48});const count=paths.length*32,cells=new THREE.InstancedMesh(cellGeometry,material,count);cells.instanceMatrix.setUsage(THREE.DynamicDrawUsage);cells.frustumCulled=false;group.add(cells);disposables.push(cellGeometry,material);
 const dummy=new THREE.Object3D(),tangent=new THREE.Vector3(),normal=new THREE.Vector3(0,1,0),dark=new THREE.Color('#8b2429'),bright=new THREE.Color('#e34a36');
 function update(seconds,bend=0,speed=1){let index=0;for(const {curve,body} of paths){const length=curve.getLength();for(let i=0;i<32;i++){
   const phase=(i/32+seconds*.11*speed/length)%1;const point=curve.getPointAt(phase);armPose(point,bend,dummy.position);tangent.copy(curve.getTangentAt(phase));dummy.quaternion.setFromUnitVectors(normal,tangent);dummy.rotateY(i*.47);dummy.rotateX(.85+Math.sin(seconds*1.2+i)*.45);dummy.rotateZ(i*.37);dummy.updateMatrix();cells.setMatrixAt(index,dummy.matrix);
   // Position follows the full loop; oxygen level is illustrative, never a measurement.
   const parameter=curve.getUtoTmapping(phase);const total=body.length+lungLoop.length-2;const returning=parameter>(body.length/2)/total&&parameter<(body.length+1)/total;cells.setColorAt(index,returning?dark:bright);index++
 }}cells.instanceMatrix.needsUpdate=true;cells.instanceColor.needsUpdate=true}
 update(0);
 return {group,vessels,cellCount:count,update,dispose:()=>disposables.forEach(d=>d.dispose())};
}
