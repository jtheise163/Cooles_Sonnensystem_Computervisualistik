# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:52:08 2023

@author: Jahn
"""

from ursina import camera, held_keys, mouse, time

class camera_operator:
    def __init__(self, speed, sensitivity):
        self.camera = camera
        self.speed
        self.mouse_sensitivity
        
    def movement(self):
        global is_rotating, last_mouse_position

        if held_keys['left mouse'] and not is_rotating:
            is_rotating = True
            last_mouse_position = mouse.position
    
        if not held_keys['left mouse']:
            is_rotating = False
    
        if is_rotating:
            delta_mouse_position = mouse.position - last_mouse_position
            rotation_x = -delta_mouse_position[1] * self.mouse_sensitivity * time.dt
            rotation_y = delta_mouse_position[0] * self.mouse_sensitivity * time.dt
    
            camera.rotation_x += rotation_x
            camera.rotation_y += rotation_y
    
            last_mouse_position = mouse.position
    
        if held_keys['w']:                               # If q is pressed
            self.camera.position += self.camera.forward * time.dt * self.speed          # move up vertically
        if held_keys['s']:                               # If a is pressed
            self.camera.position -= self.camera.forward * time.dt * self.speed 
        if held_keys['a']:                               # If q is pressed
            self.camera.position -= self.camera.right * time.dt * self.speed           # move up vertically
        if held_keys['d']:                               # If a is pressed
            self.camera.position += self.camera.right * time.dt * self.speed  