# original script: https://scipython.com/blog/floyd-steinberg-dithering/

import numpy as np
import streamlit as st
from PIL import Image  # Pillow: https://pillow.readthedocs.io/en/stable/index.html
from os import path

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
  # Read in the image, convert to 8-bit greyscale.
  img = Image.open(uploaded_file)
  img = img.convert('L')  # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
  width, height = img.size

def get_new_val(old_val, nc):
    """
    Get the "closest" colour to old_val in the range [0,1] per channel divided
    into nc values.

    """

    return np.round(old_val * (nc - 1)) / (nc - 1)


def fs_dither(img, nc):
    """
    Floyd-Steinberg dither the image img into a palette with nc colours per
    channel.

    """

    arr = np.array(img, dtype=float) / 255

    for ir in range(height):
        for ic in range(width):
            # NB need to copy here for RGB arrays otherwise err will be (0,0,0)!
            old_val = arr[ir, ic].copy()
            new_val = get_new_val(old_val, nc)
            arr[ir, ic] = new_val
            err = old_val - new_val
            # In this simple example, we will just ignore the border pixels.
            if ic < width - 1:
                arr[ir, ic+1] += err * 7/16
            if ir < height - 1:
                if ic > 0:
                    arr[ir+1, ic-1] += err * 3/16
                arr[ir+1, ic] += err * 5/16
                if ic < width - 1:
                    arr[ir+1, ic+1] += err / 16

    carr = np.array(arr/np.max(arr, axis=(0,1)) * 255, dtype=np.uint8)
    return Image.fromarray(carr)

if uploaded_file is not None:
  nc = 2  # two colours: black and white
  # dim = fs_dither(img, nc)
  st.image(img, caption='output')  # https://discuss.streamlit.io/t/need-help-displaying-images/54490
