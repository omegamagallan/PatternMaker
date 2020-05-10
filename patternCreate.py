from PIL import Image
import json


def create_pattern(im, width, scale, pattern_type="none_shift"):
    with open("data/pattern_types.json", "r") as read_file:
        patterns = json.load(read_file)
    if pattern_type in patterns:
        scale = int(scale)
        width = int(width)
        pattern = patterns[pattern_type]
        amount = len(pattern) - 1
        width_of_im, length_of_im = im.size
        width_of_im, length_of_im = int(width_of_im / 100 * scale), int(length_of_im / 100 * scale)
        im = im.resize((width_of_im, length_of_im))
        width_of_background, length_of_background = (width_of_im * amount + width * amount,
                                                     length_of_im * amount + width * amount)
        background = Image.new("RGBA", (width_of_background, length_of_background), "#00000000")
        num_of_step = 1
        len_of_steps = len(pattern) - 1
        if pattern[0]:
            for x in range(0, width_of_background, width_of_im + width):
                for y in range(0, length_of_background, length_of_im + width):
                    background = insert_image(im, background, x + int(width / 100 * pattern[num_of_step][0]),
                                              y + int(width / 100 * pattern[num_of_step][1]))
                    if num_of_step == len_of_steps:
                        num_of_step = 0
                    num_of_step += 1
                num_of_step = 1
        else:
            for y in range(0, length_of_background, length_of_im + width):
                for x in range(0, width_of_background, width_of_im + width):
                    background = insert_image(im, background, x + int(width / 100 * pattern[num_of_step][0]),
                                              y + int(width / 100 * pattern[num_of_step][1]))
                    if num_of_step == len_of_steps:
                        num_of_step = 0
                    num_of_step += 1
                num_of_step = 1
        return background
    else:
        return 'fail'


def insert_image(im, background, x, y):
    if im.mode != 'RGBA':
        im = im.convert('RGB')
        im = im.convert('RGBA')
    x_background_size, y_background_size = background.size
    x_im_size, y_im_size = im.size

    im_pixels = im.load()

    background_pixels = background.load()
    actual_x_position, actual_y_position = 0, 0

    for j in range(y, y + y_im_size):
        for i in range(x, x + x_im_size):
            if x_im_size == actual_x_position:
                break
            elif y_im_size == actual_y_position:
                break
            if i < 0:
                x_draw_pixel = i + x_background_size
            else:
                x_draw_pixel = i
            if j < 0:
                y_draw_pixel = j + y_background_size
            else:
                y_draw_pixel = j
            r_back, g_back, b_back, a_back = background_pixels[x_draw_pixel, y_draw_pixel]
            r_im, g_im, b_im, a_im = im_pixels[actual_x_position, actual_y_position]
            background_pixels[x_draw_pixel, y_draw_pixel] = (r_back * a_back + (1 - a_back) * r_im,
                                                             g_back * a_back + (1 - a_back) * g_im,
                                                             b_back * a_back + (1 - a_back) * b_im,
                                                             a_back * a_back + (1 - a_back) * a_im)
            actual_x_position += 1
            if actual_x_position >= x_im_size or x + actual_x_position > x_background_size:
                actual_x_position = 0
                actual_y_position += 1
    return background


if __name__ == '__main__':
    way = input('Введите путь к изображению, для создания паттерна: ') or 'start_pattern_in.png'
    img = Image.open(way, 'r')
    percent = int(input("Введите относительный размер изображения в процентах (число): ") or '10')
    Width = int(input("Введите растояние между изображениями (число): ") or '100')
    with open("data/pattern_types.json", "r") as Read_file:
        patternss = json.load(Read_file)
    Pattern = input(f"Введите название паттерна из предложенного списка\n{' '.join([i for i in patternss])}\n")
    create_pattern(img, Width, percent, Pattern).save("out.png")
    print('Паттерн находится в папке с программой под именем "out.png"')
    input()
