# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:38:33 2023

@author: Jahn
"""

import numpy as np

AU = 149600000e3

def flatten(t):
    '''formatiert 2d_Liste M[n, k] zu 1d-Liste V[n*k]'''
    return [item for sublist in t for item in sublist]

class Orbit_object:
    def __init__(self, mass, p0, v0, r, name, texture):
        self.v0 = np.asarray(v0, float)
        self.p0 = np.asarray(p0, float)
        self.mass = np.float64(mass)
        self.pos = self.p0
        self.vel = self.v0
        self.acc = np.zeros(3)
        self.radius = r
        self.name = name
        self.texture = texture
        
class N_body_system():
    def __init__(self, Objects):
        self.Objects = Objects
        self.n = len(self.Objects)
        self.y = []
        for obj in Objects:
            self.y.append(obj.pos)
            self.y.append(obj.vel)
        self.y = np.asarray(self.y)
        self.y = self.y.reshape(self.n * 6)
        
        
    def gravitation(self, Object1, Object2):
        '''Gravitationsgesetz: Wechselwirkung von jeweils 2 Objekten'''
        gamma = 6.67408e-11 #Gravitationskonstante
        r = Object1.pos - Object2.pos #Abstandsvektor der beiden Objekte
        r_betrag = np.linalg.norm(r) * AU #Betrag des Abstandsvektors
        if r_betrag < (Object1.radius + Object2.radius): #einfache Kollisionsdetektion
            print(Object1.name + '_' + 'crash' + '_' + Object2.name) 
            return np.zeros(3)
        grav = np.asarray(-gamma * Object1.mass * Object2.mass/(r_betrag**2)* (r/r_betrag)) #Gravitationsgesetz
       #print(r)
        return grav
    
    def sum_acceleration(self):
        net_acc = np.zeros((self.n, 3))
        acc = np.zeros((self.n, self.n, 3))
        #print(np.shape(acc))
        for i in range(self.n): 
            for k in range(i + 1, self.n):
                grav_i_k = self.gravitation(self.Objects[i], self.Objects[k]) #paarweise Wechselwirkung der Objekte i und k
                #print(grav_i_k)
                acc[i, k, :] = grav_i_k / self.Objects[i].mass
                acc[k, i, :] = -grav_i_k / self.Objects[k].mass #Actio = Reactio Objekt i zieht Objekt k genscaleso stark an wie Objekt k Objekt i anzieht
        net_acc = np.sum(acc, axis = 1) #Summe aller Beschleunigung der n Objekte durch jedes andere Objekt  
        #print(np.shape(net_acc[1]))
        return net_acc
        
    def y_dot(self, y):
        dydt = np.zeros((self.n * 6))
        for i, obj in enumerate(self.Objects):
            obj.pos = y[i * 6: i * 6 + 3] #Update Objekt Position
            obj.vel = y[i * 6 + 3 : i * 6 + 6] #Update Objekt Geschwindigkeit
            obj.acc = self.sum_acceleration()[i] #Update Objekt Beschleunigung
            dydt[i * 6: i * 6 + 3] = obj.vel
            dydt[i * 6 + 3: i * 6 + 6] = obj.acc
        #print(np.shape(dydt))
        return dydt

    def Integrate_Runge_Kutta_4(self, h):
        ''' !!!nicht benutzt!!! Runge Kutta Verfahren vierter Ordnung'''
        k1 = self.y_dot(self.y)
        k2 = self.y_dot(self.y + h * k1/2)
        k3 = self.y_dot(self.y + h * k2/2)
        k4 = self.y_dot(self.y + h * k3)
        self.y += (1/6) * h * (k1 + 2* k2 + 2*k3 + k4)
        #print(self.y)
        
    def center_Impuls(self):
        '''Galileotransformation scalef Koordinatensystem mit Geschwindigkeit des Schwerpunktes v_system'''
        systemimpuls = 0
        systemmasse = 0
        for obj in self.Objects:
            systemimpuls += obj.vel * obj.mass
            systemmasse += obj.mass
        v_system = systemimpuls/systemmasse
        for i, obj in enumerate(self.Objects):
            obj.vel -= v_system
            self.y[i*6 +3: i*6+6] -= v_system