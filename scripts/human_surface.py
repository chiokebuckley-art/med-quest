"""Adapt CC0 MakeHuman topology to the Med Quest standing anatomy exhibit.
No MakeHuman/MPFB application code is used. See docs/THIRD-PARTY-ASSETS.md.
"""
import bpy, bmesh, json, gzip, math, random
from mathutils import Vector

def build_surface(root, tag, ell, tube, skin, hair, eye, iris, pupil, fabric):
 source=root/'scripts/vendor/makehuman'
 vertices=[];uv=[];faces=[];groups={};group=''
 for line in (source/'base.obj').read_text().splitlines():
  fields=line.split()
  if not fields:continue
  if fields[0]=='v':vertices.append(Vector(map(float,fields[1:4])))
  elif fields[0]=='vt':uv.append(tuple(map(float,fields[1:3])))
  elif fields[0]=='g':group=fields[1]
  elif fields[0]=='f':
   f=[(int(p.split('/')[0])-1,int(p.split('/')[1])-1) for p in fields[1:]]
   groups.setdefault(group,[]).append(f)
 # A Black adult volunteer, using the CC0 African adult shape target rather than a real-person likeness.
 for filename,weight in [('african-male-young.target.gz',1),('universal-male-young-averagemuscle-averageweight.target.gz',1)]:
  for line in gzip.decompress((source/filename).read_bytes()).decode().splitlines():
   p=line.split()
   if len(p)==4 and not p[0].startswith('#'):vertices[int(p[0])]+=Vector(map(float,p[1:]))*weight
 used=sorted({p[0] for f in groups['body'] for p in f});low=min(vertices[i].y for i in used);high=max(vertices[i].y for i in used);scale=1.75/(high-low)
 raw=[Vector((v.x*scale,-v.z*scale+.035,(v.y-low)*scale)) for v in vertices]
 def joint(name):
  ids=set(p[0] for f in groups[name] for p in f)
  return sum((raw[i] for i in ids),Vector())/len(ids)
 def point(x,h,f):return Vector((x,-f,h))
 transforms={}
 def transform(start,end,a,b):
  rotation=(end-start).rotation_difference(b-a).to_matrix()
  return lambda p:a+rotation@(p-start)
 for side,sgn in [('L',1),('R',-1)]:
  js={n:joint('joint-'+side.lower()+'-'+n) for n in ['shoulder','elbow','hand','upper-leg','knee','ankle']}
  shoulder=point(sgn*.19,1.395,-.004);elbow=point(sgn*.275,1.102,0);wrist=point(sgn*.338,.837,.01)
  upper=transform(js['shoulder'],js['elbow'],shoulder,elbow)
  lower=transform(js['elbow'],js['hand'],elbow,wrist)
  middle=joint('joint-'+side.lower()+'-finger-3-4')
  hand=transform(js['hand'],middle,wrist,point(sgn*.352,.702,.027))
  thigh=transform(js['upper-leg'],js['knee'],point(sgn*.093,.896,-.006),point(sgn*.106,.477,.008))
  shin=transform(js['knee'],js['ankle'],point(sgn*.106,.477,.008),point(sgn*.103,.087,-.006))
  shift=point(sgn*.103,.087,-.006)-js['ankle']
  for name in json.loads((source/'weights.default.json').read_text())['weights']:
   if not name.endswith('.'+side):continue
   if name.startswith('upperarm'):transforms[name]=upper
   elif name.startswith('lowerarm'):transforms[name]=lower
   elif name.startswith(('wrist','finger','metacarpal')):transforms[name]=hand
   elif name.startswith('upperleg'):transforms[name]=thigh
   elif name.startswith('lowerleg'):transforms[name]=shin
   elif name.startswith(('foot','toe')):transforms[name]=lambda p,s=shift:p+s
 weights=json.loads((source/'weights.default.json').read_text())['weights'];posed=[Vector() for p in raw];totals=[0.0]*len(raw)
 for name,values in weights.items():
  fn=transforms.get(name,lambda p:p)
  for index,w in values:
   posed[index]+=fn(raw[index])*w;totals[index]+=w
 for i in range(len(raw)):
  posed[i]=posed[i]/totals[i] if totals[i]>.001 else raw[i]
 index={old:i for i,old in enumerate(used)}
 mesh=bpy.data.meshes.new('Human continuous quad topology');mesh.from_pydata([posed[i] for i in used],[],[[index[p[0]] for p in f] for f in groups['body']]);mesh.update()
 body=bpy.data.objects.new('Human detailed surface',mesh);bpy.context.collection.objects.link(body);tag(body,'Skin','Skin',skin)
 uv_layer=mesh.uv_layers.new(name='HumanUV')
 for poly,face in zip(mesh.polygons,groups['body']):
  for loop,p in zip(poly.loop_indices,face):uv_layer.data[loop].uv=uv[p[1]]
 # Neutral vertex colors preserve the CC0 UV skin texture without tinting it twice.
 tint=mesh.color_attributes.new(name='SkinTint',type='BYTE_COLOR',domain='POINT');mesh.color_attributes.active_color=tint
 for old,i in index.items():
  tint.data[i].color=(1,1,1,1)
 # Preserve joint influence data through subdivision and glTF optimization.
 motion=mesh.attributes.new(name='_MQ_ARM_WEIGHTS',type='FLOAT_VECTOR',domain='POINT')
 arm_weights=[0.0]*len(raw);forearm_weights=[0.0]*len(raw)
 for bone_name,values in weights.items():
  if not bone_name.endswith('.L') or not bone_name.startswith(('upperarm','lowerarm','wrist','finger','metacarpal')):continue
  lower=not bone_name.startswith('upperarm')
  for old,w in values:
   arm_weights[old]+=w
   if lower:forearm_weights[old]+=w
 for old,i in index.items():
  arm=arm_weights[old]/totals[old] if totals[old]>.001 else 0
  lower=forearm_weights[old]/arm_weights[old] if arm_weights[old]>.001 else 0
  motion.data[i].vector=(min(1,arm),min(1,lower),0)
 body['armMotionAttribute']='_MQ_ARM_WEIGHTS'
 material=skin.copy();material.name='Human skin microdetail';material.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(1,1,1,1)
 bsdf=material.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Roughness'].default_value=.57;bsdf.inputs['Subsurface Weight'].default_value=.06
 albedo=bpy.data.images.load(str(source/'young_darkskinned_male_diffuse.png'));albedo.name='MakeHuman CC0 natural skin albedo';albedo.pack()
 albedo_tex=material.node_tree.nodes.new('ShaderNodeTexImage');albedo_tex.image=albedo;material.node_tree.links.new(albedo_tex.outputs['Color'],bsdf.inputs['Base Color'])
 # Tangent normal and roughness textures stay embedded in the glTF. UV-aligned
 # pore noise varies surface response, avoiding the polished plastic appearance.
 import numpy as np
 rng=np.random.default_rng(8);size=512
 noise=rng.normal(0,1,(size,size));smooth=(noise+np.roll(noise,1,0)+np.roll(noise,1,1))/3
 dx=(np.roll(smooth,-1,1)-np.roll(smooth,1,1))*.08;dy=(np.roll(smooth,-1,0)-np.roll(smooth,1,0))*.08
 normal=np.stack([dx,dy,np.ones_like(dx)],axis=-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
 pixels=np.ones((size,size,4),dtype=np.float32);pixels[:,:,:3]=normal*.5+.5
 normal_image=bpy.data.images.new('Human skin pores tangent normal',width=size,height=size);normal_image.colorspace_settings.name='Non-Color';normal_image.pixels.foreach_set(pixels.ravel());normal_image.pack()
 tex=material.node_tree.nodes.new('ShaderNodeTexImage');tex.image=normal_image;normal_node=material.node_tree.nodes.new('ShaderNodeNormalMap');material.node_tree.links.new(tex.outputs['Color'],normal_node.inputs['Color']);material.node_tree.links.new(normal_node.outputs['Normal'],bsdf.inputs['Normal'])
 pixels[:,:,:3]=np.clip(.57+smooth[:,:,None]*.025,.45,.7)
 rough_image=bpy.data.images.new('Human skin roughness',width=size,height=size);rough_image.colorspace_settings.name='Non-Color';rough_image.pixels.foreach_set(pixels.ravel());rough_image.pack()
 rough_tex=material.node_tree.nodes.new('ShaderNodeTexImage');rough_tex.image=rough_image;material.node_tree.links.new(rough_tex.outputs['Color'],bsdf.inputs['Roughness'])
 mesh.materials.clear();mesh.materials.append(material)
 bpy.context.view_layer.objects.active=body;body.select_set(True)
 sub=body.modifiers.new('Human surface detail','SUBSURF');sub.levels=1;bpy.ops.object.modifier_apply(modifier=sub.name);body.select_set(False)
 mesh=body.data
 # Breathing is local to chest/abdomen, feet and head stay still.
 body.shape_key_add(name='Basis');breath=body.shape_key_add(name='Breath')
 for v in mesh.vertices:
  p=v.co;w=math.exp(-((p.z-1.27)/.17)**4)*math.exp(-(p.x/.18)**4)
  breath.data[v.index].co.y-=.005*w;breath.data[v.index].co.x+=p.x*.009*w
 # Eyeballs sit inside the modeled orbital lids. Small separate iris and pupil.
 for side,sgn in [('l',1),('r',-1)]:
  p=joint('joint-'+side+'-eye');r=.015
  ell('Eye',(p.x,p.z,-p.y),(r,r,r),eye,'Face',32,20)
  ell('Iris',(p.x,p.z,-p.y+r*.95),(.0062,.0062,.0016),iris,'Face',32,16)
  ell('Pupil',(p.x,p.z,-p.y+r*1.045),(.0026,.0026,.0005),pupil,'Face',24,12)
  # Brow paths fitted to the actual brow ridge of the new face.
  pts=[]
  for x in [p.x-.019,p.x,p.x+.020]:
   nearby=[v for v in raw if abs(v.x-x)<.005 and abs(v.z-(p.z+.025))<.006]
   front=max((-v.y for v in nearby),default=-p.y)
   pts.append((x,p.z+.023+(0.003 if x==p.x else 0),front+.001))
  tube('Brow',pts,.00055,hair,'Face')
 # Hair follows the scalp itself, preserving the cranium silhouette.
 scalp_faces=[p for p in body.data.polygons if all(body.data.vertices[i].co.z>1.685 or (body.data.vertices[i].co.z>1.647 and body.data.vertices[i].co.y>-.007) for i in p.vertices)]
 scalp_ids=sorted({i for p in scalp_faces for i in p.vertices});si={old:i for i,old in enumerate(scalp_ids)}
 hm=bpy.data.meshes.new('Close cropped scalp');hm.from_pydata([body.data.vertices[i].co+body.data.vertices[i].normal*.0016 for i in scalp_ids],[],[[si[i] for i in p.vertices] for p in scalp_faces]);hm.update()
 ho=bpy.data.objects.new('Close cropped hair',hm);bpy.context.collection.objects.link(ho);tag(ho,'Face','Hair',hair)
 # Fine, short curled strands break up the smooth cap silhouette and light response.
 rng=random.Random(34)
 curve=bpy.data.curves.new('Close cropped curls','CURVE');curve.dimensions='3D';curve.bevel_depth=.00038;curve.bevel_resolution=1;curve.resolution_u=1
 for strand in range(1700):
  polygon=rng.choice(scalp_faces);ids=list(polygon.vertices)
  a,b,c=[body.data.vertices[i] for i in ids[:3]]
  u,v=rng.random(),rng.random()
  if u+v>1:u,v=1-u,1-v
  center=a.co+(b.co-a.co)*u+(c.co-a.co)*v
  normal=(a.normal*(1-u-v)+b.normal*u+c.normal*v).normalized()
  tangent=normal.cross(Vector((0,0,1)))
  if tangent.length<.01:tangent=normal.cross(Vector((1,0,0)))
  tangent.normalize();bitangent=normal.cross(tangent).normalized()
  phase=rng.random()*math.tau;radius=rng.uniform(.0006,.0012)
  spline=curve.splines.new('POLY');spline.points.add(4)
  for j,p in enumerate(spline.points):
   t=j/4;angle=phase+t*math.tau*.8
   q=center+normal*(.0017+math.sin(t*math.pi)*.0024)+tangent*(math.cos(angle)*radius)+bitangent*(math.sin(angle)*radius)
   p.co=(*q,1);p.radius=.65+.35*math.sin(t*math.pi)
 curls=bpy.data.objects.new('Fine close cropped curls',curve);bpy.context.collection.objects.link(curls);bpy.context.view_layer.objects.active=curls;curls.select_set(True);bpy.ops.object.convert(target='MESH');curls.select_set(False);tag(curls,'Face','Hair',hair)

 # Garment duplicates the body's hip surface; tailored, no intersecting blobs.
 garment_faces=[p for p in body.data.polygons if abs(sum(body.data.vertices[i].co.x for i in p.vertices)/len(p.vertices))<.19 and .695<sum(body.data.vertices[i].co.z for i in p.vertices)/len(p.vertices)<1.004]
 ids=sorted({i for p in garment_faces for i in p.vertices});gi={old:i for i,old in enumerate(ids)}
 gm=bpy.data.meshes.new('Tailored surface shorts');gm.from_pydata([body.data.vertices[i].co+body.data.vertices[i].normal*.0055 for i in ids],[],[[gi[i] for i in p.vertices] for p in garment_faces]);gm.update()
 bm=bmesh.new();bm.from_mesh(gm)
 for v in {v for e in bm.edges if e.is_boundary for v in e.verts}:v.co.z=1.003 if v.co.z>.9 else .696
 bm.to_mesh(gm);bm.free()
 go=bpy.data.objects.new('Academy shorts',gm);bpy.context.collection.objects.link(go);tag(go,'Clothing','Academy_Shorts',fabric)
 solid=go.modifiers.new('Hem thickness','SOLIDIFY');solid.thickness=.0017;bpy.context.view_layer.objects.active=go;go.select_set(True);bpy.ops.object.modifier_apply(modifier=solid.name);go.select_set(False)
 return body,material
