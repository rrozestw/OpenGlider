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
import os
import random
import sys
import unittest
from openglider.plots.glider.cell import flattened_cell

try:
    import openglider
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
    import openglider
import openglider.graphics
import openglider.plots
from test_glider import GliderTestClass

testfolder = os.path.dirname(os.path.abspath(__file__))
importpath = testfolder+"/demokite.ods"


class TestGlider_Flatten(GliderTestClass):
    def setUp(self, complete=False):
        super(TestGlider_Flatten, self).setUp(complete=complete)

    def get_flattened_cell(self, allowance=0.02):
        cell = self.glider.cells[random.randint(0, len(self.glider.cells)-1)]
        left_bal, left, right, right_bal = flattened_cell(cell)
        left_out = left.copy()
        right_out = right.copy()
        left_out.add_stuff(-allowance)
        right_out.add_stuff(allowance)
        return left_out, left, right, right_out

    def showcut(self, num):
        """"""
        left_out, left, right, right_out = self.get_flattened_cell()
        cuts_front = [random.random()*len(left)*0.1 for __ in range(2)]
        cuts_back = [(random.random()+1)*len(left)*0.2 for __ in range(2)]
        outlist_1, leftcut, rightcut = openglider.plots.cuts[num]([[left, cuts_front[0]], [right, cuts_front[1]]],
                                                                  left_out, right_out, -0.02)
        outlist_2, leftcut_2, rightcut_2 = openglider.plots.cuts[num]([[left, cuts_back[0]], [right, cuts_back[1]]],
                                                                      left_out, right_out, 0.02)
        cuts = [left_out[leftcut:leftcut_2], outlist_1, right_out[rightcut:rightcut_2], outlist_2]
        marks = [left[cuts_front[0]:cuts_back[0]], right[cuts_front[1]:cuts_back[1]]]
        openglider.graphics.Graphics2D([openglider.graphics.Line(thalist) for thalist in cuts] +
                                       [openglider.graphics.Point(thalist) for thalist in marks])

    def test_cut1(self):
        self.showcut(0)

    def test_cut2(self):
        self.showcut(1)

    def test_cut3(self):
        self.showcut(2)

    def test_mirror(self):
        left_out, left, right, right_out = self.get_flattened_cell()
        mirrored_left = left_out.copy()
        mirrored_right = right_out.copy()
        p1 = mirrored_left.data[-1].copy()
        p2 = mirrored_right.data[-1].copy()
        #print(mirrored_left.data[-1])
        mirrored_left.mirror(p1, p2)
        mirrored_right.mirror(p1, p2)
        openglider.graphics.Graphics2D([openglider.graphics.Line(left_out.data),
                                        openglider.graphics.Line(right_out.data),
                                        openglider.graphics.Green,
                                        openglider.graphics.Line(mirrored_left.data),
                                        openglider.graphics.Line(mirrored_right.data)
                                        ])

    def test_flattened_glider(self):
        parts = openglider.plots.flatten_glider(self.glider)
        all = parts['panels']
        all.join(parts['ribs'])
        layers = {}
        for part in all.parts:
            for name, layer in part.layers.iteritems():
                layers.setdefault(name, [])
                layers[name] += layer

        openglider.graphics.Graphics3D([openglider.graphics.Line(l) for l in layers['OUTER_CUTS']] +
                                       [openglider.graphics.Red] +
                                       [openglider.graphics.Line(l) for l in layers['SEWING_MARKS']])

if __name__ == '__main__':
    unittest.main(verbosity=2)