bl_info = {
    "name": "Intussusception",
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
     bl_label = "Intussuception"
     bl_options = {'REGISTER', 'UNDO'} 
     
#Declares all customizable variables in UI of addon

     prin = bpy.props.BoolProperty(name = "Print Ready", description = "Adjust model to be dimensions for printing", default = False)
     
     im = bpy.props.BoolProperty(name = "Imaging Scale", description = "Modifies scale for imaging with 8mm diagonal constraint", default = False)
     
     twoD = bpy.props.BoolProperty(name = "2D Model", description = "2D positive flow model", default = False)
     
     pback = bpy.props.BoolProperty(name = "Narrow", description = "Moves first 2 verticies back to allow for more space", default = False)
     
     spacefill = bpy.props.BoolProperty(name = "Spacefilling", description = "Modifies model to maximize covered area by displacing opposite sides", default = False)

     len = bpy.props.IntProperty(name = "Length",description = "Length of Whole Structure", default = 20, min = 0, max = 50)

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

         
         bpy.context.space_data.viewport_shade = 'SOLID'
         verts = []
         length = self.len
         theta = self.angle
         if(self.prin == True):
             length = 16 
             theta = 90
         if(self.im==True):
             length = 5
             theta = 90
         init_x = -length/2
         init_verts = [(init_x,0,0)]
             
         divs = self.bran
         dist = math.ceil(math.tan(math.radians(theta/2))*length/2)

         
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
                 if(self.pback and divs>3):
                     x = (x+3*init_x)/4
                     y/=4
                 else:
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
     
 
     
            
            
         #Define mesh and object
         mymesh = bpy.data.meshes.new("ScriptedVessels")
          
         #the mesh variable is then referenced by the object variable
         myobject = bpy.data.objects.new("ScriptedVessels", mymesh)
 
         #Set location and scene of object
         # myobject.location = bpy.context.scene.cursor_location # the cursor location
         bpy.context.scene.objects.link(myobject) # linking the object to the scene
 
         myobject.modifiers.new('mirror', type = 'MIRROR')
         #myobject.modifiers['mirror'].
         # subdivide modifier
         myobject.modifiers.new("smoothVertices", type='SUBSURF')
          
         # Increase subdivisions
         myobject.modifiers['smoothVertices'].levels = 3
         myobject.modifiers['smoothVertices'].render_levels = 3
         # bpy.ops.object.skin_root_mark()
 
 
 
         #Create mesh
 
         mymesh.from_pydata(verts, edges ,[]) 
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
         
         if(self.inout):
             if(self.boundBox):
                 x = -2*length
                 y = .375* length
                 if(self.spacefill):
                     y=length/3.2
             else:
                 x = -length
                 y = -length/8
             verts = [(x,0,0),(y,0,0)]
             edges = [(0,1)]
             mymesh = bpy.data.meshes.new("inout")
          
             myobject = bpy.data.objects.new("inout", mymesh)

             bpy.context.scene.objects.link(myobject) # linking the object to the scene
 
             myobject.modifiers.new('mirror', type = 'MIRROR')

             myobject.modifiers.new("smoothVertices", type='SUBSURF')
     
             myobject.modifiers['smoothVertices'].levels = 3
             myobject.modifiers['smoothVertices'].render_levels = 3
   
             mymesh.from_pydata(verts,edges ,[]) 
             mymesh.update(calc_edges=True) 
 
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
 
 
             mymesh.update(calc_edges=True)
         
         obj = bpy.data.objects['ScriptedVessels']
         r = self.vertRad
         
         if(self.boundBox == True):
             bpy.ops.view3d.snap_cursor_to_center()
             if(not self.prin and not self.im):
                 bpy.ops.mesh.primitive_cube_add(radius = length/2)
                 if(self.twoD == True):
                    bpy.context.object.scale = (1.25,.75,.25)
                 else:
                     bpy.context.object.scale = (1.25, .75,.5)
                 bpy.context.space_data.viewport_shade = 'WIREFRAME'
                 bpy.data.objects[1]
             else:
                 if(self.im == True):
                     bpy.ops.mesh.primitive_cube_add(radius = 2*math.pow(2,1/2))
                     bpy.context.space_data.viewport_shade = 'WIREFRAME'
                 else:
                     bpy.ops.mesh.primitive_cube_add(radius = 1)
                     if(self.twoD == True):
                         bpy.context.object.scale = (16,7,2)
                     else:
                         bpy.context.object.scale = (16,7,5.5)
                     bpy.context.space_data.viewport_shade = 'WIREFRAME'
                     bpy.data.objects[1]
             
         for v in obj.data.skin_vertices[0].data:
             v.radius = r,r
             
         if(self.inout == True):
             for v in bpy.data.objects['inout'].data.skin_vertices[0].data:
                 v.radius = r,r
             
         if(self.emurray == True and self.rmurray == False):  
             for i in range(1,int(math.pow(2,divs)-1)):
                 if(i == 1 or (i+1)%4==0):
                     r/=(math.pow(2,1/self.murrayNum))

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
                     
                     
         # Make the new object active / the only selected
         bpy.ops.object.select_all(action='DESELECT')
         bpy.data.objects['ScriptedVessels'].select = True
         bpy.context.scene.objects.active = bpy.data.objects['ScriptedVessels']
         
         if(self.spacefill):
             bpy.ops.object.modifier_apply(apply_as='DATA', modifier="mirror")
             iter = math.pow(2,divs+1)+math.pow(2,divs)-2
             iter = int(iter)
             for f in range(3,iter):
                 x,y,z = bpy.data.objects['ScriptedVessels'].data.vertices[f].co
                 if(z!=0):
                     if(y>0):
                         bpy.data.objects['ScriptedVessels'].data.vertices[f].co = (x+3,y,z)
                     else:
                         bpy.data.objects['ScriptedVessels'].data.vertices[f].co = (x-3,y,z)
                     
                 print(bpy.data.objects['ScriptedVessels'].data.vertices[f].co)
                 
          
         if(self.twoD):
             for f in range(len(bpy.data.objects['ScriptedVessels'].data.vertices)):
                 x,y,z = bpy.data.objects['ScriptedVessels'].data.vertices[f].co
                 bpy.data.objects['ScriptedVessels'].data.vertices[f].co = (x,y,0)      
         if(self.inout):
             bpy.data.objects['ScriptedVessels'].select = True
             bpy.context.scene.objects.active = bpy.data.objects['ScriptedVessels']
             bpy.ops.object.modifier_apply(apply_as='DATA', modifier="mirror")
             
             bpy.ops.object.select_all(action='DESELECT')
             bpy.data.objects['inout'].select = True
             bpy.context.scene.objects.active = bpy.data.objects['inout']
             bpy.ops.object.modifier_apply(apply_as='DATA', modifier="mirror")
             
             bpy.ops.object.select_all(action='DESELECT')
             bpy.data.objects['ScriptedVessels'].select = True
             bpy.data.objects['inout'].select = True
             bpy.ops.object.join()
             
             bpy.ops.object.select_all(action='DESELECT')
             bpy.data.objects['inout'].select = True
             bpy.context.scene.objects.active = bpy.data.objects['inout']
             bpy.data.objects['inout'].data.vertices[1].co = verts[0]
             bpy.data.objects['inout'].data.vertices[1].co = verts[1]  
         
         
         if(divs!=0):    
             p = 600/1.5/20#scale factor
             l = length/2 * math.pow(2,1/2) 
             d = self.vertRad*2
             
              #resistance of inner branch
             if(divs>=2):
                 l/=2
             
             if(divs == 1):
                 res = (l*d*p)/(math.pow(2,divs)*divs)*2
                 
             if(divs == 2):
                 res = (l*d*p)
                 res+= l*p*d/2

             else:
                 res = (l*d*p)/(math.pow(2,divs))
                 for f in range(0,divs-1):
                     res+=l*p*d/(math.pow(2,f)*(f+1))
           
             print(res)
         
         
                        
         # go to editmode and apply remove doubles
        # bpy.ops.object.mode_set(mode='EDIT')
         #bpy.ops.mesh.remove_doubles(threshold=0.01, use_unselected=False)
         #bpy.ops.object.mode_set(mode='OBJECT')
         return {'FINISHED'} 
     
 



def menu_func(self, context):
    self.layout.operator(Intus.bl_idname)
    
def register():
    bpy.utils.register_class(Intus)

def unregister():
    bpy.utils.unregister_class(Intus)

if __name__ == "__main__":
    register()
