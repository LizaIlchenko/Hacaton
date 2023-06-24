import cv2
import numpy as np
import os
import pandas as pd

# Параметры видео
video_path = 'vidosic.mp4'  # Путь к видеофайлу
output_folder = 'vidtr/folder'  # Папка для сохранения срезов видео
label_file = 'vidlabels.csv'  # Файл для сохранения меток

# Параметры разметки
classes = ['грузовой автомобиль', 'трактор', 'экскаватор', 'подъёмный кран']  # Список классов техники
frame_rate = 30  # Частота кадров видео (кадров в секунду)
event_threshold = 0.5  # Пороговое значение для определения наличия техники

# Загрузка видео
cap = cv2.VideoCapture(video_path)

# Проверка успешной загрузки видео
if not cap.isOpened():
    raise ValueError("Не удалось загрузить видео!")

# Получение общего количества кадров в видео
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Создание пустого DataFrame для хранения меток
labels_df = pd.DataFrame(columns=['frame', 'class', 'start_time', 'end_time'])

# Инициализация переменных
current_event_start = None
current_event_class = None

# Перебор кадров видео
for frame_index in range(total_frames):
    # Чтение кадра
    ret, frame = cap.read()
    
    # Обработка кадра (детекция техники и определение класса)
    # <Ваш код для обработки кадра и определения класса техники>
    
    # Проверка наличия техники выше порогового значения
    if detection_confidence > event_threshold:
        # Если уже идет событие
        if current_event_start is not None:
            current_event_end = frame_index / frame_rate
        else:
            current_event_start = frame_index / frame_rate
            current_event_class = detected_class
    else:
        # Если событие завершилось
        if current_event_start is not None:
            current_event_end = frame_index / frame_rate
            
            # Добавление метки в DataFrame
            labels_df = labels_df.append({
                'frame': frame_index,
                'class': current_event_class,
                'start_time': current_event_start,
                'end_time': current_event_end
            }, ignore_index=True)
            
            # Сброс текущего события
            current_event_start = None
            current_event_class = None

# Закрытие видеофайла
cap.release()

# Сохранение DataFrame с метками в CSV файл
labels_df.to_csv(label_file, index=False)

# Создание папки для сохранения срезов видео
os.makedirs(output_folder, exist_ok=True)

# Загрузка видео снова для сохранения срезов
cap = cv2.VideoCapture(video_path)

# Перебор кадров для сохранения срезов видео
for index, row in labels_df.iterrows():
    frame_index = int(row['frame'])
    start_time = row['start_time']
    end_time = row['end_time']
    
    # Установка текущий кадр
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    
    # Чтение текущего кадра
    ret, frame = cap.read()
    
    # Сохранение среза видео
    output_path = os.path.join(output_folder, f"frame_{frame_index}.jpg")
    cv2.imwrite(output_path, frame)

# Закрытие видеофайла
cap.release()

print("Датасет и метки успешно созданы!")
