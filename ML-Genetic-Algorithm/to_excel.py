from pandas import *
import random
from datetime import datetime

def create_table(data):
	writer = pandas.ExcelWriter("../Analys/run_{}.xlsx".format(datetime.now().strftime('%H.%M_%d-%m-%Y')))
	df = pandas.DataFrame()
	df.to_excel(writer)
	writer.save()
	return writer, df
	
def write_to_excel(df, writer, data):
	df2 = pandas.DataFrame(data)
	result = df.append(df2)
	result.to_excel(writer)
	writer.save()
	return result
