# MatplotLeap
Plotting the hand using a Leap Motion, and other data science tasks.  

![Plotting the hand in MatplotLib](media/MatPlotLeap.gif?raw=true)

After getting Leap Motion up and running with a SWIG wrapper:

```
# Tested on Ubuntu 20.04 LTS
sudo leapd
# Open a seperate terminal
python3 plot_hand.py
```

By default `plot_hand` saves all the gathered data in all_points.csv.   
These can be animated and shown using `python3 animate_saved.py`.   

### Windows Support
resources/Windows includes a LeapSDK generated for Python 3.8 and Orion 4.1.0  

If python3.8 is not your base install of windows, you may need to install a separate version.  
For example you can install python 3.8.9 [here](https://www.python.org/downloads/release/python-389/).  
You can install it in a virtualenv, see [tutorial](https://www.freecodecamp.org/news/installing-multiple-python-versions-on-windows-using-virtualenv/).


For use with Ubuntu, see the [Ubuntu branch](https://github.com/PerlinWarp/MatplotLeap/tree/Ubuntu) for the last tested Ubuntu version.  

### Resources
[Generating a Python 3.3.0 Wrapper with SWIG 2.0.9](https://support.leapmotion.com/hc/en-us/articles/360004362237-Generating-a-Python-3-3-0-Wrapper-with-SWIG-2-0-9)  
[Using Leap Motion on Ubuntu](https://blog.keithkim.com/2020/07/note-leap-motion-on-ubuntu-2004.html)

#### To Do:
Fix the wrist measurement using the [bone](https://developer-archive.leapmotion.com/documentation/python/api/Leap.Bone.html) length and direction.  
The current wrist measurement, I believe is a mid point from the wrist, it is shifted up compared to the thumb metacarpal.
