def print_equilateral_triangle(height):
    """Prints an equilateral triangle of a given height."""
    for i in range(height):
        # Print leading spaces
        print(' ' * (height - i - 1), end='')
        # Print stars
        print('* ' * (i + 1))

# Example usage
if __name__ == "__main__":
    height = 5  # You can change this value for different heights
    print_equilateral_triangle(height)
