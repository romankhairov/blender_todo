bl_info = {
    "name": "TODO Manager",
    "blender": (2, 80, 0),
    "category": "Object",
    "version": (1, 0, 0),
    "author": "Your Name",
    "description": "A TODO management add-on for Blender",
}

import bpy

# Create Data Structure for TODO Items
TODO_ITEMS = []

# Add Mark TODO Operator
class MarkTodoOperator(bpy.types.Operator):
    bl_idname = "object.mark_todo"
    bl_label = "Mark TODO"
    bl_description = "Mark the selected object with a TODO note"

    description: bpy.props.StringProperty(name="Description", default="TODO Item")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.object
        if obj:
            TODO_ITEMS.append({"object": obj.name, "description": self.description})
            self.report({'INFO'}, f"TODO added for {obj.name}: {self.description}")
        else:
            self.report({'WARNING'}, "No object selected")
        return {'FINISHED'}

# Add Delete TODO Operator
class DeleteTodoOperator(bpy.types.Operator):
    bl_idname = "object.delete_todo"
    bl_label = "Delete TODO"
    bl_description = "Delete a TODO note"

    index: bpy.props.IntProperty()

    def execute(self, context):
        if 0 <= self.index < len(TODO_ITEMS):
            removed = TODO_ITEMS.pop(self.index)
            self.report({'INFO'}, f"Removed TODO for {removed['object']}")
        else:
            self.report({'WARNING'}, "Invalid TODO index")
        return {'FINISHED'}

# Add View TODO Panel
class ViewTodoPanel(bpy.types.Panel):
    bl_label = "TODO Manager"
    bl_idname = "OBJECT_PT_todo_manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TODO"

    def draw(self, context):
        layout = self.layout
        layout.label(text="TODO Items:")

        for i, item in enumerate(TODO_ITEMS):
            row = layout.row()
            row.label(text=f"- {item['object']}: {item['description']}")
            row.operator(DeleteTodoOperator.bl_idname, text="Delete").index = i

# Register and Unregister the Add-on
classes = [MarkTodoOperator, DeleteTodoOperator, ViewTodoPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
