game
====
This game is made by me and <a href="https://github.com/nitinsaroha">Nitin</a> for kivy contest.Hope people like it.

Requirements:
    cython
    cymunk

First make sure you have kivy installed.
Then install cython and cymunk.

1. <a href="http://cython.org">Cython</a>
Download latest release from <a href="http://cython.org">cython.org</a>
Unpack the tarball or zip file, enter the directory, and then run:
    
    python setup.py install

Or if you have Python setuptools, install it using:
        
    easy_install cython

For more information, <a href="http://docs.cython.org/src/quickstart/install.html">Check installation guide</a>

2. <a href="https://cymunk.readthedocs.org/en/latest/">cymunk</a>
<a href="https://github.com/tito/cymunk.git">Clone the github repository</a> or <a href="https://github.com/tito/cymunk/archive/master.zip">download</a> the zip.
Unpack the zip, enter the directory and run:

    python setup.py build_ext --inplace

After installing cython and cymunk, enter the directory and run:

    kivy main.py
