from data_filler import DataMaker


class GetNews:
    @staticmethod
    def get_news(tik):
        import requests
        url = "https://stock-market-data.p.rapidapi.com/stock/buzz/news"
        querystring = {"ticker_symbol": f"{tik}", "date": f"{DataMaker.y}-{DataMaker.m}-{DataMaker.d}"}
        headers = {
            'x-rapidapi-key': "11d8bc37d8mshf186de22a127423p1552c3jsnd379e8ad19aa",
            'x-rapidapi-host': "stock-market-data.p.rapidapi.com"
        }
        response = requests.request("GET",
                                    url,
                                    headers=headers,
                                    params=querystring)
        response = response.json()
        news = response['news']
        for i in news:
            for j in i.keys():
                if j == "title":
                    print(i['title'] + "\n")
