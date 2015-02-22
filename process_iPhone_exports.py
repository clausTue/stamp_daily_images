#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
background: 
- Pictures exported from iPhoto do not have their original date in the finder. 
- This info is hidden in exif
- this has to do with the daily photo app on iOS

This script
- loops over images in a folder (exported from iPhoto)
- extracts date-time-stamp from exif information
- saves image with a date stamp (PIL)

possible Improvements:
- currently movie is made using command line `mencoder`. This could soon be accomplished using OpenCV

"""

import sys
import os
import datetime
import numpy as np

from PIL import Image
from PIL.ExifTags import TAGS
from PIL import ImageFont
from PIL import ImageDraw 

__author__ = "Claus Haslauer (mail@planetwater.org)"
__version__ = "$Revision: 0.1 $"
__date__ = datetime.date(2015,2,21)
__copyright__ = "Copyright (c) 2015 Claus P. Haslauer"
__license__ = "Python"


def main():
    # folder where images (exported from iPhoto) reside
    top_path = r'XXX'
    # folder where output images are to be saved
    out_path = r'YYY'
    
    # FONT info: path where your fonts reside
    font_path = r'/YYY'  
    font_file = "AlteHaasGroteskRegular.ttf"
    
    
    
    
    # start investigating into top_path
    filenames = next(os.walk(top_path))[2]
    n_fnames = len(filenames)
    print "found %i pictures" % n_fnames
    
    for cur_fname in filenames:#[:10]:
        if cur_fname[0] != '.':
            print cur_fname
            cur_fobj = os.path.join(top_path,cur_fname)
            
            # EXIF INFORMATION
            cur_exif = get_exif(cur_fobj)
            aufnahme_datum_str = cur_exif['DateTimeOriginal']
            # 'DateTimeOriginal': '2014:08:27 14:01:39'
            aufname_time_fmt = '%Y:%m:%d %H:%M:%S'
            aufname_datum = datetime.datetime.strptime(aufnahme_datum_str, aufname_time_fmt)
            # 'ExifImageHeight': 1280,
            height = int(cur_exif['ExifImageHeight'])
            width = int(cur_exif['ExifImageWidth'])
            
            
            # SHOW IMAGE
            im = Image.open(cur_fobj)
            draw = ImageDraw.Draw(im)
            font_fobj = os.path.join(font_path, font_file)
            font = ImageFont.truetype(font_fobj, 44)
            time_format = "%d-%b-%y"
            date_to_print = aufname_datum.strftime(time_format)
            draw.text((44, 0.95*height)
                    , date_to_print
                    ,(255,255,255)
                    ,font=font) # 
            #im.show()
            out_fname = cur_fname[:-4] + '.png'
            #print out_fname
            
            out_fobj = os.path.join(out_path, out_fname)
            im.save(out_fobj, 'PNG')
    
    
            # mencoder "mf://*.png" -o movie_out.avi -ovc x264 [-ofps 0.1]

            # from mayavi doc: http://docs.enthought.com/mayavi/mayavi/tips.html#making-movies-from-a-stack-of-images
            # mencoder "mf://*.png" -mf fps=1 -o anim.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=500
            
            # possibly this could be done using openCV
            # v 3.0 is currently in beta
            # http://stackoverflow.com/questions/14440400/creating-a-video-using-opencv-2-4-0-in-python
            #http://opencv.org

    print "Done! Yay!"


def get_exif(fn):
    """
    this is what a typical exif dictionary looks like
    {41990: 0,
         'ColorSpace': 1,
         'ComponentsConfiguration': '\x01\x02\x03\x00',
         'DateTime': '2014:08:27 14:01:39',
         'DateTimeDigitized': '2014:08:27 14:01:39',
         'DateTimeOriginal': '2014:08:27 14:01:39',
         'ExifImageHeight': 1280,
         'ExifImageWidth': 960,
         'ExifOffset': 140,
         'ExifVersion': '0221',
         'FlashPixVersion': '0100',
         'Orientation': 1,
         'ResolutionUnit': 2,
         'Software': 'Dayli',
         'XResolution': (72, 1),
         'YResolution': (72, 1)}
    """
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret


if __name__ == '__main__':
    main()