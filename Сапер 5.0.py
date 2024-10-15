from fltk import *  # Импорт библиотеки FLTK для графического интерфейса
from random import randint  # Импорт функции для генерации случайных чисел
import time  # Импорт модуля для работы со временем


# Определение класса кнопки с миной
class MineButton(Fl_Button):
    def __init__(self, x, y, w, h, label=''):
        super(MineButton, self).__init__(x, y, w, h, label)

    def handle(self, event):
        if event == FL_PUSH and Fl.event_button() == FL_RIGHT_MOUSE:
            if self.label() == '':
                self.label('F')
                self.color(FL_YELLOW)
            elif self.label() == 'F':
                self.label('')
                self.color(FL_LIGHT1)
            self.redraw()
            return 1
        else:
            return super(MineButton, self).handle(event)


# Определение класса игры "Сапёр"
class MineSweeper:
    def __init__(self):
        self.win = Fl_Window(390, 490, 'Сапёр')
        self.win.resizable(self.win)  # Устанавливаем окно масштабируемым
        self.start_time = time.time()
        self.timer_display = Fl_Box(290, 50, 100, 30, "")
        self.timer_display.box(FL_FLAT_BOX)
        self.timer_display.labelsize(14)
        self.menu = Fl_Menu_Bar(0, 0, 430, 30)
        self.menu.add("Меню/Начать игру")
        self.menu.add("Меню/Настройки/Маленькое поле", 0, self.set_small)
        self.menu.add("Меню/Настройки/Среднее поле", 0, self.set_medium)
        self.menu.add("Меню/Настройки/Большое поле", 0, self.set_large)
        self.menu.add("Меню/Выйти из игры")
        self.is_game_over = False
        self.menu.add("Помощь/ Добро пожаловть в игру Сапёр! "
                      "\n Плоское или объёмное игровое поле разделено на смежные ячейки (квадраты, шестиугольники, кубы и т. п.), некоторые из которых «заминированы»."
                      "\n Игрок открывает ячейки, стараясь не открыть ячейку с миной. Открыв ячейку с миной, он проигрывает."
                      "\n Если под открытой ячейкой мины нет, то в ней появляется число, показывающее, сколько ячеек, соседствующих с только что открытой, «заминировано»."
                      "\n«Заминированные» ячейки игрок может пометить(Нажав на правую кнопку мыши). Открыв все «не заминированные» ячейки, игрок выигрывает.")


        self.menu.add("О программе/ Разработчик: Чуднов Дмитрий"
                      "\n Программа была разработана для изучения библиотеки pyFLTK и общей разработки оконных приложений")

        self.cell_size = 30
        self.rows = 13
        self.cols = 13
        self.mines = self.generate_mines()
        self.buttons = {}

        for i in range(self.rows):
            for j in range(self.cols):
                identifier = i * self.cols + j
                btn = MineButton(j * self.cell_size, i * self.cell_size + 100, self.cell_size, self.cell_size, '')
                btn.color(FL_LIGHT1)
                btn.callback(self.cell_callback, identifier)
                self.buttons[identifier] = btn

        self.reset_button = Fl_Button(171, 50, 50, 30, "Сброс")
        self.reset_button.callback(self.reset_game)
        self.win.end()
        self.win.show()
        self.update_reset_button_position()  # Инициализация правильной позиции кнопки
        Fl.add_timeout(1.0, self.update_timer)
        self.win.resize = self.on_resize  # Привязка события изменения размера окна
        self.win.resize = self.on_resize
        self.update_reset_button_position()
        Fl.add_timeout(1.0, self.update_timer)

    def update_reset_button_position(self):
        win_width = self.win.w()
        self.reset_button.position((win_width - self.reset_button.w()) // 2, 50)


    def on_resize(self, win, new_w, new_h):
        self.update_reset_button_position()
        self.create_buttons(new_w, new_h)

    def create_buttons(self, win_width, win_height):
        # Удаление старых кнопок
        for btn in self.buttons.values():
            btn.hide()
        self.buttons.clear()

        # Пересчитаем количество строк и столбцов
        self.cols = win_width // self.cell_size
        self.rows = (win_height - 100) // self.cell_size

        # Создание новых кнопок
        for i in range(self.rows):
            for j in range(self.cols):
                identifier = i * self.cols + j
                btn = MineButton(j * self.cell_size, i * self.cell_size + 100, self.cell_size, self.cell_size, '')
                btn.color(FL_LIGHT1)
                btn.callback(self.cell_callback, identifier)
                self.buttons[identifier] = btn

    # Метод для установки маленького поля
    def set_small(self, *args):
        self.rows, self.cols = 8, 8  # Размеры маленького поля
        self.win.size(self.cols * self.cell_size, self.rows * self.cell_size + 130)  # Изменение размеров окна
        self.reset_game()  # Перезапуск игры

    # Метод для установки среднего поля
    def set_medium(self, *args):
        self.rows, self.cols = 13, 13  # Размеры среднего поля
        self.win.size(self.cols * self.cell_size, self.rows * self.cell_size + 130)  # Изменение размеров окна
        self.reset_game()  # Перезапуск игры

    # Метод для установки большого поля
    def set_large(self, *args):
        self.rows, self.cols = 16, 30  # Размеры большого поля
        self.win.size(self.cols * self.cell_size, self.rows * self.cell_size + 130)  # Изменение размеров окна
        self.reset_game()  # Перезапуск игры

    # Метод для генерации мин
    def generate_mines(self):
        return {(randint(0, self.cols - 1), randint(0, self.rows - 1)) for _ in range(int(self.rows * self.cols * 0.16))}

    # Метод для сброса игры
    def reset_game(self, *args):
        self.mines = self.generate_mines()  # Перегенерация мин
        for btn in self.buttons.values():  # Цикл по всем кнопкам
            btn.label('')  # Очистка текста кнопки
            btn.color(FL_LIGHT1)  # Восстановление исходного цвета
            btn.activate()  # Активация кнопки
        self.start_time = time.time()  # Обновление времени старта
        self.is_game_over = False  # Сброс состояния игры

    # Метод обратного вызова при нажатии на клетку
    def cell_callback(self, widget, data):
        if widget.label() == 'F':  # Если нажата кнопка с флагом, игнорировать нажатие
            return
        self.checked = set()  # Инициализация множества проверенных ячеек
        x = data % self.cols  # Определение столбца
        y = data // self.cols  # Определение строки
        if (x, y) in self.mines:
            self.game_over(widget)  # Вызов метода завершения игры, если нажата мина
        else:
            self.open_cells(x, y)  # Открытие ячеек, если нет мины
        if self.is_game_over:
            return  # Если игра окончена, ничего не делать
        if (data % self.cols, data // self.cols) in self.mines:  # Если нажатие попало на мину
            self.is_game_over = True  # Устанавливаем флаг окончания игры
            for btn in self.buttons.values():  # Деактивируем все кнопки
                btn.deactivate()
            return

    # Метод для подсчёта соседних мин
    def count_nearby_mines(self, x, y):
        count = 0  # Счётчик мин
        for i in range(max(0, y - 1), min(self.rows, y + 2)):  # Перебор соседних строк
            for j in range(max(0, x - 1), min(self.cols, x + 2)):  # Перебор соседних столбцов
                if (j, i) in self.mines:  # Если на позиции есть мина
                    count += 1
        return count  # Возврат количества мин

    # Метод для открытия ячеек
    def open_cells(self, x, y):
        if (x, y) in self.checked or (x, y) in self.mines:
            return  # Если ячейка уже проверена или содержит мину, выйти из функции
        self.checked.add((x, y))  # Добавление ячейки в проверенные
        count = self.count_nearby_mines(x, y)  # Подсчёт соседних мин
        identifier = y * self.cols + x  # Идентификатор кнопки
        btn = self.buttons[identifier]  # Получение кнопки по идентификатору
        if count > 0:
            btn.label(str(count))  # Установка количества мин, если есть соседние мины
        else:
            btn.label(' ')  # Установка пустого значения, если мин нет
            for i in range(max(0, y - 1), min(self.rows, y + 2)):  # Перебор соседних строк
                for j in range(max(0, x - 1), min(self.cols, x + 2)):  # Перебор соседних столбцов
                    self.open_cells(j, i)  # Рекурсивный вызов открытия ячеек
        btn.deactivate()  # Деактивация кнопки после открытия

    # Метод для вызова при завершении игры
    def game_over(self, widget):
        for x, y in self.mines:
            identifier = y * self.cols + x  # Идентификатор кнопки с миной
            btn = self.buttons[identifier]  # Получение кнопки
            btn.label('X')  # Установка метки с миной
            btn.color(FL_RED)  # Изменение цвета на красный
            btn.redraw()  # Перерисовка кнопки

    # Метод для обновления таймера
    def update_timer(self):
        current_time = time.time() - self.start_time
        self.timer_display.label(f"{int(current_time)} сек")
        self.timer_display.redraw()
        Fl.add_timeout(1.0, self.update_timer)

if __name__ == '__main__':
    app = MineSweeper()
    Fl.run()