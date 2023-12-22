import cv2
import numpy as np
import random
import uuid

def random_color():
    return tuple(random.randint(0, 255) for _ in range(3))

def random_shape():
    shapes = ['rectangle', 'circle', 'triangle', 'ellipse', 'pentagon', 'hexagon', 'star', 'parallelogram', 'diamond', 'trapezoid', 'octagon', 'cross', 'arrow']
    return random.choice(shapes)

def create_video(num_videos=1, duration=10, frame_rate=30, resolution=(640, 640), aspect_ratio=(1, 1)):
    for _ in range(num_videos):
        # Adjust resolution based on aspect ratio
        resolution = (resolution[0], int(resolution[0] * aspect_ratio[1] / aspect_ratio[0]))

        # Video properties
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = f"v/{str(uuid.uuid4())}.mp4"
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
