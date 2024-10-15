from fltk import *  # Импорт библиотеки FLTK для графического интерфейса
from random import randint  # Импорт функции для генерации случайных чисел
import time  # Импорт модуля для работы со временем

# Определение класса кнопки с миной, наследуется от стандартной кнопки FLTK
class MineButton(Fl_Button):
    def __init__(self, x, y, w, h, label=''):  # Инициализатор для кнопки
        super(MineButton, self).__init__(x, y, w, h, label)  # Вызов инициализатора базового класса

    # Метод обработки нажатий на кнопку
    def handle(self, event):
        if event == FL_PUSH and Fl.event_button() == FL_RIGHT_MOUSE:  # Проверка правой кнопки мыши
            if self.label() == '':  # Если флаг не установлен
                self.label('F')  # Установка флага
                self.color(FL_YELLOW)  # Изменение цвета кнопки на жёлтый
            elif self.label() == 'F':  # Если уже был установлен флаг
                self.label('')  # Удаление флага
                self.color(FL_LIGHT1)  # Возвращение исходного цвета кнопки
            self.redraw()  # Перерисовка кнопки
            return 1  # Возвращение 1, указывая, что событие обработано
        else:
            return super(MineButton, self).handle(event)  # Вызов метода обработки базового класса

# Определение класса игры "Сапёр"
class MineSweeper:
    def __init__(self):  # Инициализатор для игры
        self.win = Fl_Window(390, 490, 'Сапёр')  # Создание окна
        self.start_time = time.time()  # Запись времени начала игры
        self.timer_display = Fl_Box(290, 50, 100, 30, "")  # Строка для таймера
        self.timer_display.box(FL_FLAT_BOX)  # Установка типа рамки для таймера
        self.timer_display.labelsize(14)  # Установка размера шрифта для таймера
        self.menu = Fl_Menu_Bar(0, 0, 430, 30)  # Создание строки меню
        self.menu.add("Меню/Маленькое поле", 0, self.set_small)  # Добавление пункта "Маленькое"
        self.menu.add("Меню/Среднее поле", 0, self.set_medium)  # Добавление пункта "Среднее"
        self.menu.add("Меню/Большое поле", 0, self.set_large)  # Добавление пункта "Большое"
        self.is_game_over = False  # Переменная для отслеживания состояния игры
        self.menu.add("Помощь")  # Добавление пункта "Помощь"
        self.menu.add("О программе")  # Добавление пункта "О программе"
        self.cell_size = 30  # Размер ячейки
        self.rows = 13  # Количество строк
        self.cols = 13  # Количество столбцов
        self.mines = self.generate_mines()  # Генерация мин
        self.buttons = {}  # Словарь для хранения кнопок
        for i in range(self.rows):  # Цикл по строкам
            for j in range(self.cols):  # Цикл по столбцам
                identifier = i * self.cols + j  # Уникальный идентификатор кнопки
                btn = MineButton(j * self.cell_size, i * self.cell_size + 100, self.cell_size, self.cell_size, '')  # Создание кнопки
                btn.color(FL_LIGHT1)  # Установка цвета кнопки
                btn.callback(self.cell_callback, identifier)  # Назначение обработчика события Click
                self.buttons[identifier] = btn  # Добавление кнопки в словарь
        self.reset_button = Fl_Button(171, 50, 50, 30, "Сброс")  # Кнопка для сброса игры
        self.reset_button.callback(self.reset_game)  # Назначение обработчика событий для кнопки сброса
        self.win.end()  # Завершение добавления элементов в окно
        self.win.show()  # Отображение окна
        Fl.add_timeout(1.0, self.update_timer)  # Добавление таймера для обновления времени every 1 second

        # Метод для установки маленького поля

    def set_small(self, *args):
        self.rows, self.cols = 8, 8  # Размеры маленького поля
        self.reset_game()  # Перезапуск игры

        # Метод для установки среднего поля

    def set_medium(self, *args):
        self.rows, self.cols = 13, 13  # Размеры среднего поля
        self.reset_game()  # Перезапуск игры

        # Метод для установки большого поля

    def set_large(self, *args):
        self.rows, self.cols = 16, 30  # Размеры большого поля
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
        elapsed_time = int(time.time() - self.start_time)  # Расчёт прошедшего времени
        self.timer_display.label(f"Время: {elapsed_time} сек.")  # Отображение времени
        Fl.repeat_timeout(1.0, self.update_timer)  # Повторный вызов таймера через 1 секунду

if __name__ == '__main__':
    MineSweeper()  # Создание экземпляра игры
    Fl.run()  # Запуск цикла событий FLTK