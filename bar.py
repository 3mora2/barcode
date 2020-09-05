# from barcode import generate
from barcode import Code39, Code128
import cv2
import numpy as np
from barcode.writer import ImageWriter
from io import BytesIO


def combine_vertically(l):
    # https://www.life2coding.com/combine-several-images-vertically-with-padding-using-opencv-python/
    images = []
    max_width = 0  # find the max width of all the images
    total_height = 0  # the total height of the images (vertical stacking)

    # for img in image:
    h = 3
    w = .23
    f = 15
    for text, ty in l:
        rv = BytesIO()
        option = {'module_width': w, 'module_height': h, 'quiet_zone': 6.5, 'text_distance': 1, 'font_size': f}
        h += 1
        # w = .22
        f = 17
        if len(text) > 10:
            text1 = text
        else:
            text1 = text.replace('', ' ').strip()
        Code128(text, writer=ImageWriter()).write(rv, options=option, text=text1)
        # Code39(text, writer=ImageWriter(), add_checksum=False).write(rv, options=option, text=text1)
        # generate('EAN13', text, writer=ImageWriter(), output=rv, writer_options=option)
        file_bytes = np.asarray(bytearray(rv.getvalue()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)[8:-15, :, :]
        # open all images and find their sizes
        images.append((img, ty))

        image_width = img.shape[1]
        image_height = img.shape[0]

        if image_width > max_width:
            max_width = image_width

        # add all the images heights
        total_height += image_height

    final_image = np.zeros((total_height + 200, max_width + 70, 3), dtype=np.uint8)
    final_image.fill(255)

    current_y = 50  # keep track of where your current image was last placed in the y coordinate
    current_x = 55
    w = 30
    h = 30
    n = 1
    cv2.putText(final_image, ' Trevi', (200, 39), cv2.FONT_ITALIC, 1, (0, 0, 0), 2, cv2.LINE_AA)
    for image, txt in images:
        # add an image to the final array and increment the y coordinate
        height = image.shape[0]
        width = image.shape[1]
        final_image[current_y:height + current_y, current_x:width + current_x, :] = image

        cv2.putText(final_image, txt, (w, current_y + h), cv2.FONT_ITALIC, 1, (0, 0, 0), 2,cv2.LINE_AA)
        h = 40
        current_x = 100
        # current_x = 80
        if n == 2:
            w = 20
            # current_x = 80
        current_y += height
        n += 1
    t = 'Bluetooth Wireless In-Ear Earbuds With Charging Case White'.strip()
    if len(t) > 32:
        n1 = t.find(' ', 30)
        if n1 < 35:
            t1 = f'{t[:n1].strip()}'
            cv2.putText(final_image, t1, (w, current_y + h), cv2.FONT_HERSHEY_SIMPLEX, .9, (0, 0, 0), 2, cv2.LINE_AA)
            current_y = current_y+h
            t1 = f'{t[n1:].strip()}'
            cv2.putText(final_image, t1, (w, current_y + h), cv2.FONT_HERSHEY_SIMPLEX, .9, (0, 0, 0), 2, cv2.LINE_AA)

    return final_image


img = combine_vertically([('A01033013N', 'ASN'), ('622739493629', 'SKU'), ('622739493629', 'Barcode')])
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('img.png', img)
# rv = BytesIO()
# option = {'module_width': 0.1, 'module_height': 6, 'quiet_zone': 6.5, 'text_distance': .5, 'font_size': 15}
# Code39('622739493629', writer=ImageWriter(), add_checksum=False).write(rv, options=option,text='')
# Code39('A01033013N', writer=ImageWriter(), add_checksum=False).write(rv, options=option)
# generate('UPCA', '622739493629', writer=ImageWriter(), output=rv, writer_options=option)
# file_bytes = np.asarray(bytearray(rv.getvalue()), dtype=np.uint8)
# img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
# cv2.imshow("Image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# file_bytes = np.asarray(bytearray(rv.getvalue()), dtype=np.uint8)
# img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)[8:-15, :, :]

# img_3 = np.zeros([512, 512, 3], dtype=np.uint8)
# img_3.fill(255)
# # cv2.putText(img_3, 'ADS : ', (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1, cv2.LINE_AA)
# cv2.imshow('3 Channel Window', img_3)
# print("image shape: ", img_3.shape)
# cv2.waitKey(0)
#
#
# print("image shape: ", img1.shape)
#
# cv2.imshow("Image", img1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# img_all = cv2.add(img_3, img)
# # cv2.imshow("Image", img_all)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# img_to_save = Image.frombytes("RGB", the_siz, p)
# img_to_save.save(name)

# img = EAN13(str(100000902922), writer=ImageWriter()).write(rv)

# or sure, to an actual file:
# with open('somefile.jpeg', 'wb') as f:
#     EAN13('100000011111', writer=ImageWriter()).write(f)
'''
module_width:	The width of one barcode module in mm as float. Defaults to 0.2.
module_height:	The height of the barcode modules in mm as float. Defaults to 15.0.
quiet_zone:	Distance on the left and on the right from the border to the first (last) barcode module in mm as float. Defaults to 6.5.
font_path:	Path to the font file to be used. Defaults to DejaVuSansMono (which is bundled with this package).
font_size:	Font size of the text under the barcode in pt as integer. Defaults to 10.
text_distance:	Distance between the barcode and the text under it in mm as float. Defaults to 5.0.
background:	The background color of the created barcode as string. Defaults to white.
foreground:	The foreground and text color of the created barcode as string. Defaults to black.

New in version 0.6.
center_text:	If true (the default) the text is centered under the barcode else left aligned.
'''
