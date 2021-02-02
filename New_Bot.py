# модули

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import logging

# функции написания сообщения

# c картинкой

def write_message1(sender, message, keyboard):
    authorise.method("messages.send",
                     {"user_id": sender, "message": message, "random_id": get_random_id(),
                      "attachment": "photo{}_{}".format(upload_image["owner_id"], upload_image["id"]),
                      "keyboard": keyboard.get_keyboard()})

# без картинки

def write_message2(sender, message, keyboard):
    authorise.method("messages.send",
                     {"user_id": sender, "message": message, "random_id": get_random_id(),
                      "keyboard": keyboard.get_keyboard()})

# с файлами

def write_message3(sender, files):
    attachments = []
    for file in files:
        attachments.append("doc{}_{}".format(file["owner_id"], file["id"]))
    authorise.method("messages.send",
                     {"user_id": sender, "random_id": get_random_id(),
                      "attachment": "," .join(attachments),
                      "keyboard": keyboard_Main_Menu.get_keyboard()})

# поиск файлов

def find_files(search):
    files = authorise.method("docs.search",
                               {"q": search, "return_tags": 1, "count": 55})["items"]
    new_files = []
    for i in files:
        if i["tags"][0] == search:
            new_files.append(i)
    return new_files

# проверка поиска

def True_Search(search):
    return search.startswith("3 семестр") or search.startswith("4 семестр") or search.startswith("2 семестр")

# создание клавиатур

# главное меню

keyboard_Main_Menu = VkKeyboard(one_time=True)
keyboard_Main_Menu.add_button("2 семестр", color=VkKeyboardColor.PRIMARY)
keyboard_Main_Menu.add_line()
keyboard_Main_Menu.add_button("3 семестр", color=VkKeyboardColor.PRIMARY)
keyboard_Main_Menu.add_line()
keyboard_Main_Menu.add_button("4 семестр", color=VkKeyboardColor.PRIMARY)

# 2 семестр

keyboard_2_semester = VkKeyboard(one_time=True)
keyboard_2_semester.add_button("Термодинамика", color=VkKeyboardColor.PRIMARY)
keyboard_2_semester.add_line()
keyboard_2_semester.add_button("Многомерный анализ", color=VkKeyboardColor.PRIMARY)
keyboard_2_semester.add_line()
keyboard_2_semester.add_button("Линейная алгебра", color=VkKeyboardColor.PRIMARY)
keyboard_2_semester.add_line()
keyboard_2_semester.add_button("Главное меню", color=VkKeyboardColor.NEGATIVE)

# 3 семестр

keyboard_3_semester = VkKeyboard(one_time=True)
keyboard_3_semester.add_button("Электричество", color=VkKeyboardColor.PRIMARY)
keyboard_3_semester.add_line()
keyboard_3_semester.add_button("Кратные интегралы", color=VkKeyboardColor.PRIMARY)
keyboard_3_semester.add_line()
keyboard_3_semester.add_button("Теор. механика", color=VkKeyboardColor.PRIMARY)
keyboard_3_semester.add_line()
keyboard_3_semester.add_button("Диф. уравнения", color=VkKeyboardColor.PRIMARY)
keyboard_3_semester.add_line()
keyboard_3_semester.add_button("Главное меню", color=VkKeyboardColor.NEGATIVE)

# подробно о предмете

keyboard_Subject_1 = VkKeyboard(one_time=True)
keyboard_Subject_1.add_button("1 задание", color=VkKeyboardColor.PRIMARY)
keyboard_Subject_1.add_line()
keyboard_Subject_1.add_button("2 задание", color=VkKeyboardColor.PRIMARY)
keyboard_Subject_1.add_line()
keyboard_Subject_1.add_button("Билеты", color=VkKeyboardColor.PRIMARY)
keyboard_Subject_1.add_line()
keyboard_Subject_1.add_button("Назад", color=VkKeyboardColor.NEGATIVE)
keyboard_Subject_1.add_line()
keyboard_Subject_1.add_button("Главное меню", color=VkKeyboardColor.NEGATIVE)

keyboard_Subject_2 = VkKeyboard(one_time=True)
keyboard_Subject_2.add_button("1 задание", color=VkKeyboardColor.PRIMARY)
keyboard_Subject_2.add_line()
keyboard_Subject_2.add_button("2 задание", color=VkKeyboardColor.PRIMARY)
keyboard_Subject_2.add_line()
keyboard_Subject_2.add_button("3 задание", color=VkKeyboardColor.PRIMARY)
keyboard_Subject_2.add_line()
keyboard_Subject_2.add_button("Билеты", color=VkKeyboardColor.PRIMARY)
keyboard_Subject_2.add_line()
keyboard_Subject_2.add_button("Назад", color=VkKeyboardColor.NEGATIVE)
keyboard_Subject_2.add_line()
keyboard_Subject_2.add_button("Главное меню", color=VkKeyboardColor.NEGATIVE)

# вспомогательные переменные

lastkeyboard = keyboard_Main_Menu
Search = ""
Last_Count_Users = 0
Id_Users = []
last_reseived_message = ""
Tasks = ["1 задание", "2 задание", "3 задание", "Билеты"]
Semesters = ["2 семестр", "3 семестр", "4 семестр"]
Subjects_T2 = ["Многомерный анализ"]
Subjects_2 = ["Термодинамика" ,"Линейная алгебра"]
Subjects_3 = ["Электричество", "Кратные интегралы", "Теор. механика", "Диф. уравнения"]

# связь с сообществом

image = "f0ufgckDlX8.jpg"
token = "4a72e9980d2ceb5b5994e2adef825045a8d62a2cdca7e697f71c479954d5909d98663d484894126f8cbdf"
authorise = vk_api.VkApi(token=token)
longpoll = VkLongPoll(authorise)

# загрузка вложений

upload = VkUpload(authorise)
upload_image = upload.photo_messages(photos=image)[0]

# основная программа

while True:
    logging.basicConfig(filename="errors.txt", format='[%(asctime)s] [%(levelname)s] => %(message)s',
                        level=logging.WARNING)
    try:
        for event in longpoll.listen():

            # идендификаторы пользователей

            if authorise.method("groups.getMembers", {"group_id": 201631051})["count"] != Last_Count_Users:
                Users = authorise.method("groups.getMembers", {"group_id": 201631051})
                Id_Users = Users["items"]
                Last_Count_Users = Users["count"]

            # проверка сообщений

            if event.type == VkEventType.MESSAGE_NEW and event.to_me and Id_Users.count(event.user_id) == 1:
                reseived_message = event.text
                sender = event.user_id
                if reseived_message.lower() == "привет":
                    write_message1(sender,
                                   "Я твой путеводитель по космическим просторам!", keyboard_Main_Menu)
                    lastkeyboard = keyboard_Main_Menu

                elif reseived_message.lower() == "главное меню":
                    write_message2(sender,
                                   "Главное меню", keyboard_Main_Menu)
                    lastkeyboard = keyboard_Main_Menu
                    Search = ""

                elif reseived_message.lower() == "2 семестр":
                    write_message2(sender, "Далее", keyboard_2_semester)
                    lastkeyboard = keyboard_2_semester
                    Search += reseived_message.lower()

                elif reseived_message.lower() == "3 семестр":
                    write_message2(sender, "Далее", keyboard_3_semester)
                    lastkeyboard = keyboard_3_semester
                    Search += reseived_message.lower()

                elif Subjects_2.count(reseived_message) == 1 or Subjects_3.count(reseived_message) == 1:
                    write_message2(sender, "Далее", keyboard_Subject_1)
                    lastkeyboard = keyboard_Subject_1
                    Search += "_" + reseived_message.lower()
                    last_reseived_message = reseived_message

                elif Subjects_T2.count(reseived_message) == 1:
                    write_message2(sender, "Далее", keyboard_Subject_2)
                    lastkeyboard = keyboard_Subject_2
                    Search +=  "_" + reseived_message.lower()
                    last_reseived_message = reseived_message

                elif Tasks.count(reseived_message) == 1:
                    if True_Search(Search) == True:
                        Search_1 = Search + "_" + reseived_message.lower()
                        if len(find_files(Search_1)) == 0:
                            write_message2(sender,
                                           "Извини, но я пока не настолько умный :)", lastkeyboard)
                        else:
                            Files = find_files(Search_1)
                            write_message3(sender, Files)
                            lastkeyboard = keyboard_Main_Menu
                            Search = ""
                    else:
                        write_message2(sender,
                                       "Извини, давай заново :)", keyboard_Main_Menu)
                        Search = ""

                elif reseived_message.lower() == "назад":
                    if Search != "":
                        Search = Search.replace("_" + last_reseived_message.lower(), "")
                        if Search == "2 семестр":
                            write_message2(sender, "Назад", keyboard_2_semester)
                            lastkeyboard = keyboard_2_semester
                        elif Search == "3 семестр":
                            write_message2(sender, "Назад", keyboard_3_semester)
                            lastkeyboard = keyboard_3_semester
                    else:
                        write_message2(sender,
                                       "Главное меню", keyboard_Main_Menu)

                else:
                    write_message2(sender,
                                   "Извини, но я пока не настолько умный :)", lastkeyboard)
    except Exception as e:
        logging.error(str(e))
        with open('errors.txt', 'a') as f:
            f.write(str(e) + '\n')