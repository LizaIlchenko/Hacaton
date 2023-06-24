import cv2
import pandas as pd

# Параметры видео
video_path = 'path/to/video.mp4'  # Путь к видеофайлу
output_file = 'path/to/output.csv'  # Файл для сохранения разметки

# Параметры разметки
classes = ['грузовой автомобиль', 'трактор', 'экскаватор', 'подъёмный кран']  # Список классов техники

# Загрузка видео
cap = cv2.VideoCapture(video_path)

# Проверка успешной загрузки видео
if not cap.isOpened():
    raise ValueError("Не удалось загрузить видео!")

# Получение общего количества кадров в видео
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Создание пустого DataFrame для хранения разметки
columns = ['frame', 'class', 'id', 'x_min', 'y_min', 'x_max', 'y_max']
labels_df = pd.DataFrame(columns=columns)

# Инициализация переменных
object_id = 1
current_objects = {}

# Перебор кадров видео
for frame_index in range(total_frames):
    # Чтение кадра
    ret, frame = cap.read()
    
    # Обработка кадра (детекция и классификация объектов)
    # <Ваш код для обработки кадра и определения класса объектов>
    
    # Проход по всем обнаруженным объектам на текущем кадре
    for detected_object in detected_objects:
        class_id = detected_object['class_id']
        class_name = classes[class_id]
        x_min, y_min, x_max, y_max = detected_object['bbox']
        
        # Проверка, если объект уже присутствует в текущих объектах
        if class_id in current_objects:
            # Обновление координаты выхода объекта
            current_objects[class_id]['x_max'] = x_max
            current_objects[class_id]['y_max'] = y_max
        else:
            # Добавление нового объекта
            current_objects[class_id] = {
                'frame': frame_index,
                'class': class_name,
                'id': object_id,
                'x_min': x_min,
                'y_min': y_min,
                'x_max': x_max,
                'y_max': y_max
            }
            object_id += 1
    
    # Удаление объектов, которые вышли из кадра
    objects_to_remove = []
    for class_id in current_objects.keys():
        if current_objects[class_id]['frame'] < frame_index:
            objects_to_remove.append(class_id)
    for class_id in objects_to_remove:
        labels_df = labels_df.append(current_objects[class_id], ignore_index=True)
        del current_objects[class_id]
    
# Сохранение разметки в CSV файл
labels_df.to_csv(output_file, index=False)

# Закрытие видеофайла
cap.release()

print("Разметка видео успешно завершена и сохранена в файл!")
