from xml.etree import ElementTree as ET
import sys

colormap = ['#39393a', '#6d1a36','#007480', '#d58936']

def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def is_dark_color(rgb):
    r, g, b = rgb
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b  # Standard luminance formula
    return luminance < 128  # Threshold for dark colors

def extract_colors_from_svg(root):
    colors = set()
    for elem in root.iter():
        for attr, value in elem.attrib.items():
            if 'rgb(' in value:
                colors.add(value)
    return colors

def replace_colors_in_svg(svg_root, existing_colors, colormap):
    colormap_rgb = [hex_to_rgb(color) for color in colormap]
    color_map_dict = {rgb: colormap_rgb[i % len(colormap_rgb)] for i, rgb in enumerate(existing_colors)}

    last_color = None
    for elem in svg_root.iter():

        for attr, value in elem.attrib.items():
            if value.startswith('rgb('):
                # Extract RGB tuple
                rgb_values = tuple(map(int, value.strip('rgb()').split(',')))
                if rgb_values in color_map_dict:
                    # Replace with new color
                    new_rgb = color_map_dict[rgb_values]
                    elem.attrib[attr] = f"rgb({new_rgb[0]},{new_rgb[1]},{new_rgb[2]})"
                    last_color = new_rgb

        # Adjust text color for dark backgrounds
        if elem.tag.endswith('text') and last_color is not None:
            if is_dark_color(last_color):
                elem.attrib['style'] = 'fill:white'  # Set text color to white
            else:
                elem.attrib['style'] = 'fill:black'  # Set text color to black
    
    return svg_root

def remove_background_from_svg(svg_root):
    for elem in svg_root.iter():
        if elem.tag.endswith('rect'):
            if (elem.attrib['fill'] == 'url(#background)'):
                elem.attrib['fill'] = 'none'
    return svg_root

def fix_color(input_svg_path):
    # Load the SVG file
    tree = ET.parse(input_svg_path)
    root = tree.getroot()

    # Namespace handling
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    ET.register_namespace('', namespaces['svg'])

    # Extract colors
    existing_colors = extract_colors_from_svg(root)
    existing_rgb_colors = {tuple(map(int, color.strip('rgb()').split(','))) for color in existing_colors}

    # Replace colors
    modified_svg_root = replace_colors_in_svg(root, existing_rgb_colors, colormap)

    # Remove background
    modified_svg_root = remove_background_from_svg(modified_svg_root)

    # Save the modified SVG
    tree.write(input_svg_path)
