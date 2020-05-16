from typing import Optional, Mapping, Iterable, Any, Union

from flask import Markup

from .web import space_join_cond


STYLE_CLASS_MAPPING = {
	'solid': 'fas',
	'regular': 'far',
	'light': 'fal',
	'brands': 'fab',
	}


def _style_class(style):
	try:
		return STYLE_CLASS_MAPPING[style]
	except KeyError:
		options = STYLE_CLASS_MAPPING.keys()
		raise ValueError(f'style must be one of {options}')


def fa_icon(
		name: str,
		style: str = 'solid',
		size: str = None,
		fixed_width: bool = False,
		brand_color: bool = False,
		title: str = None,
		*,
		add_classes: Union[Mapping[str, Any], Iterable[str]] = None,
		add_attrs: Mapping[str, Optional[str]] = None,
		) -> Markup:
	"""Render a FontAwesome icon.

	See: http://fontawesome.io/examples/

	Args:
		name: The name of the icon from FontAwesome.
		style: 'solid', 'regular', 'light', 'brand'
		size: options are 'xs', 'sm', 'lg', '2x', '3x', '4x', '5x', '7x', '10x'
			or None for the default.
		fixed_width: Whether to display
		brand_color: Whether or not to display the icon in the brand color.
		title: An optional title attribute for the element.
		add_classes: A Collection of additional classes to add to the element.
		add_attrs: A Mapping from
	"""
	# Additional improvements:
	# lists:
	#  https://fontawesome.com/how-to-use/on-the-web/styling/icons-in-a-list
	# rotating/flipping:
	#  https://fontawesome.com/how-to-use/on-the-web/styling/rotating-icons
	# animating:
	#  https://fontawesome.com/how-to-use/on-the-web/styling/animating-icons
	# border/pull:
	#  https://fontawesome.com/how-to-use/on-the-web/styling/bordered-pulled-icons
	# stacking:
	#  https://fontawesome.com/how-to-use/on-the-web/styling/stacking-icons
	# power-transforms:
	#  https://fontawesome.com/how-to-use/on-the-web/styling/power-transforms
	# masking:
	#  https://fontawesome.com/how-to-use/on-the-web/styling/masking
	# layering:
	#  https://fontawesome.com/how-to-use/on-the-web/styling/layering
	style_class = _style_class(style)
	classes = {
		style_class: True,
		f'fa-{name}': True,
		'fa-color': brand_color,
		f'fa-{size}': size,
		'fa-fw': fixed_width,
		}
	if add_classes:
		if not isinstance(add_classes, Mapping):
			add_classes = {val: True for val in add_classes}
		classes.update(add_classes)
	attrs = {
		'class': space_join_cond(classes),
		}
	if title:
		attrs['title'] = title
	if add_attrs:
		attrs.update(add_attrs)
	attr_strings = []
	for k, v in attrs.items():
		if v is None:
			attr_strings.append(k)
		else:
			attr_strings.append(f'{k}="{v}"')
	attr_string = ' '.join(attr_strings)
	return Markup(f'<span {attr_string}></span>')
