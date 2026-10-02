"""Human anatomy exhibit with adapted CC0 MakeHuman surface. Blender Z-up -> glTF Y-up on export.
Not a clinical anatomical atlas. Surface provenance is recorded in docs/THIRD-PARTY-ASSETS.md. Internal anatomy is authored locally.
"""
import bpy, bmesh, math, json, random
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
random.seed(12)

def pos(x,h,f=0): return (x,-f,h)
def mat(name,color,rough=.65):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough
 return m
skin=mat('Skin warm natural matte',(.49,.29,.18),.66);lip=mat('Lips soft natural',(.43,.24,.20),.66);hair=mat('Hair dark brown',(.035,.018,.012),.86);eye=mat('Eye warm ivory',(.71,.69,.59),.35);iris=mat('Iris brown',(.075,.043,.02),.42);pupil=mat('Pupil',(.008,.008,.01),.28);fabric=mat('Academy modesty shorts teal',(.025,.19,.21),.9)
bone=mat('Bone ivory',(.79,.75,.59),.76);muscle=mat('Muscle muted rose',(.42,.17,.13),.72);tendon=mat('Tendon warm ivory',(.76,.66,.47),.8);heart=mat('Heart contained tissue',(.38,.085,.066),.52);lung=mat('Lungs calm tissue',(.62,.32,.3),.7);digest=mat('Digestion peach',(.65,.35,.2),.68);kidney=mat('Kidneys plum',(.31,.12,.14),.62);artery=mat('Arteries contained red',(.55,.075,.045),.5);vein=mat('Veins blue diagram',(.08,.24,.39),.53);nerve=mat('Nerves pale gold diagram',(.76,.53,.12),.7);brain=mat('Brain warm grey rose',(.53,.36,.3),.75)
objects=[];bodyparts=[];fingerparts=[]
def tag(o,layer,label,m):
 o.name=f'MQ_{layer}_{label}';o['layer']=layer;o['part']=label;o.data.materials.clear();o.data.materials.append(m)
 if o.type=='MESH':
  for p in o.data.polygons:p.use_smooth=True
 objects.append(o);return o

def ell(name,c,scale,m,layer='Skin',segments=16,rings=12):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=pos(*c));o=bpy.context.object;o.scale=(scale[0],scale[2],scale[1]);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return tag(o,layer,name,m)

def tube(name,points,radius,m,layer,cyclic=False):
 curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D';curve.resolution_u=8;curve.bevel_depth=radius;curve.bevel_resolution=3;curve.use_fill_caps=True
 sp=curve.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for b,c in zip(sp.bezier_points,points):b.co=pos(*c);b.handle_left_type='AUTO';b.handle_right_type='AUTO'
 sp.use_cyclic_u=cyclic;o=bpy.data.objects.new(name,curve);bpy.context.collection.objects.link(o);bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False);return tag(o,layer,name,m)

def loft(name,rings,m,layer='Skin',sides=32):
 # ring: height, x center, width, depth, front center
 verts=[];faces=[]
 for h,x,w,d,f in rings:
  for j in range(sides):
   a=2*math.pi*j/sides;verts.append(pos(x+w*math.cos(a),h,f+d*math.sin(a)))
 for i in range(len(rings)-1):
  for j in range(sides):k=i*sides+j;l=i*sides+(j+1)%sides;faces.append((k,k+sides,l+sides,l))
 faces.append(tuple(range(sides)));faces.append(tuple((len(rings)-1)*sides+j for j in range(sides-1,-1,-1)))
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);tag(o,layer,name,m)
 sub=o.modifiers.new('Sculpt surface smoothing','SUBSURF');sub.levels=1;bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.modifier_apply(modifier=sub.name);o.select_set(False);return o

def join(obs,name,m,layer):
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();o=bpy.context.object;return tag(o,layer,name,m)

import sys
sys.path.insert(0,str(ROOT/'scripts'))
from human_surface import build_surface
body,sculpt_skin=build_surface(ROOT,tag,ell,tube,skin,hair,eye,iris,pupil,fabric)

# Muscle groups follow the limbs and chest, with pale tendon insertions.
for sign in [-1,1]:
 ell('Muscles',(sign*.119,1.336,.105),(.1,.075,.028),muscle,'Muscle')
 ell('Muscles',(sign*.224,1.36,.028),(.045,.065,.055),muscle,'Muscle')
 for h,x,sz in [(1.23,.269,.09),(.986,.33,.081),(.685,.1,.112),(.289,.108,.088)]:
  ell('Muscles',(sign*x,h,.026 if h>1 else .04),(.036,sz,.023),muscle,'Muscle')
  tube('Tendons',[(sign*x,h-sz,.038),(sign*(x+.009),h-sz-.046,.027)],.006,tendon,'Muscle')
 for i in range(3):ell('Muscles',(sign*.049,1.23-i*.066,.104),(.037,.026,.016),muscle,'Muscle')
# Skeleton: skull, jaw, vertebrae, 12 rib pairs, pelvis and paired limb bones.
skull=ell('Bones',(0,1.644,-.011),(.08,.099,.072),bone,'Bone',32,24)
for sign in [-1,1]:
 cutter=ell('socket cutter',(sign*.031,1.63,.058),(.022,.022,.032),bone)
 mod=skull.modifiers.new('Orbital opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;bpy.context.view_layer.objects.active=skull;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 tube('Bones',[(sign*.075,1.603,-.01),(sign*.062,1.556,.036),(sign*.023,1.539,.051),(0,1.539,.053)],.013,bone,'Bone')
 tube('Bones',[(sign*.185,1.43,0),(sign*.11,1.441,.027),(0,1.42,.05)],.008,bone,'Bone')
 tube('Bones',[(sign*.211,1.39,0),(sign*.297,1.083,0)],.013,bone,'Bone')
 for delta in [-.012,.012]:tube('Bones',[(sign*(.3+delta),1.079,0),(sign*(.356+delta),.824,0)],.006,bone,'Bone')
 tube('Bones',[(sign*.084,.874,0),(sign*.106,.483,0)],.017,bone,'Bone')
 for delta in [-.012,.012]:tube('Bones',[(sign*(.107+delta),.475,0),(sign*(.101+delta),.088,0)],.008,bone,'Bone')
 for h,x in [(1.08,.299),(.483,.106),(.09,.101)]:ell('Joints',(sign*x,h,.005),(.02,.021,.02),bone,'Bone')
 tube('Bones',[(sign*.065,.966,-.005),(sign*.153,.93,.009),(sign*.16,.865,.017),(sign*.104,.822,.032),(sign*.036,.865,.046)],.022,bone,'Bone')
 for i in range(12):
  h=1.387-i*.024;w=.142+math.sin(i/11*math.pi)*.045 if i<9 else .13-(i-9)*.015
  tube('Bones',[(0,h,-.043),(sign*w*.7,h-.014,-.058),(sign*w,h-.043,0),(sign*w*.75,h-.055,.074),(sign*.025,h-.047,.096)],.0038,bone,'Bone')
 for i in range(4):
  x=sign*(.344+i*.016);tube('Bones',[(x,.775,.008),(x,.73,.01),(x+sign*.003,.688,.021)],.0038,bone,'Bone')
 for i in range(5):tube('Bones',[(sign*(.075+i*.012),.047,0),(sign*(.075+i*.012),.03,.125)],.004,bone,'Bone')
for i in range(24):ell('Bones',(0,1.485-i*.025,-.028),(.012,.009,.013),bone,'Bone',12,8)
tube('Bones',[(0,1.392,.096),(0,1.213,.111)],.007,bone,'Bone')
# Anatomy organs, all closed, clean education silhouettes. Patient left = viewer right.
for sign in [-1,1]:
 rings=[(1.154,sign*.095,.055,.046,.004),(1.18,sign*.094,.077,.06,.004),(1.24,sign*.091,.083,.063,.004),(1.32,sign*.089,.07,.06,.004),(1.383,sign*.076,.044,.04,.003),(1.413,sign*.066,.009,.013,.003)]
 o=loft('Lungs',rings,lung,'Organs');o.name='MQ_Organs_Lungs_'+('left' if sign>0 else 'right');o['part']='Lungs'
 tube('Lungs',[(0,1.458,.036),(0,1.349,.038),(sign*.07,1.293,.04),(sign*.114,1.242,.043)],.009,tendon,'Organs')
 for dy in [0,.036]:tube('Lungs',[(sign*.07,1.29-dy,.043),(sign*.123,1.275-dy,.046)],.0035,tendon,'Organs')
# Heart chambers merge to an asymmetrical tapered silhouette.
hs=[]
for x,h,w,hh in [(.032,1.259,.039,.057),(.072,1.222,.035,.061),(-.004,1.25,.034,.046)]:hs.append(ell('Heart',(x,h,.079),(w,hh,.038),heart,'Organs'))
heart_surface=join(hs,'Heart',heart,'Organs')
rem=heart_surface.modifiers.new('Continuous cardiac silhouette','REMESH');rem.mode='VOXEL';rem.voxel_size=.0025;rem.use_smooth_shade=True;bpy.context.view_layer.objects.active=heart_surface;bpy.ops.object.modifier_apply(modifier=rem.name)
sm=heart_surface.modifiers.new('Cardiac surface','SMOOTH');sm.factor=.8;sm.iterations=6;bpy.ops.object.modifier_apply(modifier=sm.name)
dec=heart_surface.modifiers.new('Cardiac detail budget','DECIMATE');dec.ratio=.16;bpy.ops.object.modifier_apply(modifier=dec.name)
tube('Heart',[(.021,1.283,.079),(.017,1.323,.071),(.04,1.335,.06),(.054,1.3,.058)],.009,artery,'Organs')
# J-shaped stomach and folded intestine, enclosed within the abdomen.
tube('Stomach',[(.017,1.24,-.013),(.026,1.168,.011),(.08,1.139,.025),(.087,1.096,.047),(.045,1.078,.06),(0,1.102,.05)],.028,digest,'Organs')
coils=[]
for i in range(73):
 t=i/72;coils.append((.07*math.sin(t*math.pi*12),1.065-t*.15,.045+.012*math.cos(t*math.pi*12)))
tube('Intestines',coils,.009,digest,'Organs')
tube('Intestines',[(-.108,.918,.062),(-.12,1.086,.043),(0,1.113,.051),(.123,1.08,.052),(.108,.923,.061),(0,.903,.064)],.016,digest,'Organs')
for sign in [-1,1]:
 o=ell('Kidneys',(sign*.097,1.092,-.055),(.033,.052,.027),kidney,'Organs')
 for v in o.data.vertices:
  if sign*v.co.x<0:v.co.x*=.62
 tube('Kidneys',[(sign*.091,1.064,-.04),(sign*.063,.967,-.035),(sign*.016,.899,-.02)],.0035,tendon,'Organs')
# Branching closed blood vessels and signal wires. No external blood.
for sign in [-1,1]:
 for m,label,offset in [(artery,'Arteries',0),(vein,'Veins',.012)]:
  tube(label,[(sign*(.016+offset),1.36,.042),(sign*(.018+offset),1.15,.047),(sign*(.024+offset),.94,.038),(sign*(.092+offset),.77,.034),(sign*(.106+offset),.48,.036),(sign*(.103+offset),.14,.019)],.0045,m,'Pipes')
  tube(label,[(sign*(.02+offset),1.37,.045),(sign*(.177+offset),1.415,.04),(sign*(.246+offset),1.26,.035),(sign*(.3+offset),1.075,.027),(sign*(.35+offset),.85,.024),(sign*(.37+offset),.758,.017)],.0037,m,'Pipes')
  tube(label,[(sign*(.015+offset),1.369,.032),(sign*(.028+offset),1.522,.018),(sign*(.037+offset),1.608,.025)],.0033,m,'Pipes')
 for x,h in [(.095,1.094),(.075,1.28)]:tube('Arteries',[(0,h,.04),(sign*x,h,.018)],.003,artery,'Pipes')
 tube('Nerves',[(0,1.546,-.015),(0,1.4,-.017),(sign*.18,1.412,.021),(sign*.25,1.23,.026),(sign*.302,1.08,.02),(sign*.356,.831,.019)],.0027,nerve,'Signals')
 tube('Nerves',[(0,1.543,-.015),(0,1.1,-.018),(sign*.087,.84,.018),(sign*.106,.49,.016),(sign*.103,.095,.015)],.003,nerve,'Signals')
 for h in [1.36,1.28,1.18,1.08]:tube('Nerves',[(0,h,-.015),(sign*.08,h-.012,.033),(sign*.144,h-.042,.048)],.0018,nerve,'Signals')
for sign in [-1,1]:
 ell('Brain',(sign*.029,1.659,-.005),(.041,.059,.052),brain,'Signals',32,20)
 for i in range(8):
  h=1.625+i*.008
  tube('Brain',[(sign*.017,h,.043),(sign*(.033+math.sin(i)*.006),h+.005,.05),(sign*.053,h,.031)],.0025,brain,'Signals')
# Merge each anatomical part for fast raycasting and low draw calls.
for layer in ['Face','Clothing','Muscle','Bone','Organs','Pipes','Signals']:
 groups={}
 for o in list(bpy.context.scene.objects):
  if o.type=='MESH' and o.get('layer')==layer:groups.setdefault((o.get('part'),o.data.materials[0].name),[]).append(o)
 for (part,mname),obs in groups.items():
  if len(obs)>1:join(obs,part,bpy.data.materials[mname],layer)
# Export runtime geometry only. Camera/lights never enter the asset.
bpy.ops.object.select_all(action='SELECT')
for o in bpy.context.scene.objects:
 if o.type=='MESH':
  # Preserve original face labels; skin's part is exposed simply as Skin.
  if o.get('layer')=='Skin':o['part']='Skin'
  o.data.validate(verbose=False)
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
  for p in o.data.polygons:p.use_smooth=True
body.data.materials.clear();body.data.materials.append(sculpt_skin)
for polygon in body.data.polygons:polygon.material_index=0

out=ROOT/'public/assets/models/MQ_human_anatomy.glb'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'docs/MQ-human-anatomy.blend'))
bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',export_extras=True,export_yup=True,export_apply=True,export_cameras=False,export_lights=False,export_morph_normal=False)
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
report={'asset':str(out.relative_to(ROOT)),'original':False,'surfaceSource':'MakeHuman hm08 CC0, adapted for Med Quest','humanHeightMeters':1.75,'layers':sorted(set(o.get('layer') for o in meshes)),'meshes':len(meshes),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes),'bytes':out.stat().st_size,'partBudgets':[{'layer':o.get('layer'),'part':o.get('part'),'triangles':sum(len(p.vertices)-2 for p in o.data.polygons)} for o in meshes],'notes':['Educational anatomy, not a clinical atlas. Adapted CC0 surface with original internal anatomy.','Detailed human topology, skin normal/roughness maps, breathing morph, facial features, five fingers, toes and fitted opaque shorts.','Anatomy groups use glTF extras for labels and layer selection.']}
(ROOT/'docs/HUMAN-MODEL-MANIFEST.json').write_text(json.dumps(report,indent=2));print('ANATOMY_RESULT',json.dumps(report))
