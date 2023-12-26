import cv2
import numpy as np
import random
import uuid
import matplotlib.pyplot as plt

def random_color():
    return tuple(random.randint(0, 255) for _ in range(3))

def random_shape():
    shapes = ['trefoil_knot', 'sine_wave', 'cubic_bezier_curve', 'quadratic_bezier_curve', 'watts_curve', 'fish', 'elephant', 'butterfly', 'turtle', 'duck', 'archimedean_spiral', 'folium_of_descartes', 'deltoid_curve', 'torus_knot', 'spirograph', 'lemniscate', 'lemniscate_gerono', 'lemniscate_booth', 'rose_curve', 'spiral_theodorus', 'epicycloid', 'hypocycloid', 'astroid', 'lissajous_curve', 'cardioid', 'rectangle', 'circle', 'triangle', 'ellipse', 'pentagon', 'hexagon', 'star', 'parallelogram', 'diamond', 'trapezoid', 'octagon', 'cross', 'arrow', 'heart', 'oval', 'pentagram', 'rounded_rectangle', 'semicircle', 'crescent', 'cloud', 'arrow_right', 'arrow_left', 'cloud', 'hexagram', 'moon', 'pentagon_star', 'flower', 'double_arrow_up', 'double_arrow_down', 'rectangle_with_triangle', 'plus', 'hourglass', 'butterfly_curve', 'elkies_trinomial_curve', 'hyperelliptic_curve', 'polynomial_lemniscate', 'fermat_curve', 'sinusoidal_spiral', 'superellipse', 'hurwitz_surface', 'bowditch_curve', 'brachistochrone', 'catenary', 'clelies', 'cochleoid', 'cycloid', 'horopter']
    return random.choice(shapes)

def create_video(num_videos=1, duration=10, frame_rate=30, resolution=(640, 640), aspect_ratio=(1, 1)):
    for _ in range(num_videos):
        # Adjust resolution based on aspect ratio
        resolution = (resolution[0], int(resolution[0] * aspect_ratio[1] / aspect_ratio[0]))

        # Video properties
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = f"/content/abcRSAG/v/{str(uuid.uuid4())}.mp4"
        video_writer = cv2.VideoWriter(output_path, fourcc, frame_rate, resolution)

        # Generate a random number of objects
        num_objects = random.randint(3, 100)  # Adjust the range as needed

        # Generate random objects
        objects = []
        for _ in range(num_objects):
            obj_size = random.randint(int(resolution[0] / 10), int(resolution[0] / 5))
            obj_color = random_color()
            obj_shape = random_shape()
            obj_x, obj_y = random.randint(0, resolution[0] - obj_size), random.randint(0, resolution[1] - obj_size)
            obj_vx, obj_vy = random.uniform(-10, 10), random.uniform(-10, 10)
            objects.append({'size': obj_size, 'color': obj_color, 'shape': obj_shape, 'x': obj_x, 'y': obj_y, 'vx': obj_vx, 'vy': obj_vy})

        # Generate frames
        for frame_count in range(int(duration * frame_rate)):
            # Generate random background color for each frame
            background_color = random_color()

            frame = np.full((resolution[1], resolution[0], 3), background_color, dtype=np.uint8)

            # Draw random objects
            for obj in objects:
                # Randomly change the size of the shapes
                size_change = random.uniform(-2, 2)
                obj['size'] += size_change

                if obj['shape'] == 'rectangle':
                    cv2.rectangle(frame, (int(obj['x']), int(obj['y'])),
                                  (int(obj['x'] + obj['size']), int(obj['y'] + obj['size'])), obj['color'], -1)
                elif obj['shape'] == 'circle':
                    cv2.circle(frame, (int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)),
                               int(obj['size'] / 2), obj['color'], -1)
                elif obj['shape'] == 'triangle':
                    points = np.array([[obj['x'] + obj['size'] // 2, obj['y']],
                                       [obj['x'], obj['y'] + obj['size']],
                                       [obj['x'] + obj['size'], obj['y'] + obj['size']]], np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [points], color=obj['color'])
                elif obj['shape'] == 'ellipse':
                    cv2.ellipse(frame, (int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)),
                                (int(obj['size'] / 2), int(obj['size'] / 4)), 0, 0, 360, obj['color'], -1)
                elif obj['shape'] == 'pentagon':
                    side = int(obj['size'] / 2)
                    cx, cy = int(obj['x'] + side), int(obj['y'] + obj['size'] / 2)
                    points = np.array([[cx, cy - side],
                                       [cx + side * np.cos(2 * np.pi / 5), cy - side * np.sin(2 * np.pi / 5)],
                                       [cx + side * np.cos(4 * np.pi / 5), cy - side * np.sin(4 * np.pi / 5)],
                                       [cx + side * np.cos(6 * np.pi / 5), cy - side * np.sin(6 * np.pi / 5)],
                                       [cx + side * np.cos(8 * np.pi / 5), cy - side * np.sin(8 * np.pi / 5)]], np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [points], color=obj['color'])
                elif obj['shape'] == 'hexagon':
                    side = int(obj['size'] / 2)
                    cx, cy = int(obj['x'] + side), int(obj['y'] + obj['size'] / 2)
                    points = np.array([[cx, cy - side],
                                       [cx + side * np.cos(np.pi / 3), cy - side * np.sin(np.pi / 3)],
                                       [cx + side * np.cos(2 * np.pi / 3), cy - side * np.sin(2 * np.pi / 3)],
                                       [cx, cy + side],
                                       [cx - side * np.cos(2 * np.pi / 3), cy - side * np.sin(2 * np.pi / 3)],
                                       [cx - side * np.cos(np.pi / 3), cy - side * np.sin(np.pi / 3)]], np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [points], color=obj['color'])
                elif obj['shape'] == 'star':
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    outer_radius = int(obj['size'] / 2)
                    inner_radius = int(obj['size'] / 4)
                    points = []
                    for i in range(10):
                        angle = i * np.pi / 5
                        if i % 2 == 0:
                            x = cx + outer_radius * np.cos(angle)
                            y = cy + outer_radius * np.sin(angle)
                        else:
                            x = cx + inner_radius * np.cos(angle)
                            y = cy + inner_radius * np.sin(angle)
                        points.append([int(x), int(y)])
                    points = np.array(points, np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [points], color=obj['color'])
                elif obj['shape'] == 'parallelogram':
                    side = int(obj['size'] / 2)
                    cx, cy = int(obj['x'] + side), int(obj['y'] + obj['size'] / 2)
                    points = np.array([[cx, cy - side],
                                       [cx + side * 2, cy - side],
                                       [cx + side, cy + side],
                                       [cx - side, cy + side]], np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [points], color=obj['color'])
                elif obj['shape'] == 'diamond':
                    side = int(obj['size'] / 2)
                    cx, cy = int(obj['x'] + side), int(obj['y'] + obj['size'] / 2)
                    points = np.array([[cx, cy - side],
                                       [cx + side, cy],
                                       [cx, cy + side],
                                       [cx - side, cy]], np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [points], color=obj['color'])
                elif obj['shape'] == 'trapezoid':
                    top_width = int(obj['size'] / 2)
                    bottom_width = int(obj['size'])
                    height = int(obj['size'] / 2)
                    cx, cy = int(obj['x'] + top_width), int(obj['y'] + height)
                    points = np.array([[cx - top_width, cy - height],
                                       [cx + top_width, cy - height],
                                       [cx + bottom_width, cy + height],
                                       [cx - bottom_width, cy + height]], np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [points], color=obj['color'])
                elif obj['shape'] == 'octagon':
                    side = int(obj['size'] / 2)
                    cx, cy = int(obj['x'] + side), int(obj['y'] + obj['size'] / 2)
                    points = np.array([[cx + side, cy - side],
                                       [cx + side, cy + side],
                                       [cx, cy + side * 2],
                                       [cx - side, cy + side],
                                       [cx - side, cy - side],
                                       [cx, cy - side * 2],
                                       [cx + side * 2, cy - side],
                                       [cx + side * 2, cy + side]], np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [points], color=obj['color'])
                elif obj['shape'] == 'cross':
                    arm_length = int(obj['size'] / 3)
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    cv2.line(frame, (cx - arm_length, cy - arm_length), (cx + arm_length, cy + arm_length), obj['color'], int(obj['size'] / 10))
                    cv2.line(frame, (cx - arm_length, cy + arm_length), (cx + arm_length, cy - arm_length), obj['color'], int(obj['size'] / 10))
                elif obj['shape'] == 'arrow':
                    arrow_length = int(obj['size'] / 2)
                    arrow_head_size = int(obj['size'] / 5)
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    cv2.arrowedLine(frame, (cx, cy), (cx + arrow_length, cy), obj['color'], int(obj['size'] / 10), tipLength=0.3)
                    # Draw arrowhead
                    points = np.array([[cx + arrow_length - arrow_head_size, cy - arrow_head_size],
                                       [cx + arrow_length, cy],
                                       [cx + arrow_length - arrow_head_size, cy + arrow_head_size]], np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [points], color=obj['color'])
                elif obj['shape'] == 'heart':
                    heart_points = np.array([
                        [obj['x'] + obj['size'] / 2, obj['y']],
                        [obj['x'] + obj['size'], obj['y'] + obj['size'] / 4],
                        [obj['x'] + obj['size'] / 2, obj['y'] + obj['size']],
                        [obj['x'], obj['y'] + obj['size'] / 4]
                    ], np.int32)
                    heart_points = heart_points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [heart_points], color=obj['color'])

                elif obj['shape'] == 'oval':
                    cv2.ellipse(frame, (int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)),
                                (int(obj['size'] / 2), int(obj['size'] / 4)), 0, 0, 360, obj['color'], -1)
                elif obj['shape'] == 'pentagram':
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    outer_radius = int(obj['size'] / 2)
                    inner_radius = int(obj['size'] / 4)
                    points = []
                    for i in range(10):
                        angle = i * np.pi / 5
                        if i % 2 == 0:
                            x = cx + outer_radius * np.cos(angle)
                            y = cy + outer_radius * np.sin(angle)
                        else:
                            x = cx + inner_radius * np.cos(angle)
                            y = cy + inner_radius * np.sin(angle)
                        points.append([int(x), int(y)])
                    points = np.array(points, np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [points], color=obj['color'])

                elif obj['shape'] == 'rounded_rectangle':
                    corner_radius = int(obj['size'] / 8)
                    rect_x, rect_y = int(obj['x']), int(obj['y'])
                    rect_width, rect_height = int(obj['size']), int(obj['size'] / 2)
                    cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), obj['color'], -1)
                    cv2.circle(frame, (rect_x + corner_radius, rect_y + corner_radius), corner_radius, (0, 0, 0), -1)
                    cv2.circle(frame, (rect_x + rect_width - corner_radius, rect_y + corner_radius), corner_radius, (0, 0, 0), -1)
                elif obj['shape'] == 'semicircle':
                    cv2.ellipse(frame, (int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)),
                                (int(obj['size'] / 2), int(obj['size'] / 4)), 0, 0, 180, obj['color'], -1)

                elif obj['shape'] == 'crescent':
                    outer_radius = int(obj['size'] / 2)
                    inner_radius = int(obj['size'] / 3)
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)

                    # Draw outer circle
                    cv2.circle(frame, (cx, cy), outer_radius, obj['color'], -1)

                    # Draw inner circle
                    cv2.circle(frame, (cx, cy), inner_radius, (0, 0, 0), -1)

                elif obj['shape'] == 'cloud':
                    cloud_radius = int(obj['size'] / 4)
                    cloud_x, cloud_y = int(obj['x']), int(obj['y'])
                    cv2.circle(frame, (cloud_x + cloud_radius, cloud_y + cloud_radius), cloud_radius, obj['color'], -1)
                    cv2.circle(frame, (cloud_x + cloud_radius * 2, cloud_y + cloud_radius), cloud_radius, obj['color'], -1)
                    cv2.circle(frame, (cloud_x + cloud_radius * 3, cloud_y + cloud_radius), cloud_radius, obj['color'], -1)

                elif obj['shape'] == 'arrow_right':
                    arrow_length = int(obj['size'] / 2)
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    cv2.arrowedLine(frame, (cx, cy), (cx + arrow_length, cy), obj['color'], int(obj['size'] / 10), tipLength=0.3)

                elif obj['shape'] == 'arrow_left':
                    arrow_length = int(obj['size'] / 2)
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    cv2.arrowedLine(frame, (cx, cy), (cx - arrow_length, cy), obj['color'], int(obj['size'] / 10), tipLength=0.3)
                    
                elif obj['shape'] == 'hexagram':
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    outer_radius = int(obj['size'] / 2)
                    inner_radius = int(obj['size'] / 4)
                    points = []
                    for i in range(12):
                        angle = i * np.pi / 6
                        if i % 2 == 0:
                            x = cx + outer_radius * np.cos(angle)
                            y = cy + outer_radius * np.sin(angle)
                        else:
                            x = cx + inner_radius * np.cos(angle)
                            y = cy + inner_radius * np.sin(angle)
                        points.append([int(x), int(y)])
                    points = np.array(points, np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [points], color=obj['color'])

                elif obj['shape'] == 'moon':
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    outer_radius = int(obj['size'] / 2)
                    inner_radius = int(obj['size'] / 2.5)
                    cv2.circle(frame, (cx, cy), outer_radius, obj['color'], -1)
                    cv2.circle(frame, (cx - inner_radius, cy), inner_radius, (0, 0, 0), -1)

                elif obj['shape'] == 'pentagon_star':
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    outer_radius = int(obj['size'] / 2)
                    inner_radius = int(obj['size'] / 4)
                    points = []
                    for i in range(10):
                        angle = i * np.pi / 5
                        if i % 2 == 0:
                            x = cx + outer_radius * np.cos(angle)
                            y = cy + outer_radius * np.sin(angle)
                        else:
                            x = cx + inner_radius * np.cos(angle)
                            y = cy + inner_radius * np.sin(angle)
                        points.append([int(x), int(y)])
                    points = np.array(points, np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [points], color=obj['color'])

                elif obj['shape'] == 'flower':
                    num_petals = 6
                    petal_length = int(obj['size'] / 2)
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    for i in range(num_petals):
                        angle = i * 2 * np.pi / num_petals
                        petal_points = np.array([
                            [cx, cy],
                            [cx + petal_length * np.cos(angle - np.pi / 6), cy + petal_length * np.sin(angle - np.pi / 6)],
                            [cx + petal_length * np.cos(angle), cy + petal_length * np.sin(angle)],
                            [cx + petal_length * np.cos(angle + np.pi / 6), cy + petal_length * np.sin(angle + np.pi / 6)]
                        ], np.int32)
                        petal_points = petal_points.reshape((-1, 1, 2))
                        cv2.fillPoly(frame, [petal_points], color=obj['color'])

                elif obj['shape'] == 'double_arrow_up':
                    arrow_length = int(obj['size'] / 2)
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    cv2.arrowedLine(frame, (cx, cy - arrow_length), (cx, cy), obj['color'], int(obj['size'] / 10), tipLength=0.3)
                    cv2.arrowedLine(frame, (cx, cy + arrow_length), (cx, cy), obj['color'], int(obj['size'] / 10), tipLength=0.3)

                elif obj['shape'] == 'double_arrow_down':
                    arrow_length = int(obj['size'] / 2)
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    cv2.arrowedLine(frame, (cx, cy), (cx, cy - arrow_length), obj['color'], int(obj['size'] / 10), tipLength=0.3)
                    cv2.arrowedLine(frame, (cx, cy), (cx, cy + arrow_length), obj['color'], int(obj['size'] / 10), tipLength=0.3)

                elif obj['shape'] == 'rectangle_with_triangle':
                    rect_width, rect_height = int(obj['size'] / 2), int(obj['size'] / 2)
                    rect_x, rect_y = int(obj['x']), int(obj['y'])
                    triangle_height = int(obj['size'] / 2)
                    triangle_points = np.array([
                        [rect_x, rect_y + rect_height],
                        [rect_x + rect_width, rect_y + rect_height],
                        [rect_x + rect_width / 2, rect_y + rect_height - triangle_height]
                    ], np.int32)
                    triangle_points = triangle_points.reshape((-1, 1, 2))
                    cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), obj['color'], -1)
                    cv2.fillPoly(frame, [triangle_points], color=obj['color'])

                elif obj['shape'] == 'plus':
                    plus_length = int(obj['size'] / 2)
                    cx, cy = int(obj['x'] + obj['size'] / 2), int(obj['y'] + obj['size'] / 2)
                    cv2.rectangle(frame, (cx - int(plus_length / 5), cy - int(plus_length / 2)), (cx + int(plus_length / 5), cy + int(plus_length / 2)), obj['color'], -1)
                    cv2.rectangle(frame, (cx - int(plus_length / 2), cy - int(plus_length / 5)), (cx + int(plus_length / 2), cy + int(plus_length / 5)), obj['color'], -1)

                elif obj['shape'] == 'hourglass':
                    hourglass_width, hourglass_height = int(obj['size'] / 4), int(obj['size'] / 2)
                    hourglass_x, hourglass_y = int(obj['x']), int(obj['y'])
                    top_triangle_points = np.array([
                        [hourglass_x, hourglass_y],
                        [hourglass_x + hourglass_width, hourglass_y],
                        [hourglass_x + hourglass_width / 2, hourglass_y + hourglass_height / 2]
                    ], np.int32)
                    bottom_triangle_points = np.array([
                        [hourglass_x, hourglass_y + hourglass_height],
                        [hourglass_x + hourglass_width, hourglass_y + hourglass_height],
                        [hourglass_x + hourglass_width / 2, hourglass_y + hourglass_height / 2]
                    ], np.int32)
                    top_triangle_points = top_triangle_points.reshape((-1, 1, 2))
                    bottom_triangle_points = bottom_triangle_points.reshape((-1, 1, 2))
                    cv2.fillPoly(frame, [top_triangle_points, bottom_triangle_points], color=obj['color'])
               
                elif obj['shape'] == 'butterfly_curve':
                    # Butterfly curve parametric equations
                    t = np.linspace(0, 12 * np.pi, 1000)
                    x = np.sin(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t) - np.sin(t / 12)**5)
                    y = np.cos(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t) - np.sin(t / 12)**5)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'elkies_trinomial_curve':
                    # Example of Elkies trinomial curve
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    b = 3
                    x = a * np.sin(t)
                    y = b * np.cos(t) * np.sin(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'hyperelliptic_curve':
                    # Example of a hyperelliptic curve
                    t = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
                    a = 2
                    b = 3
                    x = a * np.sin(t)
                    y = b * np.cos(t) * np.sin(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))
                    
                elif obj['shape'] == 'polynomial_lemniscate':
                    # Polynomial lemniscate parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    b = 1
                    x = (a * np.cos(t)) / (1 + b * np.sin(t)**2)
                    y = (a * np.sin(t) * np.cos(t)) / (1 + b * np.sin(t)**2)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'fermat_curve':
                    # Fermat curve parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * np.cos(t)
                    y = a * np.sin(t) * np.sin(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'sinusoidal_spiral':
                    # Sinusoidal spiral parametric equations
                    t = np.linspace(0, 6 * np.pi, 1000)
                    a = 5
                    b = 0.2
                    x = a * np.cos(t) * np.sin(b * t)
                    y = a * np.sin(t) * np.sin(b * t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'superellipse':
                    # Superellipse parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    b = 1
                    n = 4
                    x = a * np.sign(np.cos(t)) * np.abs(np.cos(t))**(2/n)
                    y = b * np.sign(np.sin(t)) * np.abs(np.sin(t))**(2/n)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'hurwitz_surface':
                    # Example of a Hurwitz surface (parametric equations are just an example, replace with actual equations)
                    u = np.linspace(-2, 2, 100)
                    v = np.linspace(-2, 2, 100)
                    u, v = np.meshgrid(u, v)
                    x = u
                    y = v
                    z = u**2 + v**2

                    # Scale and translate the surface
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']
                    z = (z * obj['size'] / 10) + obj['size'] / 2

                    # Draw the surface on the frame
                    curve_points = np.array(list(zip(x.flatten().astype(int), y.flatten().astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'bowditch_curve':
                    # Bowditch curve parametric equations
                    t = np.linspace(0, 4 * np.pi, 1000)
                    a = 2
                    b = 1
                    x = (a + b) * np.cos(t) - b * np.cos((a/b + 1) * t)
                    y = (a + b) * np.sin(t) - b * np.sin((a/b + 1) * t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'brachistochrone':
                    # Brachistochrone curve parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * (t - np.sin(t))
                    y = a * (1 - np.cos(t))

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'catenary':
                    # Catenary curve parametric equations
                    t = np.linspace(-2, 2, 1000)
                    a = 1
                    x = a * np.cosh(t)
                    y = a * np.sinh(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'clelies':
                    # Clélies curve parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * np.cos(t) * np.cos(t) * np.cos(t)
                    y = a * np.sin(t) * np.sin(t) * np.sin(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'cochleoid':
                    # Cochleoid curve parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * (t - np.sin(t))
                    y = a * (1 - np.cos(t))

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'cycloid':
                    # Cycloid curve parametric equations
                    t = np.linspace(0, 4 * np.pi, 1000)
                    a = 1
                    x = a * (t - np.sin(t))
                    y = a * (1 - np.cos(t))

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'horopter':
                    # Example of a Horopter curve (parametric equations are just an example, replace with actual equations)
                    u = np.linspace(-2, 2, 100)
                    v = np.linspace(-2, 2, 100)
                    u, v = np.meshgrid(u, v)
                    x = u
                    y = v
                    z = u**2 + v**2

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']
                    z = (z * obj['size'] / 10) + obj['size'] / 2

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.flatten().astype(int), y.flatten().astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'bowditch_curve':
                    # Bowditch curve parametric equations
                    t = np.linspace(0, 4 * np.pi, 1000)
                    a = 2
                    b = 1
                    x = (a + b) * np.cos(t) - b * np.cos((a/b + 1) * t)
                    y = (a + b) * np.sin(t) - b * np.sin((a/b + 1) * t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'brachistochrone':
                    # Brachistochrone curve parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * (t - np.sin(t))
                    y = a * (1 - np.cos(t))

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))
                    
                elif obj['shape'] == 'epicycloid':
                    # Epicycloid parametric equations
                    t = np.linspace(0, 4 * np.pi, 1000)
                    a = 2
                    b = 1
                    x = (a + b) * np.cos(t) - b * np.cos((a/b + 1) * t)
                    y = (a + b) * np.sin(t) - b * np.sin((a/b + 1) * t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'hypocycloid':
                    # Hypocycloid parametric equations
                    t = np.linspace(0, 4 * np.pi, 1000)
                    a = 2
                    b = 1
                    x = (a - b) * np.cos(t) + b * np.cos((a/b - 1) * t)
                    y = (a - b) * np.sin(t) - b * np.sin((a/b - 1) * t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'astroid':
                    # Astroid parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * np.cos(t)**3
                    y = a * np.sin(t)**3

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'lissajous_curve':
                    # Lissajous curve parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    b = 3
                    x = a * np.sin(3 * t)
                    y = b * np.sin(2 * t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'cardioid':
                    # Cardioid parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * (1 - np.cos(t)) * np.cos(t)
                    y = a * (1 - np.cos(t)) * np.sin(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))


                elif obj['shape'] == 'catenary':
                    # Catenary curve parametric equations
                    t = np.linspace(-2, 2, 1000)
                    a = 1
                    x = a * np.cosh(t)
                    y = a * np.sinh(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'clelies':
                    # Clélies curve parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * np.cos(t) * np.cos(t) * np.cos(t)
                    y = a * np.sin(t) * np.sin(t) * np.sin(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'cochleoid':
                    # Cochleoid curve parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * (t - np.sin(t))
                    y = a * (1 - np.cos(t))

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'cycloid':
                    # Cycloid curve parametric equations
                    t = np.linspace(0, 4 * np.pi, 1000)
                    a = 1
                    x = a * (t - np.sin(t))
                    y = a * (1 - np.cos(t))

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'horopter':
                    # Example of a Horopter curve (parametric equations are just an example, replace with actual equations)
                    u = np.linspace(-2, 2, 100)
                    v = np.linspace(-2, 2, 100)
                    u, v = np.meshgrid(u, v)
                    x = u
                    y = v
                    z = u**2 + v**2

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']
                    z = (z * obj['size'] / 10) + obj['size'] / 2

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.flatten().astype(int), y.flatten().astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'lemniscate':
                    # Lemniscate of Bernoulli parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * np.cos(t) / (1 + np.sin(t)**2)
                    y = a * np.cos(t) * np.sin(t) / (1 + np.sin(t)**2)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'lemniscate_gerono':
                    # Lemniscate of Gerono parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * np.cos(t)
                    y = a * np.sin(t) * np.cos(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))
                    
                elif obj['shape'] == 'lemniscate_booth':
                    # Lemniscate of Booth parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * np.cos(t) / (1 + np.sin(t)**2)
                    y = a * np.sin(t) * np.cos(t) / (1 + np.sin(t)**2)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'lemniscate_booth':
                    # Lemniscate of Booth parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * np.cos(t) / (1 + np.sin(t)**2)
                    y = a * np.sin(t) * np.cos(t) / (1 + np.sin(t)**2)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'rose_curve':
                    # Rose curve parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    n = 6  # Adjust the number of petals
                    x = a * np.cos(n * t) * np.cos(t)
                    y = a * np.cos(n * t) * np.sin(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))
                    
                elif obj['shape'] == 'spiral_theodorus':
                    # Spiral of Theodorus parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 1
                    x = a * np.cos(t) * np.sqrt(t)
                    y = a * np.sin(t) * np.sqrt(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'spirograph':
                    # Spirograph parametric equations
                    t = np.linspace(0, 6 * np.pi, 1000)
                    a = 1
                    b = 0.5
                    x = (a + b) * np.cos(t) - b * np.cos((a/b + 1) * t)
                    y = (a + b) * np.sin(t) - b * np.sin((a/b + 1) * t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'torus_knot':
                    # Torus Knot parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 1
                    b = 2
                    x = (a + b * np.cos(3 * t)) * np.cos(2 * t)
                    y = (a + b * np.cos(3 * t)) * np.sin(2 * t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'deltoid_curve':
                    # Deltoid Curve parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 1
                    x = a * (2 * np.cos(t) + np.cos(2 * t))
                    y = a * (2 * np.sin(t) - np.sin(2 * t))

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'folium_of_descartes':
                    # Folium of Descartes parametric equations
                    t = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
                    a = 1
                    x = a * np.sin(t) / (1 + np.cos(t))
                    y = a * np.sin(t) * np.cos(t) / (1 + np.cos(t))

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'archimedean_spiral':
                    # Archimedean Spiral parametric equations
                    t = np.linspace(0, 4 * np.pi, 1000)
                    a = 1
                    b = 0.5
                    x = (a + b * t) * np.cos(t)
                    y = (a + b * t) * np.sin(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'fish':
                    # Fish parametric equations
                    t = np.linspace(0, 2 * np.pi, 1000)
                    a = 2
                    x = a * np.cos(t) - np.sin(t) + a * np.cos(2*t) / 2
                    y = a * np.sin(t) + np.cos(t) - a * np.sin(2*t) / 2

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the fish on the frame
                    fish_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    fish_points = fish_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [fish_points], isClosed=True, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'elephant':
                    # Elephant geometric construction
                    head_radius = obj['size'] / 4
                    body_length = obj['size'] * 2
                    leg_length = obj['size'] / 2

                    # Draw the elephant on the frame
                    head_center = (obj['x'], obj['y'] - head_radius)
                    body_top_left = (obj['x'] - obj['size'], obj['y'])
                    body_bottom_left = (obj['x'] - obj['size'], obj['y'] + body_length)
                    body_top_right = (obj['x'] + obj['size'], obj['y'])
                    body_bottom_right = (obj['x'] + obj['size'], obj['y'] + body_length)
                    leg_top_left = (obj['x'] - obj['size'] / 2, obj['y'] + body_length)
                    leg_bottom_left = (obj['x'] - obj['size'] / 2, obj['y'] + body_length + leg_length)
                    leg_top_right = (obj['x'] + obj['size'] / 2, obj['y'] + body_length)
                    leg_bottom_right = (obj['x'] + obj['size'] / 2, obj['y'] + body_length + leg_length)

                    cv2.circle(frame, (int(head_center[0]), int(head_center[1])), int(head_radius), obj['color'], -1)
                    cv2.rectangle(frame, (int(body_top_left[0]), int(body_top_left[1])),
                                  (int(body_bottom_right[0]), int(body_bottom_right[1])), obj['color'], -1)
                    cv2.rectangle(frame, (int(leg_top_left[0]), int(leg_top_left[1])),
                                  (int(leg_bottom_right[0]), int(leg_bottom_right[1])), obj['color'], -1)

                elif obj['shape'] == 'butterfly':
                    # Butterfly geometric construction
                    wing_length = obj['size'] * 2
                    body_length = obj['size'] / 2

                    # Draw the butterfly on the frame
                    wing_top_left = (obj['x'] - wing_length / 2, obj['y'])
                    wing_bottom_left = (obj['x'] - wing_length / 2, obj['y'] + wing_length)
                    wing_top_right = (obj['x'] + wing_length / 2, obj['y'])
                    wing_bottom_right = (obj['x'] + wing_length / 2, obj['y'] + wing_length)
                    body_top_left = (obj['x'] - obj['size'] / 4, obj['y'] + wing_length / 2 - body_length / 2)
                    body_bottom_left = (obj['x'] - obj['size'] / 4, obj['y'] + wing_length / 2 + body_length / 2)
                    body_top_right = (obj['x'] + obj['size'] / 4, obj['y'] + wing_length / 2 - body_length / 2)
                    body_bottom_right = (obj['x'] + obj['size'] / 4, obj['y'] + wing_length / 2 + body_length / 2)

                    cv2.rectangle(frame, (int(wing_top_left[0]), int(wing_top_left[1])),
                                  (int(wing_bottom_right[0]), int(wing_bottom_right[1])), obj['color'], -1)
                    cv2.rectangle(frame, (int(body_top_left[0]), int(body_top_left[1])),
                                  (int(body_bottom_right[0]), int(body_bottom_right[1])), obj['color'], -1)

                elif obj['shape'] == 'turtle':
                    # Turtle geometric construction
                    body_length = obj['size'] * 2
                    head_radius = obj['size'] / 4
                    leg_length = obj['size'] / 3

                    # Draw the turtle on the frame
                    body_top_left = (obj['x'] - obj['size'], obj['y'])
                    body_bottom_left = (obj['x'] - obj['size'], obj['y'] + body_length)
                    body_top_right = (obj['x'] + obj['size'], obj['y'])
                    body_bottom_right = (obj['x'] + obj['size'], obj['y'] + body_length)
                    head_center = (obj['x'], obj['y'] - head_radius)
                    leg_top_left = (obj['x'] - obj['size'] / 2, obj['y'] + body_length)
                    leg_bottom_left = (obj['x'] - obj['size'] / 2, obj['y'] + body_length + leg_length)
                    leg_top_right = (obj['x'] + obj['size'] / 2, obj['y'] + body_length)
                    leg_bottom_right = (obj['x'] + obj['size'] / 2, obj['y'] + body_length + leg_length)

                    cv2.circle(frame, (int(head_center[0]), int(head_center[1])), int(head_radius), obj['color'], -1)
                    cv2.rectangle(frame, (int(body_top_left[0]), int(body_top_left[1])),
                                  (int(body_bottom_right[0]), int(body_bottom_right[1])), obj['color'], -1)
                    cv2.rectangle(frame, (int(leg_top_left[0]), int(leg_top_left[1])),
                                  (int(leg_bottom_right[0]), int(leg_bottom_right[1])), obj['color'], -1)

                elif obj['shape'] == 'duck':
                    # Duck geometric construction
                    body_length = obj['size'] * 2
                    head_radius = obj['size'] / 3
                    beak_length = obj['size'] / 4

                    # Draw the duck on the frame
                    body_top_left = (obj['x'] - obj['size'], obj['y'])
                    body_bottom_left = (obj['x'] - obj['size'], obj['y'] + body_length)
                    body_top_right = (obj['x'] + obj['size'], obj['y'])
                    body_bottom_right = (obj['x'] + obj['size'], obj['y'] + body_length)
                    head_center = (obj['x'] + head_radius, obj['y'] - head_radius)
                    beak_top = (obj['x'] + head_radius, obj['y'] - head_radius)
                    beak_bottom = (obj['x'] + head_radius + beak_length, obj['y'] - head_radius + beak_length)

                    cv2.circle(frame, (int(head_center[0]), int(head_center[1])), int(head_radius), obj['color'], -1)
                    cv2.rectangle(frame, (int(body_top_left[0]), int(body_top_left[1])),
                                  (int(body_bottom_right[0]), int(body_bottom_right[1])), obj['color'], -1)
                    cv2.line(frame, (int(beak_top[0]), int(beak_top[1])), (int(beak_bottom[0]), int(beak_bottom[1])), obj['color'], int(obj['size'] / 20))

                elif obj['shape'] == 'watts_curve':
                    # Watt's Curve parametric equations
                    t = np.linspace(0, 4 * np.pi, 1000)
                    a = 1
                    b = 0.5
                    x = a * np.cos(b * t) + np.cos(t)
                    y = a * np.sin(b * t) - np.sin(t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'quadratic_bezier_curve':
                    # Quadratic Bézier Curve control points
                    p0 = np.array([obj['x'], obj['y']])
                    p1 = np.array([obj['x'] + obj['size'] / 2, obj['y'] + obj['size']])
                    p2 = np.array([obj['x'] + obj['size'], obj['y']])

                    # Compute Bézier Curve points
                    t = np.linspace(0, 1, 1000)
                    x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
                    y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'cubic_bezier_curve':
                    # Cubic Bézier Curve control points
                    p0 = np.array([obj['x'], obj['y']])
                    p1 = np.array([obj['x'] + obj['size'] / 3, obj['y'] + obj['size']])
                    p2 = np.array([obj['x'] + 2 * obj['size'] / 3, obj['y']])
                    p3 = np.array([obj['x'] + obj['size'], obj['y'] + obj['size']])

                    # Compute Bézier Curve points
                    t = np.linspace(0, 1, 1000)
                    x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
                    y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'sine_wave':
                    # Sine Wave parametric equations
                    t = np.linspace(0, 4 * np.pi, 1000)
                    a = 1
                    b = 0.5
                    x = t
                    y = a * np.sin(b * t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))

                elif obj['shape'] == 'trefoil_knot':
                    # Trefoil Knot parametric equations
                    t = np.linspace(0, 4 * np.pi, 1000)
                    a = 1
                    x = (a + np.sin(t)) * np.cos(2 * t)
                    y = (a + np.sin(t)) * np.sin(2 * t)

                    # Scale and translate the curve
                    x = (x * obj['size'] / 10) + obj['x']
                    y = (y * obj['size'] / 10) + obj['y']

                    # Draw the curve on the frame
                    curve_points = np.array(list(zip(x.astype(int), y.astype(int))), np.int32)
                    curve_points = curve_points.reshape((-1, 1, 2))
                    cv2.polylines(frame, [curve_points], isClosed=False, color=obj['color'], thickness=int(obj['size'] / 20))


                # Update object position with more random velocity
                obj['x'] += obj['vx'] + random.uniform(-2, 2)
                obj['y'] += obj['vy'] + random.uniform(-2, 2)

                # Bounce off the walls
                if obj['x'] < 0 or obj['x'] > resolution[0] - obj['size']:
                    obj['vx'] *= -1
                if obj['y'] < 0 or obj['y'] > resolution[1] - obj['size']:
                    obj['vy'] *= -1

            # Write the frame to the video
            video_writer.write(frame)

        # Release the video writer
        video_writer.release()

        print(f"Video {output_path} generated and saved.")

if __name__ == "__main__":
    num_videos_to_generate = int(input("Enter the number of videos to generate: "))
    create_video(num_videos=num_videos_to_generate, aspect_ratio=(9, 16))
