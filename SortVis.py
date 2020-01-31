import pygame
from pygame import KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT, QUIT, DOUBLEBUF
from os import environ
from math import pi, cos
from random import randint
from BubbleSort import BubbleSort
from QuickSort import QuickSort
from MergeSort import MergeSort
from SelectionSort import SelectionSort
from InsertionSort import InsertionSort
from CountSort import CountSort
from HeapSort import HeapSort
from ShellSort import ShellSort


WIDTH = 1200
HEIGHT = 800
NUM_ELEMENTS = 10
POINT_RADIUS = 80 // NUM_ELEMENTS
FPS = 60
STEP_SIZE = 3
TOLERANCE = 2
BLACK = (0, 0, 0)
FIRST_COL = (255, 20, 20)
LAST_COL = (20, 255, 255)


def generate_colour_map(num_elements):
    colour_map = []
    for i in range(127):
        colour_map.insert(i, (128 + i, 0, 0))
        colour_map.insert(2 * i + 1, (255, i, 0))
        colour_map.insert(3 * i + 2, (255, 128 + i, 0))
        colour_map.insert(4 * i + 3, (255, 255, 2 * i))
    colour_map.insert(254, (255, 127, 0))
    colour_map.append((255, 255, 255))
    element_colours = []
    for i in range(num_elements):
        step = i * (len(colour_map) - 1) // (num_elements - 1)
        element_colours.append(colour_map[step])
    return element_colours


def get_intermediate_colour(num_elements, element_position):
    if element_position == 0:
        return FIRST_COL
    elif element_position == num_elements - 1:
        return LAST_COL
    else:
        delta_r = (LAST_COL[0] - FIRST_COL[0]) / num_elements
        delta_g = (LAST_COL[1] - FIRST_COL[1]) / num_elements
        delta_b = (LAST_COL[2] - FIRST_COL[2]) / num_elements
        red = FIRST_COL[0] + element_position * delta_r
        green = FIRST_COL[1] + element_position * delta_g
        blue = FIRST_COL[2] + element_position * delta_b

    return int(red), int(green), int(blue)


def trace_element_through_generations(generations, element, x_spacing, y_spacing):
    xs = []
    ys = []
    for i, generation in enumerate(generations[1: -1]):
        element_index = generation.index(element)
        xs.append(int(x_spacing * (i + 2)))
        ys.append(int(y_spacing * (element_index + 1)))
    return xs, ys


def main():
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF, 32)

    # Initialise pygame
    fps_clock = pygame.time.Clock()

    # Setup unsorted data
    unsorted = []
    for i in range(NUM_ELEMENTS):
        r = randint(-100, 100)
        if r not in unsorted:
            unsorted.append(r)
    # unsorted = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]  # Can be interesting to see sometimes
    # unsorted = [7, 3, 3]  # <== Need to find a way to visualise arrays with repeating elements
    num_elems = len(unsorted)
    colour_map = generate_colour_map(num_elems)

    # Pick an algorithm!
    s = BubbleSort()
    s.sort(unsorted)
    generations = s.generations
    pygame.display.set_caption(f'Visualise Sorting Algorithms - {s.name}')

    # Calculate some values to display the results
    num_generations = len(generations)
    curr_gen = 1
    x_spacing = WIDTH / (num_generations + 1)
    y_spacing = HEIGHT / (num_elems + 1)

    # Calculate curves - these are based on Cosine curves between each point
    curves = []
    for i, elem in enumerate(unsorted):
        coords = trace_element_through_generations(generations, elem, x_spacing, y_spacing)
        temp = {'x': coords[0], 'y': coords[1], 'curve_x': [], 'curve_y': []}
        for j in range(len(temp['x']) - 1):
            x_diff = temp['x'][j + 1] - temp['x'][j]
            y_diff = temp['y'][j + 1] - temp['y'][j]
            temp['curve_x'].extend([temp['x'][j] + k for k in range(x_diff + 1)])
            temp['curve_y'].extend([int(temp['y'][j] + y_diff * 0.5 - y_diff * 0.5 * cos(pi * k / x_diff))
                                    for k in range(x_diff + 1)])
        curves.append(temp)

    curr_x = curves[0]['x'][0]

    while True:
        screen.fill(BLACK)

        # Handle keydown events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == K_LEFT:
                    curr_gen = max(1, curr_gen - 1)
                    if curr_gen == len(generations) - 2:
                        curr_gen -= 1
                elif event.key == K_RIGHT:
                    curr_gen = min(len(generations) - 2, curr_gen + 1)
                    if curr_gen == len(generations) - 2:
                        curr_gen += 1

        # Draw the curves first
        if curr_gen - 1 == len(curves[0]['x']):
            max_x = curves[0]['x'][curr_gen - 2]
            prev_x = curves[0]['x'][curr_gen - 3]
        else:
            max_x = curves[0]['x'][curr_gen - 1]
            prev_x = curves[0]['x'][max(0, curr_gen - 2)]

        for i, elem in enumerate(curves):
            curve_x = [e for e in elem['curve_x'] if e <= curr_x]
            while len(curve_x) < 2:
                curve_x.append(prev_x)
            curve_y = elem['curve_y'][:len(curve_x)]
            coords = list(zip(curve_x, curve_y))
            pygame.draw.aalines(screen, colour_map[i], False, coords)
            pygame.draw.circle(screen, colour_map[i], coords[-1], POINT_RADIUS)
        if curr_x <= max_x - TOLERANCE:
            curr_x += STEP_SIZE
        elif curr_x > max_x + TOLERANCE:
            curr_x -= STEP_SIZE

        # Display the array data; each generation is a vertical column
        for g, generation in enumerate(generations):
            if int(x_spacing * (g + 1)) <= curr_x + TOLERANCE:
                for e, element in enumerate(generation):
                    pygame.draw.circle(screen, colour_map[unsorted.index(element)],
                                       (int(x_spacing * (g + 1)), int(y_spacing * (e + 1))), POINT_RADIUS)
                    if g + 2 == len(generations):
                        pygame.draw.circle(screen, colour_map[unsorted.index(element)],
                                           (int(x_spacing * (g + 2)), int(y_spacing * (e + 1))), POINT_RADIUS)

        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    main()
