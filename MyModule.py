import string
from time import *
from random import * 
# +----------------------Save AND Load DATA--------------------------------+
# +----------------------------------------------------------------------+
def UserIntoString(user):
    return_string = ""
    arv = 0
    for index, data in user[0].items():
        arv += 1
        return_string += index + ":" + str(data) + ("," if len(user[0]) != arv else "")
    return return_string

def SaveUserData(user):
    user_data.append(user)
    user_args_data = UserIntoString(user)
    with open(file="user_data.txt", mode="a", encoding="utf-8") as f:
        f.write(f"{user_args_data};")

def LoadUserData():
    temp_user_data = []
    with open(file="user_data.txt", mode="r+", encoding="utf-8") as f:
        unformated_users = f.readline().split(";")
        for unformated_data in unformated_users:
            temp_user_data.append({})
            new_user_index_list = len(temp_user_data) - 1
            formated_datas = unformated_data.split(",")
            for i in formated_datas:
                if len(i) != 0:
                    formated_data = i.split(":")
                    temp_user_data[new_user_index_list].update({formated_data[0]:formated_data[1]})
                else:
                    temp_user_data.pop(len(temp_user_data) - 1)
    return temp_user_data

def PushCurrentUserData():
    for user in user_data:
        with open(file="user_data.txt", mode="w", encoding="utf-8") as f:
            f.write("")
        SaveUserData(user)
    user_data = LoadUserData()
# +----------------------------------------------------------------------+
# +----------------------------------------------------------------------+

user_data = LoadUserData()
print(user_data)
symbols_list = [string.octdigits, string.ascii_letters, string.punctuation]

def InputQuit(value):
    quit_words = ['QUIT', '404', 'BREAK', 'EXIT', 'LÕPETADA', 'LÕPP', 'КОНЕЦ']
    if any(i in value.upper() for i in quit_words):
        return True
    return False


def VariableCheck(input_text, false_text, func, find_user_condition=False): 
    if find_user_condition:
        find_user = not None
        while find_user is not None:
            variable = input(input_text)
            if InputQuit(variable):
                return 'EXIT'
            find_user = func(variable)
            if func(variable) is not None:
                print(false_text)
                sleep(1)
    else:
        variable = None
        while variable is None:
            variable = input(input_text)
            if InputQuit(variable):
                return 'EXIT'
            variable = func(variable)
            if variable is None:
                print(false_text)
                sleep(1)
    return variable


def ChangeValueOfUserData(user_id, variable, value):
    user_data[user_id][variable] = value


def AnswerConverter(answer=None, make_question=True):
    t_ans = ['JAH', '1', 'YES', 'ДА']
    f_ans = ['EI', '0', 'NO', 'НЕТ']

    if any(i in answer.upper() for i in t_ans):
        return True
    elif any(i in answer.upper() for i in f_ans):
        return False
    else:
        return None

def PasswordGeneration():
    password = str()
    for _ in range(0, randint(5, 9)):
        random_symbol_lst_index = randint(0, 2)
        password += str(
            symbols_list[random_symbol_lst_index][randint(0, len(symbols_list[random_symbol_lst_index]) - 1)])
    return password


def PasswordCheck(password: str):
    if len(password) < 5:
        return False, "Paroolil peab olema vähemalt 5 tähemärki"
    for symbol_list in symbols_list:
        for symbol in symbol_list:
            if list(password).count(symbol) == len(password):
                return False, "Parool ei tohi koosneda samadest sümbolitest"
    maybe_password = ""
    for number in range(0, 20):
        maybe_password += str(number)
        if password == maybe_password or password == maybe_password[1:-1]:
            return False, "Keerulisemad salasõnad"
    return True, 'success'


def MakePassword(random_password=None, choice=True):
    if choice:
        random_password = VariableCheck("Kas soovite parooli geniseerida või ise välja mõelda? ", "Vale vastus",
                                        AnswerConverter)
    password = None
    if random_password:
        password = PasswordGeneration()
    else:
        while True:
            password = input("Mõtle välja parool: ")
            success, message = PasswordCheck(password)
            if success:
                return password
            else:
                print(message)
    return password


def FindUserByValue(value, get_value):
    for user in user_data:
        if value == user.get(get_value):
            return user
    return None


def FindUserByEmail(email):
    return FindUserByValue(email, "email")


def FindUserByName(name):
    return FindUserByValue(name, "user_name")


def CheckEmailCode(email, code):
    for email_code in email_data:
        if code == email_code.get("code") and email == email_code.get('email'):
            return True
    return False


def Registration(name: str, password: str, secret_word: str, email: str):
    user = {
        "user_id": len(user_data),
        "user_name": name,
        "user_password": password,
        "secret_word": secret_word
    }
    if email is not None:
        user["email"] = email
    else:
        user["email"] = None

    SaveUserData(user)

    return user


def Authorization(name, password):
    user = FindUserByName(name)
    if user is None:
        return False
    if password != user.get("user_password"):
        return False
    return user


def CodeGenerator(email):
    letters_numbers_list = [string.ascii_letters, string.digits]
    code = str()
    for _ in range(0, randint(5, 9)):
        random_symbol_lst_index = randint(0, 1)
        code += str(
            letters_numbers_list[random_symbol_lst_index][
                randint(0, len(letters_numbers_list[random_symbol_lst_index]) - 1)])

    file = "email.txt"
    email_data.append({'email': email, 'code': code})
    with open(file, mode="w", encoding="utf-8") as f:
        f.write(f"{email} - {code}")

    return code


def SendMail(email):
    import smtplib, ssl
    from email.message import EmailMessage

    code = CodeGenerator(email)

    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "sans1999lorf@gmail.com"
    password = "aycm hnxh optg nfhs"

    msg = EmailMessage()

    msg['subject'] = code  # "Parooli uuendamise kood"
    msg['from'] = "sans1999lorf@gmail.com"
    msg['to'] = email

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.send_message(msg)

    except Exception as e:
        print(e)
    finally:
        server.quit()

    return code


def InformationDisplay(user):
    print("+-------------------------+")
    print(
        f"Nimi - '{user.get('user_name')}'\nPassword - '{user.get('user_password')}'\nSecret word - '{user.get('secret_word')}'\n{'Email - ' + user.get('email') if 'email' in user else ''}")
    print("+-------------------------+\n")