Installation
============

::

    $ git clone https://github.com/ktosiek/pip2nix
    $ nix-env -f pip2nix/release.nix -iA pip2nix.python34  # Same Python as target packages

Basic usage
===========

Ad-hoc python-packages.nix generation
-------------------------------------

To generate python-packages.nix for a set of requirements::

    $ pip2nix generate -r requirements.txt

``pip2nix generate`` takes the same set of package specifications ``pip install`` does.
It understands ``-r``, git links, package specifications, and ``-e`` (which is just ignored).

Using pip2nix in a project
--------------------------

When packaging a project with pip2nix you'll want to make sure it's called the same way every time you bump dependencies.
To do that, you can create a ``pip2nix.ini`` file::

    [pip2nix]
    requirements = -r ./requirements.txt

This way you can just run ``pip2nix generate`` in the project's root.
More about the configuration file in :doc:`configuration`.
