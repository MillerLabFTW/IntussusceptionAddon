
bl_info = {
    "name": "Intusseception",
    "category": "Add Mesh",
    "author": "Saarang Panchavati"
}

import bpy
import math
import random


from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )

class Intus(bpy.types.Operator):
     bl_idname = "mesh.gen_intus"
     bl_label = "Intusseception"
     bl_options = {'REGISTER', 'UNDO'} 

     prin = bpy.props.BoolProperty(name = "Print Ready", description = "Adjust model to be dimensions for printing", default = False)

     len = bpy.props.IntProperty(name = "Length",description = "Length of Whole Structure", default = 20, min = 10, max = 50)

     angle = bpy.props.IntProperty(name = "Angle", description = "Initial angle of branching", default = 90, min = 30, max = 150)

     bran = bpy.props.IntProperty(name = "Divisions",description = "Number of times the structure divides", default = 0, min = 0, max = 7)
     
     reduction = bpy.props.FloatProperty(name = "Reduction", description = "Amount by which the distance between branches reduces", default = 2.0, min = 1.0, max = 10.0)
     
     inout = bpy.props.BoolProperty(name = "Inlet/Outlet", description = "Inlet and Outlet for Structure", default = False)
     
     boundBox = bpy.props.BoolProperty(name = "Bounding Box", description = "Bounding Box around Structure", default = False)
     
     vertRad = bpy.props.FloatProperty(name = "Skin Radius", description = "Radius of Skin Modifier on Each Vertex", default = .25, min = .1, max = .7)
     
     emurray = bpy.props.BoolProperty(name = """Equal Murray's Law""", description = """Apply Equal Tapering Murray's Law to Structure""", default = False)
     
     rmurray = bpy.props.BoolProperty(name = """Random Murray's Law""", description = """Apply Random(inequal) Murray's Law to Structure""", default = False)
     
     murrayNum = bpy.props.FloatProperty(name = """Murray's Exponent""", description = """Exponent for Murray's Law""", default = 3.0, min = 1.0  ,max=4.0)
     
     
     def execute(self,context):
         bpy.ops.object.select_all(action='TOGGLE')
         bpy.ops.object.delete(use_global=True)
         bpy.context.space_data.viewport_shade = 'SOLID'
         verts = []
         if(self.prin == True):
             length = 16
             theta = 90
             
         length = self.len
         theta = self.angle
         init_x = -length/2
         init_verts = [(init_x,0,0)]
             
         divs = self.bran
         dist = math.ceil(math.tan(math.radians(theta/2))*length/2)
         print(dist)
         
         boxheight = dist/self.reduction
         boxlen = length
         boxwidth = length/2
         
         allArr =[]
         allArr+=init_verts
         currentBranch = 1
         verts+=allArr

         def calcMid(ind):
             x,y,z = allArr[currentBranch-1][ind]
             if(len(allArr[currentBranch-1])==2):
                 x = init_x/2
                 y/=2
                 z/=2
             else:
                 x = (allArr[currentBranch-2][int(ind/2)][0]+x)/2
                 y = (allArr[currentBranch-2][int(ind/2)][1]+y)/2
                 z = (allArr[currentBranch-2][int(ind/2)][2]+z)/2
             return (x,y,z)

         def findBranch(x,y):
             nextx,nexty,nextz= x
             xm,ym,zm = y
             if(currentBranch==1):
                 nextx += length/2
                 pos = nexty+dist
                 neg = nexty-dist
                 return [(nextx,pos,nextz),(nextx,neg,nextz)]
             else:
                 if(currentBranch%2 == 0):
                     cpos = nextz+dist
                     cneg = nextz - dist
                     return [(nextx,ym,cpos),(nextx,ym,cneg)]
                 else:
                     cpos = nexty + dist
                     cneg = nexty - dist
                     return [(nextx,cpos,zm),(nextx,cneg,zm)]

         if(divs == 0):
             verts = init_verts
         else:
             for i in range(divs):
                 br = allArr[i]
                 x = []
                 if(currentBranch==1):
                     allArr.append(findBranch(br,[1,1,1]))
                 else:
                     for f in range(len(br)):
                         
                         y = br[f]
                         br[f] = calcMid(f)
                         x+=findBranch(y,br[f])


                     allArr.append(x)


                 currentBranch+=1
                 l = 1/self.reduction
                 dist*=l

                     
            

         for f in allArr:
             for k in f:
                 verts.append(k)
         verts.pop(1)
         verts.pop(1)
         verts.pop(1)


         edges = []

         for i in range(int(math.pow(2,divs)-1)):
             edges.append((i,i+i+1))
             edges.append((i,i+i+2))
            
         if(divs == 0):
             verts+=[(-init_x,0,0)]
             edges = [(0,1)]
             
         addition = 10
         if(self.prin == True):
             addition = 15
     
         print(edges)  
         if(self.inout):
             verts.insert(0,(init_x - addition, 0,0))
             print(verts)
             for f in range(len(edges)):
                 x,y=edges[f]
                 edges[f] = (x+1,y+1)
         edges.insert(0,(0,1))
         bpy.ops.object.delete(use_global=False)

            
            
         #Define mesh and object
         mymesh = bpy.data.meshes.new("ScriptedVessels")
          
         #the mesh variable is then referenced by the object variable
         myobject = bpy.data.objects.new("ScriptedVessels", mymesh)
 
         #Set location and scene of object
         # myobject.location = bpy.context.scene.cursor_location # the cursor location
         bpy.context.scene.objects.link(myobject) # linking the object to the scene
 
         myobject.modifiers.new('mirror', type = 'MIRROR')

         # subdivide modifier
         myobject.modifiers.new("smoothVertices", type='SUBSURF')
          
         # Increase subdivisions
         myobject.modifiers['smoothVertices'].levels = 3
         myobject.modifiers['smoothVertices'].render_levels = 3
         # bpy.ops.object.skin_root_mark()
 
 
 
         #Create mesh
 
         mymesh.from_pydata(verts,edges ,[]) 
         mymesh.update(calc_edges=True) 
 
 
 
         # add skin modifier after mesh is already created so that the skin root
         # mark will be automatically set as the first vertex
         myobject.modifiers.new("addSkin", type='SKIN')
         myobject.modifiers['addSkin'].use_x_symmetry = True
         myobject.modifiers['addSkin'].use_y_symmetry = True
         myobject.modifiers['addSkin'].use_z_symmetry = True
         myobject.modifiers['addSkin'].use_smooth_shade = True
          
         #subdivide modifier
         myobject.modifiers.new("makeCylindrical", type='SUBSURF')
         
         # Increase subdivisions
         myobject.modifiers['makeCylindrical'].levels = 3
         myobject.modifiers['makeCylindrical'].render_levels = 3
 
 
         mymesh.update(calc_edges=True) #so the edges display properly...
         
         obj = bpy.data.objects[0]
         r = self.vertRad
         
         if(self.boundBox == True):
             if(not self.prin):
                 bpy.ops.mesh.primitive_cube_add(radius = length/2)
                 bpy.context.object.scale = (1.25,.75,.5)
                 bpy.context.space_data.viewport_shade = 'WIREFRAME'
                 bpy.data.objects[1]
             else:
                 bpy.ops.mesh.primitive_cube_add(radius = 1)
                 bpy.context.object.scale = (17,7,5.5)
                 bpy.context.space_data.viewport_shade = 'WIREFRAME'
                 bpy.data.objects[1]
             
         for v in obj.data.skin_vertices[0].data:
             v.radius = r,r
             
         if(self.emurray == True and self.rmurray == False):
             for i in range(1,int(math.pow(2,divs)-1)):
                 if(i == 1 or i%4==0):
                     r/=(math.pow(2,1/self.murrayNum))
                 print(r)
                 obj.data.skin_vertices[0].data[2*i+1].radius = r,r
                 obj.data.skin_vertices[0].data[2*i+2].radius = r,r   
                 
   
         if(self.rmurray == True and self.emurray == False):
             for i in range(2,int(math.pow(2,divs)-1)):
                 if(i ==1):
                     r/=math.pow(2,1/self.murrayNum)
                 else:
                     r,q = obj.data.skin_vertices[0].data[i].radius
                     r1 = random.uniform(0,r)
                     r2 = math.pow((r ** 3.0 + r1 ** 3.0),1/3.0)
                     obj.data.skin_vertices[0].data[2*i+1].radius = r1,r1
                     obj.data.skin_vertices[0].data[2*i+2].radius = r2,r2
                     
         return {'FINISHED'} 

def menu_func(self, context):
    self.layout.operator(Intus.bl_idname)
    
def register():
    bpy.utils.register_class(Intus)

def unregister():
    bpy.utils.unregister_class(Intus)

if __name__ == "__main__":
    register()

