import requests
from datetime import datetime

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%y")
api_url_telegram = "https://api.telegram.org/bot1566836970:AAG7CT4lQ6Z1KgA7pRQLRvCNNjqLxKL3CPg/sendMessage?chat_id=-1001314831324&text="
group_id = ""
dist_id = [363]

def fetch_data_from_cowin(district_id):
    query_params = "?district_id={}&date={}".format(district_id,today_date)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}
    final_url = base_cowin_url+query_params
    response = requests.get(final_url, headers=headers)
    extract_availability_data(response)


def fetch_data_for_district(district_ids):
    for district_id in district_ids:
        fetch_data_from_cowin(district_id)

def extract_availability_data(response):
    response_json = response.json()
    #for center in response_json["centers"]:
    for session in response_json["sessions"]:
        if session["available_capacity"] > 0:
            message = "Pin code : {} \n\nAge Group : {} \nCenter Name : {} \n\nDose 1 Available Capacity : {} \nDose 2 Available Capacity : {} \n\nFee : ₹{} \nVaccine : {} \n\nCowin : https://selfregistration.cowin.gov.in/".format(session["pincode"],session["min_age_limit"],session["name"],session["available_capacity_dose1"],session["available_capacity_dose2"],session["fee"],session["vaccine"])
            send_message_telegram(message)

def send_message_telegram(message):
    final_telegram_url = api_url_telegram
    final_telegram_url = final_telegram_url + message
    response = requests.get(final_telegram_url)
    print(response)


if __name__== "__main__":
    fetch_data_for_district(dist_id)
