# Scripting environment for testing molecular dynamics engine from Concord Consortium 'lab' repository

## To get started:

Unfortunately there are some manual steps in the installation process. 

First (assuming you are using OS X and Homebrew) install ZeroMQ and gfortran:

    $ brew install zeromq
    $ brew install gfortran

Create an isolated virtualenv called 'lab-md-analysis' and activate it:

    $ python vendor/virtualenv.py lab-md-analysis
    $ source lab-md-analysis/bin/activate
    
It is necessary to install readline by hand using easy_install instead of pip, and matplotlib must be installed *after* `pip install -r requirements.txt`

    (lab-md-analysis)$ easy_install readline
    (lab-md-analysis)$ pip install -r requirements.txt
    (lab-md-analysis)$ pip install matplotlib

(You may also find that it's necessary to remove scipy from requirements.txt and install it via
`pip install scipy` at the end.)

Once the smoke test passes, install the lab repo:

    $ npm install

    (optionally)

    $ npm link <path to local installation of lab repo>

## Matplotlib smoke test:

    (lab-md-analysis)$ ipython --pylab
    ...
    In [1]: x = randn(100000)

    In [2]: hist(x, 100)

You should see a histogram approximating a normal distribution.

## Example script:

Some data from the constrained random walk of the center of mass of the Lab molecular dynamics simulation is in data/. Once you have done the install steps above, to plot this data, run `./plot-cm-random-walk.py` in the root of this repository to generate the figure; open `figure/cm-random-walk.png` to view the figure.

You *may* find that you need Python 2.7 installed.
