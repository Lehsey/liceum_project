from PIL import Image

def slicing(image_name, rows, column):
    imag = Image.open('data\\sprites\\' + image_name + '.png')
    orig_x, orig_y = imag.size
    need_x, need_y = orig_x // column, orig_y // rows
    num = 0
    for j in range(rows):
        for i in range(column):
            need_sprite = imag.crop((need_x * i, need_y * j, need_x * (i + 1), need_y * (j + 1)))
            need_sprite.save(image_name + f'_{num}.png')
            num += 1
            need_sprite.close()
    imag.close()

slicing('player_run_l', 1, 8)