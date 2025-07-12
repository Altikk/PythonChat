import tkinter
from tkinter import ttk
import requests
from tkinter.messagebox import showerror
import sys
import json
from PIL import ImageTk, Image
import os
from typing import Optional, Dict, Any, List, Union

FILE_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(FILE_PATH)
SERVER_URL = "http://127.0.0.1:5000"

try:
    requests.get(f"{SERVER_URL}/get_message")
except:
    showerror("Нет подключения к серверу", "Сервер в данное время не активен")
    sys.exit()

class CharacterSelectMenu(tkinter.Toplevel):
    """Окно выбора персонажа для чата."""
    
    def __init__(self, master: tkinter.Tk) -> None:
        """
        Инициализирует окно выбора персонажа.
        
        Args:
            master: Родительское окно.
        """
        super().__init__(master)
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.id: Optional[int] = None

        self.button1: ttk.Button
        self.button2: ttk.Button

        self.__configure_window()
        self.__configure_images()
        self.__configure_widgets()
        self.__pack_widgets()
    
    def __configure_images(self) -> None:
        """Загружает и настраивает изображения для кнопок выбора персонажей."""
        self.button1_sprite_path = f"{DIR_PATH}\\base\\char1\\char1.jpg"
        self.button2_sprite_path = f"{DIR_PATH}\\base\\char2\\char2.jpg"

        self.button1_sprite = Image.open(self.button1_sprite_path)
        self.button2_sprite = Image.open(self.button2_sprite_path)

        self.button1_sprite = self.button1_sprite.resize((200, 200), Image.LANCZOS)
        self.button2_sprite = self.button2_sprite.resize((200, 200), Image.LANCZOS)

        self.button1_sprite = ImageTk.PhotoImage(self.button1_sprite)
        self.button2_sprite = ImageTk.PhotoImage(self.button2_sprite)

    def __configure_widgets(self) -> None:
        """Создает и настраивает виджеты окна."""
        self.button1 = ttk.Button(self, command=lambda: self.__select_char(1), image=self.button1_sprite)
        self.button2 = ttk.Button(self, command=lambda: self.__select_char(2), image=self.button2_sprite)

    def __pack_widgets(self) -> None:
        """Размещает виджеты в окне."""
        self.button1.pack()
        self.button2.pack()

    def __select_char(self, id: int) -> None:
        """
        Обрабатывает выбор персонажа.
        
        Args:
            id: ID выбранного персонажа.
        """
        self.id = id
        self.destroy()

    def __configure_window(self) -> None:
        """Настраивает параметры окна."""
        self.geometry("420x420")
        self.title("Character Menu")
        self.resizable(False, False)
        self.grab_set()

class Character(ttk.Frame):
    """Класс для отображения персонажа чата."""
    
    def __init__(self, master: ttk.Frame, id: int) -> None:
        """
        Инициализирует персонажа.
        
        Args:
            master: Родительский виджет.
            id: ID персонажа.
        """
        super().__init__(master)
        self.master = master
        self.id = id

        self.configure_character()
        self.pack_widgets()
    
    def configure_sprite(self) -> ImageTk.PhotoImage:
        """Загружает и настраивает изображение персонажа."""
        self.__sprite_path = f"{DIR_PATH}\\base\\char{self.id}\\char{self.id}.jpg"
        self.sprite = Image.open(self.__sprite_path)
        self.sprite = self.sprite.resize((320, 320), Image.LANCZOS)
        self.sprite = ImageTk.PhotoImage(self.sprite)
        return self.sprite
    
    def configure_character(self) -> None:
        """Настраивает виджет для отображения персонажа."""
        self.__sprite_image = self.configure_sprite()
        self.__sprite_label = ttk.Label(self, image=self.__sprite_image)
    
    def update(self) -> None:
        """Обновляет изображение персонажа."""
        self.__sprite_image = self.configure_sprite()
        self.__sprite_label.configure(image=self.__sprite_image)

    def pack_widgets(self) -> None:
        """Размещает виджеты персонажа."""
        self.__sprite_label.pack(expand=False, fill=tkinter.BOTH)
        

class Widgets(ttk.Frame):
    """Основной класс виджетов чата."""
    
    def __init__(self, master: tkinter.Tk, character_id: int) -> None:
        """
        Инициализирует виджеты чата.
        
        Args:
            master: Родительское окно.
            character_id: ID выбранного персонажа.
        """
        self.master = master
        super().__init__(master)
        self.character_id = character_id

        self.main_window: ttk.Frame
        self.widgets_frame: ttk.Frame
        self.message_frame: ttk.Frame
        self.history_frame: ttk.Frame
        self.chat_label: ttk.Label
        self.nickname_label: ttk.Label
        self.send_button: ttk.Button
        self.message_entry: ttk.Entry
        self.nickname_entry: ttk.Entry
        self.history_text: tkinter.Text
        self.character: Character
        
        self.__configure_widgets()
        self.__configure_styles()
        self.__pack_widgets()
        self.__start_updating()

    def __configure_widgets(self) -> None:
        """Создает и настраивает все виджеты чата."""
        self.main_window = ttk.Frame(self, style="MainWindowStyle.TFrame", relief=tkinter.SUNKEN)
        self.widgets_frame = ttk.Frame(self)
        self.message_frame = ttk.Frame(self.main_window, relief=tkinter.RIDGE)
        self.history_frame = ttk.Frame(self.main_window, relief=tkinter.SOLID)
        self.character = Character(self.main_window, self.character_id)
        self.chat_label = ttk.Label(self.message_frame, text=self.__get_message())
        self.message_entry = ttk.Entry(self.widgets_frame, width=50)
        self.send_button = ttk.Button(self.widgets_frame, text="Send", command=lambda: self.__send_message(f"{self.nickname_entry.get()} : {self.message_entry.get()}"))
        self.nickname_label = ttk.Label(self.widgets_frame, text="Showname:")
        self.nickname_entry = ttk.Entry(self.widgets_frame)
        self.history_text = tkinter.Text(self.history_frame, state="disabled", width=0, wrap="word")

        self.master.bind("<KeyPress-Return>", lambda event: self.__send_message(f"{self.nickname_entry.get()}: {self.message_entry.get()}"))

    def __configure_styles(self) -> None:
        """Настраивает стили виджетов."""
        styleobject = ttk.Style()
        styleobject.theme_use("classic")
        styleobject.configure("MainWindowStyle.TFrame", background="#AD9292")

    def __pack_widgets(self) -> None:
        """Размещает виджеты в окне."""
        self.main_window.pack(expand=True, fill=tkinter.BOTH)
        self.history_frame.pack(expand=False, side=tkinter.LEFT, fill=tkinter.BOTH, ipadx=110)
        self.history_text.pack(expand=True, fill=tkinter.BOTH)
        self.message_frame.pack(expand=True, side=tkinter.LEFT, fill=tkinter.BOTH, pady=(370, 0))
        self.chat_label.pack(side=tkinter.LEFT, padx=50, fill=tkinter.X)
        self.widgets_frame.pack(fill=tkinter.BOTH)
        self.send_button.pack(side=tkinter.RIGHT, padx=100, pady=(0, 150))
        self.message_entry.pack(side=tkinter.RIGHT, pady=(0, 150))
        self.nickname_label.place(x=0, y=60)
        self.nickname_entry.pack(side=tkinter.LEFT)
        self.character.place(x=370, y=50, height=320, width=320)

    def __get_message(self) -> str:
        """
        Получает текущее сообщение от сервера.
        
        Returns:
            Текущее сообщение чата.
        """
        message = requests.get(f"{SERVER_URL}/get_message")
        message = json.loads(message.text)
        char_id = message["id"]
        self.update_character(char_id)
        return message["message"]

    def __send_message(self, message: str = "Подключился новый пользователь!") -> None:
        """
        Отправляет сообщение на сервер.
        
        Args:
            message: Текст сообщения.
        """
        params = {"message" : message,
                  "char_id" : self.character_id}
        requests.post(url=f"{SERVER_URL}/send_message", params=params)
        self.message_entry.delete(0, tkinter.END)
        self.update()

    def update_character(self, char_id: int) -> None:
        """
        Обновляет отображаемого персонажа.
        
        Args:
            char_id: ID нового персонажа.
        """
        self.character.id = char_id
        self.character.update()

    def update(self) -> None:
        """Обновляет все виджеты чата."""
        self.history_text.configure(state="normal")
        self.history_text.delete("1.0", tkinter.END)
        self.history_text.insert("1.0", self.__get_history())
        self.history_text.configure(state="disabled")
        self.chat_label['text'] = self.__get_message()

    def __start_updating(self) -> None:
        """Запускает периодическое обновление чата."""
        self.update()
        self.master.after(500, self.__start_updating)

    def __get_history(self) -> str:
        """
        Получает историю сообщений с сервера.
        
        Returns:
            История сообщений в виде строки.
        """
        history = requests.get(f"{SERVER_URL}/show_history").text
        history = json.loads(history)["msg"]
        history = "\n".join(history)
        return history

    def show(self) -> None:
        """Отображает виджеты чата."""
        self.pack(expand=True, fill=tkinter.BOTH)


class MainApp(tkinter.Tk):
    """Главный класс приложения."""
    
    def __init__(self) -> None:
        """Инициализирует главное окно приложения."""
        super().__init__()

        self.widgets: Widgets

        self.__configure_window()
        self.__configure_widgets()
    
    def __select_character(self) -> int:
        """
        Открывает окно выбора персонажа и возвращает выбранный ID.
        
        Returns:
            ID выбранного персонажа.
        """
        menu = CharacterSelectMenu(self.master)
        self.wait_window(menu)
        return menu.id

    def __configure_window(self) -> None:
        """Настраивает параметры главного окна."""
        self.title("ALT-AO")
        self.geometry("800x600")
        self.resizable(False, False)

    def __configure_widgets(self) -> None:
        """Настраивает виджеты приложения."""
        self.widgets = Widgets(self, self.__select_character())
        self.widgets.show()

    def run(self) -> None:
        """Запускает главный цикл приложения."""
        self.mainloop()
        
if __name__ == "__main__":
    app = MainApp()
    app.run()