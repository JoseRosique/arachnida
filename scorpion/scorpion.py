# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: joslopez <joslopez@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/17 18:35:23 by joslopez          #+#    #+#              #
#    Updated: 2023/04/18 22:05:51 by joslopez         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(filename):
    with Image.open(filename) as img:
        exifdata = img.getexif()
        if exifdata:
            exif = {}
            for tag_id, value in exifdata.items():
                tag = TAGS.get(tag_id, tag_id)
                exif[tag] = value
            return exif
        else:
            return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: scorpion.py FILE1 [FILE2 ...]")
        sys.exit(1)

    for filename in sys.argv[1:]:
        print("File: %s" % filename)
        exif = get_exif_data(filename)
        if exif:
            print("EXIF data:")
            for tag, value in exif.items():
                print("%s = %s" % (tag, value))
        else:
            print("No EXIF data found.")
