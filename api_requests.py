from tkinter import Tk, Button, END, Entry
import requests
from time import sleep
from config import *
import tk_windows


def validate_user_token(win: Tk, token: str):
	USER_HEADERS = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/x-www-form-urlencoded",
    "grant_type": "authorization_code",
	}

	req = requests.get("https://api.hh.ru/resumes/mine", headers=USER_HEADERS)
	
	win.destroy()
	sleep(0.5)
	
	if req.status_code == 200:
		global USER_TOKEN
		USER_TOKEN = token 
		tk_windows.show_success_window()
	else: 
		tk_windows.welcome_window(incorrent_token=True)


def get_resumes(token: str = ""):
	USER_HEADERS = {
    	"Authorization": f"Bearer {USER_TOKEN}",
	    "Content-Type": "application/x-www-form-urlencoded",
	    "grant_type": "authorization_code",
	}
	req = requests.get("https://api.hh.ru/resumes/mine", headers=USER_HEADERS)
	if req.status_code != 200:return

	short_resume_info = req.json() 
	if short_resume_info:
		# resumes = parse_resume([resume['id'] for resume in short_resume_info['items']])
		resumes = [parse_resume(resume['id']) for resume in short_resume_info['items']]
		return resumes
	else: return


def parse_resume(resume_id: str):
	USER_HEADERS = {
    	"Authorization": f"Bearer {USER_TOKEN}",
	    "Content-Type": "application/x-www-form-urlencoded",
	    "grant_type": "authorization_code",
	}
	
	req = requests.get(f"https://api.hh.ru/resumes/{resume_id}", headers=USER_HEADERS)
	if req.status_code != 200: 
		print(req.json())
		return

	# save_to_json(f"resume_{resume_id}.json", req.json())
	resume = parse_json(data=req.json())
	return resume

def parse_json(data: dict | list[dict]) -> Resume:
    gender = Gender(ID=data["gender"]["id"], name=data["gender"]["name"])
    try:salary = Salary(amount=data['salary']['amount'], currency=data['salary']['currency'])
    except: salary = Salary(amount=0, currency="RUR")
    photo = data['photo']
    area = Area(ID=data['area']['id'], name=data['area']['name'], url=data['area']['url'])

    resume_locale = Locale(ID=data['resume_locale']['id'], name=data['resume_locale']['name'])
    descr = data['skills']
    citizenship = [Area(item['id'], item['name'], item['url']) for item in data['citizenship']]
    employment = Employment(ID=data['employment']['id'], name=data['employment']['name'])
    access = Access(ID=data['access']['type']['id'], name=data['access']['type']['name'])

    contact = Contact(email='', phone=Phone(
        country=data['contact'][0]['value']['country'],
        city=data['contact'][0]['value']['city'],
        number=data['contact'][0]['value']['number'],
        formatted=data['contact'][0]['value']['formatted']))

    language = [Language(
        ID=LanguageId(
            ID=lang['id'],
            name=lang['name']
        ),
        level=LanguageLevel(
            ID=lang['level']['id'],
            name=lang['level']['name'],
        )
    ) for lang in data['language']]

    return Resume(
        last_name=data['last_name'],
        first_name=data['first_name'],
        middle_name=data['middle_name'],
        title=data['title'],
        area=area,
        salary=salary,
        gender=gender,
        locale=resume_locale,
        skills_descr=descr,
        citizenship=citizenship,
        access=access,
        contact=contact,
        language=language,
        schedule='',
        travel_time='',
        business_trip_readiness='',
        skills_set=data['skill_set'],
        proffessionl_roles='',
        birth_date='',
        employment=employment,
        education=''
    )


def validate_user_data(data: Resume) -> bool:
    ...


def get_actived_responses(): # список активных откликов
    req = requests.get("https://api.hh.ru/negotiations", headers=USER_HEADERS) 
    return req.json()
    # save_to_json("responses.json", data=req.json())


def get_vacancies():
    req = requests.get("https://api.hh.ru/vacancies/", headers=USER_HEADERS)
    # save_to_json("vacancies.json", data=req.json())
    return req.json()


def set_response_to_vacance(event, vacance_id):
    resume_id = "58909510ff0b3ea2730039ed1f52566243704f"
    responce_data = {
        "Content-Type": "multipart/form-data",
        "vacancy_id": str(vacance_id),
        "resume_id": resume_id
    }
    req = requests.post("https://api.hh.ru/negotiations", headers=USER_HEADERS, data=responce_data)
    
    if req.status_code != 201:
        quit()
    else: print("Success")


class Table:
    # Initialize a constructor
    def __init__(self, gui, total_rows, total_columns, employee_list, vacancies=False):

        # An approach for creating the table
        for i in range(total_rows):
            for j in range(total_columns):
                if i ==0:
                    self.entry = Entry(gui, width=20, bg='LightSteelBlue',fg='Black',
                                       font=('Arial', 16, 'bold'))
                else:
                    self.entry = Entry(gui, width=20, fg='blue',
                               font=('Arial', 14, ''))

                self.entry.grid(row=i, column=j)
                if employee_list[i][j] != None:
                    self.entry.insert(END, employee_list[i][j])
                else:
                    self.entry.insert(END, "")
            if vacancies and i != 0:
                self.btn = Button(text="Откликнуться")
                self.btn.bind("<Button-1>", lambda event, value=employee_list[i][j]: set_response_to_vacance(event, value))
                self.btn.grid(row=i, column=total_columns+1)
        
        btn_comeback = Button(text="Меню", font=font(16), width=40, command=lambda : tk_windows.show_success_window(old_win=gui))
        btn_comeback.grid(row=i+1, column=total_columns//2,)