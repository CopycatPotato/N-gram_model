# N-граммная языковая модель

Написано для отбора на **ML by Tinkoff**

В папке **data** находятся все тексты, использованные для обучения моделей

Уже обученные модели можно скачать [**здесь**](https://drive.google.com/drive/folders/1BT2nWGqzZ8B8X_K1Gw2efIai0hPrUg3e?usp=sharing)
## generate.py

- ❗ **--model** – путь к модели, которую нужно использовать для генерации
- ❗ **--length** – длина генерируемой последовательности
- **--prefix** – кастомное начало для сгенерированного текста
- **-N** – константа для N-граммной языковой модели *(по умолчанию: 3)*

## train.py

- ❗ **--model** – путь, куда нужно сохранить обученную модель
- **--input-dir** – директория, в которой хранятся тексты для обучения (если не указано, текст берётся из *stdin*)
- **-N** – константа для N-граммной языковой модели *(по умолчанию: 3)*

❗  - обязательный аргумент