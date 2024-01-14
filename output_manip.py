# Function to convert array to a string
def array_to_string(arr):
    return '\n'.join([' '.join('[ {} ]'.format(c) for c in row) for row in arr])


# Define the array for each arm
top_arm = [
    ['#', '#', '#', 'X', '#', '#', '#', '#'],
    ['#', '#', '#', '#', 'X', '#', '#', '#'],
    ['#', '#', '#', 'X', '#', '#', '#', '#']
]

right_arm = [
    ['#', '#', '#', 'S', '#', '#', '#', 'N'],
    ['#', '#', '#', '#', 'EE', 'D', 'U', '#'],
    ['#', '#', '#', 'X', '#', '#', '#', '#']
]

bottom_arm = [
    ['#', '#', '#', 'X', '#', '#', '#', '#'],
    ['#', '#', '#', '#', 'X$', '#', '#', '#'],
    ['#', '#', '#', 'X', '#', '#', '#', '#']
]

left_arm = [
    ['S', '#', '#', 'X', '#', '#', '#', '#'],
    ['#', 'E', 'N', '#', 'X', '#', '#', '#'],
    ['#', '#', '#J', 'D', '#', '#', '#', '#']
]


# Function to print the board with all four arms
def get_board_str(top, right, bottom, left):
    middle = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]
    # Convert arrays to string representation
    top_str = array_to_string(list(zip(*top))[::-1])
    right_str = array_to_string([row[::-1] for row in right])
    bottom_str = array_to_string(list(zip(*bottom[::-1])))
    left_str = array_to_string(left)
    middle_str = array_to_string(middle)
    middle_lines = middle_str.split('\n')

    # Padding for alignment
    padding = ' ' * (len(left[0]) + 40)

    # Prepare the sections of the board
    top_lines = top_str.split('\n')
    right_lines = right_str.split('\n')
    bottom_lines = bottom_str.split('\n')
    left_lines = left_str.split('\n')

    result_str = ''
    # Print the board
    for line in top_lines:
        result_str += padding + line + '\n'

    for l, m, r in zip(left_lines, middle_lines, right_lines):
        result_str += l + ' ' + m + ' ' + r + ' ' + '\n'

    for line in bottom_lines:
        result_str += padding + line + '\n'

    return result_str

# Print the board with all four arms
# print(get_board_str(top_arm, right_arm, bottom_arm, left_arm))
# DEBUG
