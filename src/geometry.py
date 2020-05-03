'''
    5____________6
    /           /|
   /           / |
 1/__________2/  |
 |           |   |
 |           |   |
 |           |   7
 |           |  /
 |           | /
 0___________3/
'''

class Geometry:
    def __init__(self):
        self.init_geometry()

    def init_geometry(self):
        self.axis_verts = (
            (-5.5, 0.0, 0.0),
            (5.5, 0.0, 0.0),
            (0.0, -5.5, 0.0),
            (0.0, 5.5, 0.0),
            (0.0, 0.0, -5.5),
            (0.0, 0.0, 5.5)
        )

        self.axes = (
            (0, 1),
            (2, 3),
            (4, 5)
        )

        self.axis_colors = (
            (1.0, 0.0, 0.0),  # Red
            (0.0, 1.0, 0.0),  # Green
            (0.0, 0.0, 1.0)  # Blue
        )

        self.center_pieces = [
            # Front 0
            [[-1, -1, 3],
             [-1, 1, 3],
             [1, 1, 3],
             [1, -1, 3],
             [-1, -1, 1],
             [-1, 1, 1],
             [1, 1, 1],
             [1, -1, 1]],

            # Left 1
            [[-3, -1, 1],
             [-3, 1, 1],
             [-1, 1, 1],
             [-1, -1, 1],
             [-3, -1, -1],
             [-3, 1, -1],
             [-1, 1, -1],
             [-1, -1, -1]],

            # Back 2
            [[-1, -1, -1],
             [-1, 1, -1],
             [1, 1, -1],
             [1, -1, -1],
             [-1, -1, -3],
             [-1, 1, -3],
             [1, 1, -3],
             [1, -1, -3],
             ],

            # Right 3
            [[1, -1, 1],
             [1, 1, 1],
             [3, 1, 1],
             [3, -1, 1],
             [1, -1, -1],
             [1, 1, -1],
             [3, 1, -1],
             [3, -1, -1],
             ],

            # Up 4
            [[-1, 1, 1],
             [-1, 3, 1],
             [1, 3, 1],
             [1, 1, 1],
             [-1, 1, -1],
             [-1, 3, -1],
             [1, 3, -1],
             [1, 1, -1]],

            # Down 5
            [[-1, -3, 1],
             [-1, -1, 1],
             [1, -1, 1],
             [1, -3, 1],
             [-1, -3, -1],
             [-1, -1, -1],
             [1, -1, -1],
             [1, -3, -1]]
        ]

        self.edge_pieces = [
            # X
            # 0
            [[[-1, -3, 3],
              [-1, -1, 3],
              [1, -1, 3],
              [1, -3, 3],
              [-1, -3, 1],
              [-1, -1, 1],
              [1, -1, 1],
              [1, -3, 1]],

             # 1
             [[-1, 1, 3],
              [-1, 3, 3],
              [1, 3, 3],
              [1, 1, 3],
              [-1, 1, 1],
              [-1, 3, 1],
              [1, 3, 1],
              [1, 1, 1]],

             # 2
             [[-1, 1, -1],
              [-1, 3, -1],
              [1, 3, -1],
              [1, 1, -1],
              [-1, 1, -3],
              [-1, 3, -3],
              [1, 3, -3],
              [1, 1, -3]],

             # 3
             [[-1, -3, -1],
              [-1, -1, -1],
              [1, -1, -1],
              [1, -3, -1],
              [-1, -3, -3],
              [-1, -1, -3],
              [1, -1, -3],
              [1, -3, -3]]],

            # Y
            # 0
            [[[-3, -1, 3],
              [-3, 1, 3],
              [-1, 1, 3],
              [-1, -1, 3],
              [-3, -1, 1],
              [-3, 1, 1],
              [-1, 1, 1],
              [-1, -1, 1]],

             # 1
             [[-3, -1, -1],
              [-3, 1, -1],
              [-1, 1, -1],
              [-1, -1, -1],
              [-3, -1, -3],
              [-3, 1, -3],
              [-1, 1, -3],
              [-1, -1, -3]],

             # 2
             [[1, -1, -1],
              [1, 1, -1],
              [3, 1, -1],
              [3, -1, -1],
              [1, -1, -3],
              [1, 1, -3],
              [3, 1, -3],
              [3, -1, -3]],

             # 3
             [[1, -1, 3],
              [1, 1, 3],
              [3, 1, 3],
              [3, -1, 3],
              [1, -1, 1],
              [1, 1, 1],
              [3, 1, 1],
              [3, -1, 1]]],

            # Z
            # 0
            [[[-3, -3, 1],
              [-3, -1, 1],
              [-1, -1, 1],
              [-1, -3, 1],
              [-3, -3, -1],
              [-3, -1, -1],
              [-1, -1, -1],
              [-1, -3, -1]],

             # 1
             [[-3, 1, 1],
              [-3, 3, 1],
              [-1, 3, 1],
              [-1, 1, 1],
              [-3, 1, -1],
              [-3, 3, -1],
              [-1, 3, -1],
              [-1, 1, -1]],

             # 2
             [[1, 1, 1],
              [1, 3, 1],
              [3, 3, 1],
              [3, 1, 1],
              [1, 1, -1],
              [1, 3, -1],
              [3, 3, -1],
              [3, 1, -1]],

             # 3
             [[1, -3, 1],
              [1, -1, 1],
              [3, -1, 1],
              [3, -3, 1],
              [1, -3, -1],
              [1, -1, -1],
              [3, -1, -1],
              [3, -3, -1]]],
        ]

        self.corner_pieces = [
            # Front
            # 0
            [[-3, -3, 3],
             [-3, -1, 3],
             [-1, -1, 3],
             [-1, -3, 3],
             [-3, -3, 1],
             [-3, -1, 1],
             [-1, -1, 1],
             [-1, -3, 1]],
            # 1
            [[-3, 1, 3],
             [-3, 3, 3],
             [-1, 3, 3],
             [-1, 1, 3],
             [-3, 1, 1],
             [-3, 3, 1],
             [-1, 3, 1],
             [-1, 1, 1]],
            # 2
            [[1, 1, 3],
             [1, 3, 3],
             [3, 3, 3],
             [3, 1, 3],
             [1, 1, 1],
             [1, 3, 1],
             [3, 3, 1],
             [3, 1, 1]],
            # 3
            [[1, -3, 3],
             [1, -1, 3],
             [3, -1, 3],
             [3, -3, 3],
             [1, -3, 1],
             [1, -1, 1],
             [3, -1, 1],
             [3, -3, 1]],

            # Back
            # 0
            [[-3, -3, -1],
             [-3, -1, -1],
             [-1, -1, -1],
             [-1, -3, -1],
             [-3, -3, -3],
             [-3, -1, -3],
             [-1, -1, -3],
             [-1, -3, -3]],
            # 1
            [[-3, 1, -1],
             [-3, 3, -1],
             [-1, 3, -1],
             [-1, 1, -1],
             [-3, 1, -3],
             [-3, 3, -3],
             [-1, 3, -3],
             [-1, 1, -3]],
            # 2
            [[1, 1, -1],
             [1, 3, -1],
             [3, 3, -1],
             [3, 1, -1],
             [1, 1, -3],
             [1, 3, -3],
             [3, 3, -3],
             [3, 1, -3]],
            # 3
            [[1, -3, -1],
             [1, -1, -1],
             [3, -1, -1],
             [3, -3, -1],
             [1, -3, -3],
             [1, -1, -3],
             [3, -1, -3],
             [3, -3, -3]],
        ]

        # [axis, index]
        self.front_edges = [
            [0, 0],  # x
            [0, 1],
            [1, 0],  # y
            [1, 3]
        ]

        self.left_edges = [
            [1, 0],  # y
            [1, 1],
            [2, 0],  # z
            [2, 1]
        ]

        self.back_edges = [
            [0, 2],  # x
            [0, 3],
            [1, 1],  # y
            [1, 2]
        ]

        self.right_edges = [
            [1, 2],  # y
            [1, 3],
            [2, 2],  # z
            [2, 3]
        ]

        self.up_edges = [
            [0, 1],  # x
            [0, 2],
            [2, 1],  # z
            [2, 2]
        ]

        self.down_edges = [
            [0, 0],  # x
            [0, 3],
            [2, 0],  # z
            [2, 3]
        ]

        self.edges = [
            self.front_edges,
            self.left_edges,
            self.back_edges,
            self.right_edges,
            self.up_edges,
            self.down_edges
        ]


        '''
               5____________6
               /           /|
              /           / |
            1/__________2/  |
            |           |   |
            |           |   |
            |           |   7
            |           |  /
            |           | /
            0___________3/
        '''
        # left-right right is positive
        # up-down up is positive
        # front-back front is positive
        self.cube_verts = (
            (-3.0, -3.0, 3.0),  # 0
            (-3.0, 3.0, 3.0),  # 1
            (3.0, 3.0, 3.0),  # 2
            (3.0, -3.0, 3.0),  # 3
            (-3.0, -3.0, -3.0),  # 4
            (-3.0, 3.0, -3.0),  # 5
            (3.0, 3.0, -3.0),  # 6
            (3.0, -3.0, -3.0)  # 7
        )

        self.cube_edges = (
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 6),
            (5, 1),
            (5, 4),
            (5, 6),
            (7, 3),
            (7, 4),
            (7, 6)
        )

        '''
            5____________6
            /           /|
           /           / |
         1/__________2/  |
         |           |   |
         |           |   |
         |           |   7
         |           |  /
         |           | /
         0___________3/
        '''

        self.cube_surfaces = (
            [0, 1, 2, 3],  # Front 0
            [4, 5, 1, 0],  # Left 1
            [7, 6, 5, 4],  # Back 2
            [3, 2, 6, 7],  # Right 3
            [1, 5, 6, 2],  # Up 4
            [4, 0, 3, 7]   # Down 5
        )

        self.pulse_color = [0.0, 0.0, 0.0]
        self.pulse_val = 0.04

        # Black inner sides of edge pieces
        self.edge_black_pat = [
            [0, 1, 2, 3, 4, 5],
            [0, 1, 2, 3, 4, 5],
            [0, 1, 2, 3, 4, 5]
            # [4, 5],
            # [0, 2]
        ]

        self.corner_color_pat = [
            [0, 1, 5],  # 0
            [0, 1, 4],  # 1
            [0, 3, 4],  # 2
            [0, 3, 5],  # 3
            [2, 1, 5],  # 4
            [2, 1, 4],  # 5
            [2, 3, 4],  # 6
            [2, 3, 5],  # 7
        ]

        self.corner_black_pat = [
            [2, 3, 4],  # 0
            [2, 3, 5],  # 1
            [2, 1, 5],  # 2
            [2, 1, 4],  # 3
            [0, 3, 4],  # 4
            [0, 3, 5],  # 5
            [0, 1, 5],  # 6
            [0, 1, 4],  # 7
        ]

        self.tex_coords = [
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1)
        ]

    # :TODO: This method needs to be fixed since, as it has been implemented originally,
    # it only does work as expected before any face has been rotated.
    def add_padding(self, value):
        for vertex in self.center_pieces[0]:
            vertex[2] += value
        for vertex in self.center_pieces[1]:
            vertex[0] -= value
        for vertex in self.center_pieces[2]:
            vertex[2] -= value
        for vertex in self.center_pieces[3]:
            vertex[0] += value
        for vertex in self.center_pieces[4]:
            vertex[1] += value
        for vertex in self.center_pieces[5]:
            vertex[1] -= value

        for vertex in self.edge_pieces[0][0]:
            vertex[1] -= value
            vertex[2] += value
        for vertex in self.edge_pieces[0][1]:
            vertex[1] += value
            vertex[2] += value
        for vertex in self.edge_pieces[0][2]:
            vertex[1] += value
            vertex[2] -= value
        for vertex in self.edge_pieces[0][3]:
            vertex[1] -= value
            vertex[2] -= value

        for vertex in self.edge_pieces[1][0]:
            vertex[0] -= value
            vertex[2] += value
        for vertex in self.edge_pieces[1][1]:
            vertex[0] -= value
            vertex[2] -= value
        for vertex in self.edge_pieces[1][2]:
            vertex[0] += value
            vertex[2] -= value
        for vertex in self.edge_pieces[1][3]:
            vertex[0] += value
            vertex[2] += value

        for vertex in self.edge_pieces[2][0]:
            vertex[0] -= value
            vertex[1] -= value
        for vertex in self.edge_pieces[2][1]:
            vertex[0] -= value
            vertex[1] += value
        for vertex in self.edge_pieces[2][2]:
            vertex[0] += value
            vertex[1] += value
        for vertex in self.edge_pieces[2][3]:
            vertex[0] += value
            vertex[1] -= value

        for vertex in self.corner_pieces[0]:
            vertex[0] -= value
            vertex[1] -= value
            vertex[2] += value
        for vertex in self.corner_pieces[1]:
            vertex[0] -= value
            vertex[1] += value
            vertex[2] += value
        for vertex in self.corner_pieces[2]:
            vertex[0] += value
            vertex[1] += value
            vertex[2] += value
        for vertex in self.corner_pieces[3]:
            vertex[0] += value
            vertex[1] -= value
            vertex[2] += value
        for vertex in self.corner_pieces[4]:
            vertex[0] -= value
            vertex[1] -= value
            vertex[2] -= value
        for vertex in self.corner_pieces[5]:
            vertex[0] -= value
            vertex[1] += value
            vertex[2] -= value
        for vertex in self.corner_pieces[6]:
            vertex[0] += value
            vertex[1] += value
            vertex[2] -= value
        for vertex in self.corner_pieces[7]:
            vertex[0] += value
            vertex[1] -= value
            vertex[2] -= value
