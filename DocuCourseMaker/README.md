структура 

DocuCourseMaker/
├── main.py
├── README.md
├── requirements.txt
├── resources/
│   └── icons/
│         ├── icon.jpeg
│         └── Logo.png
└── src/
    ├── main_window.py       # Основной интерфейс (выше)
    ├── themes.py            # Определения тем
    ├── template_manager.py  # Функции для предпросмотра шаблонов
    ├── template_loader.py   # Функция load_template для выбора файлов шаблонов
    ├── date_picker.py       # Класс DatePicker (виджет с календарём)
    ├── institutes.py        # Словарь институтов и кафедр
    ├── animated_button.py   # Класс AnimatedButton
    ├── about_dialog.py      # Диалог "О программе"
    ├── input_panel.py       # Панель "Входные данные"
    └── templates_panel.py   # Панель "Шаблоны документов" (с колбэками)