"""
Sync render visibility with viewport visibility for all objects and their modifiers.

Inspired by https://github.com/lexbailey/blender_sync_hide_viewport
"""

import bpy


def run(o):
    if o.hide_render != o.hide_viewport:
        print(f'[{o.name}] syncing visibility')
        o.hide_render = o.hide_viewport

    for m in o.modifiers:
        if m.show_render != m.show_viewport:
            print(f'[{o.name}] syncing modifier visibility')
            m.show_render = m.show_viewport

    if o.animation_data and o.animation_data.action and o.animation_data.action.fcurves:
        curves = o.animation_data.action.fcurves

        def sync_keyframes(curve_0, curve_1_path):
            print(f'[{o.name}] syncing curve \'{curve_0.data_path}\' to \'{curve_1_path}\'')

            curve_1 = curves.find(curve_1_path)

            if curve_1 is None:
                curve_1 = curves.new(curve_1_path)
            else:
                curve_1.keyframe_points.clear()

            for p in curve_0.keyframe_points:
                frame, value = p.co
                f = curve_1.keyframe_points.insert(frame, value)
                f.easing = p.easing
                f.back = p.back
                f.interpolation = p.interpolation

        for curve in curves:
            if 'hide_viewport' in curve.data_path:
                sync_keyframes(curve, 'hide_render')
            elif '.show_viewport' in curve.data_path:
                sync_keyframes(curve, curve.data_path.replace('.show_viewport', '.show_render'))


for o in bpy.data.objects:
    run(o)
