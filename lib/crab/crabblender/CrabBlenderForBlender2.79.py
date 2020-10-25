#!/usr/bin/env python
# 

#####################################
# 
# Functions for Blender Python API
#   
#   Usage:
#       Open blender app, open a panel and switch to Python Console, then input:
#       import sys
#       sys.path.append('/Users/dzliu/Cloud/Github/Crab.Toolkit.Python/lib/crab/crabblender')
#       import CrabBlender
#   
#   Example:
#       import importlib
#       importlib.reload(CrabBlender)
#       a = CrabBlender.create_3D_axes()
#       b1 = CrabBlender.create_a_sphere((0.55,0.35,0.7), 0.02)
#       b2 = CrabBlender.create_a_sphere((0.35,0.35,0.6), 0.02)
# 
#   Tips:
#       CrabBlender.__dir__() # print all functions
#       CrabBlender.create_a_cylinder.__code__.co_argcount # print function argument count
#       CrabBlender.create_a_cylinder.__code__.co_varnames # print function argument names
#   
#   Notes:
#       Require bpy.app.version_string >= 2.79
#   
#   Blender API Documentation:
#       https://docs.blender.org/api/2.79/bpy.ops.mesh.html?highlight=primitive%20cube
# 
#   Last update: 
#       20190803, initialized
# 
#####################################

import bpy
import math


# 
# define function to create a cylinder with emission
# 
def create_a_cylinder(my_cylinder_origin, 
                      my_cylinder_endpoint, 
                      my_cylinder_radius, 
                      my_cylinder_name = 'My_cylinder', 
                      my_cylinder_color = (1.0, 1.0, 1.0), 
                     ):
    # 
    # compute coordinates and lengths, to create the cylinder object we need its center coordinate. 
    x1, y1, z1 = my_cylinder_origin
    x2, y2, z2 = my_cylinder_endpoint
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    # 
    # create it
    bpy.ops.mesh.primitive_cylinder_add(
        radius = my_cylinder_radius, 
        depth = dist, 
        location = (dx/2 + x1, dy/2 + y1, dz/2 + z1), 
    )
    # 
    # rorate it
    phi = math.atan2(dy, dx) 
    theta = math.acos(dz/dist)
    bpy.context.object.rotation_euler[1] = theta 
    bpy.context.object.rotation_euler[2] = phi 
    # 
    # then retrieve its object variable and set its name
    my_cylinder_obj = bpy.context.object
    my_cylinder_obj.name = my_cylinder_name
    # 
    # create a material
    my_cylinder_mat = bpy.data.materials.new(name = my_cylinder_name + '_material')
    my_cylinder_mat.diffuse_color = my_cylinder_color # (1., 0., 0.) # RGB, here is red
    my_cylinder_mat.diffuse_shader = 'LAMBERT'
    my_cylinder_mat.diffuse_intensity = 1.0
    my_cylinder_mat.specular_color = (1., 1., 1.)
    my_cylinder_mat.specular_shader = 'COOKTORR'
    my_cylinder_mat.specular_intensity = 0.5
    my_cylinder_mat.alpha = 1
    my_cylinder_mat.ambient = 1
    my_cylinder_mat.emit = 1 # set it to emit light
    #my_cylinder_mat.type # 'SURFACE'
    # 
    # apply the material to the object
    my_cylinder_obj.data.materials.append(my_cylinder_mat)
    # 
    # end of function, return the created object
    return my_cylinder_obj


# 
# define function to create a cone with emission
# 
def create_a_cone(my_cone_origin, 
                  my_cone_endpoint, 
                  my_cone_radius, 
                  my_cone_name = 'My_cone',
                  my_cone_color = (1.0, 1.0, 1.0), 
                  end_fill_type = 'NGON', 
                 ):
    # 
    # compute coordinates and lengths, to create the cone object we need its center coordinate. 
    x1, y1, z1 = my_cone_origin
    x2, y2, z2 = my_cone_endpoint
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    # 
    # create it
    bpy.ops.mesh.primitive_cone_add(
        radius1 = my_cone_radius, 
        radius2 = 0.0, 
        depth = dist, 
        end_fill_type = end_fill_type, 
        location = (dx/2 + x1, dy/2 + y1, dz/2 + z1), 
    )
    # 
    # rorate it
    phi = math.atan2(dy, dx) 
    theta = math.acos(dz/dist)
    bpy.context.object.rotation_euler[1] = theta 
    bpy.context.object.rotation_euler[2] = phi 
    # 
    # then retrieve its object variable and set its name
    my_cone_obj = bpy.context.object
    my_cone_obj.name = my_cone_name
    # 
    # create a material
    my_cone_mat = bpy.data.materials.new(name = my_cone_name + '_material')
    my_cone_mat.diffuse_color = my_cone_color # (1., 0., 0.) # RGB, here is red
    my_cone_mat.diffuse_shader = 'LAMBERT'
    my_cone_mat.diffuse_intensity = 1.0
    my_cone_mat.specular_color = (1., 1., 1.)
    my_cone_mat.specular_shader = 'COOKTORR'
    my_cone_mat.specular_intensity = 0.5
    my_cone_mat.alpha = 1
    my_cone_mat.ambient = 1
    my_cone_mat.emit = 1 # set it to emit light
    #my_cone_mat.node_tree.nodes.new("ShaderNodeEmission")
    #my_cone_mat.node_tree.nodes["Emission"].inputs["Color"].default_value = my_cone_color # RGB or RGBA
    # 
    # apply the material to the object
    my_cone_obj.data.materials.append(my_cone_mat)
    # 
    # end of function, return the created object
    return my_cone_obj


# 
# define function to create a cube
# 
def create_a_cube(my_cube_origin, 
                  my_cube_endpoint, 
                  my_cube_name = 'My_cube',
                  my_cube_color = None, 
                  my_cube_rotation = (0.0, 0.0, 0.0), 
                  enable_cube_particle_systems = False, 
                 ):
    # 
    # compute coordinates and lengths, to create the cube object we need its center coordinate. 
    x1, y1, z1 = my_cube_origin
    x2, y2, z2 = my_cube_endpoint
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    # 
    # create it
    bpy.ops.mesh.primitive_cube_add(
        location = (dx/2 + x1, dy/2 + y1, dz/2 + z1), 
        rotation = my_cube_rotation, 
    )
    #bpy.context.object.scale = (1.0, 1.0, 1.0) # not recommended to use
    #bpy.context.object.dimensions = (dx, dy, dz) # not recommended to use
    bpy.context.object.scale = (dx/2, dy/2, dz/2) # it is recommended to change the scale, see https://blender.stackexchange.com/questions/32882/create-and-return-a-cube-using-a-python-script
    # 
    # then retrieve its object variable and set its name
    my_cube_obj = bpy.context.object
    my_cube_obj.name = my_cube_name
    # 
    # create a material
    my_cube_mat = bpy.data.materials.new(name = my_cube_name + '_material')
    # 
    # check if we need to enable particle systems or not
    if enable_cube_particle_systems == True:
        my_cube_mat.type = 'HALO'
        ##bpy.ops.object.particle_system_add() # an alternative way to add particle systems
        my_cube_obj.modifiers.new(my_cube_name + '_particle_systems', type='PARTICLE_SYSTEM') # this will create my_cube_obj.particle_systems[0]
        my_cube_mat.halo.size = 0.01 * (max([dx,dy,dz])) # 1/100 size normalized to axes lengths
        my_cube_mat.halo.hardness = 0.0
        my_cube_mat.halo.use_vertex_normal = True # hide the cube vertex
        my_cube_particle_settings = my_cube_obj.particle_systems[0].settings
        my_cube_particle_settings.frame_start = 100 # number of particles
        my_cube_particle_settings.frame_start = 1 # generate particles in just one frame
        my_cube_particle_settings.frame_end = 1 # generate particles in just one frame
        my_cube_particle_settings.emit_from = 'VOLUME'
        my_cube_particle_settings.physics_type = 'NO'
        #my_cube_particle_settings.particle_size = 0.1
        #my_cube_particle_settings.render_type = 'OBJECT'
        #my_cube_particle_settings.dupli_object = bpy.data.objects['Cube']
        #my_cube_particle_settings.show_unborn = True
        #my_cube_particle_settings.use_dead = True
    else:
        my_cube_mat.type = 'WIRE'
    # 
    # set the material color if needed
    if my_cube_color is not None:
        #my_cube_mat.type = 'SURFACE'
        my_cube_mat.diffuse_color = my_cube_color # RGB
        my_cube_mat.diffuse_shader = 'LAMBERT'
        my_cube_mat.diffuse_intensity = 1.0
        my_cube_mat.specular_color = (1., 1., 1.)
        my_cube_mat.specular_shader = 'COOKTORR'
        my_cube_mat.specular_intensity = 0.5
        my_cube_mat.alpha = 1
        my_cube_mat.ambient = 1
        #my_cube_mat.emit = 0 # set it to NOT emit light
    # 
    # apply the material to the object
    my_cube_obj.data.materials.append(my_cube_mat)
    # 
    # end of function, return the created object
    return my_cube_obj


# 
# define function to create a sphere with emission
# 
def create_a_sphere(my_sphere_location, 
                    my_sphere_radius, 
                    my_sphere_name = 'My_sphere',
                    my_sphere_type = 'ico_sphere', 
                    my_sphere_color = (1.0, 1.0, 1.0), 
                   ):
    # 
    # notes:
    #   before 2020-01-22 the default my_sphere_type is 'uv_sphere'
    # 
    # create it
    if my_sphere_type == 'ico_sphere':
        # ico_sphere
        bpy.ops.mesh.primitive_ico_sphere_add(
            size = my_sphere_radius, 
            location = my_sphere_location, 
        )
    else:
        # uv_sphere
        bpy.ops.mesh.primitive_uv_sphere_add(
            size = my_sphere_radius, 
            location = my_sphere_location, 
        )
    # 
    # then retrieve its object variable and set its name
    my_sphere_obj = bpy.context.object
    my_sphere_obj.name = my_sphere_name
    # 
    # create a material
    my_sphere_mat = bpy.data.materials.new(name = my_sphere_name + '_material')
    my_sphere_mat.diffuse_color = my_sphere_color # RGB
    my_sphere_mat.diffuse_shader = 'LAMBERT'
    my_sphere_mat.diffuse_intensity = 1.0
    my_sphere_mat.specular_color = (1., 1., 1.)
    my_sphere_mat.specular_shader = 'COOKTORR'
    my_sphere_mat.specular_intensity = 0.5
    my_sphere_mat.alpha = 1
    my_sphere_mat.ambient = 1
    my_sphere_mat.emit = 1 # set it to emit light
    # 
    # apply the material to the object
    my_sphere_obj.data.materials.append(my_sphere_mat)
    # 
    # end of function, return the created object
    return my_sphere_obj


# 
# define function to create 3D X Y Z axes
# 
def create_3D_axes(my_axes_lengths = (1.0, 1.0, 1.0), 
                   my_axes_thickness = 0.01, 
                   my_axes_color_RGB = (0.8, 0.8, 0.8), 
                   enable_particles = False, 
                  ):
    # create X axis stem
    my_axis_X_stem_obj = create_a_cylinder((0.0, 0.0, 0.0), 
                                           (my_axes_lengths[0], 0.0, 0.0), 
                                           my_axes_thickness / 2, 
                                           my_cylinder_name = 'My_axis_X_stem', 
                                           my_cylinder_color = my_axes_color_RGB, 
                                          )
    # create X axis cone, the cone radius is twice the stem radius, and length is 0.15 the stem length. 
    my_axis_X_cone_obj = create_a_cone((my_axes_lengths[0], 0.0, 0.0), 
                                       (my_axes_lengths[0]*1.15, 0.0, 0.0), 
                                       my_axes_thickness / 2 * 2, 
                                       my_cone_name = 'My_axis_X_cone', 
                                       my_cone_color = my_axes_color_RGB, 
                                      )
    # create Y axis stem
    my_axis_Y_stem_obj = create_a_cylinder((0.0, 0.0, 0.0), 
                                           (0.0, my_axes_lengths[1], 0.0), 
                                           my_axes_thickness / 2, 
                                           my_cylinder_name = 'My_axis_Y_stem', 
                                           my_cylinder_color = my_axes_color_RGB, 
                                          )
    # create Y axis cone, the cone radius is twice the stem radius, and length is 0.15 the stem length. 
    my_axis_Y_cone_obj = create_a_cone((0.0, my_axes_lengths[1], 0.0), 
                                       (0.0, my_axes_lengths[1]*1.15, 0.0), 
                                       my_axes_thickness / 2 * 2, 
                                       my_cone_name = 'My_axis_Y_cone', 
                                       my_cone_color = my_axes_color_RGB, 
                                      )
    # create Z axis stem
    my_axis_Z_stem_obj = create_a_cylinder((0.0, 0.0, 0.0), 
                                           (0.0, 0.0, my_axes_lengths[2]), 
                                           my_axes_thickness / 2, 
                                           my_cylinder_name = 'My_axis_Z_stem', 
                                           my_cylinder_color = my_axes_color_RGB, 
                                          )
    # create Z axis cone, the cone radius is twice the stem radius, and length is 0.15 the stem length. 
    my_axis_Z_cone_obj = create_a_cone((0.0, 0.0, my_axes_lengths[2]), 
                                       (0.0, 0.0, my_axes_lengths[2]*1.15), 
                                       my_axes_thickness / 2 * 2, 
                                       my_cone_name = 'My_axis_Z_cone', 
                                       my_cone_color = my_axes_color_RGB, 
                                      )
    # create a cube for the particle systems
    if enable_particles == True:
        my_axes_cube_obj = create_a_cube((0.0, 0.0, 0.0), 
                                         my_axes_lengths, 
                                         my_cube_name = 'My_axes_cube', 
                                         my_cube_color = None, 
                                         enable_cube_particle_systems = enable_particles, 
                                        )
    # 
    class my_3D_axis_obj_class:
        def __init__(self, input_axis_stem_obj, input_axis_cone_obj):
            self.stem = input_axis_stem_obj
            self.cone = input_axis_cone_obj
    # 
    class my_3D_axes_obj_class:
        def __init__(self):
            self.X = None
            self.Y = None
            self.Z = None
            self.cube = None
    #         
    my_3D_axes_obj = my_3D_axes_obj_class()
    my_3D_axes_obj.X = my_3D_axis_obj_class(my_axis_X_stem_obj, my_axis_X_cone_obj)
    my_3D_axes_obj.Y = my_3D_axis_obj_class(my_axis_Y_stem_obj, my_axis_Y_cone_obj)
    my_3D_axes_obj.Z = my_3D_axis_obj_class(my_axis_Z_stem_obj, my_axis_Z_cone_obj)
    if enable_particles == True:
        my_3D_axes_obj.cube = my_axes_cube_obj
    return my_3D_axes_obj


# 
# define function to delete all objects
# 
def delete_all_mesh_objects():
    # Delect objects by type
    for t_obj in bpy.context.scene.objects:
        if t_obj.type == 'MESH':
            t_obj.select = True
        else:
            t_obj.select = False
    # Call the operator only once
    bpy.ops.object.delete()
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')


# 
# define function to delete all sphere objects
# 
def delete_all_sphere_objects():
    # Delect objects by type
    for t_obj in bpy.context.scene.objects:
        if t_obj.type == 'MESH' and t_obj.name.startswith('My_sphere') == True:
            t_obj.select = True
        else:
            t_obj.select = False
    # Call the operator only once
    bpy.ops.object.delete()
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')



# 
# test function
# 
def test_creating_a_cylinder():
    # set testing parameters
    my_cylinder_radius = 0.05
    my_cylinder_origin = (0.0, 0.0, 0.0) # X, Y, Z
    my_cylinder_endpoint = (5.0, 0.0, 0.0) # X, Y, Z
    # run testing function
    my_cylinder_obj = create_a_cylinder(my_cylinder_origin, 
                                        my_cylinder_endpoint, 
                                        my_cylinder_radius, 
                                        my_cylinder_name = 'My_cylinder',
                                        my_cylinder_color = (1.0, 1.0, 1.0),
                                       )
    # check obj properties
    #my_cylinder_obj.data.materials[0].node_tree.nodes #--> node_tree is empty...
    # return the obj
    return my_cylinder_obj


# 
# test function
# 
def test_creating_a_cone():
    # set testing parameters
    my_cone_radius = 0.12
    my_cone_origin = (5.0, 0.0, 0.0) # X, Y, Z
    my_cone_endpoint = (6.0, 0.0, 0.0) # X, Y, Z
    # run testing function
    my_cone_obj = create_a_cone(my_cone_origin, 
                                my_cone_endpoint, 
                                my_cone_radius, 
                                my_cone_name = 'My_cylinder',
                                my_cone_color = (1.0, 1.0, 1.0),
                               )
    # return the obj
    return my_cone_obj





