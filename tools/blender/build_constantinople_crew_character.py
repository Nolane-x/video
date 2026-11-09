#!/usr/bin/env python3
"""Build a CC0 MakeHuman-derived medieval artillery crew character proof in Blender."""
import bpy, json, os, math
from mathutils import Vector, Matrix

ASSETS=os.environ.get("CHARACTER_ASSETS","character-assets")
OUT=os.environ.get("CHARACTER_OUTPUT","character-proof")
os.makedirs(OUT,exist_ok=True)
bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine="BLENDER_EEVEE"
scene.eevee.taa_render_samples=32
scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
scene.view_settings.view_transform="AgX"
scene.view_settings.look="AgX - Medium High Contrast"
scene.world.use_nodes=True
scene.world.node_tree.nodes.get("Background").inputs["Color"].default_value=(0.10,0.13,0.17,1)
scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value=0.25

def import_gltf(path):
    before=set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.abspath(path))
    return [o for o in bpy.data.objects if o not in before]

def set_male_morph_state(objects):
    """The upstream GLB stores morph weights in its node defaults. Reset all of them before rendering."""
    for obj in objects:
        if obj.type!="MESH" or not obj.data.shape_keys:
            continue
        blocks=obj.data.shape_keys.key_blocks
        for key in blocks[1:]:
            key.value=0.0
        if blocks.get("gender_male"):
            blocks["gender_male"].value=1.0
        for name in ("blink_left","blink_right","look_left","look_right","look_down"):
            if blocks.get(name):
                blocks[name].value=0.0

def apply_tint(mat,tint):
    if not mat.use_nodes: mat.use_nodes=True
    nodes=mat.node_tree.nodes;links=mat.node_tree.links
    bs=next((n for n in nodes if n.type=="BSDF_PRINCIPLED"),None)
    if not bs:return
    socket=bs.inputs.get("Base Color")
    if socket is None:return
    old=list(socket.links)
    if old:
        src=old[0].from_socket
        mix=nodes.new("ShaderNodeMixRGB");mix.blend_type="MULTIPLY";mix.inputs[0].default_value=1.0
        mix.inputs[2].default_value=(*tint,1.0)
        links.new(src,mix.inputs[1]);links.new(mix.outputs[0],socket)
    else:
        col=socket.default_value
        socket.default_value=(col[0]*tint[0],col[1]*tint[1],col[2]*tint[2],col[3])

def mat(name,color,metal=0.0,rough=.7):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF");bs.inputs["Base Color"].default_value=(*color,1)
    bs.inputs["Metallic"].default_value=metal;bs.inputs["Roughness"].default_value=rough
    return m

def rebind_import(imported,main_arm,actor_root,label,tint=None):
    meshes=[o for o in imported if o.type=="MESH"]
    for mesh in meshes:
        for mod in [m for m in mesh.modifiers if m.type=="ARMATURE"]:
            mod.object=main_arm
        if not any(m.type=="ARMATURE" for m in mesh.modifiers) and len(mesh.vertex_groups):
            mod=mesh.modifiers.new("CC0 character skinning","ARMATURE");mod.object=main_arm
        if mesh.name.lower().startswith("icosphere"):
            if mesh in imported: imported.remove(mesh)
            bpy.data.objects.remove(mesh,do_unlink=True)
            continue
        set_male_morph_state([mesh])
        for m in mesh.data.materials:
            if m and tint:apply_tint(m,tint)
        world=mesh.matrix_world.copy();mesh.parent=actor_root;mesh.matrix_world=world
        mesh.name=label+"_"+mesh.name
    for o in imported:
        if o.type=="ARMATURE" and o is not main_arm:
            bpy.data.objects.remove(o,do_unlink=True)
        elif o.type=="EMPTY":
            bpy.data.objects.remove(o,do_unlink=True)
    return meshes

# Import a rigged, textured MakeHuman-derived body with baked idle/walk/run animation tracks.
body_path=os.path.join(ASSETS,"base_body_anim.glb")
base=import_gltf(body_path)
set_male_morph_state(base)
main_arm=next((o for o in base if o.type=="ARMATURE"),None)
assert main_arm is not None,"base_body_anim.glb did not contain an armature"
body_meshes=[o for o in base if o.type=="MESH"]
root=bpy.data.objects.new("Ottoman artillery crew root",None);scene.collection.objects.link(root)
for o in list(base):
    if o.type=="EMPTY":bpy.data.objects.remove(o,do_unlink=True);continue
    if o.type=="MESH" and o.name.lower().startswith("icosphere"):
        bpy.data.objects.remove(o,do_unlink=True);continue
    world=o.matrix_world.copy();o.parent=root;o.matrix_world=world
root.location=(0,0,0)

# Base layers only. The modern trenchcoat is deliberately excluded.
outfit=[("clothing_shirt.glb",(0.72,0.54,0.31),"linen-under-tunic"),
        ("clothing_jeans.glb",(0.25,0.15,0.07),"wool-trousers"),
        ("clothing_boots.glb",(0.38,0.18,0.065),"leather-boots")]
for filename,tint,label in outfit:
    path=os.path.join(ASSETS,filename)
    if not os.path.isfile(path):continue
    imported=import_gltf(path)
    rebind_import(imported,main_arm,root,label,tint)

# Build a historically inspired layered wool caftan over the rig. This is an
# illustrative work garment, not a claim to reproduce a documented uniform.
bones=main_arm.data.bones
def bone_point(name,which="head"):
    b=bones.get(name)
    if b is None: raise RuntimeError("Missing expected rig bone: "+name)
    return main_arm.matrix_world @ Vector(getattr(b,which+"_local"))
hip=bone_point("pelvis")
sp1=bone_point("spine_01")
sp2=bone_point("spine_02")
sp3=bone_point("spine_03")
neck=bone_point("neck_01")
sh_l=bone_point("upperarm_l")
sh_r=bone_point("upperarm_r")
shoulder_span=abs(sh_l.x-sh_r.x)
cx=(hip.x+sp2.x)*.5
cy=hip.y
bottom_z=hip.z-.60
top_z=min(neck.z-.055,sp3.z+.035)
if top_z-bottom_z<.72:
    bottom_z=hip.z-.52
    top_z=sp3.z+.10

def woven_mat(name,color,rough=.88):
    m=mat(name,color,0,rough)
    nodes=m.node_tree.nodes;links=m.node_tree.links
    bs=next((n for n in nodes if n.type=="BSDF_PRINCIPLED"),None)
    if bs:
        noise=nodes.new("ShaderNodeTexNoise");noise.inputs["Scale"].default_value=74
        noise.inputs["Detail"].default_value=3.0;noise.inputs["Roughness"].default_value=.78
        bump=nodes.new("ShaderNodeBump");bump.inputs["Strength"].default_value=.16
        bump.inputs["Distance"].default_value=.018
        links.new(noise.outputs["Fac"],bump.inputs["Height"])
        links.new(bump.outputs["Normal"],bs.inputs["Normal"])
        sheen=bs.inputs.get("Sheen Weight")
        if sheen:sheen.default_value=.22
    return m

caftan_mat=woven_mat("Ottoman-workwear muted brown-red wool",(.205,.115,.058),.93)
caftan_trim=woven_mat("Wool caftan edging",(.42,.275,.105),.9)
leather_mat=woven_mat("Oiled oxhide artillery apron",(0.105,.047,.022),.96)
belt_mat=mat("Dark hand-cut leather belt",(.075,.034,.016),0,.84)
brass_mat=mat("Worn brass fastenings",(.34,.22,.075),.72,.38)

def weighted_mesh(name,verts,faces,material,weight_fn,solidify=0.0):
    arm_inv=main_arm.matrix_world.inverted()
    local_verts=[tuple(arm_inv @ Vector(v)) for v in verts]
    md=bpy.data.meshes.new(name+" mesh");md.from_pydata(local_verts,[],faces);md.update()
    obj=bpy.data.objects.new(name,md);scene.collection.objects.link(obj)
    obj.parent=root;obj.matrix_world=main_arm.matrix_world.copy()
    obj.data.materials.append(material)
    groups={}
    for idx,v in enumerate(verts):
        for bone_name,weight in weight_fn(Vector(v)):
            if weight<=0 or bones.get(bone_name) is None:continue
            if bone_name not in groups:groups[bone_name]=obj.vertex_groups.new(name=bone_name)
            groups[bone_name].add([idx],float(weight),"REPLACE")
    arm_mod=obj.modifiers.new(name+" skin","ARMATURE");arm_mod.object=main_arm
    if solidify:
        sol=obj.modifiers.new(name+" cloth thickness","SOLIDIFY");sol.thickness=solidify;sol.offset=0
    for poly in md.polygons:poly.use_smooth=True
    return obj

# Caftan body: a shaped, slightly flared robe, open at the neck and hem.
ring_fracs=[0,.09,.22,.36,.50,.64,.77,.88,1.0]
ring_rx=[.255,.27,.26,.225,.23,.25,.285,max(.29,shoulder_span*.64),.185]
ring_ry=[.138,.145,.14,.122,.128,.14,.154,.154,.108]
ring_z=[bottom_z+(top_z-bottom_z)*v for v in ring_fracs]
seg=40;verts=[];faces=[]
for ri,z in enumerate(ring_z):
    for j in range(seg):
        a=math.tau*j/seg
        verts.append((cx+ring_rx[ri]*math.cos(a),cy+ring_ry[ri]*math.sin(a),z))
for ri in range(len(ring_z)-1):
    for j in range(seg):
        a=ri*seg+j;b=ri*seg+(j+1)%seg
        c=(ri+1)*seg+(j+1)%seg;d=(ri+1)*seg+j
        faces.append((a,b,c,d))
def robe_weights(v):
    z=v.z
    if z<hip.z-.22:return [("pelvis",.55),("thigh_l",.225),("thigh_r",.225)]
    if z<sp1.z:return [("pelvis",.62),("spine_01",.38)]
    if z<sp2.z:return [("spine_01",.55),("spine_02",.45)]
    if z<sp3.z:return [("spine_02",.58),("spine_03",.42)]
    return [("spine_03",.76),("neck_01",.24)]
weighted_mesh("Long olive wool caftan",verts,faces,caftan_mat,robe_weights,.012)

# The imported rigged under-tunic already supplies fitted sleeves. Avoid a second
# procedural sleeve shell: it caused visible detached loops around the elbows.

# Leather smith's apron, broad waist belt and brass buckle.
apron_verts=[];apron_faces=[];cols=8;rows=7
apron_top=hip.z+.01;apron_bottom=hip.z-.405
for ri in range(rows):
    v=ri/(rows-1);z=apron_top+(apron_bottom-apron_top)*v
    width=.148*(.94+.06*v)
    for ci in range(cols):
        u=ci/(cols-1);x=cx+(u*2-1)*width
        y=cy-.153-.018*(1-((u*2-1)**2)) + .010*v
        apron_verts.append((x,y,z))
for ri in range(rows-1):
    for ci in range(cols-1):
        a=ri*cols+ci;b=a+1;c=b+cols;d=a+cols
        apron_faces.append((a,b,c,d))
def apron_weights(v):
    t=(apron_top-v.z)/max(.001,apron_top-apron_bottom)
    if t>.78:return [("pelvis",.58),("thigh_l",.21),("thigh_r",.21)]
    return [("pelvis",.88),("spine_01",.12)]
weighted_mesh("Leather artillery loading apron",apron_verts,apron_faces,leather_mat,apron_weights,.014)

# Elliptical belt and stitched hem piping.
belt_verts=[];belt_faces=[];major=64;minor=10
for i in range(major):
    t=math.tau*i/major
    for j in range(minor):
        a=math.tau*j/minor
        belt_verts.append((cx+(.232+.021*math.cos(a))*math.cos(t),
                           cy+(.137+.021*math.cos(a))*math.sin(t),
                           hip.z-.055+.022*math.sin(a)))
for i in range(major):
    for j in range(minor):
        a=i*minor+j;b=i*minor+(j+1)%minor
        c=((i+1)%major)*minor+(j+1)%minor;d=((i+1)%major)*minor+j
        belt_faces.append((a,b,c,d))
weighted_mesh("Wide leather waist belt",belt_verts,belt_faces,belt_mat,lambda v:[("pelvis",1.0)],.006)
# Thin trim along the robe hem makes its silhouette read as a tailored caftan.
hem_verts=[];hem_faces=[]
for i in range(major):
    t=math.tau*i/major
    for j in range(8):
        a=math.tau*j/8
        hem_verts.append((cx+(.291+.009*math.cos(a))*math.cos(t),
                          cy+(.162+.009*math.cos(a))*math.sin(t),
                          bottom_z+.045+.009*math.sin(a)))
for i in range(major):
    for j in range(8):
        a=i*8+j;b=i*8+(j+1)%8;c=((i+1)%major)*8+(j+1)%8;d=((i+1)%major)*8+j
        hem_faces.append((a,b,c,d))
weighted_mesh("Wool caftan hem piping",hem_verts,hem_faces,caftan_trim,lambda v:[("pelvis",.8),("thigh_l",.1),("thigh_r",.1)],.003)

# A small brass buckle on the apron-facing side of the belt.
buckle_verts=[(cx-.032,cy-.181,hip.z-.085),(cx+.032,cy-.181,hip.z-.085),
              (cx+.032,cy-.181,hip.z-.02),(cx-.032,cy-.181,hip.z-.02),
              (cx-.032,cy-.158,hip.z-.085),(cx+.032,cy-.158,hip.z-.085),
              (cx+.032,cy-.158,hip.z-.02),(cx-.032,cy-.158,hip.z-.02)]
buckle_faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
weighted_mesh("Worn brass belt buckle",buckle_verts,buckle_faces,brass_mat,lambda v:[("pelvis",1.0)],.002)

# Replace the single floating ring with a wrapped linen turban: a low cloth cap
# plus five descending-to-rising spiral turns, all skinned to the head bone.
wrapmat=woven_mat("Saffron and umber linen turban",(0.34,.245,.12),.96)
head_bone=bones.get("head")
if head_bone:
    hp=main_arm.matrix_world @ ((head_bone.head_local+head_bone.tail_local)*.5)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,location=hp+Vector((0,0,.20)))
    cap=bpy.context.object;cap.name="Linen turban crown";cap.scale=(.126,.132,.062);cap.data.materials.append(wrapmat)
    for poly in cap.data.polygons:poly.use_smooth=True
    curve=bpy.data.curves.new("Five-turn wrapped linen turban","CURVE");curve.dimensions="3D";curve.resolution_u=2
    spl=curve.splines.new("POLY");count=320;spl.points.add(count-1)
    for i,pt in enumerate(spl.points):
        u=i/(count-1);ang=math.tau*5*u
        rx=.137-.018*u;ry=.143-.018*u
        z=hp.z+.13+.145*u
        pt.co=(hp.x+rx*math.cos(ang),hp.y+ry*math.sin(ang),z,1)
    curve.bevel_depth=.021;curve.bevel_resolution=5
    wrap=bpy.data.objects.new("Five-turn linen turban wrap",curve);scene.collection.objects.link(wrap)
    wrap.data.materials.append(wrapmat)
    bpy.context.view_layer.objects.active=wrap;wrap.select_set(True);bpy.ops.object.convert(target="MESH")
    wrap=bpy.context.object;wrap.name="Five-turn linen turban mesh"
    for obj in (cap,wrap):
        wm=obj.matrix_world.copy();obj.parent=root;obj.matrix_world=wm
        vg=obj.vertex_groups.new(name="head");vg.add([v.index for v in obj.data.vertices],1.0,"REPLACE")
        mod=obj.modifiers.new("Turban follows head rig","ARMATURE");mod.object=main_arm

# Sample the middle of a relaxed breathing action and lift the head slightly for a neutral standing portrait.
scene.render.fps=30;scene.render.fps_base=1
actions=sorted([a.name for a in bpy.data.actions])
if main_arm.animation_data is None:main_arm.animation_data_create()
idle=next((a for a in bpy.data.actions if "idle_breathe" in a.name.lower()),None)
if idle is None:
    idle=next((a for a in bpy.data.actions if "idle" in a.name.lower() and "breathe" not in a.name.lower()),None)
if idle:
    main_arm.animation_data.action=idle
    mid=int((idle.frame_range[0]+idle.frame_range[1])*.5)
else:
    mid=1
scene.frame_set(mid)
head_pose=main_arm.pose.bones.get("head")
if head_pose:
    head_pose.rotation_mode="XYZ"
    head_pose.rotation_euler.x -= math.radians(10)
neck_pose=main_arm.pose.bones.get("neck_01")
if neck_pose:
    neck_pose.rotation_mode="XYZ"
    neck_pose.rotation_euler.x -= math.radians(3)

ground=mat("Warm limestone studio floor",(.18,.16,.13),0,.95)
bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.02));floor=bpy.context.object;floor.name="Ground";floor.data.materials.append(ground)
def area(name,loc,energy,color,size,target):
    d=bpy.data.lights.new(name,"AREA");d.energy=energy;d.color=color;d.shape="DISK";d.size=size
    o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc
    o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()
area("Large soft key",(-3,-4,6),650,(1,.81,.62),4,(0,0,1))
area("Cool fill",(4,-2,3.8),380,(.62,.73,.9),3,(0,0,1))
area("Warm rim",(0,3,5),850,(1,.58,.32),3,(0,0,1))
bpy.ops.object.camera_add(location=(1.8,-5.6,1.75));cam=bpy.context.object;cam.name="Crew full-body camera";cam.data.lens=58
target=Vector((0,0,.92));cam.rotation_euler=(target-cam.location).to_track_quat("-Z","Y").to_euler();scene.camera=cam

# Export a self-contained GLB and a review still for reuse in the siege scene.
for o in bpy.context.selected_objects:o.select_set(False)
export_objs=[o for o in bpy.context.scene.objects if o.type in {"MESH","ARMATURE"} and o.name!="Ground"]
for o in export_objs:o.select_set(True)
bpy.context.view_layer.objects.active=main_arm
glb_out=os.path.join(OUT,"ottoman-artillery-crew-cc0.glb")
bpy.ops.export_scene.gltf(filepath=glb_out,export_format="GLB",use_selection=True,export_animations=True,export_skins=True)
scene.render.image_settings.file_format="PNG";scene.render.filepath=os.path.abspath(os.path.join(OUT,"crew-preview.png"))
scene.frame_set(mid);bpy.ops.render.render(write_still=True)
bpy.ops.object.camera_add(location=(1.0,-3.05,1.65));closecam=bpy.context.object;closecam.name="Crew face and torso close-up";closecam.data.lens=72
close_target=Vector((0,0,1.42));closecam.rotation_euler=(close_target-closecam.location).to_track_quat("-Z","Y").to_euler();scene.camera=closecam
scene.render.filepath=os.path.abspath(os.path.join(OUT,"crew-closeup.png"));bpy.ops.render.render(write_still=True)
verts=sum(len(o.data.vertices) for o in export_objs if o.type=="MESH")
tris=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in export_objs if o.type=="MESH")
report={"status":"CHARACTER_ASSET_SMOKE_PASS_PENDING_VISUAL_REVIEW","source":"kblood/CharacterCreator/output","license":"CC0-1.0 for generated output assets per output/asset_licenses.json and LICENSE-NOTES.md","armature":main_arm.name,"bones":len(main_arm.data.bones),"actions":actions,"meshes":[o.name for o in export_objs if o.type=="MESH"],"materials":sorted({m.name for o in export_objs if o.type=="MESH" for m in o.data.materials if m}),"vertices":verts,"triangles":tris,"export_glb":os.path.basename(glb_out),"visual_approval":"pending","costume_note":"CC0-derived male base rig with a bespoke rig-weighted olive wool caftan, separate arm sleeves, leather artillery apron, waist belt and five-turn linen turban. Illustrative 15th-century workwear adaptation, not an authenticated uniform."}
open(os.path.join(OUT,"manifest.json"),"w").write(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2),flush=True)
