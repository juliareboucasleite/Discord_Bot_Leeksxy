from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO

def create_ship_image(avatar1_url, avatar2_url, percentage, size=(600, 300)):
    bg_color = (255, 192, 115)  # laranja claro
    img = Image.new("RGBA", size, bg_color)
    draw = ImageDraw.Draw(img)

    circle_size = 128
    spacing = 40
    center_y = size[1] // 2
    left_x = size[0] // 2 - circle_size - spacing
    right_x = size[0] // 2 + spacing

    def get_circle_avatar(url):
        response = requests.get(url)
        avatar = Image.open(BytesIO(response.content)).convert("RGBA").resize((circle_size, circle_size))
        mask = Image.new("L", (circle_size, circle_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, circle_size, circle_size), fill=255)
        return ImageOps.fit(avatar, (circle_size, circle_size)), mask

    avatar1, mask1 = get_circle_avatar(avatar1_url)
    avatar2, mask2 = get_circle_avatar(avatar2_url)

    img.paste(avatar1, (left_x, center_y - circle_size // 2), mask1)
    img.paste(avatar2, (right_x, center_y - circle_size // 2), mask2)

    heart_size = 72
    heart = Image.new("RGBA", (heart_size, heart_size), (255, 0, 0, 0))
    heart_draw = ImageDraw.Draw(heart)
    heart_draw.ellipse([0, 0, heart_size, heart_size], fill=(255, 85, 85))
    img.paste(heart, (size[0] // 2 - heart_size // 2, 20), heart)

    percent_text = f"{percentage}%"
    try:
        font = ImageFont.truetype("arialbd.ttf", 42)
    except:
        font = ImageFont.load_default()
    w, h = draw.textsize(percent_text, font=font)
    draw.text(((size[0] - w) // 2, size[1] - h - 20), percent_text, font=font, fill=(255, 255, 255))

    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output
