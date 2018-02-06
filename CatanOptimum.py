import random
from collections import namedtuple
import tkinter as tk
from tkinter import ttk
import itertools

# TODO: Pair-wise comparisons
# TODO: 2nd settlement selector

class Board:
    """
    Object representing a Settlers of Catan Board.
    """

    @classmethod
    def random_board(cls, seed="PyTN2018"):
        """
        Return a random Board object.

        :param seed: Seed of the randomizer.
        :return:
        """
        random.seed(a=seed)

        res = (['lumber'] * 4) + \
              (['grain'] * 4) + \
              (['brick'] * 3) + \
              (['ore'] * 3) + \
              (['wool'] * 4)

        random.shuffle(res)

        nums = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]

        random.shuffle(nums)

        description = list(zip(res, nums))
        description.append((None, None))

        random.shuffle(description)

        return Board(description)

    def __init__(self, tiles):
        """
        Initialize the board based on the description. The description is a
        list of tuples, detailing the board. Tuples are (resource, number)
        ordered 0 to 18. Starting in the top left-most tile as 0, then going
        down each row sequentially.

             00 01 02
           03 04 05 06
         07 08 09 10 11
           12 13 14 15
             16 17 18

        :param tiles: a list of tuples as (resource, number) of tiles.
        """
        self.tiles = [Tile() for _ in range(19)]

        for i, (resource, number) in enumerate(tiles):
            self.tiles[i].resource = resource
            self.tiles[i].number = number

        self.nodes = [Node(i) for i in range(54)]
        self.ports = [Port(i) for i in range(9)]

        self._setup_nodes()
        self._setup_ports()

    def _setup_nodes(self):
        """
        Setup the nodes of the board.
        Nodes are laid out starting in the top left-most at 0 and  then
        increasing sequentially to the right and down.

               00  01  02
              / \ / \ / \
             03  04  05  06
             |   |   |   |
             07  08  09  10
            / \ / \ / \ / \
           11  12  13  14  15
           |   |   |   |   |
           16  17  18  19  20
          / \ / \ / \ / \ / \
        21  22  23  24  25  26
        |   |   |   |   |   |
        27  28  29  30  31  32
         \ / \ / \ / \ / \ /
         33  34  35  36  37
         |   |   |   |   |
         38  39  40  41  42
          \ / \ / \ / \ /
          43  44  45  46
          |   |   |   |
         47  48  49  50
          \ / \ / \ /
          51  52  53
        :return:
        """

        # Hard Coded connections based on indices.
        # ([Tiles], [Neighbors])
        Connection = namedtuple('Connection', ['tiles', 'neighbors'])
        connections = {
            0: Connection([0], [3, 4]),
            1: Connection([1], [4, 5]),
            2: Connection([2], [5, 6]),
            3: Connection([0], [0, 7]),
            4: Connection([0, 1], [0, 1, 8]),
            5: Connection([1, 2], [1, 2, 9]),
            6: Connection([2], [2, 10]),
            7: Connection([0, 3], [3, 11, 12]),
            8: Connection([0, 1, 4], [4, 12, 13]),
            9: Connection([1, 2, 5], [5, 13, 14]),
            10: Connection([2, 6], [6, 14, 15]),
            11: Connection([3], [7, 16]),
            12: Connection([0, 3, 4], [7, 8, 17]),
            13: Connection([1, 4, 5], [8, 9, 18]),
            14: Connection([2, 5, 6], [9, 10, 19]),
            15: Connection([6], [10, 20]),
            16: Connection([3, 7], [11, 21, 22]),
            17: Connection([3, 4, 8], [12, 22, 23]),
            18: Connection([4, 5, 9], [13, 23, 24]),
            19: Connection([5, 6, 10], [14, 24, 25]),
            20: Connection([6, 11], [15, 25, 26]),
            21: Connection([7], [16, 27]),
            22: Connection([3, 7, 8], [16, 17, 28]),
            23: Connection([4, 8, 9], [17, 18, 29]),
            24: Connection([5, 9, 10], [18, 19, 30]),
            25: Connection([6, 10, 11], [19, 20, 31]),
            26: Connection([11], [20, 32]),
            27: Connection([7], [21, 33]),
            28: Connection([7, 8, 12], [22, 33, 34]),
            29: Connection([8, 9, 13], [23, 34, 35]),
            30: Connection([9, 10, 14], [24, 35, 36]),
            31: Connection([10, 11, 15], [25, 36, 37]),
            32: Connection([11], [26, 37]),
            33: Connection([7, 12], [27, 28, 38]),
            34: Connection([8, 12, 13], [28, 29, 39]),
            35: Connection([9, 13, 14], [29, 30, 40]),
            36: Connection([10, 14, 15], [30, 31, 41]),
            37: Connection([11, 15], [31, 32, 42]),
            38: Connection([12], [33, 43]),
            39: Connection([12, 13, 16], [34, 43, 44]),
            40: Connection([13, 14, 17], [35, 44, 45]),
            41: Connection([14, 15, 18], [36, 45, 46]),
            42: Connection([15], [37, 46]),
            43: Connection([12, 16], [38, 39, 47]),
            44: Connection([13, 16, 17], [39, 40, 48]),
            45: Connection([14, 17, 18], [40, 41, 49]),
            46: Connection([15, 18], [41, 42, 50]),
            47: Connection([16], [43, 51]),
            48: Connection([16, 17], [44, 51, 52]),
            49: Connection([17, 18], [45, 52, 53]),
            50: Connection([18], [46, 53]),
            51: Connection([16], [47, 48]),
            52: Connection([17], [48, 49]),
            53: Connection([18], [49, 50])
        }

        # Setup nodes w/ tiles.
        for i in range(54):
            self.nodes[i].tiles = [self.tiles[j]
                                   for j
                                   in connections[i].tiles]

        # Connect nodes to each other
        for i in range(54):
            self.nodes[i].neighbors = [self.nodes[j]
                                       for j
                                       in connections[i].neighbors]

    def _setup_ports(self, ports=None):
        """
        Setup the ports of the board.
        Indices of ports start in the top left and go clockwise.

        :param ports: list of nested tuples describing ports.
        :return:
        """
        for node in self.nodes:
            node.ports.clear()

        if not ports:
            ports = [
                ('all', (0, 3)),
                ('grain', (1, 5)),
                ('ore', (10, 15)),
                ('all', (26, 32)),
                ('wool', (42, 46)),
                ('all', (49, 52)),
                ('all', (47, 51)),
                ('brick', (33, 38)),
                ('lumber', (11, 16))
            ]

        for i, (resource, nodes) in enumerate(ports):
            self.ports[i].resource = resource
            self.ports[i].nodes = nodes

            for node in nodes:
                self.nodes[node].ports.append(self.ports[i])

    def get_pairwise_dot_sum(self):
        dot_pairs = []
        for a, b in itertools.combinations(self.nodes, 2):
            if a in b.neighbors or b in a.neighbors:
                continue
            dot_pairs.append(((a.index, b.index), a.get_dot_sum() + b.get_dot_sum()))

        return dot_pairs

    def get_pairwise_hit_frequency(self):
        freq_pairs = []
        for a, b in itertools.combinations(self.nodes, 2):
            if a in b.neighbors or b in a.neighbors:
                continue
            nums_a = set(tile.number for tile in a.tiles)
            nums_b = set(tile.number for tile in b.tiles)

            nums = nums_a | nums_b

            freq_pairs.append((
                (a.index, b.index),
                sum((Tile.number_to_dots(num) / 36) for num in nums)))

        return freq_pairs

    def get_pairwise_flow_rate_no_trades(self):
        flow_pairs = []
        for a, b in itertools.combinations(self.nodes, 2):
            if a in b.neighbors or b in a.neighbors:
                continue
            flow_pairs.append((
            (a.index, b.index),
            (a.get_flow_rate_no_trades() + b.get_flow_rate_no_trades())))

        return flow_pairs

    def get_pairwise_flow_rate(self):
        flow_pairs = []

        for a, b in itertools.combinations(self.nodes, 2):
            if a in b.neighbors or b in a.neighbors:
                continue
            a_flow = a.get_flow_rate()
            b_flow = b.get_flow_rate()

            flow = {
                resource: a_flow.get(resource, 0) + b_flow.get(resource, 0)
                for resource
                in set(a_flow) | set(b_flow)
            }

            flow_pairs.append(((a.index, b.index), flow))

        return flow_pairs

    def get_pairwise_fill_rate(self, needs):
        fill_pairs = []

        for pair, flow in self.get_pairwise_flow_rate():
            num_turns = {
                resource: needs.get(resource, 0) / (
                    flow.get(resource, 0)
                    if flow.get(resource, 0) != 0
                    else 1 / 1000000000
                )
                for resource
                in set(needs) | set(flow)
            }

            fill_pairs.append((pair, max(num_turns.values())))

        return fill_pairs


class Tile:
    """
    Object representing an intersection of roads on a Settlers of Catan board.
    """

    resources = ['brick', 'lumber', 'ore', 'grain', 'wool']

    @classmethod
    def number_to_dots(cls, number):
        """
        Return the dots printed on the numbered tile.

        :param number: number of the tile
        :return: integer of the number of dots
        """
        if not number:
            return 0

        if 0 < number < 7:
            return number - 1
        elif 7 < number < 13:
            return 13 - number

    def get_dots(self):
        """
        Return the number of dots for this tile.

        :return:
        """
        return Tile.number_to_dots(self.number)

    def get_odds(self):
        """
        Return the odds of this tile's number being rolled on 2d6.

        :return: odds out of 1 of the number being rolled
        """
        return Tile.number_to_dots(self.number) / 36

    def __init__(self, resource=None, number=None):
        """
        Initialize the Node with a given terrain and number.

        :param terrain: terrain for the node
        :param number: number for the node
        """
        self.resource = resource
        self.number = number


class Port:
    """
    Object representing a port in Settlers of Catan.
    """

    def __init__(self, index, resource=None):
        """
        Initialize the Port object.

        :param resource: Resource the port takes in trade.
        """
        self.index = index
        self.resource = resource
        self.nodes = []


class Node:
    """
    An object representing an intersection of roads on a Settlers of Catan
    board.
    """

    def __init__(self, index, status='active'):
        """
        Initialize the Node object.

        :param index: index of the node on the Catan board.
        :param status: Status of the node.
        """
        self.index = index
        self.status = status
        self.tiles = []
        self.ports = []
        self.neighbors = []

    def claim(self):
        """
        If available, claim the node and set the neighbor tiles to "dead".
        :return: boolean if claim is successful.
        """

        if self.status == 'active':
            self.status = 'claimed'
            for neighbor in self.neighbors:
                neighbor.status = 'dead'
            return True

        return False

    def get_dot_sum(self):
        """
        Return the sum of the dots for the node.
        :return:
        """
        return sum(tile.get_dots() for tile in self.tiles)

    def get_hit_frequency(self):
        """
        Return the hit frequency for the node.
        :return:
        """
        nums = set(tile.number for tile in self.tiles)

        return sum((Tile.number_to_dots(num) / 36) for num in nums)

    def get_flow_rate_no_trades(self):
        """
        Return the flow rate for just the resource generated.
        :return:
        """
        return sum((Tile.number_to_dots(tile.number) / 36)
                   for tile
                   in self.tiles)

    def get_flow_rate(self):
        """
        Return the per resource flow rate.
        Flow rate described as Amount per Turn * Tile Odds.
        :return:
        """
        flow = {resource: 0 for resource in Tile.resources}
        for tile in self.tiles:
            trade_rate = 1 / 4
            if self.ports:
                port_resources = [port.resource for port in self.ports]
                if tile.resource in port_resources:
                    trade_rate = 1 / 2
                elif 'all' in port_resources:
                    trade_rate = 1 / 3

            hit_odds = tile.get_odds()

            tile_flow = {
                resource: trade_rate * hit_odds
                for resource
                in Tile.resources
                if resource != tile.resource
            }

            if tile.resource:
                tile_flow[tile.resource] = hit_odds

            flow = {
                resource: tile_flow.get(resource, 0) + flow.get(resource, 0)
                for resource
                in set(tile_flow) | set(flow)
            }

        return flow

    def get_fill_rate(self, needs):
        """
        Return the number of turns the node will take to fill needs.

        :param needs: dictionary of resources and associated need values
        :return:
        """
        flow = self.get_flow_rate()

        num_turns = {
            resource: needs.get(resource, 0) / (
                flow.get(resource, 0)
                if flow.get(resource, 0) != 0
                else 1 / 1000000000
            )
            for resource
            in set(needs) | set(flow)
        }

        return max(num_turns.values())


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        # Setup variables for resource needs.
        self.needs = {
            'lumber': tk.IntVar(),
            'brick': tk.IntVar(),
            'grain': tk.IntVar(),
            'ore': tk.IntVar(),
            'wool': tk.IntVar()
        }

        for need in self.needs:
            self.needs[need].set(10)

        # Setup the menu
        self.menu = tk.Menu(self)
        filemenu = tk.Menu(self.menu, tearoff=0)
        filemenu.add_command(label='Edit Board', command=self.setup_board)
        filemenu.add_command(label='Set Resource Needs', command=self.set_needs)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=root.quit)
        self.menu.add_cascade(label='Setup', menu=filemenu)

        # Get Board object to manipulate
        self.board = Board.random_board()

        # Setup sizes for canvas.
        self.canvas_size = 400
        self.canvas_pad = 50

        # Setup Left & Right frames.
        self.left = tk.Frame(self)
        self.left.grid(column=0, row=0, sticky='NESW')
        self.right = tk.Frame(self)
        self.right.grid(column=1, row=0, sticky='NE')

        # Setup and draw canvas on the right.
        self.canvas = tk.Canvas(self.right,
                                width=self.canvas_size + (2 * self.canvas_pad),
                                height=self.canvas_size + (2 * self.canvas_pad))
        self.canvas.grid()
        self.draw_board()

        # Left control panel.
        self.metric_label = ttk.Label(self.left, text='Judging Metric')
        self.metric_label.grid(row=0, sticky='EW')

        self.metric = tk.StringVar()
        metric_options = [
            'Dot Count',
            'Hit Frequency',
            'Resource Rate',
            'Resource Rate with Trades',
            'Resource Needs'
        ]
        self.metric_box = ttk.Combobox(
            self.left,
            values=metric_options,
            textvariable=self.metric,
            width=max(len(x) for x in metric_options)
            )
        self.metric_box.grid(row=1, columnspan=2, sticky='NEW')

        self.pairwise = tk.IntVar()
        self.pairwise_check = ttk.Checkbutton(
            self.left,
            variable=self.pairwise,
            text='Pairwise'
        )
        self.pairwise_check.grid(row=0, column=1, sticky='E')

        self.submit = ttk.Button(self.left,
                                 text='Submit',
                                 command=self.select_optimum)
        self.submit.grid(column=0, columnspan=2, row=2, sticky='EW')

        # Sorted list of pieces.
        self.list = tk.Frame(self.left)
        self.list.grid(column=0, row=3, sticky='NESW')

        self.list.id_header = ttk.Label(self.list, text='ID')
        self.list.id_header.grid(column=0, row=0, sticky='W', padx=10)
        self.list.score_header = ttk.Label(self.list, text='Score')
        self.list.score_header.grid(column=1, row=0, sticky='W', padx=10)

        self.list.list = None

    def setup_board(self):
        window = tk.Toplevel(self)

        numbers = [0, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
        resources = ['brick', 'lumber', 'ore', 'grain', 'wool', 'desert']
        res_values = [
            tk.StringVar()
            for i
            in range(19)
        ]
        num_values = [
            tk.IntVar()
            for i
            in range(19)
        ]
        for i in range(19):
            if self.board.tiles[i].resource:
                res_values[i].set(self.board.tiles[i].resource)
            else:
                res_values[i].set('desert')
            if self.board.tiles[i].number:
                num_values[i].set(self.board.tiles[i].number)
            else:
                num_values[i].set(0)

        ttk.Label(window, text='ID').grid(column=0, row=0)
        ttk.Label(window, text='Resource').grid(column=1, row=0)
        ttk.Label(window, text='Number').grid(column=2, row=0)

        for i in range(19):
            ttk.Label(window, text=str(i)).grid(column=0, row=i+1, sticky='W')
            res = ttk.Combobox(
                window,
                textvariable=res_values[i],
                width=max(len(r) for r in resources),
                values=resources)
            res.grid(column=1, row=i+1, sticky='EW')
            num = ttk.Combobox(
                window,
                textvariable=num_values[i],
                width=4,
                values=numbers)
            num.grid(column=2, row=i+1, sticky='W')

        def create_board():
            for i in range(19):
                if res_values[i].get() != 'desert':
                    self.board.tiles[i].resource = res_values[i].get()
                else:
                    self.board.tiles[i].resource = None

                if res_values[i].get() != 'desert':
                    self.board.tiles[i].number = num_values[i].get()
                else:
                    self.board.tiles[i].number = None

            self.draw_board()

            window.destroy()

        ttk.Button(window, text='Create Board', command=create_board).grid(column=1, columnspan=2, row=21, sticky='W')

    def set_needs(self):
        window = tk.Toplevel(self)

        ttk.Label(window, text='Resource').grid(column=0, row=0)
        ttk.Label(window, text='Needs').grid(column=1, row=0)

        ttk.Label(window, text='Lumber').grid(column=0, row=1, sticky='W')
        ttk.Label(window, text='Brick').grid(column=0, row=2, sticky='W')
        ttk.Label(window, text='Grain').grid(column=0, row=3, sticky='W')
        ttk.Label(window, text='Wool').grid(column=0, row=4, sticky='W')
        ttk.Label(window, text='Ore').grid(column=0, row=5, sticky='W')

        tk.Scale(window,
                  from_=1,
                  to=100,
                  orient=tk.HORIZONTAL,
                  variable=self.needs['lumber']).grid(column=1, row=1)
        tk.Scale(window,
                  from_=1,
                  to=100,
                  orient=tk.HORIZONTAL,
                  variable=self.needs['brick']).grid(column=1, row=2)
        tk.Scale(window,
                  from_=1,
                  to=100,
                  orient=tk.HORIZONTAL,
                  variable=self.needs['grain']).grid(column=1, row=3)
        tk.Scale(window,
                  from_=1,
                  to=100,
                  orient=tk.HORIZONTAL,
                  variable=self.needs['wool']).grid(column=1, row=4)
        tk.Scale(window,
                  from_=1,
                  to=100,
                  orient=tk.HORIZONTAL,
                  variable=self.needs['ore']).grid(column=1, row=5)

        ttk.Button(window, text='Done', command=window.destroy).grid(column=1, row=6)

    def select_optimum(self):
        self.list.length = 20

        if self.list.list:
            self.list.list.destroy()
        self.list.list = tk.Frame(self.list)
        self.list.list.grid(column=0, row=1, columnspan=2, sticky='NESW')

        method = self.metric_box.get()

        if method == 'Dot Count' and not self.pairwise.get():
            scores = [(node.index, node.get_dot_sum())
                      for node
                      in self.board.nodes]
            scores.sort(key=lambda x: x[1], reverse=True)
        elif method == 'Hit Frequency' and not self.pairwise.get():
            scores = [(node.index, node.get_hit_frequency())
                      for node
                      in self.board.nodes]
            scores.sort(key=lambda x: x[1], reverse=True)
        elif method == 'Resource Rate' and not self.pairwise.get():
            scores = [(node.index, node.get_flow_rate_no_trades())
                      for node
                      in self.board.nodes]
            scores.sort(key=lambda x: x[1], reverse=True)
        elif method == 'Resource Rate with Trades' and not self.pairwise.get():
            scores = [(node.index, sum(node.get_flow_rate().values()))
                      for node
                      in self.board.nodes]
            scores.sort(key=lambda x: x[1], reverse=True)
        elif method == 'Resource Needs' and not self.pairwise.get():
            needs = {k: v.get() for k, v in self.needs.items()}
            scores = [(node.index, node.get_fill_rate(needs))
                      for node
                      in self.board.nodes]
            scores.sort(key=lambda x: x[1])
        elif method == 'Dot Count' and self.pairwise.get():
            scores = self.board.get_pairwise_dot_sum()
            scores.sort(key=lambda x: x[1], reverse=True)
        elif method == 'Hit Frequency' and self.pairwise.get():
            scores = self.board.get_pairwise_hit_frequency()
            scores.sort(key=lambda x: x[1], reverse=True)
        elif method == 'Resource Rate' and self.pairwise.get():
            scores = self.board.get_pairwise_flow_rate_no_trades()
            scores.sort(key=lambda x: x[1], reverse=True)
        elif method == 'Resource Rate with Trades' and self.pairwise.get():

            scores = [(pair, sum(flow.values()))
                      for pair, flow
                      in self.board.get_pairwise_flow_rate()]
            scores.sort(key=lambda x: x[1], reverse=True)
        elif method == 'Resource Needs' and self.pairwise.get():
            needs = {k: v.get() for k, v in self.needs.items()}
            scores = self.board.get_pairwise_fill_rate(needs)
            scores.sort(key=lambda x: x[1])
        else:
            scores = []

        if scores:
            for i, score in enumerate(scores[:self.list.length]):

                score_text = '{0:.2f}'.format(float(score[1]))
                ttk.Label(self.list.list, text=str(score[0])).grid(column=0,
                                                                row=i,
                                                                sticky='E',
                                                                padx=10)
                ttk.Label(self.list.list, text=score_text).grid(column=1,
                                                                row=i,
                                                                sticky='E',
                                                                padx=10)

    def draw_board(self):
        # Clear canvas.
        self.canvas.delete('all')

        # Add background.
        self.canvas.create_rectangle(0, 0,
                                     self.canvas_size + (2 * self.canvas_pad),
                                     self.canvas_size + (2 * self.canvas_pad),
                                     fill='light blue')

        colors = {
            'lumber': 'dark green',
            'ore': 'gray',
            'brick': 'red',
            'grain': 'yellow',
            'wool': 'green',
            None: '#404020',
            'all': 'white'
        }
        # Draw Tiles
        hex_starts = [
            (120, 0),
            (200, 0),
            (280, 0),
            (80, 75),
            (160, 75),
            (240, 75),
            (320, 75),
            (40, 150),
            (120, 150),
            (200, 150),
            (280, 150),
            (360, 150),
            (80, 225),
            (160, 225),
            (240, 225),
            (320, 225),
            (120, 300),
            (200, 300),
            (280, 300),
        ]

        # For every hex
        for i, (x, y) in enumerate(hex_starts):
            # Add and color the hex.
            self.canvas.create_polygon(
                *self.get_hex_coords(x + self.canvas_pad, y + self.canvas_pad),
                fill=colors[self.board.tiles[i].resource])

            # If there is a number, add it.
            if self.board.tiles[i].number:
                self.canvas.create_oval(
                    x - 20 + self.canvas_pad, y + 30 + self.canvas_pad,
                    x + 20 + self.canvas_pad, y + 70 + self.canvas_pad,
                    fill='white'
                )
                self.canvas.create_text(
                    x + self.canvas_pad, y + 50 + self.canvas_pad,
                    text=str(self.board.tiles[i].number)
                )

        # Draw ports to the board.
        port_locs = [
            (120, 30, 120, 0, 80, 25),
            (270, 15, 200, 0, 240, 25),
            (400, 90, 320, 75, 360, 100),
            (470, 240, 400, 175, 400, 225),
            (405, 385, 360, 300, 320, 325),
            (275, 450, 240, 375, 200, 400),
            (110, 450, 120, 400, 80, 375),
            (30, 325, 40, 250, 40, 300),
            (40, 150, 40, 100, 40, 150)
        ]

        for i, port in enumerate(self.board.ports):
            port_size = 20

            x, y, line_one_x, line_one_y, line_two_x, line_two_y = port_locs[i]

            self.canvas.create_line(
                x + (port_size / 2), y + (port_size / 2),
                line_one_x + self.canvas_pad, line_one_y + self.canvas_pad
            )
            self.canvas.create_line(
                x + (port_size / 2), y + (port_size / 2),
                line_two_x + self.canvas_pad, line_two_y + self.canvas_pad
            )
            self.canvas.create_rectangle(
                x, y,
                x + 20, y + 20,
                fill=colors[port.resource]
            )

        # Add node indexes to board.
        node_coords = set()
        for x, y in hex_starts:
            for coord in self.get_hex_coords(x + self.canvas_pad,
                                             y + self.canvas_pad):
                node_coords.add(coord)
        node_coords = list(node_coords)
        node_coords.sort(key=lambda x: x[0])
        node_coords.sort(key=lambda x: x[1])

        for i, (x, y) in enumerate(node_coords):
            self.canvas.create_oval(x - 10, y - 10,
                                    x + 10, y + 10,
                                    fill='light gray')
            self.canvas.create_text(x, y, text=str(i))

    def get_hex_coords(self, x, y):
        return [
            (x, y),
            (x + 40, y + 25),
            (x + 40, y + 75),
            (x, y + 100),
            (x - 40, y + 75),
            (x - 40, y + 25)
        ]


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Settlers of Catan: Optimum Intersection')
    app = Application(master=root)
    root.config(menu=app.menu)
    app.mainloop()
