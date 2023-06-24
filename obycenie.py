import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms
from dataset import CustomDataset
from model import YOLO

# Параметры обучения
batch_size = 8
num_epochs = 10
learning_rate = 0.001
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Предварительная обработка данных
transform = transforms.Compose([
    transforms.ToTensor()
])

# Загрузка датасета
dataset = CustomDataset(data_path='path/to/output/folder', label_path='path/to/labels.csv', transform=transform)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Инициализация модели YOLO
model = YOLO(num_classes=4).to(device)

# Определение оптимизатора и функции потерь
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
criterion = ...  # Определите функцию потерь, например, nn.MSELoss() или nn.CrossEntropyLoss()

# Обучение модели
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    
    for images, targets in dataloader:
        images = images.to(device)
        targets = targets.to(device)
        
        optimizer.zero_grad()
        
        # Получение предсказаний модели
        predictions = model(images)
        
        # Расчет функции потерь
        loss = criterion(predictions, targets)
        
        # Обратное распространение и оптимизация
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    epoch_loss = running_loss / len(dataloader)
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss}")
    
# Сохранение обученной модели
torch.save(model.state_dict(), 'path/to/save/model.pt')

print("Обучение завершено!")
