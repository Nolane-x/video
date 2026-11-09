#!/usr/bin/env python3
"""Build a CC0 MakeHuman-derived medieval artillery crew character proof in Blender."""
import bpy, json, os, math
from mathutils import Vector

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

# Outfit layers: recolour the long coat to undyed wool/earth, darken trousers and leather footwear.
outfit=[("clothing_shirt.glb",(0.62,0.48,0.29),"under-tunic"),
        ("clothing_jeans.glb",(0.22,0.14,0.075),"wool-trousers"),
        ("clothing_boots.glb",(0.32,0.16,0.055),"leather-boots"),
        ("clothing_dress.glb",(0.34,0.19,0.075),"wool-tunic")]
for filename,tint,label in outfit:
    path=os.path.join(ASSETS,filename)
    if not os.path.isfile(path):continue
    imported=import_gltf(path)
    rebind_import(imported,main_arm,root,label,tint)

# Short dark hair and a wrapped linen headband sit on the actual head-bone position.
hair_path=os.path.join(ASSETS,"hair_short04.glb")
if os.path.isfile(hair_path):
    imported=import_gltf(hair_path)
    rebind_import(imported,main_arm,root,"crew-hair",(0.055,0.04,0.025))

wrapmat=mat("Dark ochre linen turban",(0.29,0.19,0.085),0,.97)

# A fuller linen cap covers the scalp, retaining only the side hair around the temples.
head_bone=main_arm.data.bones.get("head")
if head_bone:
    hp=main_arm.matrix_world @ ((head_bone.head_local+head_bone.tail_local)*.5)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,location=(hp.x,hp.y,hp.z+.055))
    cap=bpy.context.object;cap.name="Linen turban crown";cap.scale=(.139,.151,.082);cap.data.materials.append(wrapmat)
    for poly in cap.data.polygons:poly.use_smooth=True
    # One diagonal wrapping strip, rising around the crown instead of stacked flat torus rings.
    curve=bpy.data.curves.new("Turban diagonal linen wrap","CURVE");curve.dimensions="3D";curve.resolution_u=2
    spl=curve.splines.new("POLY");count=160;spl.points.add(count-1)
    for i,pt in enumerate(spl.points):
        t=i/(count-1);ang=t*math.pi*2*2.15
        radius=.145-.022*t
        z=hp.z-.015+.125*t
        pt.co=(hp.x+radius*math.cos(ang),hp.y+radius*math.sin(ang),z,1)
    curve.bevel_depth=.018;curve.bevel_resolution=4
    wrap=bpy.data.objects.new("Diagonal turban cloth wrap",curve);scene.collection.objects.link(wrap);wrap.data.materials.append(wrapmat)
    # Attach the headwear to the moving head bone, preserving its evaluated world placement.
    for obj in (cap,wrap):
        wm=obj.matrix_world.copy();obj.parent=main_arm;obj.parent_type="BONE";obj.parent_bone="head";obj.matrix_world=wm

# Attach the imported animation clips and sample a relaxed mid-idle pose for the stills.
scene.render.fps=30;scene.render.fps_base=1
actions=sorted([a.name for a in bpy.data.actions])
if main_arm.animation_data is None:main_arm.animation_data_create()
idle=next((a for a in bpy.data.actions if "idle" in a.name.lower() and "breathe" not in a.name.lower()),None)
if idle:
    main_arm.animation_data.action=idle
    mid=int((idle.frame_range[0]+idle.frame_range[1])*.5)
    scene.frame_set(mid)

# Keep source scene timing at 30 fps for this still-frame asset proof; the final documentary is sampled at 240 fps.
scene.render.fps=30;scene.render.fps_base=1
actions=sorted([a.name for a in bpy.data.actions])
if main_arm.animation_data is None:main_arm.animation_data_create()
idle=next((a for a in bpy.data.actions if "idle" in a.name.lower()),None)
if idle:main_arm.animation_data.action=idle

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
scene.frame_set(1);bpy.ops.render.render(write_still=True)
bpy.ops.object.camera_add(location=(1.0,-3.05,1.65));closecam=bpy.context.object;closecam.name="Crew face and torso close-up";closecam.data.lens=72
close_target=Vector((0,0,1.42));closecam.rotation_euler=(close_target-closecam.location).to_track_quat("-Z","Y").to_euler();scene.camera=closecam
scene.render.filepath=os.path.abspath(os.path.join(OUT,"crew-closeup.png"));bpy.ops.render.render(write_still=True)
verts=sum(len(o.data.vertices) for o in export_objs if o.type=="MESH")
tris=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in export_objs if o.type=="MESH")
report={"status":"CHARACTER_ASSET_SMOKE_PASS_PENDING_VISUAL_REVIEW","source":"kblood/CharacterCreator/output","license":"CC0-1.0 for generated output assets per output/asset_licenses.json and LICENSE-NOTES.md","armature":main_arm.name,"bones":len(main_arm.data.bones),"actions":actions,"meshes":[o.name for o in export_objs if o.type=="MESH"],"materials":sorted({m.name for o in export_objs if o.type=="MESH" for m in o.data.materials if m}),"vertices":verts,"triangles":tris,"export_glb":os.path.basename(glb_out),"visual_approval":"pending","costume_note":"CC0-derived long tunic garment recoloured as muted wool, trousers, leather boots and a procedural linen turban. Illustrative historical adaptation, not authenticated Ottoman uniform."}
open(os.path.join(OUT,"manifest.json"),"w").write(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2),flush=True)
