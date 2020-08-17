from tkinter import * 
from tkinter import ttk
from bs4 import BeautifulSoup
from PIL import ImageTk, Image 
import requests
import datetime


#reading lines of databse and extracting url
file = open('database.txt', 'r').readlines()
url = str(file[0])

#requesting url, initializing soup with parser
try:
	res = requests.get(url)
except:
	print(("Couldn't request information, check your internet and browser.").upper())

#storing content and defining soup
soup = BeautifulSoup(res.content, 'html.parser')


#storing elements
day = soup.find(id='WxuCurrentConditions-main-b3094163-ef75-4558-8d9a-e35e6b9b1034')
items = day.find_all(class_ = '_-_-components-src-organism-CurrentConditions-CurrentConditions--CurrentConditions--1XEyg')
location = items[0].find(class_='_-_-components-src-organism-CurrentConditions-CurrentConditions--location--1YWj_').get_text()
update = items[0].find(class_='_-_-components-src-organism-CurrentConditions-CurrentConditions--timestamp--1ybTk').get_text()
temp = items[0].find(class_='_-_-components-src-organism-CurrentConditions-CurrentConditions--tempValue--MHmYY').get_text()
forecast = items[0].find(class_='_-_-components-src-organism-CurrentConditions-CurrentConditions--phraseValue--mZC_p').get_text()

try:
	warning = items[0].find(class_='_-_-components-src-organism-CurrentConditions-CurrentConditions--precipValue--2aJSf').get_text()
except:
	pass

high_low = items[0].find(class_='_-_-components-src-organism-CurrentConditions-CurrentConditions--tempHiLoValue--3T1DG').get_text()

quality = soup.find(id='WxuAirQuality-sidebar-aa4a4fb6-4a9b-43be-9004-b14790f57d73')
items1 = quality.find_all(class_ = 'card _-_-components-src-molecule-Card-Card--card--2AzRg')
quality_title = items1[0].find(class_='_-_-components-src-molecule-Card-Card--cardHeading--2H1-_').get_text()
index = items1[0].find(class_='_-_-components-src-molecule-DonutChart-DonutChart--innerValue--3_iFF').get_text()
quality_type = items1[0].find(class_='_-_-components-src-molecule-AirQualityText-AirQualityText--severity--1smy9').get_text()
description = items1[0].find(class_='_-_-components-src-molecule-AirQualityText-AirQualityText--severityText--1wSKp').get_text()

details = soup.find(id='WxuTodayDetails-main-fd88de85-7aa1-455f-832a-eacb037c140a')
items2 = details.find_all(class_ = 'card _-_-components-src-molecule-Card-Card--card--2AzRg _-_-components-src-organism-TodayDetailsCard-TodayDetailsCard--todaysDetailsCard--2yzWB')
wind = items2[0].find(class_='_-_-components-src-atom-WeatherData-Wind-Wind--windWrapper--3Ly7c undefined').get_text()
humidity = items2[0].find('span', {'data-testid':'PercentageValue'}).get_text()
pressure = items2[0].find('span', {'data-testid':'PressureValue'}).get_text()
uv = items2[0].find('span', {'data-testid':'UVIndexValue'}).get_text()
visibility = items2[0].find('span', {'data-testid':'VisibilityValue'}).get_text()

#stores current date
date = datetime.date.today()


#initializing tkinter with master as root
root = Tk()
root.title('Weather Forecast App') 
root.configure(bg='white')


#weather images
image_list = {
	'cloudy': ImageTk.PhotoImage(Image.open('cloudy.png')),
	'rain' : ImageTk.PhotoImage(Image.open('rain.png')),
	'thunderstorm' : ImageTk.PhotoImage(Image.open('thunderstorms.png')),
	'partly cloudy' : ImageTk.PhotoImage(Image.open('partly_cloudy.png')),
	'showers' : ImageTk.PhotoImage(Image.open('rain_light.png')),
	'cloudy rain' : ImageTk.PhotoImage(Image.open('rain_s_cloudy.png')),
	'sunny' : ImageTk.PhotoImage(Image.open('sunny.png')),
	'cloudy sun' : ImageTk.PhotoImage(Image.open('sunny_s_cloudy.png'))
}



#selects image based on forecast
def ImageSelector(images, forecast):
	if forecast == 'Cloudy':
		image = images['cloudy']
	elif forecast == 'Partly Cloudy' or forecast == 'Mostly Cloudy':
		image = images['partly cloudy']
	elif forecast == 'Rain':
		image = images['rain']
	elif forecast == 'Scattered Thunderstorms' or forecast == 'Thunderstorms':
		image = images['thunderstorm']
	elif forecast == 'Sunny' or forecast == 'Clear':
		image = images['sunny']
	elif forecast == 'Showers':
		image = images['showers']
	elif forecast == 'Chance of Showers' or forecast == 'Isolated Thunderstorms':
		image = images['cloudy rain']
	elif forecast == 'Mostly Sunny' or 'Mostly Clear':
		image = images['cloudy sun']
	else:
		image = images['partly cloudy']
	
	return image


#stores output of function
selected_image = ImageSelector(image_list, forecast)


#changes location and replaces url in database
def clicked():
	res = 'Please restart the program.'
	Label(root, bg='white', text=res, font=('Comic Sans MS', 15, 'underline', 'bold')).grid(row=16, column=0, columnspan=2, pady=5)
	new_url = str(new_location.get())
	lines = open('database.txt', 'r').readlines()
	lines[0] = new_url
	
	file = open('database.txt', 'w')
	for line in lines:
		file.write(line)
	file.close()


#shows and hides extra content
def ShowAirInfo():
	global air_info_hider  
	if air_info_hider:
		des.grid(row=9, column=0, columnspan=2, padx=10)
		air_info_hider = False
	else:
		des.grid_remove()
		air_info_hider = True


#elements
des = Label(root, bg='white', text=description, font=('Comic Sans MS', 10))
air_info_hider = True


#shows how to add a new location
def LearnMore():
	global learn_more_hider
	if learn_more_hider:
		info.grid(row=18, column=0, columnspan=2, padx=10, pady=10)
		learn_more_hider = False
	else:
		info.grid_remove()
		learn_more_hider = True


#elements
info = Label(root, bg='white', text='To add a new location a url is needed from the "Today" page in weather.com with the seleced location', font=('Comic Sans MS', 10))
learn_more_hider = True


#input for new location
def ShowLocation():	
	global location_hider
	if location_hider:
		new_location.grid(row=14, column=0, columnspan=2, padx=10)
		location_button.grid(row=15, column=0, columnspan=2, pady=5)
		learn_more_button.grid(row=16, column=0, columnspan=2)
		location_hider = False
	else:
		new_location.grid_remove()
		location_button.grid_remove()
		location_hider = True

location_hider = True

#elements
learn_more_button = Checkbutton(root, bg='white', text='Learn More', command=LearnMore, font=('Comic Sans MS', 15))
new_location = Entry(root, width=48, bg='white', font=('Comic Sans MS', 12))
new_location.insert(0,'Enter the url for new location here.')
location_button = Button(root, width=10, bg='white', text='Enter', font=('Comic Sans MS', 10), command=clicked)



#elements
Label(root, bg='white', fg='Green', text='Weather Forecast App', font=('Comic Sans MS', 30, 'underline', 'bold')).grid(row=0, column=0, columnspan=2, padx=20)  

Label(root, bg='white', fg='LightGreen', text=location, font=('Comic Sans MS', 15, 'underline')).grid(row=2, column=0, padx=10, columnspan=2)

Label(root, bg='white', text=str(date), font=('Comic Sans MS', 10, 'bold')).grid(row=3, column=0, columnspan=2)

image_label = Label(root, bg='white', image=selected_image).grid(column=0, row=4)

Label(root, bg='white', text=temp, font=('Comic Sans MS', 50)).grid(column=1, row=4)

Label(root, bg='white', fg='Orange', text=forecast, font=('Comic Sans MS', 15, 'bold')).grid(column=0, row=5)

#checks for warning 
try:
	Label(root, bg='white', fg='Red', text=warning, font=('Comic Sans MS', 15, 'bold')).grid(column=0, row=6, columnspan=2)
except:
	Label(root, bg='white', fg='Red', text='No Warnings', font=('Comic Sans MS', 15)).grid(column=0, row=6, columnspan=2)

Label(root, bg='white', fg='LightBlue', text='High/Low : ' + high_low, font=('Comic Sans MS', 15, 'bold')).grid(column=1, row=5)

Label(root, bg='white', text=quality_title + ' : ' + index, font=('Comic Sans MS', 15)).grid(column=1, row=7)

Label(root, bg='white', text='Air Quality : ' + quality_type, font=('Comic Sans MS', 15)).grid(column=0, row=7)

Checkbutton(root, bg='white', text='Learn more about the air quality:', command=ShowAirInfo, font=('Comic Sans MS', 15)).grid(row=8, column=0, columnspan=2)

Label(root, bg='white', text='Wind: ' + wind, font=('Comic Sans MS', 15)).grid(column=0, row=10)

Label(root, bg='white', text='Humidity: ' + humidity, font=('Comic Sans MS', 15)).grid(column=1, row=10)

Label(root, bg='white', text='Pressure: ' + pressure, font=('Comic Sans MS', 15)).grid(column=0, row=11)

Label(root, bg='white', text='UV Index: ' + uv, font=('Comic Sans MS', 15)).grid(column=1, row=11)

Label(root, bg='white', text='Visibility: ' + visibility, font=('Comic Sans MS', 15)).grid(column=0, row=12, columnspan=2)

Checkbutton(root, bg='white', text='Choose different location?', command=ShowLocation, font=('Comic Sans MS', 15)).grid(row=13, column=0, columnspan=2)


#only runs if this is the main file being run
if __name__ == '__main__':
	root.mainloop()

