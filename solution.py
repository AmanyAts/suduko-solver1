
from utils import *


# Encode the board: units and peers
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ("ABC","DEF","GHI") for cs in ("123","456","789")]
diagonal_units = [[rows[i] + cols[i] for i in range(9)]] + [[rows[i] + cols[::-1][i] for i in range(9)]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
# unitlist = unitlist

# Must be called after all units (including diagonals) are added to the unitlist


units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


# units = extract_units(unitlist, boxes)
# peers = extract_peers(units, boxes)


def naked_twins(values):
    two_item_boxes = [box for box in values if len(values[box]) == 2]

    naked_twins = [(box1,box2) for box1 in two_item_boxes for box2 in peers[box1] if sorted(values[box1]) == sorted(values[box2])]
    for twins in naked_twins:
        common_peers = set(peers[twins[0]]).intersection(peers[twins[1]])
        for peer in common_peers:
            for val in values[twins[0]]:
                values[peer] = values[peer].replace(val,'')

    return values
    

  
    # TODO: Implement this function!
#     raise NotImplementedError


def eliminate(values):

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values
  
    # TODO: Copy your code from the classroom to complete this function


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
                
      # TODO: Copy your code from the classroom to complete this function


def reduce_puzzle(values):
   
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    # TODO: Copy your code from the classroom and modify it to complete this function


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    # TODO: Copy your code from the classroom to complete this function
    raise NotImplementedError


def solve(grid):
    values = grid2values(grid)
    values = search(values)
    values = naked_twins(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
