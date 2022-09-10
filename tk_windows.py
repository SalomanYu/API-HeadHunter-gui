from tkinter import *
from tkinter import ttk

from tkhtmlview import HTMLLabel
from config import Schedule, ScheduleName, TravelTimeName, VacancyResponse, font, load_data_from_json,  CLIENT_ID
from api_requests import validate_user_data, validate_user_token, get_resumes, get_actived_responses, get_vacancies, Table


def welcome_window(incorrent_token: bool = False):
	window = Tk()
	window.geometry("600x200")

	welcome = Label(text="Вставьте токен пользователя", font=font(24))
	welcome.grid(row=0, column=0, sticky="n")

	token_input = Entry(font=font(15))
	token_input.grid(row=1, column=0, pady=15, ipadx=100)

	continue_btn = Button(text="Продолжить", font=font(15), command= lambda: validate_user_token(window, token=token_input.get()))
	continue_btn.grid(row=2, column=0)

	if incorrent_token:
		error_label = Label(text="Неправильный токен!", fg="red")
		error_label.grid(row=3)
		get_token_label = HTMLLabel(window, html=f"Нет токена? <a href='https://hh.ru/oauth/authorize?response_type=code&client_id={CLIENT_ID}' style='font-size:13px;'>Получить </a>")
		get_token_label.grid(row=4, column=0)
	else:
		get_token_label = HTMLLabel(window, html=f"Нет токена? <a href='https://hh.ru/oauth/authorize?response_type=code&client_id={CLIENT_ID}' style='font-size:13px;'>Получить </a>")
		get_token_label.grid(row=3, column=0)

	window.mainloop()


def show_success_window(old_win: Tk = ""):
	if old_win: old_win.destroy()

	window = Tk(className="Имя пользователя")
	window.geometry("600x400")

	my_resumes_btn = Button(text="Мои резюме", font=font(15), command=lambda :resumes_window(window, command=0))
	my_resumes_btn.pack(pady=20, fill=X)

	update_resumes_btn = Button(text="Обновить резюме", font=font(15), command= lambda: resumes_window(window, command=1))
	update_resumes_btn.pack(pady=20, fill=X)

	create_resume_btn = Button(text="Создать резюме", font=font(15), command=resumes_window)
	create_resume_btn.pack(pady=20, fill=X)

	vacancies_btn = Button(text="Посмотреть вакансии", font=font(15), command=lambda : show_vacancies_window(old_win=window))
	vacancies_btn.pack(pady=20, fill=X)

	responses_btn = Button(text="Мои отклики", font=font(15), command=lambda: show_my_responses(old_win=window))
	responses_btn.pack(pady=20, fill=X)

	window.mainloop()


def resumes_window(old_win: Tk, command:int = ""):
	old_win.destroy()
	win = Tk()
	win.geometry("600x400")

	# resume_titles = [item['title'] for item in get_resumes(token=USER_TOKEN)]
	btn_comeback = Button(text="Назад", command=lambda : show_success_window(old_win=win))
	btn_comeback.pack()

	resume_titles = [item.title for item in get_resumes()]
	listbox = Listbox(width=600, height=400)
	listbox.pack()
	listbox.bind('<Double-1>', lambda ev: _select_resume_by_list(win, listbox, resume_titles, command))

	for item in resume_titles:
		listbox.insert(0,0, item)
	
	win.mainloop()

def _select_resume_by_list(win:Tk, listbox, titles, command):
	collections = listbox.curselection()
	win.quit()
	win.destroy()
	if command == 0: show_more_info_about_resume(title_resume = titles[-collections[0]-1])
	elif command == 1: 
		edit_resume_window(title_resume=titles[-collections[0]-1])


def show_more_info_about_resume(title_resume: str):
	resume = [resume for resume in get_resumes() if resume.title == title_resume][0]
	
	win = Tk()
	win.geometry("800x600")
	win.title(resume.title)

	btn_comeback = Button(text="Назад", command=lambda : show_success_window(old_win=win))
	btn_comeback.pack()

	frame = Frame(win)
	frame.pack()

	name_label = Label(frame, text='Имя:', font=font(15)).grid(column=0, row=0)
	name = Label(frame, text=resume.first_name, font=font(15)).grid(column=1, row=0)

	last_name_label = Label(frame, text='Фамилия:', font=font(15)).grid(column=0, row=1)
	last_name = Label(frame, text=resume.last_name, font=font(15)).grid(column=1, row=1)

	middle_name_label = Label(frame, text='Отчество:', font=font(15)).grid(column=0, row=2)
	middle_name = Label(frame, text=resume.middle_name, font=font(15)).grid(column=1, row=2)
	
	area_label = Label(frame, text='Город:', font=font(15)).grid(column=0, row=3)
	area = Label(frame, text=resume.area.name, font=font(15)).grid(column=1, row=3)
	
	salary_label = Label(frame, text='Желаемая зарплата:', font=font(15)).grid(column=0, row=4)
	salary = Label(frame, text=f"{resume.salary.amount} {resume.salary.currency}", font=font(15)).grid(column=1, row=4)
	
	gender_label = Label(frame, text='Пол:', font=font(15)).grid(column=0, row=5)
	gender = Label(frame, text=resume.gender.name, font=font(15)).grid(column=1, row=5)
	
	descr_label = Label(frame, text='Обо мне:', font=font(15)).grid(column=0, row=6)
	descr = Label(frame, text=resume.skills_descr, width=30, font=font(15)).grid(column=1, row=6)
	
	citizenship_label = Label(frame, text='Гражданство:', font=font(15)).grid(column=0, row=7)
	citizenship = Label(frame, text=" ; ".join([item.name for item in resume.citizenship]), font=font(15)).grid(column=1, row=7)
	
	access_label = Label(frame, text='Видимость:', font=font(15)).grid(column=0, row=8)
	access = Label(frame, text=resume.access.name, font=font(15)).grid(column=1, row=8)
	
	employment_label = Label(frame, text='Занятность:', font=font(15)).grid(column=0, row=9)
	employment = Label(frame, text=resume.employment.name, font=font(15)).grid(column=1, row=9)
	
	language_label = Label(frame, text='Знание языков:', font=font(15)).grid(column=0, row=10)
	languages = Label(frame, text=" ; ".join([item.ID.name + " " + item.level.name for item in resume.language]), font=font(15)).grid(column=1, row=10)
	
	skills_label = Label(frame, text='Навыки:', font=font(15)).grid(column=0, row=11)
	skills = Label(frame, text=" ; ".join([item for item in resume.skills_set]), font=font(15)).grid(column=1, row=11)
	
	contact_label = Label(frame, text='Контакты:', font=font(15)).grid(column=0, row=12)
	contacts = Label(frame, text=resume.contact.phone.formatted, font=font(15)).grid(column=1, row=12)

	win.mainloop()


def edit_resume_window(title_resume: str):
	resume = [resume for resume in get_resumes() if resume.title == title_resume][0]
	win = Tk()
	win.geometry("800x600")
	win.title(resume.title)

	btn_comeback = Button(text="Назад", command=lambda : show_success_window(old_win=win))
	btn_comeback.pack()

	frame = Frame(win)
	frame.pack()

	name_label = Label(frame, text='*Имя:', font=font(15)).grid(column=0, row=0)
	name = Entry(frame, font=font(15))
	name.insert(0,resume.first_name)
	name.grid(column=1, row=0)

	last_name_label = Label(frame, text='*Фамилия:', font=font(15)).grid(column=0, row=1)
	last_name = Entry(frame, font=font(15))
	last_name.insert(0, resume.last_name)
	last_name.grid(column=1, row=1)

	middle_name_label = Label(frame, text='Отчество:', font=font(15)).grid(column=0, row=2)
	middle_name = Entry(frame, font=font(15))
	try:middle_name.insert(0,resume.middle_name)
	except: ...
	
	middle_name.grid(column=1, row=2)

	area_label = Label(frame, text='*Город:', font=font(15)).grid(column=0, row=3)
	area = Entry(frame, font=font(15))
	area.insert(0,resume.area.name)
	area.grid(column=1, row=3)

	salary_label = Label(frame, text='Желаемая зарплата:', font=font(15)).grid(column=0, row=4)
	salary = Entry(frame, font=font(15))
	salary.insert(0,f"{resume.salary.amount}")
	salary.grid(column=1, row=4)

	currency_label = Label(frame, text='Валюта:', font=font(15)).grid(column=0, row=5)
	currency_values = [item['code'] for item in load_data_from_json(filename="../JSON/guide.json")['currency']]
	currency = ttk.Combobox(frame, values=currency_values).grid(column=1, row=5)

	gender_label = Label(frame, text='*Пол:', font=font(15)).grid(column=0, row=6)
	gender = Entry(frame, font=font(15))
	gender.insert(0,resume.gender.name)
	gender.grid(column=1, row=6)

	descr_label = Label(frame, text='*Обо мне:', font=font(15)).grid(column=0, row=7)
	descr = Entry(frame, font=font(15))
	descr.insert(0,resume.skills_descr)
	descr.grid(column=1, row=7)
	
	citizenship_label = Label(frame, text='*Гражданство:', font=font(15)).grid(column=0, row=8)
	citizenship = Entry(frame, font=font(15))
	citizenship.insert(0," ; ".join([item.name for item in resume.citizenship]))
	citizenship.grid(column=1, row=8)

	access_label = Label(frame, text='*Видимость:', font=font(15)).grid(column=0, row=9)
	access = Entry(frame, font=font(15))
	access.insert(0,resume.access.name)
	access.grid(column=1, row=9)

	employment_label = Label(frame, text='*Занятность:', font=font(15)).grid(column=0, row=10)
	employment = Entry(frame, font=font(15))
	employment.insert(0,resume.employment.name)
	employment.grid(column=1, row=10)

	language_label = Label(frame, text='*Знание языков:', font=font(15)).grid(column=0, row=11)
	languages = Entry(frame, font=font(15))
	languages.insert(0," ; ".join([item.ID.name + " " + item.level.name for item in resume.language]))
	languages.grid(column=1, row=11)

	skills_label = Label(frame, text='Навыки:', font=font(15)).grid(column=0, row=12)
	skills = Entry(frame, font=font(15))
	skills.insert(0," ; ".join([item for item in resume.skills_set]))
	skills.grid(column=1, row=12)

	contact_label = Label(frame, text='*Контакты:', font=font(15)).grid(column=0, row=13)
	contacts = Entry(frame, font=font(15))
	contacts.insert(0,resume.contact.phone.formatted)
	contacts.grid(column=1, row=13)

	title_label = Label(frame, text='Название резюме:', font=font(15)).grid(column=0, row=13)
	title = Entry(frame, font=font(15))
	title.insert(0,resume.title)
	title.grid(column=1, row=14)

	schedule_label = Label(frame, text='График работы:', font=font(15)).grid(column=0, row=15)
	schedule_values = [item.value for item in ScheduleName]
	schedule = ttk.Combobox(frame, values=schedule_values).grid(column=1, row=15)

	travel_time_label = Label(frame, text='Желательное время в пути до работы:', font=font(15)).grid(column=0, row=16)
	travel_time_values = [item.value for item in TravelTimeName]
	travel_time = ttk.Combobox(frame, values=travel_time_values).grid(column=1, row=16)


	business_trip_readiness_label = Label(frame, text='*Разрешение на работу:', font=font(15)).grid(column=0, row=17)
	business_trip_readiness = Entry(frame, font=font(15))
	business_trip_readiness.insert(0," ; ".join([item.name for item in resume.business_trip_readiness]))
	business_trip_readiness.grid(column=1, row=17)


	save_btn = Button(frame, text='Обновить', font=font(18), command= lambda : validate_user_data(data=resume))
	save_btn.grid(column=1, row=18, pady=15)


def show_my_responses(old_win: Tk):
	old_win.destroy()
	
	responses = get_actived_responses()
	table_rows = [("Вакансия", "Резюме", "Статус")]
	for res in responses['items']:
		try: vacance = res['vacancy']['name']
		except: vacance = ''
		try: resume = res['resume']['title']
		except: resume = ''
		if resume:table_rows.append((vacance, resume, res['state']['name']))
		

	win = Tk()
	table = Table(win, total_rows=len(table_rows), total_columns=len(table_rows[0]), employee_list=table_rows)
	win.mainloop()


def show_vacancies_window(old_win: Tk):
	old_win.destroy()
	
	vacancies = get_vacancies()	  
	table_rows = [('Вакансия', 'Зарплата', "Валюта", "Город", "Индетификатор")]
	for vac in vacancies['items']:
		# print(vac['name'], vac['salary']['to'], vac['salary']['currency'], vac['area']['name'], vac['id'])
		table_rows.append((vac['name'], vac['salary']['to'], vac['salary']['currency'], vac['area']['name'], vac['id']))
	
	win = Tk()

	table = Table(win, total_rows=len(table_rows), total_columns=len(table_rows[0]), employee_list=table_rows, vacancies=True)
	win.mainloop()