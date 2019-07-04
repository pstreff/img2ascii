from PIL import Image, ImageDraw, ImageFont, ImageOps


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


def grayscale_image(image: Image):
    return image.convert('L')


def calculate_cols_and_rows(size: dict, character_size: dict):
    cols = size['width'] // character_size['width']
    print(str(cols) + ' Columns')

    rows = size['height'] // character_size['height']
    print(str(rows) + ' Rows')

    return cols, rows


def choose_output_dimensions(arguments, image: Image):
    output_width = arguments.width if arguments.width else image.size[0]
    output_height = arguments.height if arguments.height else image.size[1]

    return output_width, output_height


def run(arguments):
    base = Image.open(arguments.input)

    grayscaled_image = grayscale_image(base)

    fnt = ImageFont.truetype('Courier.dfont', arguments.font_size)

    char_list = '@%#*+=-:. '
    # char_list = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    max_char_width, max_char_height = get_max_char_size(char_list, fnt)

    print('Original Size: ' + str(grayscaled_image.size))

    output_width, output_height = choose_output_dimensions(arguments, grayscaled_image)
    print('Output Image Size: Width: ' + str(output_width) + ' Height: ' + str(output_height))

    cols, rows = calculate_cols_and_rows(
        size={'width': output_width, 'height': output_height},
        character_size={'width': max_char_width, 'height': max_char_height}
    )

    mask_width = grayscaled_image.size[0] // cols
    mask_height = grayscaled_image.size[1] // rows

    print('Mask size: ' + str(mask_width) + 'x' + str(mask_height))

    output_image = Image.new('L', (output_width, output_height), 255)

    draw = ImageDraw.Draw(output_image)
    grayscaled_image.show()
    for j in range(0, rows):
        for i in range(0, cols):
            width_from = i*mask_width
            width_to = i*mask_width + mask_width - 1
            height_from = j*mask_height
            height_to = j*mask_height + mask_height - 1

            pixel_sum = sum_pixels_under_mask(grayscaled_image, height_from, height_to, width_from, width_to)

            average = pixel_sum / (mask_width * mask_height)
            average = round(average * len(char_list) / 255)

            fitting_char = char_list[min(average, len(char_list)-1)]
            draw.text((i * max_char_width, j * max_char_height), fitting_char, fill=0, font=fnt)

    output_image.show()
    ImageOps.invert(output_image).show()
