import os

def extract_preview(file_path: str) -> str:
    """
    Извлекает текстовый предпросмотр содержимого файла.
    Поддерживаются:
      - Word-документы (*.doc, *.docx): возвращаются первые 5 непустых абзацев.
      - Excel-документы (*.xls, *.xlsx): возвращаются первые 5 строк первого листа.
    Если извлечение невозможно, возвращается сообщение об ошибке.
    """
    ext = os.path.splitext(file_path)[1].lower()
    preview_content = ""
    if ext in [".docx", ".doc"]:
        try:
            from docx import Document
            document = Document(file_path)
            paras = [para.text for para in document.paragraphs if para.text.strip()]
            preview_content = "\n".join(paras[:5])
            if not preview_content:
                preview_content = "[Нет текста для отображения]"
        except Exception as e:
            preview_content = f"Ошибка при загрузке документа: {e}"
    elif ext in [".xlsx", ".xls"]:
        try:
            import pandas as pd
            df = pd.read_excel(file_path)
            preview_content = df.head(5).to_string()
        except Exception as e:
            preview_content = f"Ошибка при загрузке Excel документа: {e}"
    else:
        preview_content = "Формат файла не поддерживается для предпросмотра."
    return preview_content

def format_loaded_templates(title_file: str, assignment_file: str, excel_file: str) -> str:
    """
    Формирует HTML-разметку со списком загруженных шаблонов.
    Если файл не загружен, выводится сообщение "Не загружен".
    """
    lines = ['<h3 style="color:#333;">Загруженные шаблоны</h3>', '<ul>']
    if title_file:
        lines.append(f'<li><strong>Титульный лист:</strong> {title_file}</li>')
    else:
        lines.append('<li><strong>Титульный лист:</strong> Не загружен</li>')
    if assignment_file:
        lines.append(f'<li><strong>Лист задания:</strong> {assignment_file}</li>')
    else:
        lines.append('<li><strong>Лист задания:</strong> Не загружен</li>')
    if excel_file:
        lines.append(f'<li><strong>Excel документ:</strong> {excel_file}</li>')
    else:
        lines.append('<li><strong>Excel документ:</strong> Не загружен</li>')
    lines.append('</ul>')
    return "\n".join(lines)