
from datetime import date
from tkinter import END
import json
from typing import NamedTuple
from dataclasses import dataclass
from enum import Enum

font = lambda size: ("Arial", size)
USER_TOKEN = "UQM1S0EOD9FHV17Q1LQLKVF4F3VD75HQUB7RKUEKOHQT417JHNQ9SKBU7EUN5D2J"
CLIENT_ID = "O3O3RKT54782U2B13H76T6K4ETRIFS15EH89C7D4NJ9PBDAG64EINVNIC9KB8RFC"
USER_HEADERS = {
    	"Authorization": f"Bearer {USER_TOKEN}",
	    "Content-Type": "application/x-www-form-urlencoded",
	    "grant_type": "authorization_code",
	}

class VacancyResponse(NamedTuple):
    vacancy: str
    resume: str
    state: str


class EmploymentName(Enum):
    FULL = "Полная занятость"
    PART = "Частичная занятость"
    PROJECT = "Проектная работа"
    VOLUNTEER = "Волонтерство"
    PROBATION = "Стажировка"

class EmploymentId(Enum):
    FULL = "full"
    PART = "part"
    PROJECT = "project"
    VOLUNTEER = "volunteer"
    PROBATION = "probation"

class Employment(NamedTuple):
    ID: EmploymentId
    name: EmploymentName

class LanguageLevel(NamedTuple):
    ID: str
    name: str

class LanguageId(NamedTuple):
    ID: str
    name: str

class Language(NamedTuple):
    ID: str
    level: str

class GengerName(Enum):
	MAN = "Мужской"	
	FEMALE = "Женский"	

class GengerID(Enum):
	MAN = "male"	
	FEMALE = "female"	

class Gender(NamedTuple):
    ID: GengerID
    name: GengerName

class LocaleName(Enum):
    """Язык заполнения резюме"""
    RUSSIAN = "Русский"
    ENGLISH = "English"

class LocaleId(Enum):
    """Язык заполнения резюме"""
    RU = "RU"
    EN = "EN"

class Locale(NamedTuple):
    """Язык заполнения резюме"""
    ID: LocaleId
    name: LocaleName

class AccessName(Enum):
    NO_ONE = "не видно никому"
    WHITELIST = "видно выбранным компаниям"
    BLACKLIST = "скрыто от выбранных компаний"
    CLIENTS = "видно всем компаниям, зарегистрированным на HeadHunter"
    EVERYONE = "видно всему интернету"
    DIRECT = "доступно только по прямой ссылке"

class AccessId(Enum):
    NO_ONE = "no_one"
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"
    CLIENTS = "clients"
    EVERYONE = "everyone"
    DIRECT = "direct"

class Access(NamedTuple):
    ID: AccessId
    name: AccessName

class Phone(NamedTuple):
    country: int
    city: int
    number: int
    formatted: int

class Contact(NamedTuple):
    email: str
    phone: Phone

class Area(NamedTuple):
	ID: int
	name: str
	url: str

class Currency(Enum):
    EURO = "EUR"
    RUB = "RUR"
    USD = "USD"

class Salary(NamedTuple):
    amount: int
    currency: Currency

class ScheduleName(Enum):
    FULLDAY = "Полный день"
    SHIFT = "Сменный график"
    FLEXIBLE = "Гибкий график"
    REMOTE = "Удаленная работа"
    FLYINFLYOUT = "Вахтовый метод"


class Schedule(NamedTuple):
    ID: str
    name: str

class TravelTimeName(Enum):
    ANY = "Не имеет значения"
    LESS_THAN_HOUR = "Не более часа"
    FROM_HOUR_TO_ONE_AND_HALF = "Не более полутора часов"

class TravelTimeID(Enum):
    ANY = "any"
    LESS_THAN_HOUR = "less_than_hour"
    FROM_HOUR_TO_ONE_AND_HALF = "from_hour_to_one_and_half"

class TravelTime(NamedTuple):
    ID: str
    name: str



@dataclass
class Resume:
    last_name: str
    first_name: str
    middle_name: str
    title: str
    area: Area
    salary: Salary
    gender: Gender
    locale: Locale
    skills_descr: str 
    citizenship: Area 
    access: Access
    contact: Contact
    education: str
    employment: Employment
    # experience: str ##
    language: Language
    schedule: Schedule ##
    travel_time: str ## время на дорогу
    business_trip_readiness: str ## командировки
    skills_set : set() # ключевые навыки
    proffessionl_roles: str
    birth_date: date

def save_to_json(filename, data:list[dict] | dict) -> None:
    with open(f"JSON/{filename}", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved json-file: {filename}")

test_resume_list = [Resume(last_name='Юношев', first_name='Ярослав', middle_name=None, title='Игра', area=Area(ID='1', name='Москва', url='https://api.hh.ru/areas/1'), salary=Salary(amount=200000, currency='RUR'), gender=Gender(ID='male', name='Мужской'), locale=Locale(ID='RU', name='Русский'), skills_descr='Lorem  ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', citizenship=[Area(ID='113', name='Россия', url='https://api.hh.ru/areas/113'), Area(ID='2511', name='Шри-Ланка', url='https://api.hh.ru/areas/2511')], access=Access(ID='direct', name='доступно только по прямой ссылке'), contact=Contact(email='', phone=Phone(country='7', city='978', number='6706890', formatted='+7 (978) 670-68-90')), education='', employment=Employment(ID='project', name='Проектная работа'), language=[Language(ID=LanguageId(ID='rus', name='Русский'), level=LanguageLevel(ID='l1', name='Родной'))], schedule='', travel_time='', business_trip_readiness='', skills_set=['Продажи', 'Настройка рекламы', 'Внимательность', 'Знание латинского языка'], proffessionl_roles='', birth_date=''),
Resume(last_name='Юношев', first_name='Ярослав', middle_name=None, title='Второе резюме', area=Area(ID='1', name='Москва', url='https://api.hh.ru/areas/1'), salary=Salary(amount=200000, currency='RUR'), gender=Gender(ID='male', name='Мужской'), locale=Locale(ID='RU', name='Русский'), skills_descr='Lorem  ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', citizenship=[Area(ID='113', name='Россия', url='https://api.hh.ru/areas/113'), Area(ID='2511', name='Шри-Ланка', url='https://api.hh.ru/areas/2511')], access=Access(ID='direct', name='доступно только по прямой ссылке'), contact=Contact(email='', phone=Phone(country='7', city='978', number='6706890', formatted='+7 (978) 670-68-90')), education='', employment=Employment(ID='project', name='Проектная работа'), language=[Language(ID=LanguageId(ID='rus', name='Русский'), level=LanguageLevel(ID='l1', name='Родной'))], schedule='', travel_time='', business_trip_readiness='', skills_set=['Продажи', 'Настройка рекламы', 'Внимательность', 'Знание латинского языка'], proffessionl_roles='', birth_date=''),
Resume(last_name='Юношев', first_name='Ярослав', middle_name=None, title='Третье', area=Area(ID='1', name='Москва', url='https://api.hh.ru/areas/1'), salary=Salary(amount=200000, currency='RUR'), gender=Gender(ID='male', name='Мужской'), locale=Locale(ID='RU', name='Русский'), skills_descr='Lorem  ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', citizenship=[Area(ID='113', name='Россия', url='https://api.hh.ru/areas/113'), Area(ID='2511', name='Шри-Ланка', url='https://api.hh.ru/areas/2511')], access=Access(ID='direct', name='доступно только по прямой ссылке'), contact=Contact(email='', phone=Phone(country='7', city='978', number='6706890', formatted='+7 (978) 670-68-90')), education='', employment=Employment(ID='project', name='Проектная работа'), language=[Language(ID=LanguageId(ID='rus', name='Русский'), level=LanguageLevel(ID='l1', name='Родной'))], schedule='', travel_time='', business_trip_readiness='', skills_set=['Продажи', 'Настройка рекламы', 'Внимательность', 'Знание латинского языка'], proffessionl_roles='', birth_date=''),
Resume(last_name='Юношев', first_name='Ярослав', middle_name=None, title='И еще одно', area=Area(ID='1', name='Москва', url='https://api.hh.ru/areas/1'), salary=Salary(amount=200000, currency='RUR'), gender=Gender(ID='male', name='Мужской'), locale=Locale(ID='RU', name='Русский'), skills_descr='Lorem  ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', citizenship=[Area(ID='113', name='Россия', url='https://api.hh.ru/areas/113'), Area(ID='2511', name='Шри-Ланка', url='https://api.hh.ru/areas/2511')], access=Access(ID='direct', name='доступно только по прямой ссылке'), contact=Contact(email='', phone=Phone(country='7', city='978', number='6706890', formatted='+7 (978) 670-68-90')), education='', employment=Employment(ID='project', name='Проектная работа'), language=[Language(ID=LanguageId(ID='rus', name='Русский'), level=LanguageLevel(ID='l1', name='Родной'))], schedule='', travel_time='', business_trip_readiness='', skills_set=['Продажи', 'Настройка рекламы', 'Внимательность', 'Знание латинского языка'], proffessionl_roles='', birth_date=''),
]

def load_data_from_json(filename: str) -> dict | list[dict]:
    data = json.load(open(filename, "r"))
    return data