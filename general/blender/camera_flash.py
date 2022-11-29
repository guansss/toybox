"""
Generate random keyframes for visibilities of camera flashes.

Hierarchy:
- Scene
    - flashes
        - flash
            - Area Light
            - Emissive Mesh
        - flash.001
            - Area Light.001
            - Emissive Mesh.001
        - flash.002
            - Area Light.002
            - Emissive Mesh.002
        ...
"""

import bpy
import numpy as np

frames = 7000
times = int(frames / 30 / 5)

parent = bpy.data.objects['flashes']

overall_keyframes = set()

rng = np.random.default_rng()

for i, flash in enumerate(parent.children):
    print(f'Processing {flash.name}')

    children = flash.children

    for o in children:
        o.animation_data_clear()

    def register_children(prop, value, frame):
        for o in children:
            setattr(o, prop, value)
            o.keyframe_insert(prop, frame=frame)
            
    def blink(frame):
        register_children('hide_viewport', False, frame)
        register_children('hide_viewport', True, frame+2)
        register_children('hide_render', False, frame)
        register_children('hide_render', True, frame+2)

    register_children('hide_viewport', True, 0)
    register_children('hide_render', True, 0)
    
    for frame in rng.integers(0, frames, times):
        overall_keyframes.add(frame)
        blink(frame)
        

overall_keyframes = list(overall_keyframes)
overall_keyframes.sort()

print(f'({len(overall_keyframes)})', overall_keyframes)
