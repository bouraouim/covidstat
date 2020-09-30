import xml.etree.ElementTree as ET

import pandas as pd
from django.shortcuts import render

df3 = pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')
import requests

url = "https://tools.cdc.gov/api/v2/resources/media/404952.rss"

payload = {}
headers = {}


def index(request):
    response = requests.request("GET", url, headers=headers, data=payload)
    root = 'df,d'
    tree = ET.fromstring(response.text.encode('utf8'))
    tt= {}
    for child in tree:
        if child.tag == "channel":
            idx = 0
            for child2 in child:

                if child2.tag == "item" and idx != 3:
                    news = {}
                    for child3 in child2:
                        if child3.tag == "title":
                            news['title'] = child3.text
                        if child3.tag == "description":
                            news['description'] = child3.text
                        if child3.tag == "link":
                            news['link'] = child3.text
                        if child3.tag == "pubDate":
                            news['pubDate'] = child3.text
                        if child3.tag == "category":
                            news['category'] = child3.text
                    tt[idx] = news
                    idx += 1

    confirmedGlobal = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        encoding='utf-8', na_values=None)
    totalCount = confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    totalCount2 = confirmedGlobal[confirmedGlobal.columns[-2]].sum()
    totalCount3 = confirmedGlobal[confirmedGlobal.columns[-3]].sum()
    totalCount4 = confirmedGlobal[confirmedGlobal.columns[-4]].sum()
    totalCount5 = confirmedGlobal[confirmedGlobal.columns[-5]].sum()
    totalCount6 = confirmedGlobal[confirmedGlobal.columns[-6]].sum()
    totalCount7 = confirmedGlobal[confirmedGlobal.columns[-7]].sum()
    totalCount8 = confirmedGlobal[confirmedGlobal.columns[-8]].sum()
    totalCount9 = confirmedGlobal[confirmedGlobal.columns[-9]].sum()
    totalCount10 = confirmedGlobal[confirmedGlobal.columns[-10]].sum()
    totalCount11 = confirmedGlobal[confirmedGlobal.columns[-11]].sum()
    train = pd.read_csv('COVID/09-17-2020.csv', encoding="ISO-8859-1", na_values=None)
    totale_confirmed = train[train.columns[7]].sum()
    totale_deaths = train[train.columns[8]].sum()
    totalere_coverd = train[train.columns[9]].sum()
    train2 = pd.read_csv('COVID/COVID-19-geographic-disbtribution-worldwide-2020-09-17.csv', encoding="ISO-8859-1",
                         na_values=None)
    continent = train2[['cases', 'deaths', train2.columns[-2]]].groupby('continentExp').sum()
    deathscon = continent['deaths'].values.tolist()
    cases = continent['cases'].values.tolist()
    barPlotData = confirmedGlobal[['Country/Region', confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    barPlotData = barPlotData.reset_index()
    barPlotData.columns = ['Country/Region', 'values']
    barPlotData = barPlotData.sort_values(by='values', ascending=False)
    countryNames = barPlotData['Country/Region'].values.tolist()
    barplotVals = barPlotData['values'].values.tolist()
    dataForMap1 = mapDataCal(barPlotData, countryNames)
    showMap = 'True'
    context = {'showMap': showMap, 'news': tt, 'totalCount': totalCount, 'totalCount2': totalCount2,
               'totalCount3': totalCount3, 'totalCount4': totalCount4, 'totalCount5': totalCount5,
               'totalCount6': totalCount6, 'totalCount7': totalCount7, 'totalCount8': totalCount8,
               'totalCount9': totalCount9, 'totalCount10': totalCount10, 'totalCount11': totalCount11,
               'barplotVals': barplotVals, 'countryNames': countryNames, 'dataForMap1': dataForMap1,
               'totalere_coverd': totalere_coverd, 'totale_deaths': totale_deaths, 'totale_confirmed': totale_confirmed,
               'deathscon': deathscon, 'cases': cases}
    return render(request, 'COVID/index.html', context)


def mapDataCal(barPlotData, countryNames):
    dataForMap = []
    for i in countryNames:
        j = ""

        if (i == "Russia"):
            j = 'Russian Federation'
        if (i == "US"):
            j = 'United States'
        if (i == "Egypt"):
            j = 'Egypt, Arab Rep.'
        if (i == "Congo "):
            j = 'Congo, Rep.'
        if (i == "Yemen"):
            j = 'Yemen, Rep.'

        if (i == "Iran"):
            j = 'Iran, Islamic Rep.'
        if (i == "Congo (Kinshasa)"):
            j = 'Congo, Dem. Rep.'
        if (i == "Congo (Brazzaville)"):
            j = 'Congo, Rep.'
        if (i == "Korea, South'"):
            j = 'Korea, Rep.'

        try:
            if (j):
                tempdf = df3[df3['name'] == j]
            else:
                tempdf = df3[df3['name'] == i]

            temp = {}
            temp["code3"] = list(tempdf['code3'].values)[0]
            temp["name"] = i
            temp["value"] = barPlotData[barPlotData['Country/Region'] == i]['values'].sum()
            temp["code"] = list(tempdf['code'].values)[0]
            dataForMap.append(temp)
        except:
            pass
    return dataForMap


def indiCountryData(request):
    countryname = request.POST.get('countryName')
    confirmedGlobal = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        encoding='utf-8', na_values=None)
    totalCount = confirmedGlobal[confirmedGlobal.columns[-1]].sum()

    train = pd.read_csv('COVID/09-17-2020.csv', encoding="ISO-8859-1", na_values=None)
    totale_confirmed = train[train.columns[7]].sum()
    totale_deaths = train[train.columns[8]].sum()
    totalere_coverd = train[train.columns[9]].sum()
    train2 = pd.read_csv('COVID/COVID-19-geographic-disbtribution-worldwide-2020-09-17.csv', encoding="ISO-8859-1",
                         na_values=None)
    continent = train2[['cases', 'deaths', train2.columns[-2]]].groupby('continentExp').sum()
    deathscon = continent['deaths'].values.tolist()
    cases = continent['cases'].values.tolist()
    barPlotData = confirmedGlobal[['Country/Region', confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    barPlotData = barPlotData.reset_index()
    barPlotData.columns = ['Country/Region', 'values']
    barPlotData = barPlotData.sort_values(by='values', ascending=False)
    countryNames = barPlotData['Country/Region'].values.tolist()
    barplotVals = barPlotData['values'].values.tolist()
    dataForMap1 = mapDataCal(barPlotData, countryNames)
    showMap = 'False'
    countryDataSpe = pd.DataFrame(confirmedGlobal[confirmedGlobal['Country/Region'] == countryname][
                                      confirmedGlobal.columns[-30:-1]].sum()).reset_index()
    dates = countryDataSpe['index'].values.tolist()
    values = countryDataSpe[0].values.tolist()
    countryDataSpe = pd.DataFrame(train[train['Country_Region'] == countryname][train.columns[7:]].sum()).reset_index()
    datacountry = countryDataSpe[0].values.tolist()
    datac = datacountry[0]
    datad = datacountry[1]
    datar = datacountry[2]
    dataa = round(datacountry[3])
    datarir = round(datacountry[-2], 2)
    dataft = round(datacountry[6], 2)

    barPlotData3 = train[['Country_Region', train.columns[10], train.columns[-1], train.columns[-2]]].groupby(
        'Country_Region').sum()

    context = {'datarir': datarir, 'dataft': dataft, 'dataa': dataa, 'datac': datac, 'datad': datad, 'datar': datar,
               'countryname': countryname, 'dates': dates, 'values': values, 'showMap': showMap,
               'totalCount': totalCount, 'barplotVals': barplotVals, 'countryNames': countryNames,
               'dataForMap1': dataForMap1, 'totalere_coverd': totalere_coverd, 'totale_deaths': totale_deaths,
               'totale_confirmed': totale_confirmed, 'deathscon': deathscon, 'cases': cases}
    return render(request, 'COVID/index.html', context)


def tunisia(request):
    tundata = pd.read_csv('COVID/tun_data.csv' , encoding = "ISO-8859-1",na_values=None)
    tundataa=tundata[['Governorate',tundata.columns[-2]]].groupby('Governorate').sum().sort_values(by=tundata.columns[-2],ascending=False)
    wileya=tundataa.index.tolist()
    tuncases=tundataa.values.tolist()
    tuncases=[i[0] for i in tuncases]
    mapdata=[]
    for i in wileya:
        a=tundata[tundata['Governorate']==i].values.tolist()
        a=a[0]
        mapdata.append([a[-1],a[-2]])
    for i in mapdata:
        if (isinstance(i[0], str)==False) :
            mapdata.remove(i)


    train = pd.read_csv('COVID/09-17-2020.csv' , encoding = "ISO-8859-1",na_values=None)
    countryDataSpe=pd.DataFrame(train[train['Country_Region']=='Tunisia'][train.columns[7:]].sum()).reset_index()
    datacountry=countryDataSpe[0].values.tolist()
    datac=datacountry[0]
    datad=datacountry[1]
    datar=datacountry[2]
    dataa=round(datacountry[3])
    datarir=round(datacountry[-2],2)
    dataft=round(datacountry[6],2)
    train2 = pd.read_csv('COVID/COVID-19-geographic-disbtribution-worldwide-2020-09-17.csv' , encoding = "ISO-8859-1",na_values=None)
    tunisiadata=pd.DataFrame(train2[train2['countriesAndTerritories']=='Tunisia'][train2.columns[2:-1]]).reset_index()
    datatun=tunisiadata.groupby('month').sum()
    deaths_month=datatun['deaths'].values.tolist()
    cases_month=datatun['cases'].values.tolist()
    context={'wileya':wileya,'tuncases':tuncases,'mapdata':mapdata,'cases_month':cases_month,'deaths_month':deaths_month,'dataa':dataa,'datar':datar,'datad':datad,'datar':datar,'wileya':wileya,'tuncases':tuncases,}
    return render(request,'COVID/tunisia.html',context)

def info(request):
    context = {}
    return render(request, 'COVID/info.html', context)