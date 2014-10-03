#! /usr/bin/python2
# -*- coding: utf-8; -*-
#
# (c) 2013 booya (http://booya.at)
#
# This file is part of the OpenGlider project.
#
# OpenGlider is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# OpenGlider is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenGlider.  If not, see <http://www.gnu.org/licenses/>.
import tempfile
import unittest
import sys
import os
from openglider.plots import flatten_glider

try:
    import openglider
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
    import openglider
from openglider.plots import flatten_glider, create_svg
from test_glider import GliderTestClass

testfolder = os.path.dirname(os.path.abspath(__file__))


class TestGlider(GliderTestClass):
    def file(self, suffix):
        file = tempfile.NamedTemporaryFile(suffix=suffix)
        return file

    def test_import_export_ods(self):
        path = self.file('.ods').name
        self.glider.export_geometry(path)
        #new_glider = glider.Glider()
        #self.assertTrue(new_glider.import_from_file(path))
        #self.assertEqual(new_glider, self.glider)

    def test_export_obj(self):
        path = self.file('.obj').name
        self.glider.export_3d(path, midribs=5)

    @unittest.skip('this hangs')
    def test_export_dxf(self):
        path = self.file('.dxf').name
        self.glider.export_3d(path, midribs=5)

    #@unittest.skip('')
    def test_export_apame(self):
        path = self.file('.inp').name
        self.glider.export_3d(path, midribs=1)

    #@unittest.skip('too slow')
    def test_export_json(self):
        path = self.file('.json').name
        self.glider.export_3d(path=path, midribs=2)  #numpoints=10)

    def test_export_plots(self):
        path = self.file('.svg').name
        create_svg(flatten_glider(self.glider), path)

    def test_export_glider_json(self):
        from openglider import jsonify
        path = self.file('.json')
        jsonify.dump(self.glider, path)
        path.seek(0)
        glider = jsonify.load(path)['data']
        self.assertEqualGlider(glider)



if __name__ == '__main__':
    unittest.main(verbosity=2)