# pages/views.py
from django.http import HttpResponse
import gspread
import pandas as pd
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials


def homePageView(request):

	# defining the scope of the application
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

	#credentials to the account
	cred = ServiceAccountCredentials.from_json_keyfile_name('auth.json',scope)

	# authorize the clientsheet
	client = gspread.authorize(cred)

	#open spreadsheet and specific sheet
	wks = client.open("Test Data umSoccer Test").sheet1

	#wks.update('A1', "test_ian_fin") 
	df = pd.DataFrame(wks.get_all_records())
	df.head()

	return HttpResponse(df["Event Date"][0])

def get_all_data(request):
    data =pd.DataFrame(np.random.randn(20, 5)) 

    render(request, 'template.html', {'data': data.to_html()})