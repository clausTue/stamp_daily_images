# stamp_daily_images
process daily images with date stamp and make movie

background: 
- iOS app "[daily](https://twitter.com/DayliApp)" used to make pictures, daily
- can export pictures to photo-stream, then to iPhoto

this script
- Pictures exported from iPhoto do not have their original date in the finder. 
- This info is hidden in exif
- this has to do with the daily photo app on iOS

the code
- loops over images in a folder (exported from iPhoto)
- extracts date-time-stamp from exif information
- saves image with a date stamp (PIL)

possible improvements:
- currently movie is made using command line `mencoder`. This could soon be accomplished using OpenCV