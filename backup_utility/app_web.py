import streamlit as st
from pathlib import Path
import os
import backup_logic

st.set_page_config(
    page_title="Мульти-бэкап утилита",
    page_icon="💾",
    layout="centered"
)

st.title("💾 Мульти-резервное копирование")
st.markdown("Добавляйте несколько папок и упаковывайте их в единый защищенный архив.")
st.divider()

# Инициализируем список путей в памяти сайта, если его еще нет
if "source_paths" not in st.session_state:
    st.session_state.source_paths = []

# --- БЛОК 1: Добавление путей ---
st.subheader("1. Список папок для копирования")

# Форма для добавления нового пути в список
with st.form("add_path_form", clear_on_submit=True):
    # Сканируем рабочий стол для быстрого выбора
    desktop_path = Path(os.path.expanduser("~")) / "Desktop"
    available_dirs = []
    try:
        if desktop_path.exists():
            available_dirs = [d.name for d in desktop_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    except Exception:
        pass

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_folder = st.selectbox("Выбрать с Рабочего стола:", options=["-- Выберите --"] + available_dirs)
    with col2:
        st.write("") # Смещение для выравнивания
        st.write("")
        add_desktop_btn = st.form_submit_button("➕ Добавить выбранную")

    custom_path_input = st.text_input("Или введите любой абсолютный путь вручную:")
    add_custom_btn = st.form_submit_button("➕ Добавить вручную")

    # Логика обработки отправки формы
    if add_desktop_btn and selected_folder != "-- Выберите --":
        path_to_add = str(desktop_path / selected_folder)
        if path_to_add not in st.session_state.source_paths:
            st.session_state.source_paths.append(path_to_add)
            
    if add_custom_btn and custom_path_input.strip():
        path_to_add = custom_path_input.strip().replace("\\", "/")
        if path_to_add not in st.session_state.source_paths:
            st.session_state.source_paths.append(path_to_add)

# Отображение текущего списка добавленных папок
if st.session_state.source_paths:
    st.write("**Выбранные папки:**")
    for i, path in enumerate(st.session_state.source_paths):
        col_text, col_btn = st.columns([5, 1])
        col_text.code(path, language="text")
        if col_btn.button("❌", key=f"del_{i}"):
            st.session_state.source_paths.pop(i)
            st.rerun()
            
    if st.button("🗑️ Очистить весь список"):
        st.session_state.source_paths = []
        st.rerun()
else:
    st.info("Список пуст. Добавьте хотя бы одну папку выше.")

st.divider()

# --- БЛОК 2: Путь сохранения ---
st.subheader("2. Куда сохранять архивы?")
custom_backup = st.text_input(
    "Укажите путь к папке бэкапов:",
    value="",  # Оставляем поле абсолютно пустым по умолчанию
    placeholder="Пример: C:/Users/User/Desktop/all_my_safe_backups"  # Подсказка для пользователя
)
final_backup = Path(custom_backup.strip()) if custom_backup.strip() else None


# --- БЛОК 3: Настройки времени ---
st.subheader("3. Параметры очистки")
retention_days = st.slider(
    "Срок хранения старых архивов (дней):",
    min_value=1,
    max_value=30,
    value=7
)

st.divider()

# --- ЗАПУСК МУЛЬТИ-БЭКАПА ---
if st.button("🚀 ЗАПУСТИТЬ ОДНОВРЕМЕННОЕ КОПИРОВАНИЕ", type="primary", use_container_width=True):
    if not st.session_state.source_paths:
        st.error("Ошибка: Вы не добавили ни одной папки для копирования!")
    elif not final_backup:
        st.error("Ошибка: Не указан путь для сохранения бэкапов!")
    else:
        # Переводим строки в объекты Path
        source_objects = [Path(p) for p in st.session_state.source_paths]
        
        with st.spinner("Идет создание единого zip-архива для всех папок..."):
            result = backup_logic.create_multi_backup(source_objects, final_backup)
            
            if "Успех" in result:
                st.success(result)
                clean_result = backup_logic.clean_old_backups(final_backup, retention_days)
                st.info(clean_result)
                st.balloons()
            elif "Внимание" in result:
                st.warning(result)
            else:
                st.error(result)

