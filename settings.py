import gspread

token = '8647685951:AAFVw_iEYUg_tJNwqHRwDecxY5QAu10G99w'

google_client = gspread.service_account(filename='creds.json')

table_url = 'https://docs.google.com/spreadsheets/d/1U5PSD4R1B1Gp8hNoVu3VXzV1_0ftp2-KUSqQ_K760us/edit?usp=sharing'
test_url = 'https://docs.google.com/spreadsheets/d/1Rpz280-yrG8exkESZXUhTw4hKYq0K3h4zGgWbAflbkA/edit?usp=sharing'