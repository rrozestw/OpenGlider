import numpy as np
from pivy import coin
from pivy import graphics

from openglider.vector.polyline import PolyLine2D
from openglider.airfoil import Profile2D


import unittest
class TestLines(unittest.TestCase):
    def testOffset(self):
        viewer = graphics.GraphicsViewer()
        prof = Profile2D.compute_trefftz()
        viewer += graphics.Line(prof)
        for _ in range(3):
            prof.add_stuff(0.01)
            viewer += graphics.Line(prof)
        p = PolyLine2D([[1, 0], [0, 1]])
        p += PolyLine2D([[0, 1], [1, 1], [0, 0]])
        viewer += graphics.Line(p)
        p.add_stuff(0.1)
        viewer += graphics.Line(p)

        viewer.show()

if __name__ == "__main__":
    unittest.main()