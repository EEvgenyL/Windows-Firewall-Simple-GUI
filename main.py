from handlers import *


# при импорте выполнится код из файла
# будет проверка на admin права

def block_site():  # эта функция здесь из-за области видимости domen_string
    """
    блокирует сайт
    использует блокировку по удаленным портам 80 и 443
    :return: ничего
    """
    domen = domen_string.get()
    ips = get_ips(domen)  # это список ip адрессов сайта

    cmd = ["netsh", "advfirewall", "firewall", "add", "rule", 'name="{site_name}"', "protocol=TCP", "remoteport=80",
           "action=block", "dir=OUT", "remoteip={site_ip}"]

    if len(ips) > 1:  # если адресов более 1
        for ip_address in ips:
            cmd[5] = "name=block " + domen
            cmd[10] = "remoteip=" + ip_address
            run_cmd(cmd)
            cmd[7] = "remoteport=443"
            run_cmd(cmd)
            cmd[7] = "remoteport=80"  # для следующей итерации

        mb.showinfo(title=None, message="Успешно")
    elif len(ips) == 1:
        cmd[5] = "name=block " + domen
        cmd[10] = "remoteip=" + ips[0]
        run_cmd(cmd)
        cmd[7] = "remoteport=443"
        run_cmd(cmd)
        mb.showinfo(title=None, message="Успешно")
    else:
        mb.showerror("Ошибка", "Ошибка при блокировке " + domen)


def unblock_site():  # тоже здесь из-за области видимости domen_string
    """
    удаляет правило блокировки сайта
    :return: ничего
    """
    name = 'name=block ' + domen_string.get()
    cmd = ["netsh", "advfirewall", "firewall", "delete", "rule", name]
    run_cmd(cmd)


window = tk.Tk()  # создание окна

# заголовок главного окна
window.title("Firewall")
# делаем фон белым
window.config(bg="white")
# указываем icon
window.iconbitmap('favicon.ico')  # загрузка картинки

# получаем размер экрана, это нужно чтобы создать окно по центру экрана
w = window.winfo_screenwidth()
h = window.winfo_screenheight()
# вычисляем середину
w = w // 2  # середина экрана
h = h // 2
w = w - 200  # смещение от середины
h = h - 200

# устанавливаем размер окна
window.geometry('290x403+{}+{}'.format(w, h))
# запрещаем изменение размеров окна
window.resizable(False, False)

# создание меню
mainmenu = tk.Menu(window)
window.config(menu=mainmenu)

# создание вкладки
configmenu = tk.Menu(mainmenu, tearoff=0)
configmenu.add_command(label="Сохранить конфигурацию", command=save_config)
configmenu.add_command(label="Импортировать конфигурацию", command=import_config)
configmenu.add_separator()
configmenu.add_command(label="Выход", command=exit)

# Создание вклдаки
helpmenu = tk.Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="О программе", command=about)
# helpmenu.add_command(label="Справка", command=help_page)

# добавляем каскады в меню
mainmenu.add_cascade(label="Файл", menu=configmenu)
mainmenu.add_cascade(label="Справка", menu=helpmenu)

# ЗАГОЛОВОК Firewall
Firewall_label = tk.Label(text="Firewall",
                          background="white",
                          foreground="black",
                          font=("Times", "15", "bold")
                          ).grid(row=0, column=0, columnspan=2)

button_firewall_on = tk.Button(
    background="black",  # фоновый цвет кнопки
    foreground="white",  # цвет текста
    text="Вкл",
    width=19,
    height=1,
    command=enable_firewall
).grid(row=1, column=0)

button_firewall_off = tk.Button(
    background="black",  # фоновый цвет кнопки
    foreground="white",  # цвет текста
    text="Выкл",
    width=19,
    height=1,
    command=disable_firewall
).grid(row=1, column=1)

button_firewall_reset = tk.Button(
    background="black",  # фоновый цвет кнопки
    foreground="white",  # цвет текста
    text="Сброс",
    width=19,
    height=1,
    command=reset_firewall
).grid(row=2, column=0)

button_firewall_block = tk.Button(
    background="black",  # фоновый цвет кнопки
    foreground="white",  # цвет текста
    text="Block all",
    width=19,
    height=1,
    command=firewall_block_all
).grid(row=2, column=1)



# ЗАГОЛОВОК HTTP трафик
block_http_label = tk.Label(text="HTTP трафик",
                            background="white",
                            foreground="black",
                            font=("Times", "12", "bold")
                            ).grid(row=3, column=0, columnspan=2)

button_http_on = tk.Button(
    background="black",  # фоновый цвет кнопки
    foreground="white",  # цвет текста
    text="Заблокировать",
    width=40,
    height=1,
    command=block_http_port
).grid(row=4, column=0, columnspan=2)

button_http_off = tk.Button(
    background="black",  # фоновый цвет кнопки
    foreground="white",  # цвет текста
    text="Разблокировать",
    width=40,
    height=1,
    command=unblock_http_port
).grid(row=5, column=0, columnspan=2)


# ЗАГОЛОВОК HTTPS трафик
block_https_label = tk.Label(text="HTTPS трафик",
                             background="white",
                             foreground="black",
                             font=("Times", "12", "bold")
                             ).grid(row=6, column=0, columnspan=2)

button_https_on = tk.Button(
    background="black",  # фоновый цвет кнопки
    foreground="white",  # цвет текста
    text="Заблокировать",
    width=40,
    height=1,
    command=block_https_port
).grid(row=7, column=0, columnspan=2)

button_https_off = tk.Button(
    background="black",  # фоновый цвет кнопки
    foreground="white",  # цвет текста
    text="Разблокировать",
    width=40,
    height=1,
    command=unblock_https_port
).grid(row=8, column=0, columnspan=2)



# ЗАГОЛОВОК Доступ в интернет приложения
block_app_lbl = tk.Label(text="Приложение",
                         background="white",
                         foreground="black",
                         font=("Times", "12", "bold")
                         ).grid(row=9, column=0, columnspan=2)

app_app_btn = tk.Button(
    background="black",  # фоновый цвет кнопки
    foreground="white",  # цвет текста
    text="Выбрать приложение",
    width=40,
    height=1,
    command=app_access
).grid(row=10, column=0, columnspan=2)

# ЗАГОЛОВОК Заблокировать домен
block_domen_lbl = tk.Label(text="Домен",
                           background="white",
                           foreground="black",
                           font=("Times", "12", "bold")
                           ).grid(row=11, column=0, columnspan=2)

domen_string = tk.StringVar(window) # создание переменной для Entry

# поле ввода для домена
domen_txt = tk.Entry(window,
                     width=47,
                     bg="gray",
                     fg="black",
                     justify="center",
                     textvariable=domen_string
                     ).grid(row=12, column=0, columnspan=2)

domen_block_btn = tk.Button(
    background="black",  # фоновый цвет кнопки
    foreground="white",  # цвет текста
    text="Заблокировать",
    width=40,
    height=1,
    command=block_site
).grid(row=13, column=0, columnspan=2)

domen_unblock_btn = tk.Button(
    background="black",  # фоновый цвет кнопки
    foreground="white",  # цвет текста
    text="Разблокировать",
    width=40,
    height=1,
    command=unblock_site
).grid(row=14, column=0, columnspan=2)


window.mainloop()
