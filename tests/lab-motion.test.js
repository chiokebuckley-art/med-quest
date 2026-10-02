import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import {armPose,ELBOW,SHOULDER,motionAt,circulationRoutes,createCirculation} from '../src/game/labMotion.js';

test('Arm flexes at its elbow while feet and trunk stay grounded across the motion',()=>{
 const hand=new THREE.Vector3(.35,.82,.024),elbow=ELBOW.clone();
 const restingLength=hand.distanceTo(elbow);
 for(const bend of [0,.25,.5,.75,1]){
  const bentElbow=armPose(elbow,bend),bentHand=armPose(hand,bend);
  assert.ok(Math.abs(bentHand.distanceTo(bentElbow)-restingLength)<.002,'Forearm must retain its length');
  for(const point of [new THREE.Vector3(.1,.02,.04),new THREE.Vector3(0,1.2,0),new THREE.Vector3(-.3,1,0),new THREE.Vector3(.2,.9,0)])assert.ok(armPose(point,bend).distanceTo(point)<1e-9,'Stationary anatomy moved');
 }
 assert.ok(armPose(hand,1).z-hand.z>.2,'Arm must visibly bend forward');
 const alias=hand.clone();armPose(alias,1,alias);assert.ok(alias.distanceTo(armPose(hand,1))<1e-9);
 assert.equal(motionAt(0,'bend'),0);assert.equal(motionAt(8,'bend'),0);assert.equal(motionAt(4,'bend'),1);assert.equal(motionAt(4,'breathe'),0);
});

test('Circulation loops join continuously through the heart, limbs and lungs without teleporting',()=>{
 const routes=circulationRoutes();assert.equal(routes.length,5);
 for(const {curve} of routes){
  assert.ok(curve.getPoint(0).distanceTo(curve.getPoint(1))<1e-9);
  assert.ok(curve.getPointAt(.9999).distanceTo(curve.getPointAt(0))<.005);
  for(let i=0;i<=100;i++){const p=curve.getPointAt(i/100);assert.ok([p.x,p.y,p.z].every(Number.isFinite));assert.ok(p.y>.1&&p.y<1.66,'Flow leaves the human vessel exhibit');}
 }
 const circulation=createCirculation();assert.equal(circulation.cellCount,160);
 for(const t of [0,1,9])circulation.update(t,.7);
 const cells=circulation.group.children.find(o=>o.isInstancedMesh);
 for(const value of cells.instanceMatrix.array)assert.ok(Number.isFinite(value));
 circulation.dispose();
});

test('Picking follows the flexed surface and leaves reusable source geometry unchanged',async()=>{
 const {installArmMotion}=await import('../src/game/labMotion.js');
 const body=new THREE.Group(),mesh=new THREE.Mesh(new THREE.BoxGeometry(.018,.08,.018).translate(.35,.82,0),new THREE.MeshStandardMaterial());body.add(mesh);body.updateMatrixWorld(true);
 const original=mesh.geometry,bytes=original.attributes.position.array.slice(),bend={value:1};const dispose=installArmMotion(mesh,body,bend);
 const target=armPose(new THREE.Vector3(.35,.82,0),1),ray=new THREE.Raycaster(target.clone().add(new THREE.Vector3(0,0,1)),new THREE.Vector3(0,0,-1));
 assert.ok(ray.intersectObject(mesh).length>0,'A visible bent arm must remain pickable');assert.equal(mesh.geometry,original);assert.deepEqual(original.attributes.position.array,bytes);
 dispose();mesh.geometry.dispose();mesh.material.dispose();
});
