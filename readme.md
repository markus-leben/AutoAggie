# What is this?

AutoAggie is an automated way to use Agatha Harkness to generate season pass levels in Marvel Snap

Before using this, be aware that it is a TOS violation, and may lead to permanent deletion of your account. However, it shouldn't harm any under user, you're always going to lose, and you're going to face mostly bots anyway. 

# How to Install

1. Download this from github.
2. Open marvel snap, set it up in the screen dimensions you'd like AutoAggie to run in, and replace each screencap in images with one of that button on your screen in your screen dimensions.
3. Open settings.json
4. Find the pixel coordinates of a box around each button screencapped in step 2, and edit settings.json with those coordinates
    * On Mac, use shift+command+4 to find those pixel coordinates
    * On PC, use the provided capscoords.AHK
5. Find the pixel coordinates of a pixel in the hexagon of each location that changes color when you're winning, and edit lanepixels in settings.json in the same way. 
6. Give it a test run and see if you've done all this successfully. 

Note that you will have to rerun steps 2-6 any time your screen changes size or location, so it's strongly recommended to force your screen into a specific size. 

This program is also in an extremely rough Alpha state, any forks or edit recommendations are always welcome!