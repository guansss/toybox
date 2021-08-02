"""
Generates ray material for each texture downloaded from https://3dtextures.me/
"""

import os
import re
import sys
from collections import namedtuple
from itertools import chain
from pathlib import Path

from utils.collection import find

TEMPLATE = r"F:\MMD\MME\ray-mmd-1.5.2\Materials\material_2.0.fx"
WORK_DIR = r"F:\MMD\MME\ray-mmd-1.5.2\Materials\extra"

# rename each texture's directory to match its name
RENAME_DIRS = False

MAP_LOOP_NUM = 0.5

Map = namedtuple('Map', 'var file_suffix')

maps = {
    'albedo': Map(var='ALBEDO', file_suffix=('COLOR', 'basecolor')),
    'spec': Map(var='SPECULAR', file_suffix=('SPEC',)),
    'normal': Map(var='NORMAL', file_suffix=('NRM', 'NORM', 'normal')),
    'occ': Map(var='OCCLUSION', file_suffix=('OCC', 'ambientOcclusion')),
    'rough': Map(var='SMOOTHNESS', file_suffix=('ROUGH', 'roughness')),

    # this map does not work well in ray, omitted
    # 'disp': Map(var='PARALLAX', file_suffix=('DISP', 'height')),
}


def main():
    with open(TEMPLATE) as f:
        template_content = f.read()

    if not template_content:
        err('Empty file.')
        return

    # select all direct subdirectories
    for tex_dir in [path for path in Path(WORK_DIR).glob('*/') if path.is_dir()]:
        print('#', tex_dir.stem)

        content = template_content

        # select all image files
        tex_files = list(chain(*[tex_dir.glob('**/' + pattern) for pattern in ['*.png', '*.jpg']]))

        accepted_files = []

        content = f'#define MAP_LOOP_NUM {MAP_LOOP_NUM}\n\n' + content

        for map_name, _map in maps.items():
            tex_file = find(tex_files, lambda file: any(file.stem.endswith(suffix) for suffix in _map.file_suffix))

            if tex_file:
                print(f'{map_name:<10}{tex_file.name}')

                accepted_files.append(tex_file)

                content = define_var(content, _map.var + '_ENABLE', '1')
                content = define_var(content, _map.var + '_MAP_FROM', '1')
                content = define_var(content, _map.var + '_MAP_FILE', f'"{tex_file.relative_to(tex_dir).as_posix()}"')
                content = set_var(content, _map.var.lower() + 'MapLoopNum', 'MAP_LOOP_NUM')

        unused_files = list(set(tex_files) - set(accepted_files))

        if len(unused_files):
            print('[unused]'.ljust(10) + ("\n".ljust(11).join([file.name for file in unused_files])))

        if not len(accepted_files):
            err('No applicable texture, skipping')
            continue

        tex_name = os.path.commonprefix([file.stem for file in accepted_files]).rstrip('_')

        if RENAME_DIRS and tex_name != tex_dir.name:
            new_tex_dir = tex_dir.parent / tex_name

            if new_tex_dir.exists():
                i = 0

                while True:
                    i += 1
                    new_tex_dir = new_tex_dir.parent / f'{tex_name}_{i}'

                    if not new_tex_dir.exists():
                        break

            tex_dir = tex_dir.rename(new_tex_dir)

        output_file = tex_dir / f'material_{tex_name}.fx'

        content = correct_file_references(content, output_file)

        print('>', output_file.relative_to(WORK_DIR), '\n')

        with open(output_file, 'w') as f:
            f.write(content)


def define_var(content, name, value):
    return re.sub(rf'#define {name}.+', f'#define {name} {value}', content)


def set_var(content, name, value):
    return re.sub(rf'{name} = .+;', f'{name} = {value};', content)


def correct_file_references(content, output_file):
    def repl(match):
        original_path = Path(TEMPLATE).parent / match[1]
        relative_path = Path(os.path.relpath(original_path, output_file.parent)).as_posix()

        return f'#include "{relative_path}"'

    return re.sub('#include "(.+)"', repl, content)


def err(*args):
    print(*args, file=sys.stderr)


if __name__ == '__main__':
    main()
