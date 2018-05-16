Ginga-based viewer for NASA Planetary Data System v4 images.
------------------------------------------------------------

-Prototype code.  Contact us with questions, comments, ideas.

Some feature ideas may be found in the `project wiki <https://github.com/Small-Bodies-Node/pds4ivy/wiki>`_.

Requirements
------------
* numpy
* ginga with Qt backend
* pds4_tools

Limitations
-----------

Ivy assumes the image can be read into memory and displayed all at once.  Very large images, either by volume, size, or both, are untested.  Users looking for a basic viewer that is intended to work with any PDS4 data product should use `pds4_viewer <http://sbndev.astro.umd.edu/wiki/PDS4_Viewer>`_.

Ivy does not export the data.  Users looking for this functionality should read and export the data with their own software.  The Python-based `pds4_tools <http://sbndev.astro.umd.edu/wiki/Python_PDS4_Tools>`_ or the IDL-based `readpds <https://pdssbn.astro.umd.edu/tools/tools_readPDS.shtml>`_ maybe useful in this regard.

License
-------

This project is Copyright (c) Michael S. P. Kelley and licensed under
the terms of the BSD 3-Clause license. This package was based upon
the `Astropy package template <https://github.com/astropy/package-template>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.
