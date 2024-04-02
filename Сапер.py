from fltk import *

buttons = []
win = None
level = 8  # добавим глобальную переменную level


def cell_callback(widget, data):
    if data == 1:
        widget.color(FL_RED)
    else:
        widget.color(FL_LIGHT1)


def difficulty_cb(widget, data):
    global level
    if not data:
        level = widget.value()
        if level == 0:
            create_buttons(8, 8)  # Маленький размер
        elif level == 1:
            create_buttons(12, 12)  # Средний размер
        elif level == 2:
            create_buttons(16, 16)  # Большой размер



def create_buttons(rows, cols):
    global buttons, win
    for btn in buttons:
        btn.hide()
    buttons.clear()

    cell_size = 30
    for i in range(rows):
        for j in range(cols):
            btn = Fl_Button(j * cell_size, i * cell_size + 30, cell_size, cell_size, '')
            btn.color(FL_LIGHT1)
            btn.callback(lambda w: cell_callback(w, 0))
            buttons.append(btn)

    win.size(cell_size * cols, cell_size * rows + 30)
    win.redraw()


def close_cb(widget, data):
    if data == 0:
        return 0
    return 1


def init_game():
    global win
    win = Fl_Window(240, 270, 'Сапёр')
    win.callback(lambda w: close_cb(w, 0))

    menu = Fl_Menu_Bar(0, 0, 240, 30)
    menu.add("Меню/Помощь")

    difficulty = Fl_Choice(140, 3, 100, 24, "Уровень сложности:")
    choices = ["Маленький", "Средний", "Большой"]
    for choice in choices:
        difficulty.add(choice)
    difficulty.callback(difficulty_cb, 0)

    create_buttons(8, 8)

    win.end()
    win.show()


def main():
    init_game()
    Fl.run()


if __name__ == '__main__':
    main()
