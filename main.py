import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import sqlite3
import socket
import threading

# Import ThemedTk from ttkthemes
from ttkthemes import ThemedTk

# Create the main application window using the themed theme
app = ThemedTk(theme="radiance")
app.title("Путешествия")
app.geometry("800x600")

# Variable to track the current theme
current_theme = "radiance"

# Create a connection to the SQLite database
db_connection = sqlite3.connect("travel_app.db")
db_cursor = db_connection.cursor()

# Create a table for safety recommendations if it doesn't exist
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS safety_recommendations (
        country TEXT PRIMARY KEY,
        recommendations TEXT
    )
''')

# Create a table for users if it doesn't exist
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')

# Create a table for chat messages
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY,
        sender TEXT,
        message TEXT
    )
''')

# Create a socket for chat
chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_socket.connect(("localhost", 8000))

# Rest of your code...



# Функция для добавления пользователя в базу данных
def add_user_to_db(username, password):
    db_cursor.execute('INSERT OR REPLACE INTO users (username, password) VALUES (?, ?)', (username, password))
    db_connection.commit()


# Функция для проверки учетных данных пользователя
def check_user_credentials(username, password):
    db_cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = db_cursor.fetchone()
    return result[0] if result and result[0] == password else None


# Функция для добавления сообщения в чат
def add_message_to_db(sender, message):
    db_cursor.execute('INSERT INTO chat_messages (sender, message) VALUES (?, ?)', (sender, message))
    db_connection.commit()


# Функция для получения сообщений из чата
def get_chat_messages_from_db():
    db_cursor.execute('SELECT sender, message FROM chat_messages')
    messages = db_cursor.fetchall()
    return messages


# Функция для очистки чата
def clear_chat():
    db_cursor.execute('DELETE FROM chat_messages')
    db_connection.commit()


# Определение функций для функциональности приложения
def register_user():
    registration_window = tk.Toplevel(app)
    registration_window.title("Регистрация")
    registration_window.geometry("400x200")

    registration_label = tk.Label(registration_window, text="Введите данные для регистрации:")
    registration_label.pack()

    username_label = tk.Label(registration_window, text="Логин:")
    username_label.pack()
    username_entry = tk.Entry(registration_window)
    username_entry.pack()

    password_label = tk.Label(registration_window, text="Пароль:")
    password_label.pack()
    password_entry = tk.Entry(registration_window, show='*')
    password_entry.pack()

    def register():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            add_user_to_db(username, password)
            registration_window.destroy()
            messagebox.showinfo("Регистрация", "Пользователь зарегистрирован")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

    register_button = ttk.Button(registration_window, text="Зарегистрироваться", command=register)
    register_button.pack()


def login_user():
    login_window = tk.Toplevel(app)
    login_window.title("Авторизация")
    login_window.geometry("400x150")

    login_label = tk.Label(login_window, text="Введите данные для входа:")
    login_label.pack()

    username_label = tk.Label(login_window, text="Логин:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Пароль:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack()

    def authenticate():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            if check_user_credentials(username, password):
                login_window.destroy()
                messagebox.showinfo("Авторизация", "Вход выполнен успешно")
            else:
                messagebox.showerror("Ошибка", "Неправильный логин или пароль")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

    login_button = ttk.Button(login_window, text="Войти", command=authenticate)
    login_button.pack()


def open_travel_chat():
    chat_window = tk.Toplevel(app)
    chat_window.title("Чат путешественников")
    chat_window.geometry("600x400")

    chat_label = tk.Label(chat_window, text="Чат путешественников")
    chat_label.pack()

    chat_text = tk.Text(chat_window)
    chat_text.pack()

    def send_message():
        message = chat_entry.get("1.0", "end-1c")
        chat_text.insert("end", "Вы: " + message + "\n")
        chat_text.see("end")
        chat_entry.delete("1.0", "end")
        # Отправляем сообщение через сокс
        chat_socket.send(message.encode())

    chat_entry = tk.Text(chat_window, height=3)
    chat_entry.pack()

    send_button = ttk.Button(chat_window, text="Отправить", command=send_message)
    send_button.pack()

    def update_chat():
        while True:
            message = chat_socket.recv(1024).decode()
            chat_text.insert("end", "Собеседник: " + message + "\n")
            chat_text.see("end")

    chat_thread = threading.Thread(target=update_chat)
    chat_thread.daemon = True
    chat_thread.start()


def get_safety_recommendations_from_db(country):
    db_cursor.execute('SELECT recommendations FROM safety_recommendations WHERE country = ?', (country,))
    result = db_cursor.fetchone()
    return result[0] if result else "Нет данных о рекомендациях по безопасности для выбранной страны"


def get_safety_recommendations():
    safety_window = tk.Toplevel(app)
    safety_window.title("Рекомендации по безопасности")
    safety_window.geometry("400x400")

    safety_label = tk.Label(safety_window, text="Выберите страну и получите рекомендации по безопасности:")
    safety_label.pack()

    # Запрос всех доступных стран из базы данных
    db_cursor.execute('SELECT country FROM safety_recommendations')
    countries = [row[0] for row in db_cursor.fetchall()]

    country_var = tk.StringVar()
    country_var.set(countries[0] if countries else "")

    if countries:
        country_dropdown = ttk.Combobox(safety_window, textvariable=country_var, values=countries)
        country_dropdown.pack()

        safety_text = tk.Text(safety_window, wrap=tk.WORD)
        safety_text.pack()

        def show_recommendations():
            selected_country = country_var.get()
            recommendations = get_safety_recommendations_from_db(selected_country)
            safety_text.config(state="normal")
            safety_text.delete("1.0", "end")
            safety_text.insert("end", recommendations)
            safety_text.config(state="disabled")

        show_button = ttk.Button(safety_window, text="Получить рекомендации", command=show_recommendations)
        show_button.pack()
    else:
        no_data_label = tk.Label(safety_window, text="Нет данных о рекомендациях по безопасности")
        no_data_label.pack()


def open_virtual_tours():
    webbrowser.open("https://www.airpano.ru/list-all-virtual-tours.php")


def toggle_theme():
    global current_theme
    if current_theme == "radiance":
        app.set_theme("black")
        current_theme = "black"
    else:
        app.set_theme("radiance")
        current_theme = "radiance"


# Добавляем изображение для дизайна
image = Image.open("background.jpg")
background_image = ImageTk.PhotoImage(image)
background_label = tk.Label(app, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Вкладки для различных функций
tab_control = ttk.Notebook(app)

# Вкладка регистрации и авторизации
registration_tab = ttk.Frame(tab_control)
tab_control.add(registration_tab, text="Регистрация и авторизация")

register_button = ttk.Button(registration_tab, text="Зарегистрироваться", command=register_user)
register_button.pack()

login_button = ttk.Button(registration_tab, text="Войти", command=login_user)
login_button.pack()

# Вкладка чата путешественников
chat_tab = ttk.Frame(tab_control)
tab_control.add(chat_tab, text="Чат путешественников")

chat_button = ttk.Button(chat_tab, text="Открыть чат", command=open_travel_chat)
chat_button.pack()

# Вкладка рекомендаций по безопасности
safety_recommendations_tab = ttk.Frame(tab_control)
tab_control.add(safety_recommendations_tab, text="Рекомендации по безопасности")

recommend_button = ttk.Button(safety_recommendations_tab, text="Получить рекомендации",
                              command=get_safety_recommendations)
recommend_button.pack()

# Вкладка "ВИРТУАЛЬНЫЕ ТУРЫ"
virtual_tours_tab = ttk.Frame(tab_control)
tab_control.add(virtual_tours_tab, text="ВИРТУАЛЬНЫЕ ТУРЫ")

virtual_tours_button = ttk.Button(virtual_tours_tab, text="Открыть виртуальные туры", command=open_virtual_tours)
virtual_tours_button.pack()

# Виджет-ползунок для переключения темы
theme_toggle_button = ttk.Button(app, text="Сменить тему", command=toggle_theme)
theme_toggle_button.pack()

# Добавляем изображение на вкладки
image_path = "travel_image.jpg"  # Замените на путь к изображению
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)

image_label_1 = tk.Label(registration_tab, image=photo)
image_label_1.image = photo
image_label_1.pack()

image_label_2 = tk.Label(chat_tab, image=photo)
image_label_2.image = photo
image_label_2.pack()

image_label_3 = tk.Label(safety_recommendations_tab, image=photo)
image_label_3.image = photo
image_label_3.pack()

image_label_4 = tk.Label(virtual_tours_tab, image=photo)
image_label_4.image = photo
image_label_4.pack()

tab_control.pack(expand=1, fill="both")

app.mainloop()

# Закрываем соединение с базой данных при выходе из приложения
db_connection.close()
