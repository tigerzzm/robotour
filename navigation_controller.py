"""
Navigation controller for the robotic vehicle.
Handles path planning and grid traversal logic.
"""

import time
from config import *

class NavigationController:
    def __init__(self):
        """Initialize the navigation controller."""
        self.grid_rows = GRID_ROWS
        self.grid_cols = GRID_COLS
        self.current_row = 0
        self.current_col = 0
        self.current_direction = 'north'  # north, south, east, west
        self.visited_cells = set()
        self.target_cells = []
        
        # Initialize target cells (example: visit all cells in a pattern)
        self.initialize_target_cells()
        
        print(f"Navigation controller initialized - Grid: {self.grid_rows}x{self.grid_cols}")
    
    def initialize_target_cells(self):
        """Initialize the target cells to visit."""
        # Example: Visit all cells in a snake pattern
        for row in range(self.grid_rows):
            if row % 2 == 0:  # Even rows: left to right
                for col in range(self.grid_cols):
                    self.target_cells.append((row, col))
            else:  # Odd rows: right to left
                for col in range(self.grid_cols - 1, -1, -1):
                    self.target_cells.append((row, col))
        
        print(f"Target cells initialized: {len(self.target_cells)} cells to visit")
    
    def update_position(self, row, col):
        """Update the current position of the vehicle."""
        if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
            self.current_row = row
            self.current_col = col
            self.visited_cells.add((row, col))
            return True
        return False
    
    def get_next_target(self):
        """Get the next target cell to visit."""
        for target in self.target_cells:
            if target not in self.visited_cells:
                return target
        return None  # All cells visited
    
    def calculate_path_to_target(self, target_row, target_col):
        """Calculate the path from current position to target."""
        if target_row is None or target_col is None:
            return []
        
        path = []
        current_row, current_col = self.current_row, self.current_col
        
        # Simple path: move to target row first, then to target column
        # Move vertically first
        while current_row != target_row:
            if current_row < target_row:
                path.append('move_south')
                current_row += 1
            else:
                path.append('move_north')
                current_row -= 1
        
        # Then move horizontally
        while current_col != target_col:
            if current_col < target_col:
                path.append('move_east')
                current_col += 1
            else:
                path.append('move_west')
                current_col -= 1
        
        return path
    
    def get_movement_commands(self, target_row, target_col):
        """Get the sequence of movement commands to reach the target."""
        path = self.calculate_path_to_target(target_row, target_col)
        commands = []
        
        for move in path:
            if move == 'move_north':
                commands.extend(self.get_commands_to_face('north'))
                commands.append('move_forward')
            elif move == 'move_south':
                commands.extend(self.get_commands_to_face('south'))
                commands.append('move_forward')
            elif move == 'move_east':
                commands.extend(self.get_commands_to_face('east'))
                commands.append('move_forward')
            elif move == 'move_west':
                commands.extend(self.get_commands_to_face('west'))
                commands.append('move_forward')
        
        return commands
    
    def get_commands_to_face(self, target_direction):
        """Get commands to turn to face the target direction."""
        commands = []
        
        if self.current_direction == target_direction:
            return commands  # Already facing the right direction
        
        # Calculate the turn needed
        direction_map = {'north': 0, 'east': 1, 'south': 2, 'west': 3}
        current_angle = direction_map[self.current_direction]
        target_angle = direction_map[target_direction]
        
        # Calculate shortest turn
        turn_angle = (target_angle - current_angle) % 4
        
        if turn_angle == 1:  # Turn right
            commands.append('turn_right')
        elif turn_angle == 2:  # Turn around
            commands.append('turn_right')
            commands.append('turn_right')
        elif turn_angle == 3:  # Turn left
            commands.append('turn_left')
        
        # Update current direction
        self.current_direction = target_direction
        
        return commands
    
    def is_navigation_complete(self):
        """Check if navigation is complete (all cells visited)."""
        return len(self.visited_cells) >= len(self.target_cells)
    
    def get_navigation_status(self):
        """Get current navigation status."""
        return {
            'current_position': (self.current_row, self.current_col),
            'current_direction': self.current_direction,
            'visited_cells': len(self.visited_cells),
            'total_cells': len(self.target_cells),
            'progress': len(self.visited_cells) / len(self.target_cells) * 100,
            'is_complete': self.is_navigation_complete()
        }
    
    def reset_navigation(self):
        """Reset navigation to start over."""
        self.current_row = 0
        self.current_col = 0
        self.current_direction = 'north'
        self.visited_cells.clear()
        print("Navigation reset")
    
    def set_custom_targets(self, target_cells):
        """Set custom target cells for navigation."""
        self.target_cells = target_cells
        self.visited_cells.clear()
        print(f"Custom targets set: {len(target_cells)} cells")
    
    def get_remaining_targets(self):
        """Get list of remaining target cells."""
        return [target for target in self.target_cells if target not in self.visited_cells]
