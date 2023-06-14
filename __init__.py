'''
Copyright (C) 2023 Nurudeen Agbonoga

Created by Nurudeen Agbonoga

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
bl_info = {
    "name": "BlenderTypeFX",
    "blender": (3,5,0),
    "category": "Animation",
    "version": (1,0),
    "description": "Create animated text effects in blender with ease",
    "location": "3D Viewport > Properties tab"
}

import bpy

# animate text operator
class TA_Animate_Text(bpy.types.Operator):
    '''animate text'''
    bl_idname = "ta.animate"
    bl_label = "text animate animate"
    bl_options = {'REGISTER'}
    
    def execute(self, context): # runs when called
        # spawn text
        text = bpy.context.scene.ta_text
        font = bpy.context.scene.ta_font
        frameStep = bpy.context.scene.ta_frame_step
        startFrame = bpy.context.scene.ta_start
        wordsPerLine = bpy.context.scene.ta_n_per_line
        textFile = bpy.context.scene.ta_text_file
        spacing = bpy.context.scene.ta_spacing
        # load text from text file if available
        if not(textFile == "" or textFile == " "): 
            textFilePath = bpy.path.abspath(textFile)
            with open(textFilePath) as f:
                text = f.read()
                print(text)

        # add text one by one at specified radius with spacing
        locationX = 0
        locationY = 0
        showFrame = startFrame
        # add empty to control position of everything
        bpy.ops.object.empty_add(type="PLAIN_AXES")
        emptyName = bpy.context.scene.objects[-1].name
        wordCount = 0
        radius = 0.3
        for c in text:
            bpy.ops.object.text_add(radius = radius, location = [locationX,locationY,0])
            bpy.context.object.data.body = c
            
            # use custom font if specified
            if not(font == "" or font == " "):
                fnt = bpy.data.fonts.load(font)
                bpy.context.object.data.font = fnt
            
            # set key frames
            
            # parent object to empty
            objectName = bpy.context.object.name
            obj = bpy.data.objects[objectName]
            obj.parent = bpy.data.objects[emptyName]
            
            # hide everything in the first frame
            obj.hide_render = True
            obj.hide_viewport = True
            obj.keyframe_insert(data_path = "hide_viewport", frame = 0)
            obj.keyframe_insert(data_path = "hide_render", frame = 0)
            
            # show object in the specified frame
            obj.hide_render = False
            obj.hide_viewport = False
            obj.keyframe_insert(data_path = "hide_viewport", frame = showFrame)
            obj.keyframe_insert(data_path = "hide_render", frame = showFrame)
            
            locationX += spacing
            showFrame += frameStep
            
            # keep track of word count and update y location
            if c == "\r" or c == "\n" or c == "\r\n":
                locationY -= (radius)
                locationX = 0
                wordCount = 0
            elif c == " ":
                wordCount += 1
                if wordCount % wordsPerLine == 0:
                    locationY -= (radius)
                    locationX = 0
        
            
        return {'FINISHED'}
    
class TA_PT_View(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender_TypeFX"
    bl_label = "Animate Text input"
    
    def draw(self, context):
        # text input field
        row = self.layout.row()
        row.label(text="Enter Text Below:")
        row = self.layout.row()
        row.prop(context.scene, "ta_text")
        
        # text file input field
        row = self.layout.row()
        row.label(text="Text file:")
        row = self.layout.row()
        row.label(text="this will overwrite the text box",icon = "INFO")
        row = self.layout.row()
        row.prop(context.scene, "ta_text_file")
        
        # font input field
        row = self.layout.row()
        row.label(text="Font:")
        row = self.layout.row()
        row.prop(context.scene, "ta_font")

        # character spacing input field
        row = self.layout.row()
        row.label(text="Character Spacing:")
        row = self.layout.row()
        row.prop(context.scene, "ta_spacing")
        
        # frame start field
        row = self.layout.row()
        row.label(text="Start Frame:")
        row = self.layout.row()
        row.prop(context.scene, "ta_start")
        
        # number of words per line field
        row = self.layout.row()
        row.label(text="Number of Words Per Line:")
        row = self.layout.row()
        row.prop(context.scene, "ta_n_per_line")
        
        # number of frames between characters field
        row = self.layout.row()
        row.label(text="Frame Step:")
        row = self.layout.row()
        row.prop(context.scene, "ta_frame_step")
        
        # animate button
        self.layout.operator("ta.animate", text = "Animate",
        icon = "PLAY")
        
        
def register():
    
    # register propertiies
    bpy.types.Scene.ta_text = bpy.props.StringProperty(name="")
    bpy.types.Scene.ta_text_file = bpy.props.StringProperty(name="", subtype='FILE_PATH')
    bpy.types.Scene.ta_spacing = bpy.props.FloatProperty(name="", default = 0.15)
    bpy.types.Scene.ta_start = bpy.props.IntProperty(name="", default = 1)
    bpy.types.Scene.ta_n_per_line = bpy.props.IntProperty(name="", default = 10)
    bpy.types.Scene.ta_frame_step = bpy.props.IntProperty(name="", default = 4)
    bpy.types.Scene.ta_font = bpy.props.StringProperty(name="", subtype='FILE_PATH')
    
    # register panel
    bpy.utils.register_class(TA_PT_View)
    
    # register operators
    bpy.utils.register_class(TA_Animate_Text)
    
def unregister():
    bpy.utils.unregister_class(TA_PT_View)
    bpy.utils.unregister_class(TA_Animate_Text)