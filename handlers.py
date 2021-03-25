import ctypes
import os
import subprocess
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb


def run_cmd(cmd):
    """
    :param cmd: исполняемая команда в командной строке
    :return: окно, успешна ли выполнена команда
    """
    cmd_struct = subprocess.run(cmd, stdout=subprocess.PIPE, encoding='866')
    if cmd_struct.returncode == 0:
        mb.showinfo(title=None, message="Успешно")
        print("----------УСПЕШНО---------")
        print()
    else:
        mb.showerror(title=None, message="Ошибка при выполнени")
        print("----------ОШИБКА----------")
        print(cmd_struct.stdout.replace("\n", ""))  # удаляем пустые строки
        print()


def is_admin():
    """
    Проверяет, запущенна ли программа от имени администратора
    :return: True or False
    """
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


if not is_admin():  # проверяет запущен ли скрипт, от имени администратора
    mb.showerror('Ошибка', 'Запустите от имени администратора')


def get_ips(domenname):
    """
    :param domenname: домен сайта str
    :return: список из ip адресов
    """
    cmd = ["nslookup", domenname]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, encoding='866')
    try:
        starts = result.stdout.rindex("Addresses:") + 10
        ends = len(result.stdout)
        ip = result.stdout[starts + 1:ends]
        ip = ip.replace("\n", "")
        ip = ip.replace(" ", "")
        ip = ip.split("\t")
        return ip
    except ValueError:
        starts = result.stdout.rindex("Address:") + 8
        ends = len(result.stdout)
        ip = result.stdout[starts + 1:ends]
        ip = ip.replace("\n", "")
        ip = ip.replace(" ", "")
        ip = [ip]
        return ip


def enable_firewall():
    """
    Включает firewall
    :return: ОК. или ERROR
    """

    cmd = ["netsh", "advfirewall", "set", "allprofiles", "state", "on"]
    run_cmd(cmd)


def disable_firewall():
    """
    Выключает firewall
    :return: ОК. или ERROR
    """
    cmd = ["netsh", "advfirewall", "set", "allprofiles", "state", "off"]
    run_cmd(cmd)


def reset_firewall():
    """
    Сбрасывает все правила Firewall
    :return: ОК. или ERROR
    """
    cmd = ["netsh", "advfirewall", "reset"]
    run_cmd(cmd)


def firewall_block_all():
    cmd = ["netsh", "advfirewall", "set", "allprofiles", "firewallpolicy", "blockinbound,blockoutbound"]
    run_cmd(cmd)
    pass


def block_http_port():
    cmd = ["netsh", "advfirewall", "firewall", "add", "rule", 'name="HTTP-block"', "protocol=TCP", "remoteport=80",
           "action=block", "dir=OUT"]
    run_cmd(cmd)


def unblock_http_port():
    cmd = ["netsh", "advfirewall", "firewall", "delete", "rule", 'name="HTTP-block"']
    run_cmd(cmd)


def block_https_port():
    cmd = ["netsh", "advfirewall", "firewall", "add", "rule", 'name=HTTPS-block', "protocol=TCP", "remoteport=443",
           "action=block", "dir=OUT"]
    run_cmd(cmd)


def unblock_https_port():
    cmd = ["netsh", "advfirewall", "firewall", "delete", "rule", 'name=HTTPS-block']
    run_cmd(cmd)


def save_config():
    try:
        file_path = fd.asksaveasfilename(filetypes=[("Windows firewall", "*.wfw")])
        cmd = ["netsh", "advfirewall", "export", file_path]
        run_cmd(cmd)
    except:
        mb.showerror("Ошибка", "Произошла ошибка при сохранении")


def import_config():
    """
    Обработчик загрузки конфигурации
    :return: ничего
    """
    try:
        filepath = fd.askopenfilename(
            filetypes=[("All files", "*.*"), ("Windows firewall", "*.wfw")]
        )

        if not filepath:  # простая защита от неправильного filepath
            mb.showerror("Ошибка", "Произошла ошибка при импорте конфигурации")
            return

        cmd = ["netsh", "advfirewall", "import", filepath]
        run_cmd(cmd)
    except:
        mb.showerror()("Ошибка", "Произошла ошибка при импорте конфигурации")


def about():
    """
    Создает окно "о программе"
    :return: окно
    """
    about_window = tk.Tk()  # создание окна (главный цикл)
    about_window.config(bg="white")
    about_window.iconbitmap('favicon.ico')  # загрузка картинки

    w = about_window.winfo_screenwidth()
    h = about_window.winfo_screenheight()
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 200  # смещение от середины
    h = h - 300
    about_window.geometry('290x60+{}+{}'.format(w, h))

    about_window.resizable(False, False)  # запрет на изменение размеров
    about_window.title("О программе")  # заголовок окна

    label = tk.Label(text="Курсовая работа Лебедева Евгения, 2021 год",
                     master=about_window,
                     background="white",  # фоновый цвет кнопки
                     foreground="black",  # цвет текста
                     )
    label.pack()
    label2 = tk.Label(text="Программа конфигурирует брандмауэр",
                      master=about_window,
                      background="white",  # фоновый цвет кнопки
                      foreground="black",  # цвет текста
                      )
    label2.pack()
    about_window.mainloop()  # главный цикл


def app_access():
    file_str = ""

    def block_app():
        nonlocal file_str

        cmd = ["netsh", "advfirewall", "firewall", "add", "rule",
               'name="App block"', "dir=out", 'program=""',
               "action=block"]
        cmd[5] = 'name="{}"'.format(file_str[file_str.rfind('\\') + 1:])
        cmd[7] = 'program="{}"'.format(file_str)
        os.system(' '.join(cmd))  # тут нельзя вызвать run_cmd() из-за "\"
        cmd[6] = "dir=in"  # блкируем трафик в обе стороны
        os.system(' '.join(cmd))
        mb.showinfo(title=None, message="ОК")

    def unblock_app():
        cmd = ["netsh", "advfirewall", "firewall", "delete", "rule", 'name={}']
        cmd[5] = 'name="{}"'.format(file_str[file_str.rfind('\\') + 1:])
        run_cmd(cmd)

    def get_file_path():
        nonlocal file_str
        file_str = fd.askopenfilename(
            filetypes=[("Executable", "*.exe")]
        )

        file_str = file_str.replace("/", "\\")

    app_access_window = tk.Tk()
    app_access_window.config(bg="white")
    w = app_access_window.winfo_screenwidth()
    h = app_access_window.winfo_screenheight()
    w = w // 2  # середина экрана
    h = h // 2
    w = w + 100  # смещение от середины
    h = h - 200
    app_access_window.geometry('273x78+{}+{}'.format(w, h))
    app_access_window.iconbitmap('favicon.ico')  # загрузка картинки
    app_access_window.resizable(False, False)  # запрет на изменение размеров
    app_access_window.title("Доступ в интернет программы")  # заголовок окна

    file_path_btn = tk.Button(
        app_access_window,
        background="black",  # фоновый цвет кнопки
        foreground="white",  # цвет текста
        text="Выбрать .exe",
        width=38,
        height=1,
        command=get_file_path
    ).grid(row=0, column=0)

    button_app_on = tk.Button(
        app_access_window,
        background="black",  # фоновый цвет кнопки
        foreground="white",  # цвет текста
        text="Заблокировать доступ в интернет",
        width=38,
        height=1,
        command=block_app
    ).grid(row=1, column=0)

    button_app_off = tk.Button(
        app_access_window,
        background="black",  # фоновый цвет кнопки
        foreground="white",  # цвет текста
        text="Разблокировать доступ в интернет",
        width=38,
        height=1,
        command=unblock_app
    ).grid(row=2, column=0)

    app_access_window.mainloop()


def help_page():
    """
    Создает окно со справкой по функционалу
    :return: окно
    """
    # TODO
    pass
