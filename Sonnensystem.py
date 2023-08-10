# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 16:54:16 2023

@author: Jahn
"""
from N_Body_Physics_Solver import Orbit_object, N_body_system, AU
#from Camera_operator import camera_operator
from ursina import * #camera, window, Ursina, color, load_model, Entity, held_keys, mouse, time
import numpy as np
import re

'''planet data'''
#sun
p_sun = np.asarray([0.0, 0.0, 0.0])
v_sun = np.asarray([0.0, 0.0, 0.0])/AU
m_sun = 1.989e30
radius_sun = 696340e3/AU 

#mercury  
p_mercury = np.asarray([-0.3075, 0, 0])
v_mercury = np.asarray([0, 58.98e3 , 0])/AU
m_mercury = 3.285e23
radius_mercury =2439.7e3/AU

#venus    
p_venus = np.asarray([-0.718, 0, 0])
v_venus = np.asarray([0, 35.2597302e3 , 0])/AU
m_venus =4.867e24
radius_venus =6051.8e3/AU 

#earth    
p_earth = np.asarray([-0.9833, 0, 0])
v_earth = np.asarray([0, 30.2836296e3 , 0])/AU
m_earth = 5.972e24
radius_earth = 6371e3/AU 

#mars
p_mars = np.asarray([-1.381, 0, 0])
v_mars = np.asarray([0, 26.4979927e3 , 0])/AU
m_mars = 6.417e23
radius_mars = 6792.4e3/AU 

#jupiter
p_jupiter = np.asarray([-4.951703121657754, 0, 0])
v_jupiter = np.asarray([0, 13.7102636e3 , 0])/AU
m_jupiter = 1.898e27
radius_jupiter = 69911e3/AU 

#saturn
p_saturn = np.asarray([-9.041, 0, 0])
v_saturn = np.asarray([0, 10.2005165e3 , 0])/AU
m_saturn = 5.683e26
radius_saturn = 58232e3/AU 

#uranus
p_uranus = np.asarray([-18.324, 0, 0])
v_uranus = np.asarray([0, 7.12380473e3 , 0])/AU
m_uranus = 8.681e25
radius_uranus = 25362e3/AU 

#neptune
p_neptune = np.asarray([-29.709, 0, 0])
v_neptune = np.asarray([0, 5.47379381e3 , 0])/AU
m_neptune = 1.024e26
radius_neptune = 24622e3/AU 

'''initialize planets'''   
sun = Orbit_object(mass = m_sun, p0 = p_sun, v0 = v_sun, r = radius_sun, name = 'sun', texture = "textures/sun.jpg")
mercury = Orbit_object(mass = m_mercury, p0 = p_mercury, v0 = v_mercury, r = radius_mercury, name = 'mercury', texture = "textures/mercury.jpg")
venus = Orbit_object(mass = m_venus, p0 = p_venus, v0 = v_venus, r = radius_venus, name = 'venus', texture = "textures/venus.jpg")
earth = Orbit_object(mass = m_earth, p0 = p_earth, v0 = v_earth, r = radius_earth, name = 'earth', texture = "textures/earth.jpg")
mars = Orbit_object(mass = m_mars, p0 = p_mars, v0 = v_mars, r = radius_mars, name = 'mars', texture = "textures/mars.jpg")
jupiter = Orbit_object(mass = m_jupiter, p0 = p_jupiter, v0 = v_jupiter, r = radius_jupiter, name = 'jupiter', texture = "textures/jupiter.jpg")
saturn = Orbit_object(mass = m_saturn, p0 = p_saturn, v0 = v_saturn, r = radius_saturn, name = 'saturn', texture = "textures/saturn.jpg")
uranus = Orbit_object(mass = m_uranus, p0 = p_uranus, v0 = v_uranus, r = radius_uranus, name = 'uranus', texture = "textures/uranus.jpg")
neptune = Orbit_object(mass = m_neptune, p0 = p_neptune, v0 = v_neptune, r = radius_neptune, name = 'neptune', texture = "textures/neptune.jpg")

#create solar system as entity with n_body_physics
solar_system = N_body_system([sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune])

'''Visualization'''
app = Ursina()
#Window parameters
window.color = color.black
window.title = 'Cooles Sonnensystem'

sky = Sky(texture='/background/stars.jpg')

#Camera Movement constants
speed = 7
rotation_speed = 10000

#loading Planet models
spheres = []
texts = []
# Create 8 spheres and add them to the list
for obj in solar_system.Objects:
    # if obj.name == 'saturn':
    #     mesh = load_model('/meshes/Saturn')
    #     sphere = Entity(model=mesh, texture = '/textures/saturn.jpg', scale = 0.0001)# np.power(obj.radius/20000000, 0.333))
    #     sphere.rotation_x += 80
    # else:
    sphere = Entity(model='sphere', scale = np.power(obj.radius, 0.333), texture = obj.texture, position=(obj.pos[0], obj.pos[1], obj.pos[2]))
    text = Text(parent = sphere, text = obj.name, scale = 10, y = 1.2, billbord = True)
    texts.append(text)
    spheres.append(sphere)

'''Update function for engine loop'''
def update():
    '''update physics'''
    solar_system.Integrate_Runge_Kutta_4(1000)

    '''update camera movement'''
    global is_rotating, last_mouse_position

    if held_keys['left mouse'] and not is_rotating:
        is_rotating = True
        last_mouse_position = mouse.position

    if not held_keys['left mouse']:
        is_rotating = False

    if is_rotating:
        delta_mouse_position = mouse.position - last_mouse_position
        rotation_x = -delta_mouse_position[1] * rotation_speed * time.dt
        rotation_y = delta_mouse_position[0] * rotation_speed * time.dt

        camera.rotation_x += rotation_x
        camera.rotation_y += rotation_y

        last_mouse_position = mouse.position

    if held_keys['w']:                               # If q is pressed
        camera.position += camera.forward * time.dt * speed          # move up vertically
    if held_keys['s']:                               # If a is pressed
        camera.position -= camera.forward * time.dt * speed 
    if held_keys['a']:                               # If q is pressed
        camera.position -= camera.right * time.dt * speed           # move up vertically
    if held_keys['d']:                               # If a is pressed
        camera.position += camera.right * time.dt * speed  
                


    '''update visualization'''       
    for i, sphere in enumerate(spheres):
        sphere.x = solar_system.Objects[i].pos[0]
        sphere.y = solar_system.Objects[i].pos[1]
        sphere.z = solar_system.Objects[i].pos[2]
        texts[i].text = solar_system.Objects[i].name + ': current position in AU:' + str(solar_system.y[i*6:i*6+3])
        
app.run()






















