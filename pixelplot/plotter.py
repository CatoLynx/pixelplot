from PIL import Image, ImageDraw, ImageFont
from .dashedimagedraw import DashedImageDraw


def _map(in_val, in_min, in_max, out_min, out_max):
    return (in_val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def _format_label(value, decimals):
    if decimals == 0:
        return str(int(round(value)))
    elif decimals > 0:
        return str(round(value, decimals))
    else:
        return str(value)

def xy_skel(width, height, points,
        x_min=None,
        x_max=None,
        x_tick_interval=0,
        x_tick_length=2,
        x_tick_space=1,
        x_tick_label_decimals=0,
        x_label=None,
        x_label_space=2,
        x_grid_style=None,
        y_min=None,
        y_max=None,
        y_tick_interval=0,
        y_tick_length=2,
        y_tick_space=1,
        y_tick_label_decimals=0,
        y_label=None,
        y_label_space=2,
        y_grid_style=None,
        data_label_font=None,
        axis_label_font=None,
        bgcolor="#00000000",
        fgcolor="#000000ff"):
    img = Image.new('RGBA', (width, height), bgcolor)
    draw = DashedImageDraw(img)
    
    # Load fonts if applicable
    if data_label_font is not None and not isinstance(data_label_font, ImageFont.ImageFont):
        data_label_font = ImageFont.load(data_label_font)
    if axis_label_font is not None and not isinstance(axis_label_font, ImageFont.ImageFont):
        axis_label_font = ImageFont.load(axis_label_font)
    
    # Calculate X axis limits if not given
    if x_min is None:
        x_min = min((p[0] for p in points))
    else:
        points = list(filter(lambda p: p[0] >= x_min, points))
        
    if x_max is None:
        x_max = max((p[0] for p in points))
    else:
        points = list(filter(lambda p: p[0] <= x_max, points))
    
    x_span = x_max - x_min
    
    # Calculate Y axis limits if not given
    if y_min is None:
        y_min = min((p[1] for p in points))
    else:
        points = list(filter(lambda p: p[1] >= y_min, points))
    
    if y_max is None:
        y_max = max((p[1] for p in points))
    else:
        points = list(filter(lambda p: p[1] <= y_max, points))
    
    y_span = y_max - y_min
    
    # Calculate X tick interval if applicable
    if x_tick_interval < 0:
        # <0 means we have n ticks distributed across the axis
        x_tick_count = -x_tick_interval
        x_tick_interval = x_span / (-x_tick_interval)
    else:
        x_tick_count = -1
    
    # Calculate Y tick interval if applicable
    if y_tick_interval < 0:
        # <0 means we have n ticks distributed across the axis
        y_tick_count = -y_tick_interval
        y_tick_interval = y_span / (-y_tick_interval)
    else:
        y_tick_count = -1
    
    # Calculate X tick positions
    if x_tick_interval > 0:
        x_tick_pos = x_min
        x_ticks = []
        while x_tick_pos < x_max:
            x_ticks.append(x_tick_pos)
            x_tick_pos += x_tick_interval
        if x_tick_count > 0:
            x_ticks = x_ticks[:x_tick_count]
        
        # Determine how much space the X data/axis labels will take up
        if data_label_font is not None:
            temp_img = Image.new('L', (width, height), 0)
            temp_draw = ImageDraw.Draw(temp_img)
            for pos in x_ticks:
                temp_draw.text((0, 0), _format_label(pos, x_tick_label_decimals), font=data_label_font, fill=255)
            bbox = temp_img.getbbox()
            x_tick_label_max_width = bbox[2] - bbox[0]
            font_height = bbox[3] - bbox[1]
            font_offset_x = bbox[0]
            font_offset_y = bbox[1]
            x_axis_y = height - 1 - font_height - x_tick_space - x_tick_length
        else:
            x_axis_y = height - 1 - x_tick_length
    else:
        x_axis_y = height - 1
        x_ticks = []
        
    if x_label and axis_label_font is not None:
        temp_img = Image.new('L', (width, height), 0)
        temp_draw = ImageDraw.Draw(temp_img)
        temp_draw.text((0, 0), x_label, font=axis_label_font, fill=255)
        bbox = temp_img.getbbox()
        x_label_width = bbox[2] - bbox[0]
        x_label_height = bbox[3] - bbox[1]
        x_label_offset_x = bbox[0]
        x_label_offset_y = bbox[1]
        x_axis_y -= x_label_height + x_label_space
    else:
        x_label_width = 0
        x_label_height = 0
        x_label_offset_x = 0
        x_label_offset_y = 0
    
    # Calculate Y tick positions
    if y_tick_interval > 0:
        y_tick_pos = y_min
        y_ticks = []
        while y_tick_pos < y_max:
            y_ticks.append(y_tick_pos)
            y_tick_pos += y_tick_interval
        if y_tick_count > 0:
            y_ticks = y_ticks[:y_tick_count]
        
        # Determine how much space the Y data/axis labels will take up
        if data_label_font is not None:
            temp_img = Image.new('L', (width, height), 0)
            temp_draw = ImageDraw.Draw(temp_img)
            for pos in y_ticks:
                temp_draw.text((0, 0), _format_label(pos, y_tick_label_decimals), font=data_label_font, fill=255)
            bbox = temp_img.getbbox()
            y_tick_label_max_width = bbox[2] - bbox[0]
            font_height = bbox[3] - bbox[1]
            font_offset_x = bbox[0]
            font_offset_y = bbox[1]
            y_axis_x = y_tick_label_max_width + y_tick_space + y_tick_length
        else:
            y_axis_x = y_tick_length
    else:
        y_axis_x = 0
        y_ticks = []
        
    if y_label and axis_label_font is not None:
        temp_img = Image.new('L', (width, height), 0)
        temp_draw = ImageDraw.Draw(temp_img)
        temp_draw.text((0, 0), y_label, font=axis_label_font, fill=255)
        bbox = temp_img.getbbox()
        # Keep in mind that this will be rotated 90 degrees
        y_label_width = bbox[2] - bbox[0]
        y_label_height = bbox[3] - bbox[1]
        y_label_offset_x = bbox[0]
        y_label_offset_y = bbox[1]
        y_axis_x += y_label_height + y_label_space
    else:
        y_label_width = 0
        y_label_height = 0
        y_label_offset_x = 0
        y_label_offset_y = 0
    
    # Define axes origin
    origin = (y_axis_x, x_axis_y)
    
    # Calculate scaling factors and functions
    x_scale = (width - origin[0]) / x_span
    y_scale = (height - origin[1]) / y_span
    
    def _x_pos(x_val):
        return round(_map(x_val, x_min, x_max, origin[0], width - 1))
    
    def _y_pos(y_val):
        return round(_map(y_val, y_min, y_max, origin[1], 0))
    
    # Draw X and Y axes
    draw.line((origin, (width - 1, x_axis_y)), fill=fgcolor)
    draw.line((origin, (y_axis_x, 0)), fill=fgcolor)
    
    # Draw X and Y axis caps
    draw.line(((width - 2, x_axis_y - 1), (width - 2, x_axis_y + 1)), fill=fgcolor)
    draw.line(((width - 3, x_axis_y - 2), (width - 3, x_axis_y + 2)), fill=fgcolor)
    draw.line(((y_axis_x - 1, 1), (y_axis_x + 1, 1)), fill=fgcolor)
    draw.line(((y_axis_x - 2, 2), (y_axis_x + 2, 2)), fill=fgcolor)
    
    # Draw X grid if applicable
    if x_grid_style:
        for pos in x_ticks:
            if type(x_grid_style) in (tuple, list):
                # Draw dashed line with dash pattern according to given sequence
                draw.dashed_line(((_x_pos(pos), x_axis_y), (_x_pos(pos), 0)), dash=x_grid_style, fill=fgcolor)
            else:
                # Draw solid line
                draw.line(((_x_pos(pos), x_axis_y), (_x_pos(pos), 0)), fill=fgcolor)
    
    # Draw Y grid if applicable
    if y_grid_style:
        for pos in y_ticks:
            if type(y_grid_style) in (tuple, list):
                # Draw dashed line with dash pattern according to given sequence
                draw.dashed_line(((y_axis_x, _y_pos(pos)), (width - 1, _y_pos(pos))), dash=y_grid_style, fill=fgcolor)
            else:
                # Draw solid line
                draw.line(((y_axis_x, _y_pos(pos)), (width - 1, _y_pos(pos))), fill=fgcolor)
    
    # Draw X axis ticks and data/axis labels if applicable
    if x_ticks:
        for pos in x_ticks:
            tick_x = _x_pos(pos)
            draw.line(((tick_x, x_axis_y), (tick_x, x_axis_y + x_tick_length)), fill=fgcolor)
            if data_label_font is not None:
                text = _format_label(pos, x_tick_label_decimals)
                temp_img = Image.new('RGBA', (x_tick_label_max_width, font_height), "#00000000")
                temp_draw = ImageDraw.Draw(temp_img)
                temp_draw.text((-font_offset_x, -font_offset_y), text, font=data_label_font, fill=fgcolor)
                bbox = temp_img.getbbox()
                label_y = x_axis_y + x_tick_length + x_tick_space + 1
                label_x = tick_x - (bbox[2] // 2)
                img.paste(temp_img, (label_x, label_y), temp_img)
            if x_label and axis_label_font is not None:
                temp_img = Image.new('RGBA', (x_label_width, font_height), "#00000000")
                temp_draw = ImageDraw.Draw(temp_img)
                temp_draw.text((-x_label_offset_x, -x_label_offset_y), x_label, font=axis_label_font, fill=fgcolor)
                label_y = x_axis_y + x_tick_length + x_tick_space + 1 + font_height + x_label_space
                label_x = y_axis_x + (width - y_axis_x - x_label_width) // 2
                img.paste(temp_img, (label_x, label_y), temp_img)
    
    # Draw Y axis ticks and data/axis labels if applicable
    if y_ticks:
        for pos in y_ticks:
            tick_y = _y_pos(pos)
            draw.line(((y_axis_x, tick_y), (y_axis_x - y_tick_length, tick_y)), fill=fgcolor)
            if data_label_font is not None:
                text = _format_label(pos, y_tick_label_decimals)
                temp_img = Image.new('RGBA', (y_tick_label_max_width, font_height), "#00000000")
                temp_draw = ImageDraw.Draw(temp_img)
                temp_draw.text((-font_offset_x, -font_offset_y), text, font=data_label_font, fill=fgcolor)
                bbox = temp_img.getbbox()
                label_y = tick_y - (bbox[3] // 2)
                label_x = y_tick_label_max_width - bbox[2]
                if y_label and axis_label_font is not None:
                    label_x += y_label_height + y_label_space
                img.paste(temp_img, (label_x, label_y), temp_img)
            if y_label and axis_label_font is not None:
                temp_img = Image.new('RGBA', (y_label_width, font_height), "#00000000")
                temp_draw = ImageDraw.Draw(temp_img)
                temp_draw.text((-y_label_offset_x, -y_label_offset_y), y_label, font=axis_label_font, fill=fgcolor)
                label_y = (x_axis_y - y_label_width) // 2
                label_x = 0
                temp_img = temp_img.rotate(90, expand=True)
                img.paste(temp_img, (label_x, label_y), temp_img)
    
    # Return: Plot image, axis intersection coordinates, filtered points (based on X/Y axes ranges), X/Y scaling functions
    return (img, origin, points, _x_pos, _y_pos)

def xy_line(width, height, points, *args, **kwargs):
    img, origin, points, _x_pos, _y_pos = xy_skel(width, height, points, *args, **kwargs)
    draw = ImageDraw.Draw(img)
    for i in range(len(points) - 1):
        draw.line(((_x_pos(points[i][0]), _y_pos(points[i][1])), (_x_pos(points[i+1][0]), _y_pos(points[i+1][1]))), fill=kwargs['fgcolor'])
    img.show()

def xy_bars(width, height, points, bar_width, *args, **kwargs):
    img, origin, points, _x_pos, _y_pos = xy_skel(width, height, points, *args, **kwargs)
    draw = ImageDraw.Draw(img)
    for i in range(len(points)):
        draw.rectangle([(_x_pos(points[i][0]) - bar_width//2, origin[1]), (_x_pos(points[i][0]) - bar_width//2 + bar_width, _y_pos(points[i][1]))], fill=kwargs['fgcolor'])
    return img
