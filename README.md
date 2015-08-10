![alt Icon](https://dl.dropboxusercontent.com/u/28491877/cloud_1.png)
Kivame
====
Kivame is fun (quiz + game) app made for Kivy contest 2014.

# Requirements:
1. [cython](http://cython.org)

Download latest release from [cython.org](http://cython.org)
Unpack the tarball or zip file, enter the directory, and then run:
    
```python setup.py install```

Or if you have Python setuptools, install it using:
        
```easy_install cython```

For more information, [check installation guide](http://docs.cython.org/src/quickstart/install.html)

2. [Cymunk](https://cymunk.readthedocs.org/en/latest/)

Cymunk is a port of [Chipmunk](http://chipmunk-physics.net/), based on Cython.
[Clone the github repository](https://github.com/tito/cymunk.git) or [download](https://github.com/tito/cymunk/archive/master.zip) the zip.
Unpack the zip, enter the directory and run:

```python setup.py build_ext --inplace```

After installing cython and cymunk, enter the directory and run:
```kivy main.py```

App contains 9 stages:

1. 1st is quiz stage.General questions are asked in a funny way.Warning: lightning!!!! :)
![alt Stage 1](https://dl.dropboxusercontent.com/u/28491877/1.png)

2. 2nd requires cymunk.This stage checks your decision making skills.Touch the circles to increase their size but remember they should not touch others during inflation.Note hint for next stage is only given when you successfully passes the current stage.
![alt Stage 2](https://dl.dropboxusercontent.com/u/28491877/2.png)

#### The following stages are not included in android app due to some technical reasons.
3. Use direction keys or wasd to play the simple stage.
![alt Stage 3](https://dl.dropboxusercontent.com/u/28491877/3.png)

Similarly there are other stages where player's decision making skills are tested.And hints provide mathematical questions ,matrices, advices, etc.
4. Hint: Green = good, red = bad
![alt Stage 4](https://dl.dropboxusercontent.com/u/28491877/4.png)

5. Hint: Mix blue and green
![alt Stage 5](https://dl.dropboxusercontent.com/u/28491877/5.png)

6. Hint: Run forrest run
![alt Stage 6](https://dl.dropboxusercontent.com/u/28491877/6.png)

7. Hint: 143%22
![alt Stage 7](https://dl.dropboxusercontent.com/u/28491877/7.png)

8. Hint: Think twice before taking any step
![alt Stage 8](https://dl.dropboxusercontent.com/u/28491877/8.png)

9. Hint:
* X O X X X X X X X X X X X X
 
* X X X X X X X X X X X X X X

* X X X X X X X X X X X X X X
 
* X X X X X X X X X X X X X X

* X X X X X X X X X X X X X X

* X X X X X X X X X X X X X X

* X X X X X X X X X X X X X X

* X X X X X X X X X X X X X X

![alt Stage 9](https://dl.dropboxusercontent.com/u/28491877/9.png)
