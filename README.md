# DataSpider_Dubov
###Preparing for using
#Grab Installaion
Installation on Linux
Run the command:

```
pip install -U Grab
```

This command will install Grab and all dependencies. Be aware that you need to have some libraries installed in your system to successfully build lxml and pycurl dependencies.

To build pycurl successfully you need to install:

```
apt-get install libcurl4-openssl-dev
```

To build lxml successfully you need to install:

```
apt-get install libxml2-dev libxslt-dev
```

###Installation on Windows
* Install lxml. You can get lxml here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
* Install pycurl. You can get pycurl here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
* Install Grab

Download the Grab package from https://pypi.python.org/pypi/grab, unpack it and run:

```
python setup.py install
```

If you use Python 2.x, then you might get an error while using python setup.py install. There is a bug in python 2.7.6. Delete it, download python 2.7.5 and try to install Grab again.

You can also install Grab via pip. If you don’t have pip installed, install pip first. Download the file get-pip.py from https://bootstrap.pypa.io/get-pip.py and then run this command:

```
python get-pip.py
```

Now you can install Grab via pip with this command:

```
python -m pip install grab
```
