# Licensed under a 3-clause BSD style license - see LICENSE.rst


class PDS4LabelHandler(object):
    """Ginga IO handler for PDS4 labels."""

    def __init__(self, logger):
        self.logger = logger
        self.factory_dict = {}

    def register_type(self, name, klass):
        self.factory_dict[name.lower()] = klass

    def load_file(self, filespec, numhdu=None, dstobj=None, **kwdargs):
        # create object of the appropriate type, usually
        # an AstroImage or AstroTable, by looking up the correct
        # class in self.factory_dict, under the keys 'image' or
        # 'table'
        import numpy as np
        from urllib.parse import urlparse
        from pds4_tools import pds4_read
        from .exceptions import InvalidPDS4Data

        urlinfo = urlparse(filespec)
        if urlinfo.scheme not in ['file', '']:
            raise IOError('File must be local: {}'.format(filespec))

        struct = pds4_read(urlinfo.path)

        if numhdu is None:
            # return the first table or array
            for i in range(len(struct)):
                if struct[i].is_array():
                    break
            else:
                raise InvalidPDS4Data('No image found in {}'.format(filespec))
        else:
            i = numhdu

        im = np.array(struct[i].data)

        # Ginga draws from bottom to top, left to right.  Transform
        # our data so that when it is drawn this way it is displayed
        # in the correct orientation
        disp_dir = struct[i].meta_data.display_settings['Display_Direction']
        haxis = struct[i].meta_data.get_axis_array(
            disp_dir['horizontal_display_axis']
        )

        # PDS4 data is Last Index Fastest and axis numbering starts at
        # 1.  Numpy arrays are also Last Index Fastest, but start at
        # 0.
        if haxis['sequence_number'] == 1:
            # Swap axes so that the horizontal axis is numpy axis 1:
            im = im.T

        hdisp_dir = disp_dir['horizontal_display_direction']
        vdisp_dir = disp_dir['vertical_display_direction']
        if 'Right to Left' in hdisp_dir:
            im = im[:, ::-1]  # invert horizontal axis
        if 'Top to Bottom' in vdisp_dir:
            im = im[::-1]     # invert vertical axis

        if dstobj is not None:
            dstobj.set_data(im)

        return im, i, None
