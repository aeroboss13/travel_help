import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import webbrowser
from ttkthemes import ThemedTk

# Создаем окно приложения с использованием темы
app = ThemedTk(theme="radiance")
app.title("Путешествия")
app.geometry("800x600")

# Переменная для отслеживания текущей темы
current_theme = "radiance"

# База данных для хранения пользователей (просто для примера)
users = {'user1': 'password1', 'user2': 'password2'}

# Создаем словарь с рекомендациями по безопасности для различных стран
safety_recommendations = {
    'Страна 1': "Рекомендации для Страны 1:\n"
                "- Поддерживайте местные законы и обычаи.\n"
                "- Обратите внимание на погодные условия и сезонные опасности.",
    'Страна 2': "Рекомендации для Страны 2:\n"
                "- Изучите местный язык и обычаи, чтобы лучше взаимодействовать с местными жителями.\n"
                "- Пользуйтесь официальными такси и избегайте неофициальных перевозчиков.",
    'Страна 3': "Рекомендации для Страны 3:\n"
                "- Перед поездкой уточните информацию о местной медицинской помощи и вакцинациях.\n"
                "- Соблюдайте осторожность при посещении отдаленных мест и предупреждайте кого-то о вашем маршруте."
}


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
            users[username] = password
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
        if username in users and users[username] == password:
            login_window.destroy()
            messagebox.showinfo("Авторизация", "Вход выполнен успешно")
        else:
            messagebox.showerror("Ошибка", "Неправильный логин или пароль")

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

    chat_entry = tk.Text(chat_window, height=3)
    chat_entry.pack()

    send_button = ttk.Button(chat_window, text="Отправить", command=send_message)
    send_button.pack()


def get_safety_recommendations():
    safety_window = tk.Toplevel(app)
    safety_window.title("Рекомендации по безопасности")
    safety_window.geometry("400x400")

    safety_label = tk.Label(safety_window, text="Выберите страну и получите рекомендации по безопасности:")
    safety_label.pack()

    countries = ['Страна 1', 'Страна 2', 'Страна 3']  # Пример списка стран

    country_var = tk.StringVar()
    country_var.set(countries[0])

    country_dropdown = ttk.Combobox(safety_window, textvariable=country_var, values=countries)
    country_dropdown.pack()

    safety_text = tk.Text(safety_window, wrap=tk.WORD)
    safety_text.pack()

    def show_recommendations():
        selected_country = country_var.get()
        recommendations = safety_recommendations.get(selected_country, "Рекомендации отсутствуют")
        safety_text.config(state="normal")
        safety_text.delete("1.0", "end")
        safety_text.insert("end", recommendations)
        safety_text.config(state="disabled")

    show_button = ttk.Button(safety_window, text="Получить рекомендации", command=show_recommendations)
    show_button.pack()


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
theme_toggle_button.pack(side="top")

tab_control.pack(expand=1, fill="both")

app.mainloop()
