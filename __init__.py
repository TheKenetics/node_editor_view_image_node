bl_info = {
	"name": "View Image Node",
	"author": "Kenetics",
	"version": (0, 1),
	"blender": (3, 0, 0),
	"location": "Node Editor > Context Menu",
	"description": "View image node in image editor.",
	"warning": "",
	"wiki_url": "",
	"category": "Node Editor"
}

import bpy
from bpy.props import EnumProperty, IntProperty, FloatVectorProperty, BoolProperty, FloatProperty, StringProperty, PointerProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel, AddonPreferences


## Operators
class VIN_OT_view_image_node(Operator):
	bl_idname = "vin.view_image_node"
	bl_label = "View Image Node"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(cls, context):
		return (
			context.active_object and
			context.active_object.active_material and
			context.active_object.active_material.node_tree and
			context.active_object.active_material.node_tree.nodes.active and
			context.active_object.active_material.node_tree.nodes.active.image
		)

	def execute(self, context):
		node = context.active_object.active_material.node_tree.nodes.active
		if not (node.type == "TEX_IMAGE" and node.image):
			return {'CANCELLED'}
		for area in context.window.screen.areas:
			if area.type == "IMAGE_EDITOR":
				area.spaces[0].image = context.active_object.active_material.node_tree.nodes.active.image
				break
		else:
			# if for loop finishes without breaking, this else will be called
			bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
			area = context.window_manager.windows[-1].screen.areas[0]
			area.type = "IMAGE_EDITOR"
			area.spaces[0].image = context.active_object.active_material.node_tree.nodes.active.image
		return {'FINISHED'}


## Append to UI Helper Functions
def draw_func(self, context):
	self.layout.operator(VIN_OT_view_image_node.bl_idname, icon="IMAGE_DATA")

## Register
classes = (
	VIN_OT_view_image_node,
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
	## Append to UI
	bpy.types.NODE_MT_context_menu.append(draw_func)

def unregister():
	## Remove from UI
	bpy.types.NODE_MT_context_menu.remove(draw_func)
	
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

if __name__ == "__main__":
	register()
