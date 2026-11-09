#!/usr/bin/env python3
"""PBR-assisted Constantinople bombardment proof. Blender 4.x, native 240fps."""
import bpy, math, os
from mathutils import Vector

FPS = 30
TOTAL_FRAMES = 120
START = int(os.environ.get("BLENDER_FRAME_START", "1"))
END = int(os.environ.get("BLENDER_FRAME_END", str(TOTAL_FRAMES)))
OUTPUT = os.environ.get("BLENDER_OUTPUT", "out/rigged-crew-integration.mp4")
CHARACTER_GLB = os.environ.get("CHARACTER_GLB", "character/ottoman-artillery-crew-cc0.glb")
ASSETS = os.environ.get("HISTORICAL_ASSETS", "historical-assets")
SMOKE_ONLY = os.environ.get("BLENDER_SMOKE_ONLY", "0") == "1"

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.frame_start, scene.frame_end = START, END
scene.render.engine = "BLENDER_EEVEE"
scene.eevee.taa_render_samples = 8
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
scene.render.resolution_percentage = 100
scene.render.fps, scene.render.fps_base = FPS, 1.0
scene.render.image_settings.color_mode = "RGB"
scene.render.filepath = os.path.abspath(OUTPUT)
scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.ffmpeg.constant_rate_factor = "HIGH"
scene.render.ffmpeg.ffmpeg_preset = "GOOD"
scene.render.ffmpeg.video_bitrate = 38000
scene.render.ffmpeg.maxrate = 48000
scene.render.ffmpeg.buffersize = 80000
scene.render.threads_mode = "FIXED"
scene.render.threads = max(1, min(4, int(os.environ.get("BLENDER_THREADS", "2"))))
scene.render.use_file_extension = True
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure, scene.view_settings.gamma = 0.0, 1.0
scene.world.color = (0.055, 0.07, 0.09)

def mat_basic(name, color, metallic=0.0, roughness=0.7, alpha=1.0, emission=0.0):
    m = bpy.data.materials.new(name); m.diffuse_color = (*color, alpha); m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = (*color, alpha)
    bs.inputs["Metallic"].default_value = metallic; bs.inputs["Roughness"].default_value = roughness
    bs.inputs["Alpha"].default_value = alpha
    if emission:
        bs.inputs["Emission Color"].default_value = (*color, 1); bs.inputs["Emission Strength"].default_value = emission
    if alpha < 1:
        try: m.blend_method = "BLEND"
        except: pass
    return m

def cube(name, loc, scale, mat, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if mat: o.data.materials.append(mat)
    if bevel:
        b=o.modifiers.new("Worn arris","BEVEL"); b.width=bevel; b.segments=2
    return o

def cyl(name, loc, radius, depth, mat, vertices=32, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc)
    o=bpy.context.object; o.name=name
    if mat:o.data.materials.append(mat)
    if bevel:
        b=o.modifiers.new("Rounded edges","BEVEL"); b.width=bevel; b.segments=2
    return o

def sphere(name, loc, scale, mat, segments=20, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=loc)
    o=bpy.context.object;o.name=name;o.scale=scale
    if mat:o.data.materials.append(mat)
    return o

def between(name,a,b,r,mat,vertices=16):
    a,b=Vector(a),Vector(b);d=b-a
    o=cyl(name,(a+b)*.5,r,d.length,mat,vertices,.008)
    o.rotation_euler=d.to_track_quat("Z","Y").to_euler()
    return o

def key(o,prop,f,v):
    setattr(o,prop,v);o.keyframe_insert(data_path=prop,frame=f)

def smooth(o):
    if o.animation_data and o.animation_data.action:
        for fc in o.animation_data.action.fcurves:
            for k in fc.keyframe_points:
                k.interpolation="BEZIER";k.handle_left_type="AUTO_CLAMPED";k.handle_right_type="AUTO_CLAMPED"

# Load actual CC0 PBR stone maps. The fort model is used as a material source;
# the wall geometry is staged as an illustrative composite, not an exact measured replica.
fort_path=os.path.join(ASSETS,"models/downloaded/modular_fort_01/modular_fort_01_1k.gltf")
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=fort_path)
fort_objs=[o for o in bpy.data.objects if o not in before]
fort_mats={m.name:m for m in bpy.data.materials if m.name.startswith("modular_fort_01_")}
wall_mat=next((m for n,m in fort_mats.items() if "wall" in n),None)
trim_mat=next((m for n,m in fort_mats.items() if "trim" in n),None)
plaster_mat=next((m for n,m in fort_mats.items() if "plaster" in n),None)
for o in fort_objs:bpy.data.objects.remove(o,do_unlink=True)
if wall_mat is None: wall_mat=mat_basic("Fallback limestone",(0.43,.39,.32),roughness=.9)
if trim_mat is None: trim_mat=wall_mat
if plaster_mat is None: plaster_mat=wall_mat

bronze=mat_basic("Aged bronze",(.16,.095,.045),.78,.3)
oak=mat_basic("Weathered oak",(.15,.075,.035),.05,.82)
iron=mat_basic("Forged iron",(.065,.075,.075),.72,.42)
shotmat=mat_basic("Rough limestone shot",(.27,.26,.23),0,.95)
earth=mat_basic("Damp trampled earth",(.10,.078,.056),0,.96)
red=mat_basic("Muted Ottoman crimson",(.18,.035,.025),0,.92)
blue=mat_basic("Byzantine deep blue",(.035,.07,.12),0,.92)
skin=mat_basic("Skin in shadow",(.24,.14,.095),0,.88)
smoke=mat_basic("Powder smoke translucent",(.19,.18,.17),0,1,.22)
dust=mat_basic("Limestone dust",(.52,.45,.35),0,1,.18)
fire=mat_basic("Powder ignition", (.98,.16,.025),0,.38,1,4.2)

# Ground, layered stone wall, battlements and towers.
cube("Trampled siege earth",(0,2,-.55),(60,70,1),earth,.12)
cube("Wall inner core",(0,16,3.4),(25,1.7,6.8),wall_mat,.08)
for row in range(5):
    z=.65+row*1.27
    for col in range(15):
        x=-11.2+col*1.6+(.8 if row%2 else 0)
        if row in (2,3) and 6<=col<=8: continue
        b=cube("Ashlar wall block",(x,15.03,z),(1.54,.42,1.18),wall_mat,.035)
        if (row+col)%3==0:b.rotation_euler[1]=math.radians((col%3-1)*1.1)
for x in (-11.8,11.8):
    cyl("Round wall tower",(x,16,4),1.72,8,plaster_mat,48,.08)
    cyl("Tower stone rim",(x,16,7.95),1.92,.48,trim_mat,48,.04)
    for i in range(12):
        a=i*math.tau/12
        b=cube("Tower merlon",(x+1.83*math.cos(a),16+1.83*math.sin(a),8.5),(.6,.6,.82),trim_mat,.04)
        b.rotation_euler[2]=a
cube("Wall walk",(0,14.15,6.45),(23.4,1.25,.45),trim_mat,.05)
for x in range(-11,12,2):cube("Parapet merlon",(x,14.9,7.25),(.92,.66,1.1),trim_mat,.05)
for x in (-2.4,0,2.4):
    between("Scaffold upright",(x,15.8,.1),(x,15.8,6.5),.11,oak,12)
    between("Scaffold crossbeam",(x-1.2,15.8,2.5),(x+1.2,15.8,2.5),.08,oak,12)
    between("Scaffold brace",(x-1,15.8,.5),(x+1,15.8,3),.055,iron,10)

# Import the textured Poly Haven cannon as a single animated assembly.
cannon_path=os.path.join(ASSETS,"models/downloaded/cannon_01/cannon_01_1k.gltf")
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=cannon_path)
parts=[o for o in bpy.data.objects if o not in before]
gun=bpy.data.objects.new("CC0 Poly Haven cannon assembly root",None);scene.collection.objects.link(gun)
for o in parts:
    if "ball_" in o.name.lower():
        o.hide_render=True
        o.hide_viewport=True
        continue
    mw=o.matrix_world.copy();o.parent=gun;o.matrix_world=mw
gun.location=(0,-7,0);gun.rotation_euler=(0,0,math.pi);gun.scale=(4,4,4)
bpy.context.view_layer.update()
bbox=[gun.matrix_world@Vector(c) for o in parts if o.type=="MESH" for c in o.bound_box]
if bbox:gun.location.z+=-min(v.z for v in bbox)+.12
base=gun.location.copy()
for f,loc in [(1,base),(1400,base),(1460,base+Vector((0,-.42,.08))),(1500,base+Vector((0,-.7,0))),(1560,base+Vector((0,-.25,0))),(1680,base)]:
    key(gun,"location",f,loc)
smooth(gun)

# Import the approved rigged character once, then clone the armature and skinned meshes per performer.
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=os.path.abspath(CHARACTER_GLB))
crew_source=[o for o in bpy.data.objects if o not in before and o.type in {"MESH","ARMATURE"}]
source_arm=next((o for o in crew_source if o.type=="ARMATURE"),None)
assert source_arm is not None,"rigged CC0 crew GLB has no armature"
source_meshes=[o for o in crew_source if o.type=="MESH"]
def crew(name,x,y,side,action_name="idle_Armature",yaw=None,scale=1.0,walk_to=None):
    root=bpy.data.objects.new(name+" actor root",None);scene.collection.objects.link(root)
    yaw=(math.pi if side=="ottoman" else 0.0) if yaw is None else yaw
    root.location=(x,y,0);root.rotation_euler=(0,0,yaw);root.scale=(scale,scale,scale)
    arm=source_arm.copy();arm.data=source_arm.data
    scene.collection.objects.link(arm)
    arm_world=source_arm.matrix_world.copy();arm.parent=root;arm.matrix_world=arm_world
    arm.animation_data_clear();arm.animation_data_create()
    action=next((a for a in bpy.data.actions if a.name.startswith(action_name)),None)
    if action is None:action=next((a for a in bpy.data.actions if a.name.startswith("idle_Armature")),None)
    if action:arm.animation_data.action=action
    for src in source_meshes:
        mesh=src.copy();mesh.data=src.data
        scene.collection.objects.link(mesh)
        world=src.matrix_world.copy();mesh.parent=root;mesh.matrix_world=world
        for mod in mesh.modifiers:
            if mod.type=="ARMATURE":mod.object=arm
        if not any(mod.type=="ARMATURE" for mod in mesh.modifiers) and len(mesh.vertex_groups):
            mod=mesh.modifiers.new("Crew skinning","ARMATURE");mod.object=arm
        # Give every performer independent materials for small clothing-palette variations.
        for i,mat in enumerate(list(mesh.data.materials)):
            if mat is not None:
                variant=mat.copy();variant.name=name+" "+mat.name
                mesh.data.materials[i]=variant
                bs=next((n for n in variant.node_tree.nodes if n.type=="BSDF_PRINCIPLED"),None) if variant.use_nodes else None
                if bs and "trenchcoat" in mat.name.lower():
                    tint=(.42,.19,.075) if side=="ottoman" else (.19,.23,.28)
                    sock=bs.inputs.get("Base Color")
                    if sock and not sock.is_linked:sock.default_value=(*tint,1)
    if walk_to is not None:
        key(root,"location",1,(x,y,0));key(root,"location",120,(walk_to[0],walk_to[1],0));smooth(root)
    print("RIGGED_CREW",name,"action",action.name if action else "none","meshes",len(source_meshes),flush=True)
    return root,arm
crew("Powder crew",-2.1,-8.5,"ottoman","idle_breathe_Armature")
crew("Rammer crew",2.1,-8.1,"ottoman","walk_Armature",scale=.98,walk_to=(2.6,-7.6))
crew("Carriage brace",-3,-6.5,"ottoman","idle_look_Armature",scale=1.03)
crew("Carriage hauler",3,-6.7,"ottoman","walk_Armature",scale=1.01,walk_to=(3.35,-6.0))
crew("Wall defender",-3.2,13.2,"byzantine","idle_Armature",yaw=0)
crew("Wall defender",3,13.4,"byzantine","idle_look_Armature",yaw=0,scale=.98)
# Remove the unused source import after all six independent performers have been cloned.
for o in crew_source:bpy.data.objects.remove(o,do_unlink=True)

for x in (-4,4.2):
    cyl("Powder cask",(x,-8.5,.65),.48,1.2,oak,24,.04)
    cyl("Cask iron hoop",(x,-8.5,.42),.51,.09,iron,24,.01)
    cyl("Cask iron hoop",(x,-8.5,.85),.51,.09,iron,24,.01)
for i in range(5):sphere("Spare stone shot",(-5+i*.58,-10.3,.52),(.24,.24,.24),shotmat,16,10)

# Ballistic shot, recoil, flash, smoke, wall impact and debris.
# Derive the muzzle from the imported barrel mesh, rather than guessing screen-space coordinates.
barrel_obj=next((o for o in parts if o.type=="MESH" and "barrel" in o.name.lower()),None)
bpy.context.view_layer.update()
if barrel_obj:
    barrel_corners=[barrel_obj.matrix_world @ Vector(v) for v in barrel_obj.bound_box]
    front_y=max(v.y for v in barrel_corners)
    muzzle=Vector((sum(v.x for v in barrel_corners)/len(barrel_corners),front_y,
                   sum(v.z for v in barrel_corners)/len(barrel_corners)))
else:
    muzzle=Vector((0,-1.7,2.55))
shot_dir=Vector((0,1,0))
shot_start=muzzle-shot_dir*.42
impact=Vector((1,15.2,2.4))
span=impact-muzzle
ball=sphere("Heavy limestone cannon shot",shot_start,(.34,.34,.34),shotmat,24,16)
trajectory=[(1,shot_start),(1450,shot_start),(1500,muzzle+shot_dir*.24),
            (1650,muzzle+span*.25+Vector((0,0,1.65))),
            (1850,muzzle+span*.53+Vector((0,0,2.8))),
            (2070,muzzle+span*.80+Vector((0,0,2.1))),
            (2250,Vector((1,14.65,3.2))),(2300,impact),(END,impact)]
for f,loc in trajectory:key(ball,"location",f,loc)
smooth(ball)
# Tapered directional fire is aligned to the true muzzle axis.
bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=.30,radius2=.012,depth=1.0,location=muzzle+shot_dir*.5)
flash=bpy.context.object;flash.name="Directional muzzle flame"
flash.rotation_euler=shot_dir.to_track_quat("Z","Y").to_euler();flash.data.materials.append(fire)
for f,s in [(1,(.001,)*3),(1460,(.001,)*3),(1500,(.70,.82,.70)),(1512,(.38,.48,.38)),(1545,(.001,)*3)]:
    key(flash,"scale",f,s)
smooth(flash)
ld=bpy.data.lights.new("Cannon muzzle flash","POINT");ld.energy=0;ld.color=(1,.29,.08);ld.shadow_soft_size=2.0
lo=bpy.data.objects.new("Cannon muzzle flash light",ld);scene.collection.objects.link(lo);lo.location=muzzle+shot_dir*.28
for f,e in [(1,0),(1495,0),(1500,1450),(1510,420),(1545,0)]:key(ld,"energy",f,e)
smoke_puffs=[]
for i in range(24):
    origin=muzzle+shot_dir*.2
    p=sphere("Powder smoke plume",origin,(.1,.1,.1),smoke,16,10)
    a=i*2.399;end=origin+Vector((math.cos(a)*(.8+(i%5)*.2),1.2+(i%6)*.42,1.5+(i%7)*.3))
    for f,loc,sc in [(1,origin,(.001,)*3),(1500,origin,(.12,)*3),(1590,end,(.55+(i%4)*.16,)*3),
                     (1800,end+Vector((0,1,1)),(.85+(i%3)*.2,)*3),(2050,end+Vector((0,2.5,1.6)),(.001,)*3)]:
        key(p,"location",f,loc);key(p,"scale",f,sc)
    smooth(p);smoke_puffs.append(p)
for i in range(34):
    a=i*2.399;start=Vector((1,15,3))
    end=start+Vector((math.cos(a)*(1+(i%5)*.36),-1-(i%4)*.3,.7+(i%6)*.3))
    b=cube("Flying broken ashlar",start,(.22+(i%3)*.08,.20,.2+(i%4)*.04),trim_mat,.015)
    for f,loc in [(1,start),(2240,start),(2300,end),(2460,end+Vector((0,-.7,-1.5))),(2600,end+Vector((0,-1,-2.2)))]:
        key(b,"location",f,loc)
    for f,rot in [(1,(0,0,0)),(2300,(a,.3,a)),(2600,(a+1.5,1,a+1.2))]:key(b,"rotation_euler",f,rot)
    smooth(b)
for i in range(22):
    a=i*2.399;p=sphere("Impact dust cloud",(1,15,3.4),(.12,.12,.12),dust,14,8)
    end=Vector((1+math.cos(a)*(1.4+(i%4)*.38),14.3+math.sin(a)*.55,4.2+(i%6)*.36))
    for f,loc,sc in [(1,(1,15,3.4),(.001,)*3),(2290,(1,15,3.4),(.001,)*3),
                     (2300,(1,15,3.4),(.18,)*3),(2480,end,(.8+(i%3)*.2,)*3),(2690,end+Vector((0,0,.5)),(.001,)*3)]:
        key(p,"location",f,loc);key(p,"scale",f,sc)
    smooth(p)

# Plain standards: no invented heraldry.
for idx,x in enumerate((-8.5,8.5)):
    cyl("Camp standard pole",(x,-11,4.2),.055,8.2,oak,12)
    banner=cube("Plain crimson banner",(x+.8,-11,6.2),(1.5,.08,1.8),red,.02)
    key(banner,"rotation_euler",1,(0,0,0));key(banner,"rotation_euler",END,(.08,.04,.10 if idx else -.12));smooth(banner)

world=scene.world;world.use_nodes=True
world.node_tree.nodes.get("Background").inputs["Color"].default_value=(.16,.20,.25,1)
world.node_tree.nodes.get("Background").inputs["Strength"].default_value=.35
def area(name,loc,energy,color,size,target):
    d=bpy.data.lights.new(name,"AREA");d.energy=energy;d.color=color;d.shape="DISK";d.size=size
    o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc
    o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler();return o
sd=bpy.data.lights.new("Dawn sun","SUN");sd.energy=2.1;sd.angle=math.radians(12);sd.color=(1,.73,.52)
sun=bpy.data.objects.new("Dawn sun",sd);scene.collection.objects.link(sun);sun.rotation_euler=(math.radians(32),math.radians(-18),math.radians(-25))
area("Warm key",(-10,-12,18),1500,(1,.82,.67),10,(0,5,3))
area("Cool sky fill",(10,-2,13),1250,(.58,.72,.88),12,(0,7,4))
area("Wall rim",(0,22,14),1450,(1,.68,.48),9,(0,15,4))
area("Bronze highlight",(-6,-5,5),900,(1,.52,.24),4,(0,-4,2))

def camera_shot(name,start,end,la,lb,ta,tb,lens,label):
    bpy.ops.object.camera_add(location=la);cam=bpy.context.object;cam.name=name;cam.data.lens=lens;cam.data.sensor_width=36
    target=bpy.data.objects.new(name+" focus",None);scene.collection.objects.link(target);target.location=ta
    c=cam.constraints.new(type="TRACK_TO");c.target=target;c.track_axis="TRACK_NEGATIVE_Z";c.up_axis="UP_Y"
    key(cam,"location",start,la);key(cam,"location",end,lb);key(target,"location",start,ta);key(target,"location",end,tb)
    smooth(cam);smooth(target);cam.data.dof.use_dof=True;cam.data.dof.focus_object=target;cam.data.dof.aperture_fstop=3.8
    marker=scene.timeline_markers.new(label,frame=start);marker.camera=cam
    return cam
cam1=camera_shot("01 bronze macro reveal",1,600,(4.4,-13,4.2),(1.7,-10.5,3.6),(0,-5,2.8),(0,-3.4,2.8),58,"01 — THE GREAT BOMBARD")
cam2=camera_shot("02 gun crew and wall",1,120,(8.4,-17,7.4),(5.4,-15,6),(0,-3,2.1),(0,2,2.8),38,"02 — SLOW TO LOAD")
cam3=camera_shot("03 recoil and smoke",1201,1800,(-8,-15,6.2),(-4.5,-11,5.2),(0,-4,2.6),(0,-1.8,3.1),36,"03 — FIRE")
cam4=camera_shot("04 projectile flight",1801,2280,(3,-1,9),(3.7,7.5,7),(0,5,4.5),(1,12,4.8),52,"04 — STONE SHOT")
cam5=camera_shot("05 wall impact",2281,END,(8.2,8.5,6.8),(6,11.8,5.5),(1,15.5,3.4),(1,15.5,3.1),45,"05 — THE WALL")
scene.camera=cam2
for f,loc in [(1480,(-3.02,-8.58,4.02)),(1500,(-2.85,-8.42,4.14)),(1520,(-3.12,-8.72,3.90)),(1560,(-3,-8.6,4))]:
    key(cam3,"location",f,loc)
smooth(cam3)
for f,loc in [(2300,(8.05,8.35,6.68)),(2320,(8.3,8.65,6.92)),(2350,(7.9,8.2,6.55)),(2420,(8.1,8.4,6.8))]:
    key(cam5,"location",f,loc)
smooth(cam5)

notes=bpy.data.texts.new("RECONSTRUCTION-NOTES.txt")
notes.write("Illustrative 3D reconstruction of Ottoman artillery at Constantinople in 1453. Hero cannon mesh and modular-fort PBR materials are Poly Haven CC0 assets. Generic gun stand-in, not an authenticated replica of Orban's great bombard. Wall is an illustrative modular arrangement, not a measured reconstruction of the Theodosian walls. Human silhouettes are not authenticated costumes or portraits. Native 1920x1080 at 240fps.\n")
scene.frame_set(START)
print("CONSTANTINOPLE RIGGED CREW INTEGRATION",bpy.app.version_string,"frames",f"{START}-{END}/{TOTAL_FRAMES}","objects",len(scene.objects),"cannon parts",len(parts),"wall material",wall_mat.name if wall_mat else "fallback",flush=True)
if SMOKE_ONLY:
    scene.render.image_settings.file_format="PNG";scene.render.filepath=os.path.abspath(os.environ.get("SMOKE_OUTPUT","out/pbr-smoke.png"))
    os.makedirs(os.path.dirname(scene.render.filepath),exist_ok=True)
    bpy.ops.render.render(write_still=True);print("PBR ONE-FRAME SMOKE FINISHED",flush=True)
else:
    os.makedirs(os.path.dirname(os.path.abspath(OUTPUT)),exist_ok=True)
    bpy.ops.render.render(animation=True);print("PBR PROOF RENDER FINISHED",flush=True)
