import bpy, time, os
from mathutils import Vector
def ov():
    win = bpy.context.window_manager.windows[0]; scr = win.screen
    area = next((a for a in scr.areas if a.type == "VIEW_3D"), scr.areas[0])
    return dict(window=win, screen=scr, area=area,
                region=next((r for r in area.regions if r.type == "WINDOW"), None))
sc = bpy.context.scene
alvo = Vector((0, 0.005, 0.0))
cam = bpy.data.objects["camera"]
cam.location = (-0.115, -0.255, 0.150)
cam.data.lens = 48
cam.rotation_euler = (alvo - cam.location).to_track_quat("-Z", "Y").to_euler()
for nome, pos, e in (("luz_principal", (-0.20, -0.28, 0.26), 16.0),
                     ("luz_preenchimento", (0.26, -0.22, 0.10), 5.0),
                     ("luz_contorno", (0.02, 0.30, 0.24), 10.0)):
    o = bpy.data.objects[nome]; o.location = pos; o.data.energy = e
    o.rotation_euler = (alvo - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
t0 = time.perf_counter()
with bpy.context.temp_override(**ov()):
    bpy.ops.render.render(write_still=True)
print("render: %.2f s | %d bytes" % (time.perf_counter()-t0, os.path.getsize(sc.render.filepath)))
bpy.ops.wm.save_mainfile()
