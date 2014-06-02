
from random import choice,shuffle
from MazeSolveAlgo import MazeSolveAlgo
from ShortestPaths import ShortestPaths


class CuldeSacFiller(MazeSolveAlgo):
    """
    1. Scan the maze, identify all fully-connected wall systems.
    2. Any wall system that touches the border is not a cul-de-sac, remove it.
    3. Determine if remaining wall systems are cul-de-sacs.
    4. If so, add a wall segment to turn the cul-de-sac into a dead end.
    5. Solve using Dead End Filler.
    """
    def __init__(self, solver=None):
        if not solver:
            self.solver = DeadEndFiller(ShortestPaths())
        else:
            self.solver = DeadEndFiller(solver)

    def _solve(self):
        raise NotImplementedError('This algorithm is under development.')
        current = self.start

        # identify all fully-connected wall systems
        walls = self._find_wall_systems()

        # remove any wall system that touches the maze boundary
        walls = self._remove_border_walls(walls)

        for wall in walls:
            border self._find_bordering_cells(wall)
            if self._wall_is_culdesac(border):
                self._fix_culdesac(border)

        return self._build_solutions()

    def _build_solutions(self):
        """Now that all of the cul-de-sac have been cut out, the maze still needs to be solved."""
        return self.solver.solve(self.grid, self.start, self.end)

    def _fix_culdesac(self, border):
        """Destroy the culdesac by blocking off the loop."""
        if len(border) > 1:
            grid[self._midpoint(border[0], border[1])] = 1

    def _wall_is_culdesac(self, border):
        """A cul-de-sac is a loop with only one entrance."""
        num_entrances = 0

        for cell in border:
            num_neighbors = len(self._find_unblocked_neighbors(cell))
            if num_neighbors > 2:
                num_entrances += 1
            if num_entrances > 1:
                return False

        return True

    def _find_bordering_cells(self, wall):
        """build a buffer, one cell wide, around the wall"""
        border = set()

        # buffer each wall cell by one, add those buffer cells to a set
        for cell in wall:
            r,c = cell
            for rdiff in xrange(-1, 2):
                for cdiff in xrange(-1, 2):
                    border.add((r + rdiff, c + cdiff))

        # remove all wall cells from the buffer
        border = filter(lambda b: for b not in wall, border)

        # remove all non-navigable cells from the buffer
        border = filter(lambda b: b[0] % == 1 and b[1] % == 1, border)

        # remove all dead ends within the cul-de-sac
        return self._remove_internal_deadends(border)

    def _remove_internal_deadends(self, border):
        """Complicated cul-de-Sacs can have internal dead ends.
        These seriously complicate the logic and need to be removed."""
        found = True
        while found:
            found = False
            new_border = border
            for cell in border:
                if len(self._find_unblocked_neighbors(cell)) < 2:
                    new_border.remove(cell)
                    found = True
            border = new_border

        return border

    def _remove_border_walls(self, walls):
        """remove any wall system that touches the maze border"""
        new_walls = []

        for wall in walls:
            touches_border = False
            for cell in wall:
                if self._is_on_border(cell):
                    touches_border = True
                    break
            if not touches_border:
                new_walls.append(wall)

        return new_walls

    def _is_on_border(self, cell):
        """Determine is a cell is on the border of the maze"""
        r,c = cell

        if r == 0 or c == 0:
            return True
        elif r == (self.grid.height - 1):
            return True
        elif c == (self.grid.width - 1):
            return True
        else:
            return False

    def _find_wall_systems(self):
        """A wall system is any continiously-adjacent set of walls."""
        walls = []
        # loop through each cell in the maze
        for r in xrange(self.grid.height):
            for c in xrange(self.grid.width):
                # if the cell is a wall
                if self.grid[r, c] == 1:
                    found = False
                    # determine which wall system it belongs in
                    for i in xrange(len(walls)):
                        if self._has_neighbor((r, c), walls[i]):
                            found = True
                            walls[i].append((r, c))
                    if not found:
                        walls.append([(r, c)])

        return walls

    def _is_neighbor(self, cell1, cell2):
        """Determine if one cell is adjacent to another"""
        r_diff = abs(cell1[0] - cell2[0])
        c_diff = abs(cell1[1] - cell2[1])

        if r_diff == 0 and c_diff == 1:
            return True
        elif c_diff == 0 and r_diff == 1:
            return True
        else:
            return False

    def _has_neighbor(self, cell, list_cells):
        """Determine if your cell has a neighbor in a list of cells"""
        for target in list_cells:
            if self._is_neighbor(cell, target):
                return True

        return False
    def _find_unblocked_neighbors(self, posi):
        """Find all the grid neighbors of the current position;
        visited, or not.
        """
        (row, col) = posi
        ns = []

        if row > 1 and self.grid[row-1, col] == False and self.grid[row-2, col] == False:
            ns.append((row-2, col))
        if row < self.grid.height-2 and self.grid[row+1, col] == False and self.grid[row+2, col] == False:
            ns.append((row+2, col))
        if col > 1 and self.grid[row, col-1] == False and self.grid[row, col-2] == False:
            ns.append((row, col-2))
        if col < self.grid.width-2 and self.grid[row, col+1] == False and self.grid[row, col+2] == False:
            ns.append((row, col+2))

        shuffle(ns)

        return ns

    def _midpoint(self, a, b):
        """Find the wall cell between to passage cells"""
        return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2
