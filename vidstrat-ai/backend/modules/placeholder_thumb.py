from PIL import Image, ImageDraw, ImageFont
import textwrap
from .cache import thumb_file_path_for_video, thumb_url_for_video, ensure_dirs
import os


def generate_placeholder_image(key: str, text: str = None, size=(1280, 720)) -> str:
    """Generate a simple placeholder JPEG with the given text and save it to thumbs dir.
    Returns the URL path (e.g., /static/thumbs/<key>.jpg).
    """
    ensure_dirs()
    path = thumb_file_path_for_video(key)
    try:
        w, h = size
        # create background color based on key hash
        color_seed = abs(hash(key)) % 0xFFFFFF
        bg = ((color_seed >> 16) & 0xFF, (color_seed >> 8) & 0xFF, color_seed & 0xFF)
        img = Image.new('RGB', (w, h), color=bg)
        draw = ImageDraw.Draw(img)

        # prepare text
        if not text:
            text = key
        # wrap text to multiple lines
        max_width = 30
        lines = textwrap.wrap(text, width=max_width)

        # font
        try:
            font = ImageFont.truetype("arial.ttf", size=int(h * 0.09))
        except Exception:
            font = ImageFont.load_default()

        # compute total text height (use draw.textsize for compatibility)
        try:
            line_height = draw.textsize('A', font=font)[1] + 8
        except Exception:
            try:
                ascent, descent = font.getmetrics()
                line_height = ascent + descent + 8
            except Exception:
                line_height = int(h * 0.09) + 8
        total_h = line_height * len(lines)
        y = (h - total_h) // 2
        for line in lines:
            try:
                tw, th = draw.textsize(line, font=font)
            except Exception:
                tw, th = (len(line) * 10, line_height)
            x = (w - tw) // 2
            # draw outline for readability
            outline_color = (0, 0, 0)
            for ox, oy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                draw.text((x + ox, y + oy), line, font=font, fill=outline_color)
            draw.text((x, y), line, font=font, fill=(255, 255, 255))
            y += line_height

        # save as JPEG
        img.save(path, format='JPEG', quality=80)
        return thumb_url_for_video(key)
    except Exception:
        # on failure, return empty string
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
        return ""
