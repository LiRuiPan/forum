from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
from config import win_font_path, linux_font_path
import platform


# 随机数字0-9:
def rand_digit():
    return random.randint(0, 9)


# 随机字母:
def rand_char():
    if random.randint(0, 1) == 0:
        return chr(random.randint(ord('A'), ord('Z')))
    else:
        return chr(random.randint(ord('a'), ord('z')))


# 随机颜色1:
def rand_color():
    return random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)


# 随机颜色2:
def rand_color2():
    return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)


# 生成验证码内容
def captcha_text():
    s = ''
    for i in range(4):
        if random.randint(0, 1) == 0:
            s += rand_char()
        else:
            s += str(rand_digit())
    return s


# 生成验证码存储路径
def captcha_path():
    s = 'cap' + str(random.randint(0, 999))
    filename = '{}.jpg'.format(s)
    path = os.path.join('static', 'photos', 'captcha', filename)
    print(path)
    return path


# 生成验证码图片
def captcha_image(content, path):
    # 120 x 36:
    width = 30 * 4
    height = 36
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    if platform.system() == "Windows":
        font_path = win_font_path
    else:
        font_path = linux_font_path
    font = ImageFont.truetype(font_path, 25)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rand_color())
    # 输出文字:
    for i in range(4):
        draw.text((30 * i + 5, 5), content[i], font=font, fill=(0, 0, 0))
    image.save(path, 'jpeg')