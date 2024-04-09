from fltk import *
from random import randint


class MineSweeper:
    def __init__(self):
        self.win = Fl_Window(330, 430, 'Сапёр')  # Создание окна Fl_Window размером 330x430 с заголовком "Сапёр"
        self.menu = Fl_Menu_Bar(0, 0, 330, 30)  # Создание меню Fl_Menu_Bar размером 330x30
        self.menu.add("Игра")  # Добавление пункта "Игра" в меню
        self.menu.add("Правка")  # Добавление пункта "Правка"
        self.menu.add("Справка")  # Добавление пункта "Справка"
        self.cell_size = 30  # Установка размера клетки
        self.rows = 11  # Установка количества строк
        self.cols = 11  # Установка количества столбцов
        self.mines = {(randint(0, self.cols - 1), randint(0, self.rows - 1)) for _ in
                      range(int(self.rows * self.cols * 0.1))}  # Генерация мин
        self.buttons = {}  # Создание словаря для кнопок

        for i in range(self.rows):
            for j in range(self.cols):
                identifier = i * self.cols + j  # Идентификатор клетки
                btn = Fl_Button(j * self.cell_size, i * self.cell_size + 100, self.cell_size, self.cell_size,
                                '')  # Создание кнопки
                if (j, i) in self.mines:
                    btn.label('@')  # Установка метки мины на кнопку
                btn.color(FL_LIGHT1)  # Установка цвета кнопки
                btn.callback(self.cell_callback, identifier)  # Назначение колбэка на кнопку
                self.buttons[identifier] = btn  # Добавление кнопки в словарь кнопок

        self.win.end()  # Завершение и составление окна
        self.win.show()  # Показ окна

    def cell_callback(self, widget, data):
        x = data % self.cols  # Получение координаты X клетки
        y = data // self.cols  # Получение координаты Y клетки
        if (x, y) in self.mines:
            widget.label('X')  # Установка метки 'X' для мины
        else:
            count = 0
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if (j, i) in self.mines:
                        count += 1
            if count > 0:
                widget.label(str(count))  # Установка количества мин вокруг клетки
            else:
                widget.label(' ')  # Открытие пустой клетки
                limit = 2  # Ограничение на распространение до 2 клеток
                self.open_cells(x, y, limit)  # Вызов метода для открытия соседних пустых клеток
        widget.color(FL_LIGHT2)  # Установка цвета кнопки

    def open_cells(self, x, y, limit):
        if limit <= 0:
            return
        for i in range(max(0, y - 1), min(self.rows, y + 2)):
            for j in range(max(0, x - 1), min(self.cols, x + 2)):
                idx = i * self.cols + j
                if self.buttons[idx].label() == '':
                    self.cell_callback(self.buttons[idx], idx)  # Рекурсивный вызов для распространения открытия
                    limit -= 1
                    if limit == 0:
                        return


if __name__ == '__main__':
    game = MineSweeper()  # Создание экземпляра игры
    Fl.run()  # Запуск графического интерфейса