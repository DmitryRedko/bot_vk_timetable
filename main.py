import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests  # для URL запроса
from bs4 import BeautifulSoup
import re
from config import passwordvk
from config import token
import psycopg2
from config import host,user,passwordbd,db_name

vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)

connection=psycopg2.connect(
    host=host,
    user=user,
    password=passwordbd,
    database=db_name
)
connection.autocommit = True

with connection.cursor() as cursor:
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS links(
        link varchar(400),
        description varchar(400));
    """
    )

class Main:
    @classmethod
    def write_msg(cls, user_id, message):
        vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": 0})

    @classmethod
    def check(cls, reqest):
    # Каменная логика ответа
        request=reqest.lower()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT link FROM links WHERE description='неделя'""",
                )
                week = cursor.fetchall()
        except:
            "Не получилось получить данные о неделе"


        if request == "ссылки":
            Admin.links()
        elif request == "расп":
            cls.write_msg(event.user_id, "https://rasp.tpu.ru/site/department.html?id=7863&cource=1")
            cls.write_msg(event.user_id, f"Сейчас {week[0][0]} неделя. Какая неделя нужна?")
            Pars.ask()
        elif request == "admin":
            cls.write_msg(event.user_id, "Введите пароль:")
            Admin.autorise()
        else:
            Main.write_msg(event.user_id, "Не понял вашего ответа... \'помощь\', чтобы посмотреть функционал")

    @classmethod
    def checktimetable(cls, reqest,week):
        # Каменная логика ответа
        request = reqest.lower()
        try:
            if (int(request) > 0) and (int(request) < 9):
                try:
                    Pars.pars(int(request),week)
                except:
                    "Проблемы с парсингом"
            else:
                Main.write_msg(event.user_id, "Попробуйте снова, после ""расп"" Введите цифру от 1 до 7")
        except:
            Main.write_msg(event.user_id, "Попробуйте снова, после ""расп"" Введите цифру от 1 до 7")

def rasp():
    cls.write_msg(event.user_id, "https://rasp.tpu.ru/site/department.html?id=7863&cource=1")
    cls.write_msg(event.user_id, f"Сейчас {week[0][0]} неделя. Какая неделя нужна?")
    yield Pars.ask()
class Pars(Main):
    askflag=False
    flagt=False
    week=None
    @classmethod
    def ask(cls):
        cls.askflag = True
    @classmethod
    def timetable(cls,week):
        cls.write_msg(event.user_id, "День недели:")
        Pars.show(week)
    @classmethod
    def pars(cls,day,week):
        try:
            print(week)
            RASP = "https://rasp.tpu.ru/gruppa_36897/2021/"+str(int(week))+"/view.html"
        except:
            Main.write_msg(event.user_id, "Неправильный тип данных текущей недели")
        headers = {'user agent': "Mozilla/5.0 (X11; Linux x86_64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/100.0.4896.127 Safari/537.36"}
        html = requests.get(RASP, headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        convert = soup.findAll('td')
        Timelist=['8.00-10.05','10.25-12.00','12.40-14.15','14.35-16.10','16.30-18.05','18.25-20.00','20.20-21.55']
        for tim in range(0,7):
            convert1=convert[day+tim*7].findAll('div')
            converted=[]
            for i in convert1:
                #print(i)
                convertv2 = re.findall(r">[,]*\s*\w+\s*[.]*\w*[.]*\s*\w*[.]*<", str(i))
                for j in convertv2:
                    converted+=[j[1:len(j)-1]]
           # print(converted)
            if(bool(len(converted))):
                Main.write_msg(event.user_id,str(Timelist[tim])+": "+" ".join(map(str,converted)))
            else:
                Main.write_msg(event.user_id,str(Timelist[tim])+": "+"Окно")
        Pars.askflag=False
        Pars.flagt=False
    @classmethod
    def show(cls,week):
        cls.write_msg(event.user_id, "1)Пн - 7)Вс")
        cls.flagt=True
        cls.week=week

class Admin:
    adchange=False
    enterflag=False
    exitflag=False
    adflag=False
    addflag=False
    delflag=False
    @classmethod
    def autorise(cls):
        cls.adflag=True

    @classmethod
    def userpass(cls,pswrd):
        if (pswrd == passwordvk):
            Main.write_msg(event.user_id, "Авторизация выполнена. Команды:\n"
                                          "links - для просмотра ссылок  \n"
                                          "change - для редактирования ссылок, в том числе текущей недели\n"
                                          "add - для добавления новых ссылок\n"
                                          "del - для удаления кривых или ненужных ссылок\n"
                                          "exit - выход из меню админа\n"
                                          "После деавторизации exit не забудьте удалиь пароли из сообщений вк.")
            cls.enterflag = True
        else:
            Main.write_msg(event.user_id, "неверный пароль, возврат в меню")
            Admin.adchange = False
            Admin.enterflag = False
            Admin.exitflag = False
            Admin.adflag = False
            Admin.addflag = False
            Admin.delflag = False
            help()



    @classmethod
    def check(cls,adminrequest):
        if (adminrequest == "links"):
            Admin.links()
        elif(adminrequest == "change"):
            Main.write_msg(event.user_id, "Введите данные в формате: ссылка пробел название")
            Admin.adchange=True
        elif(Admin.adchange==True):
            print(adminrequest)
            Admin.changelink(adminrequest)
        elif (adminrequest == "exit"):
            Main.write_msg(event.user_id, "Деавторизация прошла успешно")
            Admin.enterflag=False
            Admin.adflag=False
        elif(adminrequest == "add"):
            Main.write_msg(event.user_id, "Введите данные в формате: ссылка пробел название")
            Admin.addflag=True
        elif (Admin.addflag == True):
            print(adminrequest)
            Admin.addlink(adminrequest)
        elif(adminrequest == "del"):
            Main.write_msg(event.user_id, "Введите название ссылки")
            Admin.delflag=True
        elif(Admin.delflag==True):
            print(adminrequest)
            Admin.dellink(adminrequest)


    @classmethod
    def links(cls):
        Links=[]
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM public.links;"""
            )
            Links+=cursor.fetchall()
        for i in Links:
            Main.write_msg(event.user_id, str(i[0]) + " - " + str(i[1]))
    @classmethod
    def changelink(cls,date):
        try:
            print(date)
            adlist=date.split()
            l=str(adlist[0])
            print(l)
            d=str(adlist[1])
            print(d)
            with connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE links SET link=%s WHERE description=%s;""", (l,d)
                )
            Admin.adchange=False
            Main.write_msg(event.user_id, "Ссылка изменена")
        except:
            Main.write_msg(event.user_id, "Ошибка ввода: введите данные в формате: ссылка пробел название")

    @classmethod
    def addlink(cls,date):
        try:
            print(date)
            adlist=date.split()
            l=str(adlist[0])
            print(l)
            d=str(adlist[1])
            print(d)
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO links (link, description) VALUES (%s, %s)", (l, d))
            Admin.addflag = False
            Main.write_msg(event.user_id, "Ссылка добавлена")
        except:
            Main.write_msg(event.user_id, "Ошибка ввода: введите данные в формате: ссылка пробел название")

    @classmethod
    def dellink(cls, date):
        print(date)
        s=str(date)
        if(date=="неделя"):
            Main.write_msg(event.user_id, "Нельзя удалять данные о неделе")
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("  DELETE FROM links WHERE description=%s", (str(s),))
                Admin.delflag = False
                Main.write_msg(event.user_id, "Ссылка удалена")
            except:
                Main.write_msg(event.user_id, "что-то пошло не так")
def help():
    Main.write_msg(event.user_id, "Привет, я бот-помошник, мои команды:\n"
                                  "1)ссылки - получить полезные ссылки\n"
                                  "2)расп - получить расписание на нужный день\n"
                                  "3)admin - команда для настройки бота, доступна кураторам")
def menu():
    Pars.askflag=False
    Pars.flagt=False
    Admin.adchange = False
    Admin.enterflag = False
    Admin.exitflag = False
    Admin.adflag = False
    Admin.addflag = False
    Admin.delflag = False

for event in longpoll.listen():

# Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

# Если оно имеет метку для меня( то есть бота)
        if event.to_me:
# Сообщение от пользователя

            request = event.text
            request = request.lower()
            print(Admin.enterflag)
            #print(Pars.flagt)
            if(request == 'меню'):
                menu()
                help()
            elif(Pars.flagt == True):
                Main.checktimetable(request,Pars.week)
                Pars.flagt=False
            elif(Admin.adflag):
                if(Admin.enterflag):
                    Admin.check(request)
                else:
                    Admin.userpass(request)
            elif(Pars.askflag):
                Pars.timetable(request)
                Pars.askflag==False
            elif(request=="помощь"):
                help()
            else:
                Main.check(request)
