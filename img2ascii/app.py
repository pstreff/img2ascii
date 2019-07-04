from PIL import Image, ImageDraw, ImageFont


def get_max_char_size(char_list, fnt):
    max_height = max_width = 0
    for char in char_list:
        char_width, char_height = fnt.getsize(char)
        if char_height > max_height:
            max_height = char_height
        if char_width > max_width:
            max_width = char_width

    print('max char size => ' + str(max_width) + ' ' + str(max_height))
    return max_width, max_height


def sum_pixels_under_mask(grayscaled_image, height_from, height_to, width_from, width_to):
    pixel_sum = 0

    for mask_j in range(height_from, height_to):
        for mask_i in range(width_from, width_to):
            pixel_sum += grayscaled_image.getpixel(xy=(mask_i, mask_j))

    return pixel_sum


def grayscaleImage(image: Image):
    return image.convert('L')


def run():
    base = Image.open('test.jpg')

    grayscaled_image = grayscaleImage(base)

    fnt = ImageFont.truetype('Courier.dfont', 10)

    char_list = '@%#*+=-:. '
    # char_list = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    max_char_width, max_char_height = get_max_char_size(char_list, fnt)

    cols = grayscaled_image.size[0] // max_char_width
    print('Original Size: ' + str(grayscaled_image.size))
    print(str(cols) + ' Columns | Cutoff: ' + str(grayscaled_image.size[0] - (cols * max_char_width)) + ' Pixel')

    rows = grayscaled_image.size[1] // max_char_height
    print(str(rows) + ' Rows | Cutoff: ' + str(grayscaled_image.size[1] - (rows * max_char_height)) + ' Pixel')

    output_image = Image.new('L', grayscaled_image.size, 255)

    draw = ImageDraw.Draw(output_image)
    grayscaled_image.show()
    for j in range(0, rows):
        for i in range(0, cols):
            width_from = i*max_char_width
            width_to = i*max_char_width + max_char_width - 1
            height_from = j*max_char_height
            height_to = j*max_char_height + max_char_height - 1

            pixel_sum = sum_pixels_under_mask(grayscaled_image, height_from, height_to, width_from, width_to)

            average = pixel_sum / (max_char_width * max_char_height)
            average = round(average * len(char_list) / 255)

            fitting_char = char_list[min(average, len(char_list)-1)]
            draw.text((width_from, height_from), fitting_char, fill=0, font=fnt)

    output_image.show()



