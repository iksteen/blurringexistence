Title: wxPython using virtualenvwrapper on OSX
Date: 2015-06-12 22:58
Tags: python, wxpython, osx
Slug: wxpython-using-virtualenvwrapper-on-osx

For a new project, I needed wxPython. Now, wxPython is notoriuous for being a pain to install inside a virtual environment on OSX. And if you do get wxPython installed in a virtual environment, you'll notice the following error message when creating a `wx.App` instance:

	This program needs access to the screen.
	Please run with a Framework build of python, and only when you are
	logged in on the main display of your Mac.

This reason this happens is that the wrapper that virtualenv creates around the python executable that somehow loses its connection to the display. The best quote describing the problem I found is from a [reply](http://stackoverflow.com/a/15754033) on StackOverflow:

>With the way that the virtualenv is constructed the Python that is there sort of loses its connection with the framework that it comes from, and so using it directly triggers that security mechanism and the wx code is not able to get full access to the screen.

The workaround to this problem is replacing the virtualenv python wrapper with the original python executable and setting the `PYTHONHOME` environment variable to the path of your virtual environment.

I use a python version installed using the *homebrew* package manager and I use *virtualenvwrapper* to manage my virtual environments. Here is the cleanest solution I've come up with so far:

```
:::sh
# Install wxpython globally
$ brew install wxpython

# Create a new virtual environment for your project
$ mkvirtualenv mywxapp

# Replace the python wrapper installed by virtualenv with the original executable
(mywxapp) $ cd $VIRTUAL_ENV/bin
(mywxapp) $ mv python python_orig
(mywxapp) $ ln -s /usr/local/bin/python python

# Set/unset PYTHONHOME when (de)activating the virtual environment
(mywxapp) $ echo "export PYTHONHOME=\"\$VIRTUAL_ENV\"" >> postactivate
(mywxapp) $ echo "unset PYTHONHOME" >> predeactivate

# Symlink wxPython into the virtual environment
(mywxapp) $ ln -s /usr/local/lib/python2.7/site-packages/wx* $VIRTUAL_ENV/lib/python2.7/site-packages

# Symlink virtualenvwrapper & dependencies into the virtual environment
(mywxapp) $ ln -s /usr/local/lib/python2.7/site-packages/virtualenvwrapper* $VIRTUAL_ENV/lib/python2.7/site-packages
(mywxapp) $ ln -s /usr/local/lib/python2.7/site-packages/stevedore* $VIRTUAL_ENV/lib/python2.7/site-packages

# Re-activate the virtual environment
(mywxapp) $ deactivate
$ workon mywxapp

# Check if it actually works
(mywxapp) $ python
Python 2.7.9 (default, Dec 18 2014, 15:18:21) 
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.56)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import wx
>>> wx.App()
<wx._core.App; proxy of <Swig Object of type 'wxPyApp *' at 0x7ffaa35b2700> >
```
