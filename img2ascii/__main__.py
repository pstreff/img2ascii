from img2ascii import app
import argparse


def parse_args():
    parser = argparse.ArgumentParser('Image to ASCII Image')
    parser.add_argument('-W', '--width', help='Width of output image', type=int)
    parser.add_argument('-H', '--height', help='Height of output image', type=int)
    parser.add_argument('-I', '--input', help='Path to input image', default='crash_bandicoot.jpeg')
    parser.add_argument('-Fs', '--font-size', help='Font size to use', type=int, default=10)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    arguments = parse_args()
    app.run(arguments)
