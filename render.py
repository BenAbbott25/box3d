import bpy

def clear_objects():
    """Clears all objects from the scene."""
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_item(w, h, d, x, y, z):
    """Creates a single item (a scaled cube) in the scene at specified coordinates."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    cube = bpy.context.object
    cube.scale.x = w
    cube.scale.y = h
    cube.scale.z = d

class Container:
    def __init__(self, width, depth, height, closed: bool = True):
        self.width = width
        self.depth = depth
        self.height = height
        self.closed = closed

    def render(self):
        """Creates the container structure with the specified dimensions."""
        # Base
        create_item(self.width, self.depth, 0.01, self.width / 2, self.depth / 2, 0)
        
        # Top
        if self.closed:
            create_item(self.width, self.depth, 0.01, self.width / 2, self.depth / 2, self.height)
        
        # YZ planes
        create_item(0.01, self.depth, self.height, 0, self.depth / 2, self.height / 2)
        create_item(0.01, self.depth, self.height, self.width, self.depth / 2, self.height / 2)
        
        # XZ planes
        create_item(self.width, 0.01, self.height, self.width / 2, 0, self.height / 2)
        create_item(self.width, 0.01, self.height, self.width / 2, self.depth, self.height / 2)

    def check_collision(self, other_object):
        """Placeholder for collision detection logic."""
        # Logic to check collision with other objects
        pass

# Usage example
clear_objects()
container = Container(2, 3, 1)
container.render()  # Render the container in Blender

# list all objects
print(bpy.context.scene.objects)
