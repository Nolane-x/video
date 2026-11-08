#!/usr/bin/env python3
"""Native-240fps cinematic 3D sequence: the great bombard at Constantinople.
Illustrative historical reconstruction, not a literal replica of Orban's exact gun.
"""
import bpy, math, os
from mathutils import Vector

 # CI installs libEGL/libGL so headless Eevee can run on the Actions CPU runner.
FPS=240
DURATION=39.14
END=round(FPS*DURATION)
FRAME_START=int(os.environ.get("BLENDER_FRAME_START","1"))
FRAME_END=int(os.environ.get("BLENDER_FRAME_END",str(END)))
if not (1 <= FRAME_START <= FRAME_END <= END):
    raise ValueError(f"Invalid render frame range {FRAME_START}..{FRAME_END}; film range is 1..{END}")
OUT=os.environ.get("BLENDER_OUTPUT","out/constantinople-bombardment-picture.mp4")

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine="BLENDER_EEVEE_NEXT" if bpy.app.version >= (4,2,0) else "BLENDER_EEVEE"
scene.render.resolution_x=1920
scene.render.resolution_y=1080
scene.render.resolution_percentage=100
scene.render.fps=FPS
scene.render.fps_base=1.0
scene.frame_start=FRAME_START
scene.frame_end=FRAME_END
scene.render.image_settings.file_format="FFMPEG"
scene.render.ffmpeg.format="MPEG4"
scene.render.ffmpeg.codec="H264"
scene.render.ffmpeg.constant_rate_factor="HIGH"
scene.render.ffmpeg.ffmpeg_preset="GOOD"
scene.render.ffmpeg.video_bitrate=32000
scene.render.ffmpeg.maxrate=48000
scene.render.ffmpeg.buffersize=96000
scene.render.filepath=os.path.abspath(OUT)
scene.render.image_settings.color_mode="RGB"
scene.render.film_transparent=False
scene.render.threads_mode="FIXED"
scene.render.threads=max(2,min(8,os.cpu_count() or 4))
if hasattr(scene,"eevee"):
    if hasattr(scene.eevee,"taa_render_samples"): scene.eevee.taa_render_samples=2
    if hasattr(scene.eevee,"use_gtao"): scene.eevee.use_gtao=True
    if hasattr(scene.eevee,"gtao_distance"): scene.eevee.gtao_distance=3.0
    if hasattr(scene.eevee,"gtao_factor"): scene.eevee.gtao_factor=1.2
os.makedirs(os.path.dirname(os.path.abspath(OUT)),exist_ok=True)
scene.view_settings.view_transform="AgX"
scene.view_settings.look="AgX - Medium High Contrast"
scene.view_settings.exposure=0
scene.view_settings.gamma=1

def mat(name,col,metal=0,rough=.8,emission=0,noise=None,bump=.12):
    m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value=(*col,1)
    bs.inputs["Metallic"].default_value=metal;bs.inputs["Roughness"].default_value=rough
    if emission:
        socket="Emission Color" if "Emission Color" in bs.inputs else "Emission"
        bs.inputs[socket].default_value=(*col,1)
        if "Emission Strength" in bs.inputs: bs.inputs["Emission Strength"].default_value=emission
    if noise:
        n=m.node_tree.nodes.new("ShaderNodeTexNoise");n.inputs["Scale"].default_value=noise;n.inputs["Detail"].default_value=4
        b=m.node_tree.nodes.new("ShaderNodeBump");b.inputs["Strength"].default_value=bump;b.inputs["Distance"].default_value=.12
        m.node_tree.links.new(n.outputs["Fac"],b.inputs["Height"]);m.node_tree.links.new(b.outputs["Normal"],bs.inputs["Normal"])
    return m

limestone=mat("Weathered Theodosian limestone",(.43,.38,.30),rough=.94,noise=5,bump=.22)
cutstone=mat("Pale cut stone",(.61,.54,.43),rough=.86,noise=8)
shadowstone=mat("Dark masonry joints",(.18,.18,.17),rough=.98,noise=5)
bronze=mat("Aged cast bronze",(.22,.12,.065),metal=.72,rough=.34,noise=18,bump=.07)
bronzeedge=mat("Worn bronze hoops",(.47,.29,.13),metal=.82,rough=.28)
iron=mat("Forged iron",(.09,.105,.11),metal=.82,rough=.33)
oak=mat("Old oak carriage",(.22,.105,.045),rough=.74,noise=12,bump=.2)
oaklight=mat("Cut oak edges",(.40,.24,.11),rough=.7,noise=15)
oakdark=mat("Tarred timber",(.11,.068,.04),rough=.85,noise=14)
earth=mat("Packed siege earth",(.18,.135,.09),rough=1,noise=4,bump=.22)
earthlight=mat("Dry earth",(.34,.25,.16),rough=1,noise=20)
crimson=mat("Ottoman muted crimson wool",(.30,.075,.045),rough=.95,noise=30,bump=.05)
ochre=mat("Ottoman ochre wool",(.48,.30,.12),rough=.95,noise=30,bump=.05)
charcoal=mat("Dark wool",(.12,.14,.15),rough=.96)
byzblue=mat("Byzantine blue grey wool",(.12,.20,.24),rough=.94,noise=25)
steel=mat("Dull hammered steel",(.29,.32,.32),metal=.75,rough=.4,noise=28,bump=.05)
leather=mat("Worn leather",(.16,.075,.035),rough=.88,noise=20)
skin1=mat("Warm skin",(.46,.30,.21),rough=.9)
skin2=mat("Sunlit skin",(.62,.43,.29),rough=.9)
dark=mat("Near black",(.02,.022,.023),rough=.6)
sail=mat("Unbleached sailcloth",(.58,.49,.36),rough=.97,noise=40)
flame=mat("Amber flame",(1,.22,.03),rough=.35,emission=2.5)
smoke=mat("Smoke grey",(.25,.26,.26),rough=1)
shotmat=mat("Granite stone shot",(.16,.16,.15),rough=.94,noise=28,bump=.23)

def parent(o,p):
    o.parent=p;o.matrix_parent_inverse=p.matrix_world.inverted();return o

def cube(n,loc,scale,m,bev=0,p=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object;o.name=n;o.dimensions=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bev:
        mod=o.modifiers.new("Worn edges","BEVEL");mod.width=bev;mod.segments=2
    if m:o.data.materials.append(m)
    return parent(o,p) if p else o

def sphere(n,loc,scale,m,seg=20,rings=12,p=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,location=loc)
    o=bpy.context.object;o.name=n;o.scale=scale
    if m:o.data.materials.append(m)
    return parent(o,p) if p else o

def cyl(n,loc,r,d,m,verts=32,rot=(0,0,0),p=None,bev=0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=d,location=loc,rotation=rot)
    o=bpy.context.object;o.name=n
    if m:o.data.materials.append(m)
    if bev:
        mod=o.modifiers.new("Soft metal edge","BEVEL");mod.width=bev;mod.segments=2
    return parent(o,p) if p else o

def cone(n,loc,r1,r2,d,m,rot=(0,0,0),verts=48):
    bpy.ops.mesh.primitive_cone_add(vertices=verts,radius1=r1,radius2=r2,depth=d,location=loc,rotation=rot)
    o=bpy.context.object;o.name=n
    if m:o.data.materials.append(m)
    return o

def between(n,a,b,r,m,verts=16,p=None):
    a,b=Vector(a),Vector(b);d=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=d.length,location=(a+b)/2)
    o=bpy.context.object;o.name=n;o.rotation_euler=d.to_track_quat("Z","Y").to_euler()
    if m:o.data.materials.append(m)
    return parent(o,p) if p else o

def torus(n,loc,major,minor,m,rot=(0,0,0),p=None):
    bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=10,location=loc,major_radius=major,minor_radius=minor,rotation=rot)
    o=bpy.context.object;o.name=n
    if m:o.data.materials.append(m)
    return parent(o,p) if p else o

def key(o,prop,f,val):
    setattr(o,prop,val);o.keyframe_insert(data_path=prop,frame=f)

def smooth(o):
    if o.animation_data and o.animation_data.action:
        for fc in o.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation="BEZIER";kp.handle_left_type="AUTO";kp.handle_right_type="AUTO"

def hidden_range(o,a,b):
    o.hide_render=True;o.keyframe_insert(data_path="hide_render",frame=1);o.keyframe_insert(data_path="hide_render",frame=a-1)
    o.hide_render=False;o.keyframe_insert(data_path="hide_render",frame=a);o.keyframe_insert(data_path="hide_render",frame=b)
    o.hide_render=True;o.keyframe_insert(data_path="hide_render",frame=b+1)

# World, terrain and long-distance city.
world=bpy.data.worlds.new("Bosphorus dawn haze") if not bpy.data.worlds else bpy.data.worlds[0]
scene.world=world;world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(.22,.27,.31,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=.42
cube("Endless packed earth",(0,5,-.4),(80,80,.7),earth)
for i in range(11):
    x=-22+i*4.3
    sphere("Low distant ridge %02d"%i,(x,25+(i%3)*1.4,.6),(3.6,2.6,.6+(i%4)*.12),earthlight,16,8)
for i in range(17):
    x=-17+i*2.1;h=3+(i%5)*.7
    cube("Distant Constantinople house %02d"%i,(x,22.4+(i%3)*.35,3+h/2),(1.25,1.1,h),shadowstone,.06)
    cone("Terracotta roof %02d"%i,(x,22.3+(i%3)*.35,3.2+h),.95,.04,1,oakdark,verts=4)
cube("Bosphorus glint",(0,30,1.6),(60,.35,.05),mat("Sea horizon",(.25,.36,.39),metal=.2,rough=.3,emission=.08))

# Theodosian-style land wall. Geometry is illustrative, not a surveyed replica.
cube("Massive land wall core",(0,18.2,3.2),(26,1.5,6.4),limestone,.12)
for row in range(8):
    z=.55+row*.77
    for col in range(26):
        x=-12.5+col*.98+(.46 if row%2 else 0)
        if x>13 or (row in (3,4) and 1.2<x<3.5):continue
        cube("Ashlar block r%02d c%02d"%(row,col),(x,17.38,z),(.88,.20,.67),cutstone if (row+col)%5==0 else limestone,.025)
cube("Wall-walk parapet",(0,17.25,6.55),(26,.62,.58),cutstone,.06)
for i in range(30):
    x=-12.6+i*.87
    cube("Crenellation merlon %02d"%i,(x,17.25,7.08),(.58,.74,.72),cutstone,.045)
for i,x in enumerate([-11,-6,-1,4,9,14]):
    cyl("Round defensive tower %02d"%i,(x,18.1,4.45),1.22,9,limestone,32)
    torus("Tower cornice %02d"%i,(x,18.1,8.4),1.28,.12,cutstone)
    for a in range(12):
        ang=2*math.pi*a/12
        cube("Tower top merlon",(x+1.17*math.cos(ang),18.1+1.17*math.sin(ang),8.96),(.44,.42,.65),cutstone,.03)
    for z in (3.4,4.45,5.5):
        cube("Tower arrow slit",(x,16.86,z),(.12,.045,.52),shadowstone,.01)

# Great bombard barrel, massive carriage and mechanical details.
barrel=cone("Great cast bombard barrel",(0,-3.45,3.05),.50,.79,6.2,bronze,rot=(-math.pi/2,0,0),verts=96)
barrel.rotation_euler[2]=math.radians(.8)
for i,y in enumerate([-6.15,-5.55,-4.85,-4.15,-3.45,-2.75,-2.05,-1.05,-.65]):
    torus("Reinforcing bronze hoop %02d"%i,(0,y,3.05),.55+i*.021,.075 if i in (0,8) else .052,bronzeedge,rot=(-math.pi/2,0,0))
torus("Heavy muzzle lip",(0,-.36,3.05),.80,.105,bronzeedge,rot=(-math.pi/2,0,0))
cyl("Dark hollow muzzle bore",(0,-.27,3.05),.59,.035,dark,64,rot=(-math.pi/2,0,0))
for s in (-1,1):
    cyl("Iron trunnion",(s*.62,-3.65,2.75),.24,.62,iron,32,rot=(0,math.pi/2,0))
    torus("Trunnion bronze collar",(s*.83,-3.65,2.75),.24,.05,bronzeedge,rot=(0,math.pi/2,0))
    cube("Oak carriage longitudinal beam",(s*.78,-4.8,1.15),(.28,5,.36),oak,.08)
    cube("Oak carriage cheek",(s*.70,-3.9,2.08),(.32,3.2,.32),oaklight,.06)
    for j in range(5):
        cyl("Carriage bolt",(s*.88,-5+j*.55,1.32),.07,.07,iron,16,rot=(0,math.pi/2,0))
cube("Carriage cross axle",(0,-4.9,.95),(2.5,.32,.34),oakdark,.06)
for s in (-1,1):
    x=s*1.24
    torus("Huge oak wheel rim",(x,-4.9,.97),.93,.12,oaklight,rot=(math.pi/2,0,0))
    cyl("Wheel hub",(x,-4.9,.97),.23,.48,oakdark,32,rot=(0,math.pi/2,0))
    cyl("Forged wheel pin",(x+s*.26,-4.9,.97),.1,.08,iron,24,rot=(0,math.pi/2,0))
    for sp in range(12):
        ang=sp*math.pi/6
        between("Wheel spoke",(x,-4.9,.97),(x+.82*math.cos(ang),-4.9,.97+.82*math.sin(ang)),.055,oaklight,12)
cube("Recoil bed",(0,-5.6,.65),(2.4,1.2,.34),oakdark,.08)
for s in (-1,1):
    between("Gun tackle under tension",(s*1.2,-5.7,1.3),(s*2.1,-3,2),.035,leather,10)
# Powder barrels, powder measures, ramming stave and spare stone balls.
for i in range(3):
    y=-9.2-i*.8
    cyl("Powder cask %02d"%i,(-2.65,y,.56),.42,.9,oaklight,32)
    for z in (.24,.84):torus("Cask iron hoop",(-2.65,y,z),.40,.035,iron)
    cube("Cask lid",(-2.65,y,1.04),(.75,.75,.08),oakdark,.03)
stoneball=sphere("Great stone shot",(-2.5,-8.3,.68),(.52,.52,.52),shotmat,32,20)
between("Ramming stave",(-1.2,-5.4,1.45),(0,-1,2.2),.065,oaklight,16)
for i in range(11):
    a=i*2.399;r=.42+(i%3)*.18
    sphere("Spare stone ball %02d"%i,(-3.65+math.cos(a)*r,-7.5+math.sin(a)*r,.47+(i%2)*.22),(.2,.2,.2),shotmat,16,10)

# Stylized but dimensional composite crew: no named historical likenesses.
def person(name,loc,faction="ottoman",scale=1):
    root=bpy.data.objects.new(name+" root",None);scene.collection.objects.link(root);root.location=loc
    tunic=crimson if faction=="ottoman" else byzblue
    accent=ochre if faction=="ottoman" else charcoal
    for s in (-1,1):
        x=s*.19*scale
        parent(between(name+" greave",(loc[0]+x,loc[1],loc[2]+.25*scale),(loc[0]+x*1.05,loc[1],loc[2]+.92*scale),.115*scale,charcoal,12),root)
        parent(sphere(name+" boot",(loc[0]+x,loc[1]-.08*scale,loc[2]+.13*scale),(.19*scale,.29*scale,.13*scale),leather,16,8),root)
    parent(cone(name+" wool tunic",(loc[0],loc[1],loc[2]+1.45*scale),.42*scale,.29*scale,1.25*scale,tunic,verts=24),root)
    cube(name+" leather belt",(loc[0],loc[1]-.006,loc[2]+1.35*scale),(.75*scale,.51*scale,.12*scale),leather,.035*scale,root)
    for s in (-1,1):
        cube(name+" shoulder guard",(loc[0]+s*.34*scale,loc[1],loc[2]+1.83*scale),(.34*scale,.45*scale,.24*scale),steel if faction=="byzantine" else leather,.07*scale,root)
    parent(cyl(name+" neck",(loc[0],loc[1],loc[2]+2.04*scale),.13*scale,.2*scale,skin1,16),root)
    parent(sphere(name+" face",(loc[0],loc[1]-.01,loc[2]+2.27*scale),(.25*scale,.22*scale,.31*scale),skin1 if len(name)%2 else skin2,20,12),root)
    if faction=="ottoman":
        parent(sphere(name+" wrapped turban",(loc[0],loc[1],loc[2]+2.49*scale),(.29*scale,.25*scale,.16*scale),accent,24,12),root)
        torus(name+" turban wrap",(loc[0],loc[1]-.01,loc[2]+2.49*scale),.22*scale,.035*scale,sail,p=root)
        cube(name+" turban tail",(loc[0]+.18*scale,loc[1]+.02,loc[2]+2.34*scale),(.14*scale,.08*scale,.34*scale),accent,.04*scale,root)
    else:
        parent(sphere(name+" steel helmet",(loc[0],loc[1],loc[2]+2.48*scale),(.29*scale,.25*scale,.2*scale),steel,24,12),root)
        parent(between(name+" nasal guard",(loc[0],loc[1]-.24*scale,loc[2]+2.37*scale),(loc[0],loc[1]-.26*scale,loc[2]+2.12*scale),.035*scale,iron,10),root)
    for s in (-1,1):
        parent(sphere(name+" eye",(loc[0]+s*.085*scale,loc[1]-.218*scale,loc[2]+2.31*scale),(.027*scale,.016*scale,.034*scale),dark,10,6),root)
        shoulder=(loc[0]+s*.36*scale,loc[1]-.015,loc[2]+1.86*scale)
        elbow=(loc[0]+s*.58*scale,loc[1]-.1*scale,loc[2]+1.48*scale)
        wrist=(loc[0]+s*.47*scale,loc[1]-.24*scale,loc[2]+1.12*scale)
        parent(between(name+" upper arm",shoulder,elbow,.13*scale,accent,12),root)
        parent(between(name+" forearm",elbow,wrist,.105*scale,steel if faction=="byzantine" else tunic,12),root)
        parent(sphere(name+" hand",wrist,(.12*scale,.11*scale,.12*scale),leather,12,8),root)
    parent(sphere(name+" rear mantle",(loc[0],loc[1]+.19*scale,loc[2]+1.55*scale),(.37*scale,.12*scale,.72*scale),accent,16,10),root)
    return root

crew=[]
specs=[
 ("powder chief",(-3.7,-7.1,0),.96),("rammer operator",(-1.7,-8,0),.92),
 ("carriage brace left",(-1.9,-4.4,0),1),("carriage brace right",(1.9,-4.6,0),1),
 ("rope hauler left",(-3.5,-5.6,0),.92),("rope hauler right",(3.3,-5.8,0),.92),
 ("shot loader",(-3,-9.8,0),.98),("gun captain",(.6,-8.7,0),1.02)]
for name,loc,sc in specs:
    r=person(name,loc,"ottoman",sc);crew.append((name,r))
    x,y,z=r.location
    key(r,"location",1,(x,y,z))
    if "powder" in name or "loader" in name:
        key(r,"location",1800,(x,y+.5,z));key(r,"location",3000,(x+.3,y+.7,z));key(r,"location",3900,(x,y+.1,z))
    elif "brace" in name or "hauler" in name:
        key(r,"location",2800,(x,y,z));key(r,"location",3500,(x*.86,y+.15,z));key(r,"location",4380,(x,y-.1,z));key(r,"location",4620,(x+(-.2 if x<0 else .2),y-.2,z))
    else:
        key(r,"location",2000,(x,y,z));key(r,"location",4200,(x,y-.3,z));key(r,"location",4650,(x,y-.75,z))
    smooth(r)
# Byzantine wall defenders: smaller, separate from Ottoman gun crews.
for i,x in enumerate([-5,-2.5,0,3.8,6.2]):
    r=person("Byzantine wall defender %02d"%i,(x,17,6.5),"byzantine",.82)
    key(r,"location",1,(x,17,6.5));key(r,"location",6300,(x,16.6,6.5))
    key(r,"location",6600,(x+(.4 if i%2 else -.45),16,6.4));key(r,"location",7200,(x+(.6 if i%2 else -.6),16.4,6.5));smooth(r)
# Repair team and scaffolds are revealed in the aftermath shot.
for i,x in enumerate([-1,1,3.6,5.2]):
    r=person("Byzantine repair crew %02d"%i,(x,16.1,0),"byzantine",.78)
    key(r,"location",1,(x,16.1,0));key(r,"location",7600,(x,16.1,0))
    key(r,"location",8300,(x+(.35 if i%2 else -.25),15.4,0))
    key(r,"location",END,(x+(.25 if i%2 else -.15),15.6,0));smooth(r)
for x in (.6,2.3,4):
    between("Repair scaffold upright",(x,16.3,.2),(x,16.3,6.8),.1,oakdark,12)
    between("Scaffold cross rail",(x-.85,16.3,2.8),(x+.85,16.3,2.8),.075,oaklight,12)
    between("Scaffold diagonal",(x-.8,16.3,.3),(x+.8,16.3,3),.055,oakdark,10)
    between("Scaffold diagonal",(x+.8,16.3,.3),(x-.8,16.3,3),.055,oakdark,10)
for i in range(8):
    sphere("Stone repair basket",(-1.6+i*.6,15.7,.32),(.22,.18,.17),oaklight,12,8)

# Camp depth: tents, stores, torch points and stakes.
for i in range(7):
    x=-12+i*4
    cube("Camp tent canvas body",(x,-13,1),(2.8,2.8,1.8),charcoal,.05)
    cone("Camp tent peak",(x,-13,2),1.8,.02,2.25,crimson,verts=4)
    between("Tent centre pole",(x,-13,.1),(x,-13,3.3),.055,oaklight,10)
for i in range(6):
    x=-10+i*4;cyl("Camp supply barrel",(x,-11.5,.55),.45,1.1,oak,24)
for i in range(12):
    x=-13+i*2.35
    cyl("Torch shaft",(x,-12.8,1.5),.045,2.1,iron,10)
    sphere("Torch flame",(x,-12.8,2.62),(.11,.11,.25),flame,12,8)
for i in range(16):
    x=-9+i*1.22;between("Field stake",(x,-10.5,0),(x,-10.5,.65),.045,oakdark,8)
for i in range(4):
    x=-10+i*6
    cyl("Camp standard pole",(x,-12.5,3.6),.06,6.8,oaklight,12)
    flag=cube("Plain crimson camp standard",(x+.8,-12.5,5.5),(1.35,.08,1.6),crimson,.02)
    key(flag,"rotation_euler",1,(0,0,0));key(flag,"rotation_euler",END,(.08,.12,.06 if i%2 else -.06));smooth(flag)

# Ball movement, cannon fire, recoil, stone impact and delayed masonry collapse.
key(stoneball,"location",1,(-2.5,-8.3,.68))
key(stoneball,"location",3000,(-.3,-1,1.75));key(stoneball,"location",3900,(-.25,-.8,2.05))
key(stoneball,"location",4400,(-.25,-.8,2.05));key(stoneball,"location",4550,(0,.1,3.05))
key(stoneball,"location",4800,(.25,4.5,5.6));key(stoneball,"location",5100,(.7,9.3,7))
key(stoneball,"location",5550,(1.4,15.8,4.3));key(stoneball,"location",5850,(1.7,17.3,3.7))
key(stoneball,"location",6000,(1.7,17.3,3.7));smooth(stoneball)
key(stoneball,"rotation_euler",1,(0,0,0));key(stoneball,"rotation_euler",5850,(8,5,4));smooth(stoneball)
flash=sphere("Muzzle fireball",(0,-.45,3.05),(.1,.1,.1),flame,16,10)
for f,val in [(1,(.001,)*3),(4480,(.001,)*3),(4500,(1.5,)*3),(4512,(.4,)*3),(4540,(.001,)*3)]:key(flash,"scale",f,val)
smooth(flash)
ld=bpy.data.lights.new("Brief muzzle flash","POINT");ld.energy=0;ld.color=(1,.32,.08);ld.shadow_soft_size=3
lo=bpy.data.objects.new("Brief muzzle flash light",ld);scene.collection.objects.link(lo);lo.location=(0,-.25,3.2)
for f,e in [(1,0),(4495,0),(4500,9500),(4510,2800),(4540,0)]:key(ld,"energy",f,e)
smooth(ld)
for f,loc in [(1,(0,-3.45,3.05)),(4470,(0,-3.45,3.05)),(4510,(0,-3.9,3.1)),(4560,(0,-3.62,3.05)),(4700,(0,-3.45,3.05))]:key(barrel,"location",f,loc)
smooth(barrel)
# Powder smoke rolls upward and downwind; these proxies are intentionally stylized volume layers.
for i in range(26):
    f=4510+i*13
    p=sphere("Powder smoke proxy %02d"%i,(0,-.2,3.3),(.12,.12,.12),smoke,12,8)
    hidden_range(p,f,f+180)
    key(p,"location",f,(0,-.4,3.3));key(p,"location",f+180,((i%5-2)*.48,1.2+(i%4)*.4,4.2+(i%6)*.32))
    key(p,"scale",f,(.12,)*3);key(p,"scale",f+180,(.82+(i%4)*.18,)*3);smooth(p)
# Masonry debris and broad dust at the wall.
for i in range(22):
    x=2.25+(i%5-2)*.31;z=3+(i//5)*.36;y=17.2-(i%3)*.06
    b=cube("Breach ashlar %02d"%i,(x,y,z),(.34+(i%3)*.05,.24,.25+(i%2)*.04),cutstone if i%4==0 else limestone,.025)
    start=(x,y,z);end=(x+(i%2-.5)*1.8,y-1.1-(i%4)*.22,z+.7+(i%5)*.35)
    for f,loc in [(1,start),(6240,start),(6300,end),(6650,(end[0],end[1],end[2]-1.5))]:key(b,"location",f,loc)
    smooth(b)
for i in range(48):
    a=i*2.399;r=.35+(i%7)*.15;start=(1.7,17.05,3.7)
    end=(1.7+math.cos(a)*r*3,16+math.sin(a)*r*1.4,4+(i%6)*.44)
    p=sphere("Limestone debris %02d"%i,start,(.07+(i%3)*.025,)*3,cutstone if i%4==0 else limestone,10,6)
    key(p,"location",1,start);key(p,"location",6240,start);key(p,"location",6300,end)
    key(p,"location",6600,(end[0],end[1],end[2]-1.8));smooth(p)
for i in range(32):
    a=i*2.399;start=(1.8,16.8,3.8);p=sphere("Impact dust %02d"%i,start,(.16,)*3,smoke,12,8)
    hidden_range(p,6300+i*2,6750+i*2)
    key(p,"location",6300+i*2,start);key(p,"location",6750+i*2,(1.8+math.cos(a)*(1+(i%5)*.3),15.5+math.sin(a)*1.2,4.4+(i%7)*.35))
    key(p,"scale",6300+i*2,(.12,)*3);key(p,"scale",6750+i*2,(1.05,)*3);smooth(p)
# A later, smaller impact repeats the damage; the wall is not obliterated by one shot.
for i in range(10):
    a=i*2.399;p=sphere("Secondary impact dust %02d"%i,(-1.5,17.1,3.4),(.12,)*3,smoke,10,6)
    hidden_range(p,7800,8250)
    key(p,"location",7800,(-1.5,17.1,3.4));key(p,"location",8250,(-1.5+math.cos(a)*1.1,16+math.sin(a)*.7,4+(i%4)*.3))
    key(p,"scale",7800,(.12,)*3);key(p,"scale",8250,(.7,)*3);smooth(p)

# Warm dawn, cold sky fill, bronzed metal highlights and impact practicals.
def area(name,loc,energy,color,size,target):
    d=bpy.data.lights.new(name,"AREA");d.energy=energy;d.color=color;d.shape="DISK";d.size=size
    o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc
    o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler();return o
sd=bpy.data.lights.new("Dawn siege sun","SUN");sd.energy=1.8;sd.angle=math.radians(16);sd.color=(1,.72,.48)
sun=bpy.data.objects.new("Dawn siege sun",sd);scene.collection.objects.link(sun);sun.rotation_euler=(math.radians(28),math.radians(-24),math.radians(-28))
area("Warm key",(-10,-8,18),2100,(1,.77,.56),9,(0,5,3))
area("Cool sky fill",(8,-3,12),1550,(.52,.68,.82),11,(0,6,4))
area("Wall rim",(0,23,14),1900,(1,.60,.36),8,(0,15,4))
area("Bronze glancing light",(-5,-4,6),900,(1,.55,.28),4,(0,-3,3))

def shot(name,start,end,loc0,loc1,tar0,tar1,lens,label):
    bpy.ops.object.camera_add(location=loc0);cam=bpy.context.object;cam.name=name;cam.data.lens=lens;cam.data.sensor_width=36
    t=bpy.data.objects.new(name+" focus target",None);scene.collection.objects.link(t);t.location=tar0
    c=cam.constraints.new(type="TRACK_TO");c.target=t;c.track_axis="TRACK_NEGATIVE_Z";c.up_axis="UP_Y"
    key(cam,"location",start,loc0);key(cam,"location",end,loc1);key(t,"location",start,tar0);key(t,"location",end,tar1)
    smooth(cam);smooth(t);cam.data.dof.use_dof=True;cam.data.dof.focus_object=t;cam.data.dof.aperture_fstop=5.6
    marker=scene.timeline_markers.new(label,frame=start);marker.camera=cam
    return cam

c1=shot("01 macro barrel reveal",1,1439,(4.8,-9.6,4.5),(2.1,-7,4.15),(0,-3.5,3.05),(0,-1.2,3),54,"SHOT 01 — THE GREAT BOMBARD")
c2=shot("02 loading and stone shot",1440,3119,(7.5,-13.4,6),(5,-11,4.7),(-.9,-6.8,1.6),(-.6,-4.8,1.9),43,"SHOT 02 — SLOW TO LOAD")
c3=shot("03 crew braces carriage",3120,4559,(-5.6,-9.5,4.5),(-3,-11,3.9),(0,-4.6,2),(0,-4,2.1),48,"SHOT 03 — MEN BRACE THE CARRIAGE")
c4=shot("04 stone shot flight",4560,5759,(4.2,.5,9),(3,9,7),(0,6,5.2),(1,13.5,5.8),52,"SHOT 04 — STONE SHOT")
c5=shot("05 wall impact",5760,7439,(10.5,8,7.8),(8,11.5,5.6),(1.5,17.3,3.8),(1.7,17.3,3.6),46,"SHOT 05 — WALL IMPACT")
c6=shot("06 repairs after repeated hits",7440,END,(6.5,4,12.5),(4,2,10),(0,16.8,3.2),(1,16.8,3),42,"SHOT 06 — THE REPAIR NEVER ENDS")
scene.camera=c1
notes=bpy.data.texts.new("RECONSTRUCTION-NOTES.txt")
notes.write("Illustrative reconstruction of a 15th-century Ottoman bombard and the Theodosian walls. Generic gun design; not a verified replica of Orban's exact cannon. Generic composite people, not portraits or authenticated uniforms. One impact does not destroy the city. Narration: 00:03:40.760–00:04:19.900. 1920x1080 native 240fps.\\n")
scene.frame_set(FRAME_START)
print("CONSTANTINOPLE 3D PROOF",bpy.app.version_string,"frames",f"{FRAME_START}-{FRAME_END} / {END}","fps",FPS,"objects",len(scene.objects),"output",scene.render.filepath,flush=True)
if os.environ.get("BLENDER_SMOKE_ONLY") == "1":
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = os.path.abspath(os.environ.get("SMOKE_OUTPUT", "out/constantinople-smoke.png"))
    os.makedirs(os.path.dirname(scene.render.filepath), exist_ok=True)
    bpy.ops.render.render(write_still=True)
    print("CONSTANTINOPLE ONE-FRAME SMOKE FINISHED", flush=True)
else:
    bpy.ops.render.render(animation=True)
    print("CONSTANTINOPLE 3D PROOF RENDER FINISHED",flush=True)
