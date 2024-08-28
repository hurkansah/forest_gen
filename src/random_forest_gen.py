
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import random
import math
import copy
import argparse
from collections import namedtuple
import os
import numpy as np
from pyDOE import lhs
from scipy.stats import qmc


""" def generate_latin_hypercube(num_points, xmin, xmax, ymin, ymax):
    # Generate 2D Latin Hypercube samples
    lhs_samples = lhs(2, samples=num_points, criterion='maximin')

    # Scale samples to the specified range
    x_values = xmin + lhs_samples[:, 0] * (xmax - xmin)
    y_values = ymin + lhs_samples[:, 1] * (ymax - ymin)

    return x_values, y_values """


def generate_random_halton(num_points, xmin, xmax, ymin, ymax):
    # Generate 2D Halton sequence
    halton_sequence = qmc.Halton(2)

    # Generate Halton points
    halton_points = halton_sequence.random(num_points)

    # Scale points to the specified range
    x_values = xmin + halton_points[:, 0] * (xmax - xmin)
    y_values = ymin + halton_points[:, 1] * (ymax - ymin)

    return x_values, y_values


def gen_worlds(save_path,num_worlds, world_length, world_width , tree_density):
    num_trees = int(world_length * world_width * tree_density)
    bush_den = tree_density * 0.75  # you can change bush density in here
    num_bush =int(world_length * world_width * bush_den)
    for world_counter in range(num_worlds):
        # Create the root element
        root = ET.Element('sdf', version='1.7')

        # Create world element
        world = ET.SubElement(root, 'world', name='default')

        # Create spherical_coordinates element
        spherical_coordinates = ET.SubElement(world, 'spherical_coordinates')
        ET.SubElement(spherical_coordinates, 'surface_model').text = 'EARTH_WGS84'
        ET.SubElement(spherical_coordinates, 'latitude_deg').text = '47.3977'
        ET.SubElement(spherical_coordinates, 'longitude_deg').text = '8.54559'
        ET.SubElement(spherical_coordinates, 'elevation').text = '0'
        ET.SubElement(spherical_coordinates, 'heading_deg').text = '0'

        # Create physics element
        physics = ET.SubElement(world, 'physics', name='default_physics', default='0', type='ode')
        ode = ET.SubElement(physics, 'ode')
        solver = ET.SubElement(ode, 'solver')
        ET.SubElement(solver, 'type').text = 'quick'
        ET.SubElement(solver, 'iters').text = '10'
        ET.SubElement(solver, 'sor').text = '1.3'
        ET.SubElement(solver, 'use_dynamic_moi_rescaling').text = '0'
        constraints = ET.SubElement(ode, 'constraints')
        ET.SubElement(constraints, 'cfm').text = '0'
        ET.SubElement(constraints, 'erp').text = '0.2'
        ET.SubElement(constraints, 'contact_max_correcting_vel').text = '1000'
        ET.SubElement(constraints, 'contact_surface_layer').text = '0.001'
        ET.SubElement(physics, 'max_step_size').text = '0.004'
        ET.SubElement(physics, 'real_time_factor').text = '1'
        ET.SubElement(physics, 'real_time_update_rate').text = '250'

        # Create scene element
        scene = ET.SubElement(world, 'scene')
        ET.SubElement(scene, 'shadows').text = '0'
        ET.SubElement(scene, 'ambient').text = '0.4 0.4 0.4 1'
        ET.SubElement(scene, 'background').text = '0.7 0.7 0.7 1'

        # Create light element
        light = ET.SubElement(world, 'light', name='sun', type='directional')
        ET.SubElement(light, 'pose').text = '0 0 1000 0.4 0.2 0'
        ET.SubElement(light, 'diffuse').text = '1 1 1 1'
        ET.SubElement(light, 'specular').text = '0.6 0.6 0.6 1'
        ET.SubElement(light, 'direction').text = '0.1 0.1 -0.9'
        attenuation = ET.SubElement(light, 'attenuation')
        ET.SubElement(attenuation, 'range').text = '20'
        ET.SubElement(attenuation, 'constant').text = '0.5'
        ET.SubElement(attenuation, 'linear').text = '0.01'
        ET.SubElement(attenuation, 'quadratic').text = '0.001'
        ET.SubElement(light, 'cast_shadows').text = '1'
        spot = ET.SubElement(light, 'spot')
        ET.SubElement(spot, 'inner_angle').text = '0'
        ET.SubElement(spot, 'outer_angle').text = '0'
        ET.SubElement(spot, 'falloff').text = '0'

        pose_x = world_length/2
        # Create model element for ground_plane
        ground_plane = ET.SubElement(world, 'model', name='ground_plane')
        ET.SubElement(ground_plane, 'static').text = '1'
        link = ET.SubElement(ground_plane, 'link', name='link')
        collision = ET.SubElement(link, 'collision', name='collision')
        ET.SubElement(collision, 'pose').text = str(pose_x) + ' ' +'0 0 0 -0 0'
        geometry = ET.SubElement(collision, 'geometry')
        plane = ET.SubElement(geometry, 'plane')
        ET.SubElement(plane, 'normal').text = '0 0 1'
        ET.SubElement(plane, 'size').text = "" + str(world_length)+ " " + str(world_length) +""
        surface = ET.SubElement(collision, "surface")
        contact = ET.SubElement(surface, "contact")
        ode = ET.SubElement(contact, "ode")
        min_depth = ET.SubElement(ode, "min_depth")
        min_depth.text = "0.01"
        max_vel = ET.SubElement(ode, "max_vel")
        max_vel.text = "0"
        friction = ET.SubElement(surface, "friction")
        ET.SubElement(friction, "ode")
        torsional = ET.SubElement(friction, "torsional")
        ET.SubElement(torsional, "ode")
        ET.SubElement(surface, "bounce")
        max_contacts = ET.SubElement(collision, "max_contacts")
        max_contacts.text = "10"
        visual = ET.SubElement(link, 'visual', name='grass')
        ET.SubElement(visual, 'pose').text = str(pose_x) + ' ' +'0 0 0 -0 0'
        ET.SubElement(visual, 'cast_shadows').text = '0'
        geometry = ET.SubElement(visual, 'geometry')
        mesh = ET.SubElement(geometry, 'mesh')
        scale_x = world_length / 190 + 0.01
        scale_y= world_width / 185 + 0.01
        ET.SubElement(mesh, 'scale').text = str(scale_x) + " " + str(scale_y)+ " " + "0.1"
        ET.SubElement(mesh, 'uri').text = 'file://grass_plane/meshes/grass_plane.dae'
        ET.SubElement(link, 'self_collide').text = '0'
        ET.SubElement(link, 'enable_wind').text = '0'
        ET.SubElement(link, 'kinematic').text = '0'



        # Create model element for the_void
        the_void = ET.SubElement(world, 'model', name='the_void')
        ET.SubElement(the_void, 'static').text = '1'
        link = ET.SubElement(the_void, 'link', name='link')
        ET.SubElement(link, 'pose').text = '0 0 0.1 0 -0 0'
        visual = ET.SubElement(link, 'visual', name='the_void')
        ET.SubElement(visual, 'pose').text = '0 0 2 0 -0 0'
        geometry = ET.SubElement(visual, 'geometry')
        sphere = ET.SubElement(geometry, 'sphere')
        ET.SubElement(sphere, 'radius').text = '0.25'
        material = ET.SubElement(visual, 'material')
        script = ET.SubElement(material, 'script')
        ET.SubElement(script, 'uri').text = 'file://media/materials/scripts/Gazebo.material'
        ET.SubElement(script, 'name').text = 'Gazebo/Black'
        ET.SubElement(link, 'self_collide').text = '0'
        ET.SubElement(link, 'enable_wind').text = '0'
        ET.SubElement(link, 'kinematic').text = '0'
        ET.SubElement(the_void, 'pose').text = '-1000 -1000 0 0 -0 0'

        # Create gui element
        gui = ET.SubElement(world, 'gui', fullscreen='0')
        camera = ET.SubElement(gui, 'camera', name='camera')
        ET.SubElement(camera, 'pose').text = '35.1577 98.6044 40.0204 0 0.407996 -1.99761'
        ET.SubElement(camera, 'view_controller').text = 'orbit'
        ET.SubElement(camera, 'projection_type').text = 'perspective'

        # Create plugin element

        #ET.SubElement(plugin, 'target_frame_id').text = 'gazebo_user_camera'
        #ET.SubElement(plugin, 'world_origin_frame_id').text = 'uav1/gps_origin'
        #ET.SubElement(plugin, 'frame_to_follow').text = 'uav1'

        # Create gravity element
        ET.SubElement(world, 'gravity').text = '0 0 -9.8066'

        # Create magnetic_field element
        ET.SubElement(world, 'magnetic_field').text = '6e-06 2.3e-05 -4.2e-05'

        # Create atmosphere element
        ET.SubElement(world, 'atmosphere', type='adiabatic')

        # Create wind element
        ET.SubElement(world, 'wind')

        # Create tree model
        x, y= generate_random_halton(num_trees,3,world_length,world_width/-2,world_width/2)
        for counter_tree in range(num_trees):
            pos_x = str(x[counter_tree])
            pos_y = str(y[counter_tree])
            #numbers =[1,2,3,4,5,6,7,9] % available tree models
            #weights = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.3]
            numbers =[1,3,2,9]  #tree model which you want to use
            weights = [0.1,0.1,0.4,0.4] # percentage of the tree model tree 1-> %10 tree 2-> %10 tree 2-> %40 tree 9-> %40 total should be 1
            mesh_num = random.choices(numbers,weights)[0]

            tree_model = ET.SubElement(world, "model", name="Tree " + str(counter_tree))
            ET.SubElement(tree_model, "static").text = "1"
            ET.SubElement(tree_model, "pose").text = pos_x + " " + pos_y + " " +"0 1.57079 -0 0"
            link = ET.SubElement(tree_model, "link", name="link")
            ET.SubElement(link, "pose").text = "0 0 0 0 -0 0"
            collision = ET.SubElement(link, "collision", name="collision")
            geometry_collision = ET.SubElement(collision, "geometry")
            mesh_collision = ET.SubElement(geometry_collision, "mesh")

            
            if mesh_num == 1 or mesh_num == 5:
            	ET.SubElement(mesh_collision, "scale").text = "4 2.5 4"
            elif mesh_num == 3:
            	ET.SubElement(mesh_collision, "scale").text = "3 2 3"
            elif mesh_num == 7:
            	ET.SubElement(mesh_collision, "scale").text = "3 8 3"
            else:
            	ET.SubElement(mesh_collision, "scale").text = "3.5 5 3.5"
            tree_name = "tree_" + str(mesh_num)

            ET.SubElement(mesh_collision, "uri").text = "model://"+ tree_name +"/meshes/"+ tree_name +".obj"
            ET.SubElement(collision, "max_contacts").text = "10"
            surface = ET.SubElement(collision, "surface")
            contact = ET.SubElement(surface, "contact")
            ET.SubElement(contact, "ode")
            ET.SubElement(surface, "bounce")
            friction = ET.SubElement(surface, "friction")
            torsional = ET.SubElement(friction, "torsional")
            ET.SubElement(torsional, "ode")
            ET.SubElement(friction, "ode")
            visual = ET.SubElement(link, "visual", name="visual")
            geometry_visual = ET.SubElement(visual, "geometry")
            mesh_visual = ET.SubElement(geometry_visual, "mesh")

            if mesh_num == 1 or mesh_num == 5:
            	ET.SubElement(mesh_visual, "scale").text = "4 2.5 4"
            elif mesh_num == 3:
            	ET.SubElement(mesh_visual, "scale").text = "3 2 3"
            elif mesh_num == 7:
            	ET.SubElement(mesh_visual, "scale").text = "4 7 4"
            else:
            	ET.SubElement(mesh_visual, "scale").text = "3.5 5 3.5"
            
            ET.SubElement(mesh_visual, "uri").text = "model://"+ tree_name +"/meshes/"+ tree_name +".obj"
            ET.SubElement(link, "self_collide").text = "0"
            ET.SubElement(link, "enable_wind").text = "0"
            ET.SubElement(link, "kinematic").text = "0"
        for counter_tree in range(num_bush):
            x = random.uniform(2.5, (world_length-2.5))
            y = random.uniform(-world_width/2, world_width/2)
            pos_x = str(x)
            pos_y = str(y)
            numbers =[0,1,2,4,5] # bush model which you want to use
            weights = [0.1,0.1,0.6,0.1,0.1] # percentage of the bush model bush 0-> %10, bush 1-> %10 bush 2-> %60 bush 4-> %10 bush 5-> %10 total should be 1
            mesh_num = random.choices(numbers,weights)[0]

            bush_model = ET.SubElement(world, "model", name="Bush " + str(counter_tree))
            ET.SubElement(bush_model, "static").text = "1"
            ET.SubElement(bush_model, "pose").text = pos_x + " " + pos_y + " " +"0 1.57079 -0 0"
            link = ET.SubElement(bush_model, "link", name="link")
            ET.SubElement(link, "pose").text = "0 0 0 0 -0 0"
            collision = ET.SubElement(link, "collision", name="collision")
            geometry_collision = ET.SubElement(collision, "geometry")
            mesh_collision = ET.SubElement(geometry_collision, "mesh")
            ET.SubElement(mesh_collision, "scale").text = "2 2 2"
            bush_name = "bush_" + str(mesh_num)

            ET.SubElement(mesh_collision, "uri").text = "model://"+ bush_name +"/meshes/"+ bush_name +".obj"
            ET.SubElement(collision, "max_contacts").text = "10"
            surface = ET.SubElement(collision, "surface")
            contact = ET.SubElement(surface, "contact")
            ET.SubElement(contact, "collide_without_contact").text = 'false'
            #ET.SubElement(surface, "bounce")
            friction = ET.SubElement(surface, "friction")
            torsional = ET.SubElement(friction, "torsional")
            ET.SubElement(torsional, "ode")
            ET.SubElement(friction, "ode")
            visual = ET.SubElement(link, "visual", name="visual")
            geometry_visual = ET.SubElement(visual, "geometry")
            mesh_visual = ET.SubElement(geometry_visual, "mesh")
            ET.SubElement(mesh_visual, "scale").text = "2 2 2"
            ET.SubElement(mesh_visual, "uri").text = "model://"+ bush_name +"/meshes/"+ bush_name +".obj"
            ET.SubElement(link, "self_collide").text = "0"
            ET.SubElement(link, "enable_wind").text = "0"
            ET.SubElement(link, "kinematic").text = "0"


        # Convert the XML to a string with pretty formatting
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent='    ')

        # Remove the XML declaration manually
        xml_str = '\n'.join(xml_str.split('\n')[1:])
        # Write the formatted XML to a file
        world_folder = "world_" + str(world_length) + "_" + str(world_width)
        if not os.path.exists(os.path.join(save_path,world_folder)):
            os.mkdir(os.path.join(save_path,world_folder))
        world_folder = os.path.join(save_path,world_folder)
        world_path = world_folder +'/forest' + str(world_counter) + '.world'
        with open(world_path, 'w') as f:
            f.write(xml_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a random gazebo forest.')   
    parser.add_argument('--num_worlds', type=int, help='Number of worlds to generate')
    parser.add_argument('--world_length', type=int, help='Length and width of world in m')
    parser.add_argument('--world_width', type=int, help='Length and width of world in m')
    parser.add_argument('--tree_density', type=float, help='Number of trees per m^2')
    #parser.add_argument('--high_res', type=int, help='Use high res tree models')
    args = parser.parse_args()

    gen_worlds('./worlds/gen_world/',args.num_worlds, args.world_length,args.world_width,args.tree_density)
