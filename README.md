Структура

DocuCourseMaker/
├── design/
│   └── mockups/
├── main.py
├── README.md
├── requirements.txt
├── resources/
│   └── icons/
│         ├── icon.jpeg
│         └── Logo.png
├── styles/
│   └── app_style.qss
└── src/
    ├── preview/                         # Если у вас там хранятся вспомогательные файлы предпросмотра
    ├── about_dialog.py                  # Диалог "О программе"
    ├── animated_button.py               # Класс AnimatedButton
    ├── date_picker.py                   # Класс DatePicker (виджет с календарём)
    ├── document_generator.py            # (опционально) Генерация документов
    ├── institutes.py                    # Словарь институтов и кафедр
    ├── input_panel.py                   # Панель "Входные данные"
    ├── main_window.py                   # Основной интерфейс
    ├── template_loader.py               # Функция load_template для выбора файлов шаблонов
    ├── template_manager.py              # Функции для предпросмотра шаблонов
    └── templates_panel.py               # Панель "Шаблоны документов" (с колбэками)
