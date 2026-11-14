#!/usr/bin/env python3
"""Render an explicitly illustrative 3D siege-engine cut-in from verified CC0 library assets.

The siege-tower / ram / trebuchet are generic Kenney Castle Kit props, not
historically authenticated reconstructions of weapons used at Constantinople.
The wall material is Poly Haven Castle Brick 02 Red (CC0). The crew model is
a separately provenance-checked CC0-derived CharacterCreator export.
"""
from __future__ import annotations
import bpy, hashlib, json, math, os
from pathlib import Path
from mathutils import Vector

ROOT = Path(os.environ.get("CUTIN_ASSETS", "assets")).resolve()
ASSETS = ROOT / "models"
TEXTURES = ROOT / "textures"
CHARACTER = ROOT / "character" / "ottoman-artillery-crew-cc0.glb"
MANIFEST = ROOT / "CUTIN-ASSET-MANIFEST.json"
OUTPUT = Path(os.environ.get("BLENDER_OUTPUT", "out/constantinople-siege-engine-cutin.mp4")).resolve()
START = int(os.environ.get("BLENDER_FRAME_START", "1"))
END = int(os.environ.get("BLENDER_FRAME_END", "1920"))
SMOKE_ONLY = os.environ.get("BLENDER_SMOKE_ONLY", "0") == "1"
SMOKE_FRAME = int(os.environ.get("BLENDER_SMOKE_FRAME", "960"))
THREADS = int(os.environ.get("BLENDER_THREADS", "3"))
FPS = 240
TOTAL = 1920
SEQUENCE_SECONDS = TOTAL / FPS

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def require_file(path: Path, expected: str | None = None) -> Path:
    if not path.is_file() or path.stat().st_size <= 0:
        raise FileNotFoundError(path)
    if expected and sha256(path) != expected:
        raise RuntimeError(f"SHA-256 mismatch: {path}")
    return path

def ensure_kenney_colormap_placeholder():
    """Create a temporary neutral atlas so Blender can resolve the GLB sidecar at import.

    This is not the missing Kenney texture. Its nodes are replaced immediately
    after import with explicit generated stone/wood/iron materials.
    """
    path=ASSETS/"Textures"/"colormap.png"
    path.parent.mkdir(parents=True,exist_ok=True)
    if not path.is_file():
        image=bpy.data.images.new("Project-generated neutral Kenney fallback atlas",width=64,height=64,alpha=False)
        pixels=[]
        for y in range(64):
            for x in range(64):
                grain=0.012*math.sin(x*.37)*math.cos(y*.29)
                r=max(0,min(1,.46+grain));g=max(0,min(1,.35+grain));b=max(0,min(1,.23+grain))
                pixels.extend((r,g,b,1.0))
        image.pixels[:]=pixels
        image.filepath_raw=str(path)
        image.file_format="PNG"
        image.save()
        bpy.data.images.remove(image)
    return {
        "path":str(path),
        "bytes":path.stat().st_size,
        "sha256":sha256(path),
        "license":"Project-generated neutral placeholder; not a Kenney source texture",
        "purpose":"Satisfy the GLB's optional colormap sidecar reference before replacing its material nodes"
    }


def material(name, color, metallic=0.0, roughness=.75):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value=(*color,1)
    bs.inputs["Metallic"].default_value=metallic
    bs.inputs["Roughness"].default_value=roughness
    return m

def cube(name, loc, scale, mat, bevel=.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:o.data.materials.append(mat)
    if bevel:
        mod=o.modifiers.new("Worn softened edges","BEVEL");mod.width=bevel;mod.segments=2
        o.modifiers.new("Weighted corner normals","WEIGHTED_NORMAL")
    return o

def cylinder(name, loc, radius, depth, mat, vertices=32, rotation=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o=bpy.context.object;o.name=name
    if rotation:o.rotation_euler=rotation
    if mat:o.data.materials.append(mat)
    return o

def area_light(name, loc, target, energy, color, size):
    bpy.ops.object.light_add(type="AREA", location=loc)
    o=bpy.context.object;o.name=name;o.data.energy=energy;o.data.color=color;o.data.shape="DISK";o.data.size=size
    o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()
    return o

def pbr_brick():
    mat=bpy.data.materials.new("Poly Haven CC0 castle_brick_02_red")
    mat.use_nodes=True
    nodes=mat.node_tree.nodes;links=mat.node_tree.links;bs=nodes.get("Principled BSDF")
    bs.inputs["Roughness"].default_value=.88
    uv=nodes.new("ShaderNodeTexCoord")
    mapping=nodes.new("ShaderNodeMapping");mapping.inputs["Scale"].default_value=(5.0,2.5,3.0)
    links.new(uv.outputs["UV"],mapping.inputs["Vector"])
    diff=bpy.data.images.load(str(TEXTURES/"castle_brick_02_red_diff_1k.jpg"), check_existing=True)
    dnode=nodes.new("ShaderNodeTexImage");dnode.image=diff;dnode.extension="REPEAT"
    links.new(mapping.outputs["Vector"],dnode.inputs["Vector"])
    links.new(dnode.outputs["Color"],bs.inputs["Base Color"])
    normal=bpy.data.images.load(str(TEXTURES/"castle_brick_02_red_nor_gl_1k.jpg"), check_existing=True)
    normal.colorspace_settings.name="Non-Color"
    nnode=nodes.new("ShaderNodeTexImage");nnode.image=normal;nnode.extension="REPEAT"
    nmap=nodes.new("ShaderNodeNormalMap");nmap.inputs["Strength"].default_value=.62
    links.new(mapping.outputs["Vector"],nnode.inputs["Vector"])
    links.new(nnode.outputs["Color"],nmap.inputs["Color"])
    links.new(nmap.outputs["Normal"],bs.inputs["Normal"])
    return mat

def terrain_material():
    m=material("Trampled siege field",(.13,.105,.073),0,.96)
    nodes=m.node_tree.nodes;links=m.node_tree.links;bs=nodes.get("Principled BSDF")
    tex=nodes.new("ShaderNodeTexNoise");tex.inputs["Scale"].default_value=3.2;tex.inputs["Detail"].default_value=5
    ramp=nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color=(.035,.025,.017,1)
    ramp.color_ramp.elements[1].color=(.24,.17,.095,1)
    bump=nodes.new("ShaderNodeBump");bump.inputs["Strength"].default_value=.28;bump.inputs["Distance"].default_value=.12
    links.new(tex.outputs["Fac"],ramp.inputs["Fac"]);links.new(ramp.outputs["Color"],bs.inputs["Base Color"])
    links.new(tex.outputs["Fac"],bump.inputs["Height"]);links.new(bump.outputs["Normal"],bs.inputs["Normal"])
    return m

def repair_missing_prop_textures(imported):
    """Replace broken optional Kenney atlas references with deterministic earthy materials.

    Build 76 contains the exact GLB geometry but not the original Castle Kit
    colormap.png sidecar. We therefore remove only missing image-node links and
    preserve the material slots with neutral, source-honest fallback colors.
    """
    replacements=0
    for obj in imported:
        if obj.type!="MESH":
            continue
        for slot in obj.material_slots:
            mat=slot.material
            if not mat or not mat.use_nodes:
                continue
            nodes=mat.node_tree.nodes
            links=mat.node_tree.links
            missing=False
            for node in list(nodes):
                if node.type!="TEX_IMAGE" or not node.image:
                    continue
                filepath=Path(bpy.path.abspath(node.image.filepath))
                is_project_placeholder=filepath.name.casefold()=="colormap.png"
                if not filepath.is_file() or is_project_placeholder:
                    missing=True
                    for link in list(links):
                        if link.from_node==node or link.to_node==node:
                            links.remove(link)
                    nodes.remove(node)
            if missing:
                label=(obj.name+" "+mat.name).casefold()
                if any(k in label for k in ("iron","metal","chain","bolt","nail")):
                    color=(.075,.085,.092,1)
                elif any(k in label for k in ("stone","brick","wall","rock","tower")):
                    color=(.34,.30,.24,1)
                elif any(k in label for k in ("cloth","canvas","rope","banner")):
                    color=(.42,.32,.20,1)
                else:
                    color=(.20,.12,.065,1)
                bs=nodes.get("Principled BSDF")
                if bs:
                    bs.inputs["Base Color"].default_value=color
                    bs.inputs["Roughness"].default_value=.84
                mat.diffuse_color=color
                replacements+=1
    return replacements


def import_prop(path: Path, name: str, target_height: float, x: float, y_start: float, y_end: float):
    before=set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    imported=[o for o in bpy.data.objects if o not in before]
    meshes=[o for o in imported if o.type=="MESH"]
    if not meshes:raise RuntimeError(f"GLB imported no meshes: {path}")
    bpy.context.view_layer.update()
    coords=[o.matrix_world @ Vector(corner) for o in meshes for corner in o.bound_box]
    min_v=Vector((min(v.x for v in coords),min(v.y for v in coords),min(v.z for v in coords)))
    max_v=Vector((max(v.x for v in coords),max(v.y for v in coords),max(v.z for v in coords)))
    height=max_v.z-min_v.z
    if height<=0:raise RuntimeError(f"Invalid GLB bounds: {path}")
    factor=target_height/height
    root=bpy.data.objects.new(name+" motion root",None);bpy.context.scene.collection.objects.link(root)
    for o in imported:
        if o.type in {"MESH","ARMATURE","EMPTY"}:
            world=o.matrix_world.copy();o.parent=root;o.matrix_world=world
    bpy.context.view_layer.update()
    root.scale=(factor,factor,factor)
    base_x=x-(min_v.x+max_v.x)*.5*factor
    base_y=y_start-(min_v.y+max_v.y)*.5*factor
    base_z=-min_v.z*factor
    root.location=(base_x,base_y,base_z)
    root.keyframe_insert(data_path="location",frame=1)
    root.location.y=y_end-(min_v.y+max_v.y)*.5*factor
    root.keyframe_insert(data_path="location",frame=TOTAL)
    if root.animation_data and root.animation_data.action:
        for fc in root.animation_data.action.fcurves:
            for kp in fc.keyframe_points:kp.interpolation="BEZIER"
    # Animate any wheel-like mesh around its local axle; the full root still advances as one unit.
    for o in imported:
        if "wheel" in o.name.casefold() or "roller" in o.name.casefold():
            r0=o.rotation_euler.copy();o.keyframe_insert(data_path="rotation_euler",frame=1)
            o.rotation_euler.x+=math.tau*3;o.keyframe_insert(data_path="rotation_euler",frame=TOTAL)
    missing_texture_replacements=repair_missing_prop_textures(imported)
    return root, imported, missing_texture_replacements

def import_worker(path: Path, name: str, x: float, y: float, action_stem: str, yaw: float=0.0, scale: float=1.0):
    before=set(bpy.data.objects)
    actions_before=set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=str(path))
    imported=[o for o in bpy.data.objects if o not in before]
    armatures=[o for o in imported if o.type=="ARMATURE"]
    if not armatures:raise RuntimeError(f"Character GLB has no armature: {name}")
    arm=armatures[0];arm.name=name+" Armature"
    arm.location=(x,y,0);arm.rotation_euler.z=yaw;arm.scale=(scale,scale,scale)
    candidates=[a for a in bpy.data.actions if a.name.startswith(action_stem)]
    if candidates:
        action=candidates[-1].copy();action.name=name+" "+action_stem
        # CharacterCreator actions are authored around 30fps; stretch them to the 240fps timeline.
        for fc in action.fcurves:
            first=min((kp.co.x for kp in fc.keyframe_points),default=0)
            for kp in fc.keyframe_points:
                kp.co.x=first+(kp.co.x-first)*8
                kp.handle_left.x=first+(kp.handle_left.x-first)*8
                kp.handle_right.x=first+(kp.handle_right.x-first)*8
        arm.animation_data_create();arm.animation_data.action=action
    for o in imported:
        if o.type=="MESH" and not o.parent:
            o.parent=arm
    return {"name":name,"action":action_stem,"armature":arm.name,"mesh_count":sum(o.type=="MESH" for o in imported)}

def look_at(obj, target):
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()

def build_scene():
    scene=bpy.context.scene
    scene.render.engine="BLENDER_EEVEE_NEXT" if bpy.app.version >= (4,2,0) else "BLENDER_EEVEE"
    scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100
    scene.render.fps=FPS;scene.render.fps_base=1
    scene.render.image_settings.color_mode="RGB"
    scene.render.image_settings.color_depth="8"
    scene.view_settings.view_transform="AgX"
    if hasattr(scene,"eevee"):
        scene.eevee.taa_render_samples=16
        scene.eevee.use_gtao=True
        scene.eevee.gtao_distance=3
        scene.eevee.gtao_factor=1.3
    world=bpy.data.worlds.new("Cinematic overcast dusk") if not bpy.data.worlds else bpy.data.worlds[0]
    scene.world=world;world.use_nodes=True
    bg=world.node_tree.nodes.get("Background");bg.inputs["Color"].default_value=(.12,.16,.21,1);bg.inputs["Strength"].default_value=.35

    ground=terrain_material()
    bpy.ops.mesh.primitive_plane_add(size=220,location=(0,0,-.12))
    bpy.context.object.name="Wide muddy siege field";bpy.context.object.data.materials.append(ground)
    brick=pbr_brick()
    # Massive Theodosian-style wall as a cinematic stand-in, not a surveyed reconstruction.
    cube("Stone curtain wall",(0,11,5.6),(34,3.0,11.2),brick,.22)
    cube("Wall parapet",(0,9.5,10.7),(34,1.0,1.1),brick,.10)
    for x in range(-16,17,2):
        cube("Wall merlon",(x,9.4,11.65),(1.3,1.4,1.0),brick,.07)
    for x in (-14,14):
        cube("Wall tower",(x,11,7.5),(4.7,4.7,15.0),brick,.20)
        cube("Tower crown",(x,11,15.2),(5.6,5.6,1.3),brick,.12)
        for k in range(-2,3):
            cube("Tower crenel",(x+k*.9,8.2,16.2),(.65,1.0,1.0),brick,.04)
    # Timber palisade and siege stores add foreground scale.
    oak=material("Weathered siege timber",(.18,.105,.055),0,.86)
    canvas=material("Undyed linen canvas",(.39,.31,.21),0,.95)
    iron=material("Dark forged iron",(.075,.082,.085),.68,.42)
    for i in range(6):
        x=-18+i*7
        cube("Siege supply chest",(x,-8,.55),(1.8,1.2,1.1),oak,.07)
    for i,x in enumerate((-18,-10,10,18)):
        bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=3.1,radius2=.05,depth=3.6,location=(x,-16,1.75))
        bpy.context.object.name="Siege camp A-frame tent";bpy.context.object.data.materials.append(canvas)
        cylinder("Tent ridge pole",(x,-16,3.6),.08,6.0,oak,12,(math.pi/2,0,0))
    # A small number of torches provide warm points, not a fantasy wall of fire.
    firemat=material("Torch flame",(.95,.31,.055),0,.4)
    for x,y in [(-15,-11),(-7,-19),(9,-18),(17,-12)]:
        cylinder("Torch post",(x,y,1.5),.08,2.8,oak,12)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.25,location=(x,y,3.0))
        bpy.context.object.data.materials.append(firemat)
        area_light("Torch practical",(x,y,3.5),(x,0,5),140,(1.0,.42,.16),3.0)

    # Import the actual CC0 Castle Kit assets and animate the siege approach.
    tower,tower_objects,tower_repaired=import_prop(ASSETS/"siege-tower.glb","CC0 Castle Kit siege tower",13.8,-3.0,-19.0,-9.0)
    ram,ram_objects,ram_repaired=import_prop(ASSETS/"siege-ram.glb","CC0 Castle Kit siege ram",4.8,8.2,-17.0,-10.5)
    trebuchet,trebuchet_objects,trebuchet_repaired=import_prop(ASSETS/"siege-trebuchet.glb","CC0 Castle Kit trebuchet",5.5,-13.0,-20.0,-17.0)

    crew=[]
    crew.extend(import_worker(CHARACTER,"Ottoman artillery crew left", -7.0,-7.5,"walk_Armature",yaw=.15,scale=1.0) for _ in range(1))
    crew.extend(import_worker(CHARACTER,"Ottoman artillery crew center", 1.5,-6.0,"run_Armature",yaw=-.25,scale=1.02) for _ in range(1))
    crew.extend(import_worker(CHARACTER,"Ottoman artillery crew ram", 10.5,-8.5,"walk_Armature",yaw=.25,scale=.96) for _ in range(1))
    crew.extend(import_worker(CHARACTER,"Ottoman artillery guard", -10.5,-10.0,"idle_Armature",yaw=0,scale=.96) for _ in range(1))
    # Camera performs a slow dolly, then lowers toward the approaching tower.
    bpy.ops.object.camera_add(location=(23,-31,17))
    cam=bpy.context.object;cam.name="Low-angle siege-engine tracking camera";cam.data.lens=43
    look_at(cam,(0,2,6));scene.camera=cam
    for frame,loc,target in [
        (1,(23,-31,17),(0,2,6)),
        (720,(21,-25,15),(0,3,6)),
        (1440,(17,-18,12),(0,6,7)),
        (TOTAL,(14,-14,10),(0,8,8))
    ]:
        cam.location=loc;look_at(cam,target)
        cam.keyframe_insert(data_path="location",frame=frame)
        cam.keyframe_insert(data_path="rotation_euler",frame=frame)
    for fc in cam.animation_data.action.fcurves:
        for kp in fc.keyframe_points:kp.interpolation="BEZIER"
    # Warm sun, cool fill and wall rim light.
    bpy.ops.object.light_add(type="SUN",location=(-10,-18,25))
    sun=bpy.context.object;sun.name="Overcast late-afternoon key";sun.data.energy=2.2;sun.data.angle=math.radians(28)
    sun.rotation_euler=(math.radians(24),math.radians(-32),math.radians(-24))
    area_light("Cool skyline fill",(18,-5,18),(0,4,6),2100,(.54,.68,1.0),14)
    area_light("Warm tower rim",(-14,10,20),(0,-5,7),2600,(1.0,.62,.34),12)
    area_light("Front soft bounce",(0,-22,10),(0,5,6),1300,(.72,.80,1.0),18)

    # Fine airborne dust and light drifting smoke, deliberately restrained.
    dustmat=material("Airborne ochre dust",(.47,.35,.22),0,1.0)
    for i in range(42):
        x=-18+(i*37)%36;y=-16+(i*23)%28;z=1.0+(i*17)%12
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=6,radius=.075+(i%4)*.025,location=(x,y,z))
        p=bpy.context.object;p.name="Suspended siege dust";p.data.materials.append(dustmat)
        p.keyframe_insert(data_path="location",frame=1)
        p.location.z+=.7+(i%5)*.24;p.location.x+=.15*math.sin(i);p.keyframe_insert(data_path="location",frame=TOTAL)
    # Every imported crew member must be a real rig with an assigned action.
    assert len(crew)==4 and all(x["action"] for x in crew), crew
    scene.frame_start=1;scene.frame_end=TOTAL
    return {
        "crew":crew,
        "tower_objects":len(tower_objects),
        "ram_objects":len(ram_objects),
        "trebuchet_objects":len(trebuchet_objects),
        "missing_texture_fallback_slots":tower_repaired+ram_repaired+trebuchet_repaired
    }

def main():
    for p in [
        ASSETS/"siege-tower.glb",ASSETS/"siege-ram.glb",ASSETS/"siege-trebuchet.glb",
        TEXTURES/"castle_brick_02_red_diff_1k.jpg",TEXTURES/"castle_brick_02_red_nor_gl_1k.jpg",
        CHARACTER,MANIFEST
    ]:require_file(p)
    if sha256(ASSETS/"siege-tower.glb")!="81909d6c33b181a9935fc7f800e8ee309454bbf99ff3b6b0ab2ecf16c3bf5e9b":raise RuntimeError("siege-tower hash mismatch")
    if sha256(ASSETS/"siege-ram.glb")!="6473c77747b1d0a2c273d5a013454a0c85e5fc33b831150dced46d89b8ff9a5e":raise RuntimeError("siege-ram hash mismatch")
    if sha256(ASSETS/"siege-trebuchet.glb")!="123711fd475e35d061738f648d9bf46c7f463d57681325c369977cee8954679a":raise RuntimeError("trebuchet hash mismatch")
    if sha256(TEXTURES/"castle_brick_02_red_diff_1k.jpg")!="526019deb0533920273a0a2272f7735ca17bb578427515c6b972e2bbecf5726c":raise RuntimeError("diffuse hash mismatch")
    if sha256(TEXTURES/"castle_brick_02_red_nor_gl_1k.jpg")!="ab172b4bb8d9a2492774336f223e7725eecf1aae1efca2923c67db3e978106a6":raise RuntimeError("normal hash mismatch")
    colormap_fallback=ensure_kenney_colormap_placeholder()
    bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
    manifest=build_scene()
    asset_manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    report={
        "status":"TECHNICAL_RENDER_PROOF_PENDING_VISUAL_REVIEW",
        "project":"53 Days to the End of an Empire",
        "sequence":"Illustrative siege-engine approach — not an authenticated reconstruction",
        "fps":FPS,"total_frames":TOTAL,"duration_seconds":SEQUENCE_SECONDS,
        "frame_range":[START,END],"resolution":[1920,1080],
        "engine":bpy.context.scene.render.engine,
        "assets":{
            "siege_tower":{"file":"siege-tower.glb","license":"CC0-1.0 Kenney Castle Kit","sha256":sha256(ASSETS/"siege-tower.glb")},
            "siege_ram":{"file":"siege-ram.glb","license":"CC0-1.0 Kenney Castle Kit","sha256":sha256(ASSETS/"siege-ram.glb")},
            "siege_trebuchet":{"file":"siege-trebuchet.glb","license":"CC0-1.0 Kenney Castle Kit","sha256":sha256(ASSETS/"siege-trebuchet.glb")},
            "castle_brick_diffuse":{"file":"castle_brick_02_red_diff_1k.jpg","license":"CC0-1.0 Poly Haven","sha256":sha256(TEXTURES/"castle_brick_02_red_diff_1k.jpg")},
            "castle_brick_normal":{"file":"castle_brick_02_red_nor_gl_1k.jpg","license":"CC0-1.0 Poly Haven","sha256":sha256(TEXTURES/"castle_brick_02_red_nor_gl_1k.jpg")},
            "character":{"file":CHARACTER.name,"license":asset_manifest["character"]["license"],"sha256":sha256(CHARACTER)}
        },
        "crew":manifest["crew"],
        "kenney_colormap_fallback":colormap_fallback,
        "missing_texture_fallback_slots":manifest["missing_texture_fallback_slots"],
        "imported_object_counts":{
            "siege_tower":manifest["tower_objects"],
            "siege_ram":manifest["ram_objects"],
            "siege_trebuchet":manifest["trebuchet_objects"]
        },
        "limits":[
            "Generic Kenney Castle Kit siege engines are illustrative assets, not authenticated Ottoman or Byzantine equipment from 1453.",
            "The wall and camp are cinematic stand-ins, not measured reconstructions of the Theodosian walls.",
            "The character outfit is a CC0-derived adaptation, not a historically authenticated Ottoman uniform.",
            "The original Kenney Castle Kit colormap.png sidecar is not present in Build 76; affected material slots use explicitly generated neutral fallback colors while the source GLB geometry and exact SHA-256 are retained."
        ],
        "missing_texture_fallback_slots":manifest["missing_texture_fallback_slots"],
        "imported_object_counts":{
            "siege_tower":manifest["tower_objects"],
            "siege_ram":manifest["ram_objects"],
            "siege_trebuchet":manifest["trebuchet_objects"]
        }
    }
    outjson=OUTPUT.with_suffix(".scene.json")
    outjson.parent.mkdir(parents=True,exist_ok=True)
    outjson.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    scene=bpy.context.scene
    if SMOKE_ONLY:
        scene.frame_set(SMOKE_FRAME)
        scene.render.image_settings.file_format="PNG"
        scene.render.filepath=os.environ.get("SMOKE_OUTPUT","out/asset-cutin-smoke.png")
        Path(scene.render.filepath).parent.mkdir(parents=True,exist_ok=True)
        bpy.ops.render.render(write_still=True)
        print("ASSET CUT-IN SMOKE PASS",scene.render.filepath,flush=True)
    else:
        scene.render.image_settings.file_format="FFMPEG"
        scene.render.ffmpeg.format="MPEG4"
        scene.render.ffmpeg.codec="H264"
        scene.render.ffmpeg.constant_rate_factor="MEDIUM"
        scene.render.ffmpeg.ffmpeg_preset="GOOD"
        scene.render.ffmpeg.audio_codec="NONE"
        scene.render.filepath=str(OUTPUT)
        scene.frame_start=START;scene.frame_end=END
        bpy.ops.render.render(animation=True)
        print("ASSET CUT-IN RENDER PASS",OUTPUT,flush=True)

if __name__=="__main__":
    main()
