from argparse import ArgumentParser
import os
import shutil
import re

COMPONENTS = ['consts','setup', 'gui', 'core', 'readme','desktop']
N_COMPS = len(COMPONENTS)
TEMPLATE_LOC = os.path.dirname(__file__)

def replace_cnsts(src, dst, cnst_vals):
	with open(src, 'r', encoding='utf-8') as f:
		contents=f.read()
	for key in cnst_vals:
		contents=cnst_vals[key][0].sub(cnst_vals[key][1], contents)
	with open(dst, 'w', encoding='utf-8') as f:
		f.write(contents)

parser = ArgumentParser(description='Process some integers.')
parser.add_argument('projects', nargs='+', type=str)
parser.add_argument('--dest-dir', '-d', type=str, default=".", 
		help="Place generated project templates here")
parser.add_argument('--generate', '-g', action='append', choices=COMPONENTS,
		default=COMPONENTS,
		help='Generate these components')

args=parser.parse_args()

if len(args.generate) > N_COMPS:
	components = set(args.generate[N_COMPS:])
else:
	components = set(args.generate)

print(components)

#hardcode this for now, make more flexible in the future
replacements={'_APPNAME_': [re.compile(re.escape('_APPNAME_')),
			"_APPNAME_"]}

for project in args.projects:
	libname="{}lib".format(project.lower())
	final_dest = os.path.join(args.dest_dir, project).replace(os.sep, '/')
	libdest=os.path.join(final_dest, libname).replace(os.sep,'/')
	replacements['_APPNAME_'][1]=project
	print("Placing", project, "in", final_dest)
	if not os.path.exists(libdest):
		os.makedirs(libdest)
	if 'consts' in components:
		src = os.path.join(TEMPLATE_LOC, 'appcode', '__init__.py.in').replace(os.sep,'/')
		dst = os.path.join(libdest, '__init__.py').replace(os.sep,'/')
		replace_cnsts(src, dst, replacements)

	if 'setup' in components:
		src = os.path.join(TEMPLATE_LOC, 'setup.py.in').replace(os.sep,'/')
		dst = os.path.join(final_dest, 'setup.py').replace(os.sep,'/')
		replace_cnsts(src, dst, replacements)

	if 'core' in components:
		src = os.path.join(TEMPLATE_LOC, 'appcode', 'core.py.in').replace(os.sep,'/')
		dst = os.path.join(libdest, 'core.py').replace(os.sep,'/')
		replace_cnsts(src, dst, replacements)

	if 'gui' in components:
		src = os.path.join(TEMPLATE_LOC, 'appcode', 'gui.py.in').replace(os.sep,'/')
		dst = os.path.join(libdest, 'gui.py').replace(os.sep,'/')
		replace_cnsts(src, dst, replacements)

		src2 = os.path.join(TEMPLATE_LOC, 'appcode', 'guiconfig.py.in').replace(os.sep,'/')
		dst2 = os.path.join(libdest, 'guiconfig.py').replace(os.sep,'/')
		replace_cnsts(src2, dst2, replacements)

	if 'readme' in components:
		src = os.path.join(TEMPLATE_LOC, 'README.md.in').replace(os.sep,'/')
		dst = os.path.join(final_dest, 'README.md').replace(os.sep,'/')
		replace_cnsts(src, dst, replacements)

	if 'desktop' in components:
		src = os.path.join(TEMPLATE_LOC, '_APPNAME_.desktop.in').replace(os.sep,'/')
		dst = os.path.join(final_dest, '{}.desktop'.format(project)).replace(os.sep,'/')
		replace_cnsts(src, dst, replacements)
