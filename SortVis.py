import pygame
from pygame import KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, QUIT,\
    DOUBLEBUF
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


WIDTH = 1400
HEIGHT = 700
NUM_ELEMENTS = 10
POINT_RADIUS = 80 // NUM_ELEMENTS
FPS = 60
STEP_SIZE = 3
TOLERANCE = 2
BLACK = (0, 0, 0)
FIRST_COL = (255, 20, 20)
LAST_COL = (20, 255, 255)
ALGORITHM_EVENT = pygame.USEREVENT
BUTTON_EVENT = pygame.USEREVENT + 1

supported_algorithms = {K_1: pygame.event.Event(ALGORITHM_EVENT, {'name': 'Bubble', 'callback': BubbleSort}),
                        K_2: pygame.event.Event(ALGORITHM_EVENT, {'name': 'Count', 'callback': CountSort}),
                        K_3: pygame.event.Event(ALGORITHM_EVENT, {'name': 'Heap', 'callback': HeapSort}),
                        K_4: pygame.event.Event(ALGORITHM_EVENT, {'name': 'Insertion', 'callback': InsertionSort}),
                        K_5: pygame.event.Event(ALGORITHM_EVENT, {'name': 'Merge', 'callback': MergeSort}),
                        K_6: pygame.event.Event(ALGORITHM_EVENT, {'name': 'Quick', 'callback': QuickSort}),
                        K_7: pygame.event.Event(ALGORITHM_EVENT, {'name': 'Selection', 'callback': SelectionSort}),
                        K_8: pygame.event.Event(ALGORITHM_EVENT, {'name': 'Shell', 'callback': ShellSort})}

supported_buttons = {K_LEFT: pygame.event.Event(BUTTON_EVENT, {'name': '<'}),
                     K_RIGHT: pygame.event.Event(BUTTON_EVENT, {'name': '>'}),
                     K_UP: pygame.event.Event(BUTTON_EVENT, {'name': '^'}),
                     K_DOWN: pygame.event.Event(BUTTON_EVENT, {'name': 'v'})}


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
        ys.append(int(y_spacing * (element_index + 1.5)))
    return xs, ys


def button(surface, button_text, font, colour, top_left_x, top_left_y, width, height,
           inactive_colour, active_colour, user_event=None):
    # Taken from https://pythonprogramming.net/pygame-button-function-events/?completed=/pygame-button-function/
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if top_left_x + width > mouse[0] > top_left_x and top_left_y + height > mouse[1] > top_left_y:
        pygame.draw.rect(surface, active_colour, (top_left_x, top_left_y, width, height))

        if click[0] == 1 and user_event is not None:
            pygame.event.post(user_event)
    else:
        pygame.draw.rect(surface, inactive_colour, (top_left_x, top_left_y, width, height))

    text_surface = font.render(button_text, True, colour)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = ((top_left_x + (width / 2)), (top_left_y + (height / 2)))
    surface.blit(text_surface, text_rectangle)


def draw_buttons(surface):
    basic_font = pygame.font.SysFont('jetbrainsmono.ttf', 36)
    text_surface = basic_font.render('Selection', True, (0, 0, 0))
    text_rectangle = text_surface.get_rect()
    text_rectangle = text_rectangle.inflate(text_rectangle.width * 0.25, text_rectangle.height * 0.5)
    for i, algo_event in enumerate(supported_algorithms.values()):
        button(surface, algo_event.name, basic_font, (0, 0, 0), i * (text_rectangle.width + 10), 10,
               text_rectangle.width, text_rectangle.height, (50, 50, 50), (100, 100, 100), algo_event)
    remaining_width = WIDTH - len(supported_algorithms) * (text_rectangle.width + 10) - 10
    button_width = remaining_width // 4 - 10
    left_most = WIDTH - remaining_width
    for i, button_event in enumerate(supported_buttons.values()):
        button(surface, button_event.name, basic_font, (0, 0, 0), left_most + i * (button_width + 10), 10,
               button_width, text_rectangle.height, (50, 50, 50), (100, 100, 100), button_event)


def calculate_curves(unsorted, generations, x_spacing, y_spacing):
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
    return curves


def switch_algorithm(callback):
    unsorted = []
    while len(unsorted) < NUM_ELEMENTS:
        r = randint(-100, 100)
        if r not in unsorted:
            unsorted.append(r)
    s = callback()
    s.sort(unsorted)
    generations = s.generations
    pygame.display.set_caption(f'Visualise Sorting Algorithms - {s.name}')
    # Calculate some values to display the results
    num_generations = len(generations)
    x_spacing = WIDTH / (num_generations + 1)
    curves = calculate_curves(unsorted, generations, x_spacing, HEIGHT / (len(unsorted) + 1))
    curr_x = curves[0]['x'][0]
    curr_gen = 1
    return curr_gen, curr_x, curves, generations, unsorted, x_spacing


def prev_generation(curr_gen, num_generations):
    curr_gen = max(1, curr_gen - 1)
    if curr_gen == num_generations - 2:
        curr_gen -= 1
    return curr_gen


def next_generation(curr_gen, num_generations):
    curr_gen = min(num_generations - 2, curr_gen + 1)
    if curr_gen == num_generations - 2:
        curr_gen += 1
    return curr_gen


def main():
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF, 32)

    # Initialise pygame
    fps_clock = pygame.time.Clock()

    basic_font = pygame.font.SysFont('verdana', 10)

    curr_gen, curr_x, curves, generations, unsorted, x_spacing = switch_algorithm(BubbleSort)

    y_spacing = HEIGHT / (len(unsorted) + 1)
    colour_map = generate_colour_map(len(unsorted))
    curr_gen = 1
    mouse_ready = True  # Used to prevent multi-clicks on the on-screen buttons

    while True:
        screen.fill(BLACK)

        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == K_LEFT:
                    curr_gen = prev_generation(curr_gen, len(generations))
                elif event.key == K_RIGHT:
                    curr_gen = next_generation(curr_gen, len(generations))
                elif event.key in supported_algorithms.keys():
                    curr_gen, curr_x, curves, generations, unsorted, x_spacing =\
                        switch_algorithm(supported_algorithms[event.key].callback)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_ready = True
            elif event.type == ALGORITHM_EVENT and mouse_ready is True:
                curr_gen, curr_x, curves, generations, unsorted, x_spacing = switch_algorithm(event.callback)
                mouse_ready = False
            elif event.type == BUTTON_EVENT:# and mouse_ready is True:
                if event.name == '<':
                    curr_gen = prev_generation(curr_gen, len(generations))
                elif event.name == '>':
                    curr_gen = next_generation(curr_gen, len(generations))
                mouse_ready = False

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
                    gen_x = g + 2 if g + 2 == len(generations) else g + 1
                    pygame.draw.circle(screen, colour_map[unsorted.index(element)],
                                       (int(x_spacing * gen_x), int(y_spacing * (e + 1.5))), POINT_RADIUS)
                    # Display the numerical values for the last generation
                    if gen_x == len(generations):
                        text_surface = basic_font.render(f'{element}', True, colour_map[unsorted.index(element)])
                        text_rectangle = text_surface.get_rect()
                        text_rectangle.midleft = (int(x_spacing * gen_x + POINT_RADIUS + 5), int(y_spacing * (e + 1.5)))
                        screen.blit(text_surface, text_rectangle)

        # Display the actual numerical values for the first generation
        for e, element in enumerate(generations[0]):
            text_surface = basic_font.render(f'{element}', True, colour_map[unsorted.index(element)])
            text_rectangle = text_surface.get_rect()
            text_rectangle.midright = (int(x_spacing - POINT_RADIUS - 5), int(y_spacing * (e + 1.5)))
            screen.blit(text_surface, text_rectangle)

        draw_buttons(screen)

        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    main()
