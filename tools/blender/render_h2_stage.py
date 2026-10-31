"""
Render a five-second, 24 fps H2 minimalist mascot style study in headless Blender.
Usage:
  BLENDER_OUTPUT=out/blender/h2-style-study.mp4 blender -b --python tools/blender/render_h2_stage.py
"""
import bpy
import math
import os
from mathutils import Vector

# ---- Reset scene ----
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.materials, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
    # Orphaned data is harmless in this short-lived render process.
    pass

scene = bpy.context.scene
available_engines = {
    item.identifier
    for item in scene.render.bl_rna.properties["engine"].enum_items
}
preferred_engines = (
    "BLENDER_EEVEE_NEXT",
    "BLENDER_EEVEE",
    "BLENDER_WORKBENCH",
    "CYCLES",
)
scene.render.engine = next(
    (engine for engine in preferred_engines if engine in available_engines),
    None,
) or next(iter(available_engines), "")
if not scene.render.engine:
    raise RuntimeError("Blender runtime did not expose any supported render engines.")
print("Selected Blender render engine:", scene.render.engine)
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 120
scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
scene.render.ffmpeg.ffmpeg_preset = "GOOD"
scene.render.filepath = os.environ.get("BLENDER_OUTPUT", os.path.join("out", "blender", "h2-style-study.mp4"))
os.makedirs(os.path.dirname(os.path.abspath(scene.render.filepath)), exist_ok=True)
scene.render.resolution_percentage = 100
scene.render.image_settings.color_mode = "RGB"
scene.render.film_transparent = False

# ---- World and materials ----
world = bpy.data.worlds.new("H2 Charcoal World") if not bpy.data.worlds else bpy.data.worlds[0]
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.012, 0.014, 0.019, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.25

def make_mat(name, color, roughness=0.82, emission=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
            bsdf.inputs["Emission Strength"].default_value = emission
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = (*color, 1.0)
    return mat

charcoal = make_mat("Charcoal", (0.035, 0.04, 0.05))
floor_mat = make_mat("Floor Graphite", (0.075, 0.08, 0.09))
cream = make_mat("Warm Cream Mascot", (0.82, 0.78, 0.68), roughness=0.92)
slate = make_mat("Hoodie Slate", (0.16, 0.18, 0.21))
ink = make_mat("Face Ink", (0.018, 0.02, 0.023))
red = make_mat("Temptation Muted Red", (0.48, 0.085, 0.11), roughness=0.72, emission=0.18)
phone_screen = make_mat("Phone Screen", (0.36, 0.055, 0.075), roughness=0.4, emission=0.45)
paper = make_mat("Warm Paper", (0.72, 0.68, 0.59))

def add_uv(name, location, scale, material, segments=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(material)
    return obj

def add_cube(name, location, scale, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel > 0:
        mod = obj.modifiers.new("Soft Corners", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    obj.data.materials.append(material)
    return obj

def add_segment(name, a, b, radius, material, parent):
    start, end = Vector(a), Vector(b)
    direction = end - start
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=radius, depth=direction.length, location=(start + end) / 2)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = "XYZ"
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    obj.data.materials.append(material)
    obj.parent = parent
    obj.matrix_parent_inverse = parent.matrix_world.inverted()
    return obj

# ---- Stage ----
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -0.03))
floor = bpy.context.object
floor.name = "Infinite Matte Floor"
floor.data.materials.append(floor_mat)

bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 3.5, 5.0))
backdrop = bpy.context.object
backdrop.name = "Charcoal Backdrop"
backdrop.rotation_euler[0] = math.radians(90)
backdrop.data.materials.append(charcoal)

# Restrained red oval shadow that gradually recedes.
shadow = add_uv("Temptation Shadow", (-2.6, 0.55, 0.85), (1.45, 0.12, 0.34), red)
shadow.scale = (1.5, 0.12, 0.34)
shadow.keyframe_insert(data_path="scale", frame=1)
shadow.scale = (0.18, 0.05, 0.08)
shadow.keyframe_insert(data_path="scale", frame=120)

# ---- Simple symbolic mascot: not a realistic human ----
root = bpy.data.objects.new("Mascot Root", None)
scene.collection.objects.link(root)
root.empty_display_type = "CIRCLE"
root.empty_display_size = 0.4

torso = add_uv("Mascot Hoodie Body", (0, 0, 1.45), (0.48, 0.36, 0.72), slate)
torso.parent = root
torso.matrix_parent_inverse = root.matrix_world.inverted()

head = add_uv("Cream Round Head", (0, -0.015, 2.38), (0.53, 0.45, 0.53), cream, segments=32, rings=20)
head.parent = root
head.matrix_parent_inverse = root.matrix_world.inverted()

# Face features on the camera-facing side (negative Y).
for side, name in [(-1, "Left Eye"), (1, "Right Eye")]:
    eye = add_uv(name, (side * 0.145, -0.445, 2.43), (0.045, 0.025, 0.06), ink, segments=16, rings=8)
    eye.parent = root
    eye.matrix_parent_inverse = root.matrix_world.inverted()

mouth_curve = bpy.data.curves.new("Small Calm Smile", "CURVE")
mouth_curve.dimensions = "3D"
mouth_curve.resolution_u = 12
mouth_curve.bevel_depth = 0.018
mouth_curve.bevel_resolution = 2
spline = mouth_curve.splines.new("BEZIER")
spline.bezier_points.add(2)
for point, coord in zip(spline.bezier_points, [(-0.09, -0.47, 2.27), (0, -0.485, 2.245), (0.09, -0.47, 2.27)]):
    point.co = coord
    point.handle_left_type = "AUTO"
    point.handle_right_type = "AUTO"
mouth = bpy.data.objects.new("Mouth", mouth_curve)
scene.collection.objects.link(mouth)
mouth.data.materials.append(ink)
mouth.parent = root
mouth.matrix_parent_inverse = root.matrix_world.inverted()

limbs = []
# Arms and legs are separate parts so their angle can be keyed.
limbs.append(add_segment("Left Arm", (-0.36, 0, 1.88), (-0.68, -0.03, 1.42), 0.105, slate, root))
limbs.append(add_segment("Right Arm", (0.36, 0, 1.88), (0.66, -0.03, 1.48), 0.105, slate, root))
limbs.append(add_segment("Left Leg", (-0.19, 0, 0.91), (-0.3, -0.01, 0.32), 0.12, slate, root))
limbs.append(add_segment("Right Leg", (0.19, 0, 0.91), (0.3, -0.01, 0.32), 0.12, slate, root))

for name, location, scale in [
    ("Left Shoe", (-0.35, -0.08, 0.18), (0.32, 0.28, 0.14)),
    ("Right Shoe", (0.36, -0.08, 0.18), (0.32, 0.28, 0.14)),
]:
    shoe = add_uv(name, location, scale, ink, segments=16, rings=8)
    shoe.parent = root
    shoe.matrix_parent_inverse = root.matrix_world.inverted()

phone = add_cube("Phone", (0.62, -0.40, 1.48), (0.18, 0.08, 0.31), ink, bevel=0.025)
phone.parent = root
phone.matrix_parent_inverse = root.matrix_world.inverted()
screen = add_cube("Phone Muted Red Screen", (0.62, -0.448, 1.49), (0.135, 0.015, 0.225), phone_screen, bevel=0.01)
screen.parent = root
screen.matrix_parent_inverse = root.matrix_world.inverted()

# Alternate leg/arm swing and slight body bob; eased by Blender's Bezier keys.
for frame in range(1, 121, 8):
    phase = (frame - 1) / 120 * math.pi * 6
    x = -2.5 + 5.0 * ((frame - 1) / 119)
    root.location = (x, 0, abs(math.sin(phase)) * 0.045)
    root.keyframe_insert(data_path="location", frame=frame)
    for i, limb in enumerate(limbs):
        base = limb.rotation_euler.copy()
        sign = -1 if i in (0, 2) else 1
        limb.rotation_euler.y = base.y + sign * math.sin(phase) * (0.3 if i >= 2 else 0.22)
        limb.keyframe_insert(data_path="rotation_euler", frame=frame, index=1)
# Ensure an exact end position for the walk.
root.location = (2.5, 0, 0)
root.keyframe_insert(data_path="location", frame=120)

# ---- Title and camera ----
def add_text(name, body, location, size, material):
    curve = bpy.data.curves.new(name, "FONT")
    curve.body = body
    curve.size = size
    curve.extrude = 0
    obj = bpy.data.objects.new(name, curve)
    scene.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler[0] = math.radians(90)
    obj.data.materials.append(material)
    return obj

add_text("Title", "ONE MORE SCROLL", (-4.75, -1.0, 5.0), 0.46, cream)
add_text("Subtitle", "ATTENTION IS A CHOICE", (-4.72, -1.0, 4.53), 0.22, paper)

bpy.ops.object.camera_add(location=(0, -14, 3.8))
camera = bpy.context.object
camera.name = "Orthographic Film Camera"
camera.data.type = "ORTHO"
camera.data.ortho_scale = 10.7
target = bpy.data.objects.new("Camera Target", None)
scene.collection.objects.link(target)
target.location = (0, 0, 2.25)
track = camera.constraints.new(type="TRACK_TO")
track.target = target
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"
scene.camera = camera

def area_light(name, location, energy, color, size):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = energy
    data.color = color
    data.shape = "DISK"
    data.size = size
    obj = bpy.data.objects.new(name, data)
    scene.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (math.radians(28), 0, math.radians(25))
    return obj

area_light("Soft Key", (-4, -5, 7), 520, (1.0, 0.86, 0.68), 5.0)
area_light("Cool Fill", (4, -3, 4.5), 280, (0.57, 0.68, 0.9), 4.0)
area_light("Muted Red Rim", (0, 2.4, 4.4), 190, (0.55, 0.12, 0.15), 3.0)

scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"
scene.view_settings.exposure = 0.0
scene.view_settings.gamma = 1.0
scene.camera.data.lens = 50
scene.render.filepath = os.environ.get("BLENDER_OUTPUT", os.path.join("out", "blender", "h2-style-study.mp4"))
scene.frame_set(1)

print("H2 Blender style study: rendering frames 1-120 at 1280x720/24fps")
print("Output:", scene.render.filepath)
bpy.ops.render.render(animation=True)
print("H2 Blender style study render finished.")
