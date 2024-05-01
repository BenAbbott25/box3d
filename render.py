# to be used in blender. create a box of size x, y, z and render it as a wireframe

print("Hello, World!")

import bpy

# clear all objects
def clear_objects():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

# create the containing box (6 sides)
# create the containing box (6 sides)
def create_container(w, d, h):
    # base
    create_item(w, d, 0.01, w/2, d/2, 0)
    
    # top
    create_item(w, d, 0.01, w/2, d/2, h)
    
    # yz plane
    create_item(0.01, d, h, 0, d/2, h/2)
    create_item(0.01, d, h, w, d/2, h/2)
    
    #xz plane
    create_item(w, 0.01, h, w/2, 0, h/2)
    create_item(w, 0.01, h, w/2, d, h/2)
    
    
# Create a box of size w, h, d at location x, y, z
def create_item(w, h, d, x, y, z):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    cube = bpy.context.object
    cube.scale.x = w
    cube.scale.y = h
    cube.scale.z = d

def run():
    clear_objects()
    create_container(2, 3, 1)
    # create_item(0.5, 2.5, 0.5, 0.5, 0, 0)
    # create_item(0.5, 1.5, 0.5, -0.5, 0, 0)
    # create_item(0.5, 1.5, 0.5, 0, 0.5, 0)

run()
