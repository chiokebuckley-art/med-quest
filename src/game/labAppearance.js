import * as THREE from 'three';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';

// Broad studio reflections reveal the skin texture without point-light glare.
export function studioEnvironment(renderer,scene){
 const room=new RoomEnvironment(),pmrem=new THREE.PMREMGenerator(renderer);
 const environment=pmrem.fromScene(room,.025);scene.environment=environment.texture;scene.environmentIntensity=.65;
 room.dispose();pmrem.dispose();return ()=>environment.dispose();
}
export function humanMaterial(source,layer,part){
 if(layer==='Face'&&part==='Hair')return new THREE.MeshPhysicalMaterial({color:source.color,roughness:.95,metalness:0,specularIntensity:.12,side:THREE.FrontSide});
 if(layer!=='Skin')return source.clone();
 const skin=new THREE.MeshPhysicalMaterial({map:source.map,normalMap:source.normalMap,roughnessMap:source.roughnessMap,color:source.color,roughness:1,metalness:0,normalScale:new THREE.Vector2(.38,.38),side:THREE.FrontSide,specularIntensity:.3,specularColor:0xffeee3});
 skin.name='Natural dark skin · soft studio response';
 return skin;
}
export const portraitTarget=new THREE.Vector3(0,.76,.09);
