import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY="HPX1BO9B6TO3DVOX"

TWILIO_SID ="AC60595cef50f52688c7bdec2112342600"
TWILIO_API_KEY="c9d059b0b7d9886029ea17a1905b49ef"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY="cd75e5e2ea4c4117b2d29ea19c6a2ce1"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

stock_params={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY

}
response=requests.get(STOCK_ENDPOINT,params=stock_params)
data=response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in data.items()]
yesterday_data= data_list[0]
yesterday_closing_price= yesterday_data["4. close"]
print(yesterday_closing_price)
#Get the day before yesterday's closing stock price
day_before_yestarday= data_list[1]
day_before_yesterday_closing_price= day_before_yestarday["4. close"]
print(day_before_yesterday_closing_price)
#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference >0:
    up_down= "up"
else:
    up_down="dowm"
print(difference)
#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
difference_percentage = round((difference/float(yesterday_closing_price))*100)
print(difference_percentage)
#If TODO4 percentage is greater than 5 then print("Get News").
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
## STEP 2: https://newsapi.org/

if abs(difference_percentage) >1:
    news_params={
        "apiKey":NEWS_API_KEY,
        "qInTitle":COMPANY_NAME,
    }
    news_response=requests.get(NEWS_ENDPOINT,params=news_params)
    articles = news_response.json()["articles"]


# Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_first_articles = articles[:3]
    print(three_first_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.
    # Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_news=[f"{STOCK_NAME} : {up_down}{difference_percentage}Headline: {articles['title']}.\n Brief:{articles['description']}" for articles in three_first_articles]
    print(formatted_news)
#Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID,TWILIO_API_KEY)


#Format the message like this:
    for article in formatted_news:
        message= client.messages.create(
            body=article,
            from_="+15392860952",
            to="Your verified Number "

        )
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

