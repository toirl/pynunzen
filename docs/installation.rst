.. highlight:: shell

============
Installation
============


Stable release
--------------

To install Pynunzen, run this command in your terminal:

.. code-block:: console

    $ pip install pynunzen

This is the preferred method to install Pynunzen, as it will always install the most recent stable release. 

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for Pynunzen can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/toirl/pynunzen

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/toirl/pynunzen/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/toirl/pynunzen
.. _tarball: https://github.com/toirl/pynunzen/tarball/master

Configuration
-------------

Settings of Pynunzen are stored in a configuration file. The default
location of the file is `$HOME/.pynunzen.ini`. 

If the file is not existing it will be generated on the first start of
the Pynunzen node with the following default values:

.. include:: example_config.ini
   :literal:
