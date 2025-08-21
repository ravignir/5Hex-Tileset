#!/usr/bin/env python3

"""
Example Python utility for automatically converting Unciv tilesets to make use of https://github.com/yairm210/Unciv/pull/5874.

See BuildTileset.sh for example use.

License:
	By https://github.com/will-ca/, https://github.com/Intralexical.

	This Source Code Form is subject to the terms of the Mozilla Public
	License, v. 2.0. If a copy of the MPL was not distributed with this
	file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

# TIP: Most of these functions can accept either a filepath or an image object as their primary operand. This makes them easily chainable/nestable.
# TIP: Most of these functions return `PIL.Image.Image` instances. Call their `.show()` method to preview them.
# E.G.: maskedHexImage(tesselatedHexImage(expandedHexImage("Hexagon.png", 1.5), 1.5), 1.5, hexMaskPolygonalBalanced(1.5)).show()

import PIL.Image, PIL.ImageEnhance, math


HEX_HEIGHT = math.sqrt(0.75) # Hexagon height— But I've also seen 7:9 thrown around for Unciv?

def asImage(image):
	"""Return a PIL image from a given PIL image or filepath."""
	if not isinstance(image, PIL.Image.Image):
		image = PIL.Image.open(image)
	return image.convert('RGBA')

def asSize(size):
	"""Return an size tuple from a given size tuple or image."""
	return size.size if isinstance(size, PIL.Image.Image) else size

def blankFrom(size):
	"""Make a new transparent image from a given image or size tuple."""
	return PIL.Image.new('RGBA', asSize(size), (0,0,0,0))

def hexSize(image, expandedfac):
	"""Calculate the bounding rectangle dimensions of the hex area on an expanded hex tile."""
	return (image.size[0] / expandedfac, image.size[0] / expandedfac * HEX_HEIGHT)


def expandedHexImage(image, factor, topmargin=1.0):
	"""Add margins around a hex tile image while still keeping the hex centered."""
	image = asImage(image)
	horimargin = image.size[0] * (factor-1)/2
	vertmargin = horimargin * HEX_HEIGHT
	expandedsize = (round(image.size[0]*factor), round(image.size[1]+vertmargin*(1+topmargin)))
	expanded = blankFrom(expandedsize)
	expanded.paste(image, (round(horimargin), round(vertmargin*topmargin)))
	return expanded

def tesselatedHexImage(image, expandedfac):
	"""Surround an expanded hex tile with six neighbours."""
	image = asImage(image)
	hexwidth, hexheight = hexSize(image, expandedfac)
	tessed = blankFrom(image)
	for x, y in ((0,-1), (-0.75,-0.5), (0.75,-0.5), (0,0), (-0.75, 0.5), (0.75, 0.5), (0, 1)):
		tessed.alpha_composite(image, (round(hexwidth*x), round(hexheight*y)))
	return tessed


def hexMaskCircularOuter(fuzzedscale=2):
	"""Return a circular mask with fuzzing entirely outside the hex area."""
	return lambda x, y: max(0, 1-max(0, (math.sqrt((x-0.5)**2+(y-0.5)**2)-0.5)*2/(fuzzedscale-1)))

def clippedModulo(v, divisor, low, high):
	if v <= low:
		return v-divisor*(low//divisor)
	elif v >= high:
		return v-divisor*(high//divisor)
	return v % divisor

def polyDistance(x, y, sides, *, rotangle=0.0, minangle=-math.inf, maxangle=math.inf):
	return math.sqrt(x**2+y**2)*math.cos(clippedModulo((math.atan2(y,x)+rotangle)%(math.pi*2), math.pi/(sides/2), minangle, maxangle)-math.pi/sides)

def hexMaskPolygonalOuter(fuzzedscale=2, sides=6):
	"""Return a polygonal mask with fuzzing entirely outside the polygon's area."""
	cornerratio = math.cos(math.pi/6)
	def mask(x, y):
		return max(0, 1-max(0, polyDistance(x-0.5, y-0.5, sides)/cornerratio*2-1)/(fuzzedscale-1))
	return mask

def hexMaskPolygonalBalanced(fuzzedscale=2, sides=6):
	"""Return a polygonal mask with fuzzing that's split between the polygon's interior and its exterior."""
	cornerratio = math.cos(math.pi/6)
	fuzzdistance = (fuzzedscale-1)
	def mask(x, y):
		return max(0, 1-max(0, polyDistance(x-0.5, y-0.5, sides, rotangle=math.pi*-2/6, minangle=math.pi*2/3, maxangle=math.pi*4/3)/cornerratio-(0.5-fuzzdistance/2))/fuzzdistance)
	return mask

def hexMaskVisHex(alpha=0.5):
	"""Return a hard-edged polygonal mask that sets alpha lower outside the hex area, for visualization purposes."""
	return lambda x, y: (1 if (abs(x-0.5)*2 / (1 - (abs(y-0.5)))) <= 1 and 0 <= y <= 1 else alpha)

def hexMaskFromImage(expandedfac):
	raise NotImplementedError()

def maskedHexImage(image, expandedfac, maskfunc=hexMaskVisHex()):
	"""Apply a transparency mask to an expanded hex tile. The mask function takes X and Y values relative to the bounding rectangle of the hexagon on the tile image, and it returns an opacity."""
	image = asImage(image)
	masked = image.copy()
	hexwidth, hexheight = hexSize(image, expandedfac)
	centercorner = (round((image.size[0]-hexwidth)/2), image.size[1]-(hexheight*(1+expandedfac)/2))
	for x in range(masked.size[0]):
		for y in range(masked.size[1]):
			coord = (x, y)
			pix = masked.getpixel(coord)
			masked.putpixel(coord, (*pix[:3], round(pix[3]*maskfunc((x-centercorner[0])/hexwidth, (y-centercorner[1])/hexheight))))
	return masked


def shadowShearedOrthoImage(image, base_y=0, scale_y=1.0, shear_x=1.0):
	# Shear an image to be flat on the ground. Doesn't blacken, blur, or make transparent. Takes parameters in pixel-space, not hex-space.
	image = asImage(image)
	return image.transform(image.size, PIL.Image.AFFINE,
			(1, shear_x, -base_y*shear_x,
			0, 1/scale_y, -((1/scale_y)-1)*base_y)
		)

def shadowOrthoImage(image, blur=5, *shear_args, **shear_kwargs):
	# Wraps above, with blackening and blurring. Takes parameters in pixel-space, not hex-space.
	image = asImage(image)
	return shadowShearedOrthoImage(PIL.ImageEnhance.Brightness(image).enhance(0.0).filter(PIL.ImageFilter.GaussianBlur(blur)), *shear_args, **shear_kwargs)

def shadowedOrthoImage(image, opacity=0.7, **shadow_kwargs):
	# Wraps above, with opacity, and composites original image on top of it. Takes parameters in pixel-space, not hex-space.
	image = asImage(image)
	r, g, b, a = shadowOrthoImage(image, **shadow_kwargs).split()
	shadowed = PIL.Image.merge('RGBA', (r, g, b, a.point(lambda a: int(a*opacity))))
	shadowed.alpha_composite(image, (0, 0))
	return shadowed

def shadowedOrthoHexImage(image, expandedfac, base=0, opacity=0.7, blur=0.05, length=1.0, shear=1.0):
	"""Add a sheared shadow to an expanded hex tile with blur radius and base height proportional to the hexagon on it. Base height of 0.0 means the shadow starts at the bottom of the hex; 1.0 means it starts at the top of the hex. Length is a vertical scale factor. Shear is a slope."""
	image = asImage(image)
	hexwidth, hexheight = hexSize(image, expandedfac)
	return shadowedOrthoImage(image, opacity=opacity, blur=hexwidth*blur, base_y=image.size[1]-hexheight*(expandedfac-1)/2-base*hexheight, scale_y=length, shear_x=shear)


def dropShadowedHexImage(image, expandedfac, opacity=0.7, blur=0.05, x=0.1, y=0.1):
	"""Add a drop shadow to an expanded hex tile with blur and offset proportional to the hexagon on it."""
	image = asImage(image)
	hexwidth, hexheight = hexSize(image, expandedfac)
	shadow = shiftedHexImage(PIL.ImageEnhance.Brightness(image).enhance(0.0).filter(PIL.ImageFilter.GaussianBlur(hexwidth*blur)), expandedfac, x, y)
	r, g, b, a = shadow.split()
	shadowed = PIL.Image.merge('RGBA', (r, g, b, a.point(lambda a: int(a*opacity))))
	shadowed.alpha_composite(image, (0, 0))
	return shadowed


def autocroppedHexImage():
	"""Trim unneeded regions from a hex image. Only trims the top, as bottom and width are used for placement."""
	raise NotImplementedError()

def shiftedHexImage(image, expandedfac, x=0, y=0):
	"""Move an expanded hex tile proportionally to the width and height of the hexagon on it."""
	image = asImage(image)
	hexwidth, hexheight = hexSize(image, expandedfac)
	return image.transform(image.size, PIL.Image.AFFINE,
		(1, 0, -x*hexwidth,
		0, 1, y*hexheight)
	)


def compositedHexImages(*layers):
	"""Scale image `layers` to the same width then layer them with their bottoms aligned."""
	layers = [asImage(image) for image in layers]
	outwidth = max(layer.size[0] for layer in layers)
	def scaledToWidth(image):
		if image.size[0] == outwidth:
			return image
		scaleFac = outwidth / image.size[0]
		return image.transform((outwidth, image.size[1]*scaleFac), PIL.Image.AFFINE,
			(1/scaleFac, 0, 0,
			0, 1/scaleFac, 0)
		)
	layers = [scaledToWidth(layer) for layer in layers]
	outheight = max(layer.size[1] for layer in layers)
	outcanvas = blankFrom((outwidth, outheight))
	for layer in layers:
		outcanvas.alpha_composite(layer, (0, outheight-layer.size[1]))
	return outcanvas


mogrifiers = {
	'expand': lambda scale=1.0, topmargin=1.0: lambda fp: expandedHexImage(fp, scale, topmargin),
	'tesselate': lambda scale=1.0: lambda fp: tesselatedHexImage(fp, scale),
	'fuzzCircularDilate': lambda scale=1.0, fuzzedscale=1.5: lambda fp: maskedHexImage(fp, scale, hexMaskCircularOuter(fuzzedscale)),
	'fuzzPolygonalDilate': lambda scale=1.0, fuzzedscale=1.5, sides=6: lambda fp: maskedHexImage(fp, scale, hexMaskPolygonalOuter(fuzzedscale, sides)),
	'fuzzPolygonalFeather': lambda scale=1.0, fuzzedscale=1.5, sides=6: lambda fp: maskedHexImage(fp, scale, hexMaskPolygonalBalanced(fuzzedscale, sides)),
	'shearShadow': lambda scale=1.0, base=0.0, opacity=0.7, blur=0.05, length=1.15, shear=0.6: lambda fp: shadowedOrthoHexImage(fp, expandedfac=scale, base=base, opacity=opacity, blur=blur, length=length, shear=shear),
	'dropShadow': lambda scale=1.0, opacity=0.5, blur=0.01, x=0.05, y=0.05: lambda fp: dropShadowedHexImage(fp, expandedfac=scale, opacity=opacity, blur=blur, x=x, y=y),
	'shift': lambda scale=1.0, x=0.0, y=0.0: lambda fp: shiftedHexImage(fp, scale, x, y),
	'addBackground': lambda *layers: lambda fp: compositedHexImages(*layers, fp)
}


flagSetters = {}

def singleton(cls):
	"""Decorator to turn a class into a single instance."""
	return cls()

@singleton
class FLAGS:
	"""Flags for the script run."""
	MULTIPROCESSING = False

def flag(*names):
	"""Return a decorator to mark a function as representing a script run flag."""
	def flagdeco(func):
		for name in names:
			flagSetters[name] = func
		return func
	return flagdeco

@flag("-P", "--multiprocessing")
def flagMultiprocessing(*argvs):
	"""Use multiple processes and CPU cores to speed up the tileset build."""
	print("Using multiprocessing.")
	FLAGS.MULTIPROCESSING = True
	return argvs

@flag("-h", "--help")
def flagHelp(*argvs):
	"""Print this help text and exit."""
	import os, sys
	global __file__
	if '__file__' not in globals():
		__file__ = "TileTransformer.py"
	print(f"""\n\nUsage: ./{os.path.basename(__file__)} [*options] "<command>(<*[[arg]=[value]]>)" [*files]""")
	print("\nAvailable options:")
	for func in set(flagSetters.values()):
		print(f"\t{', '.join(k for k, v in flagSetters.items() if v is func)}\n\t\t{func.__doc__}")
	print("\nAvailable commands:")
	for m, f in mogrifiers.items():
		print(f"\t{m}({', '.join(f'{n}={v}' for n, v in zip(f.__code__.co_varnames, f.__defaults__ or iter(lambda: '*', None)))})")
	print()
	sys.exit()
	return argvs

def doTransform(*argvs):
	"""Consume the last arguments passed to a script run after all flags have been processed."""
	import sys
	mogstr = argvs[0]
	mogrifier = eval(mogstr, {**mogrifiers})
	global _MOG # Global for pickleability.
	def _MOG(fp): 
		print(f"Doing {mogstr} on {fp}.")
		mogrifier(fp).save(fp)
	inputs = argvs[1:]
	if FLAGS.MULTIPROCESSING:
		import multiprocessing
		with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
			pool.map(_MOG, inputs)
	else:
		print("Multiprocessing is disabled.")
		for fp in inputs:
			_MOG(fp)


if __name__ == '__main__':
	import sys
	argv = tuple(sys.argv[1:])
	try:
		while (len(argv) or None) and argv[0] in flagSetters:
			argv = flagSetters[argv[0]](*argv[1:])
		if not argv:
			raise RuntimeError("No command specified.")
	except Exception as e:
		print(f"Error: {e!r}")
		flagHelp()
	else:
		doTransform(*argv)
