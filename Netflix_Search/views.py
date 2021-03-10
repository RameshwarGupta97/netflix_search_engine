# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import requests
from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

host = 'https://tux-es1.cci.drexel.edu:9200/lk596_info624_201904_netflixtitles_v2/_doc'  # Change the end port

es = Elasticsearch(hosts=host, verify_certs=False, http_auth='lk596:tuquaz4Uh7Ei',
                   connection_class=RequestsHttpConnection, )


def home(request):
    # template_name = 'home.html'
    return render(request, 'home.html')


def search_results(request):
    query = request.GET.get('q')

    title = request.GET.get('title')
    cast = request.GET.get('cast')
    director = request.GET.get('director')
    country = request.GET.get('country')
    description = request.GET.get('description')

    rating_dd = request.GET.get('rating_dd')
    language_dd = request.GET.get('language_dd')
    Year_dd = request.GET.get('Year_dd')
    Country_dd = request.GET.get('Country_dd')
    listed_in_dd = request.GET.get('listed_in_dd')
    sort_key = request.GET.get('sort_dd')


    filter_list = []
    if title == 'on':
        filter_list.append('title')
    if cast == 'on':
        filter_list.append('cast')
    if country == 'on':
        filter_list.append('country')
    if description == 'on':
        filter_list.append('description')
    if director == 'on':
        filter_list.append('director')

    if not filter_list:
        filter_list.append('title')

    result = es.search(index="", body={"from": 0, "size": 100,
                                       "query": {
                                           "multi_match": {
                                               "query": query,
                                               "fields": filter_list
                                           }
                                       }})
    object_list = []
    # object_list =  [ITEM['_source']['title'] for ITEM in result['hits']['hits']]

    for ITEM in result['hits']['hits']:
        try:
            year_chk = False
            rating_chk = False
            lang_chk = False
            country_chk = False
            genre_chk = False

            if Year_dd == 'All' and rating_dd == 'All' and language_dd == 'All' and Country_dd == 'All':
                if listed_in_dd == 'All':
                    object_list.append(ITEM['_source'])
                    continue

            if Year_dd != 'All' and Year_dd in ITEM['_source']['release_year']:
                year_chk = True
            elif Year_dd == 'All':
                year_chk = True
            else:
                year_chk = False

            if rating_dd != 'All' and rating_dd in ITEM['_source']['rating']:
                rating_chk = True
            elif rating_dd == 'All':
                rating_chk = True
            else:
                rating_chk = False

            if language_dd != 'All' and language_dd in ITEM['_source']['language']:
                lang_chk = True
            elif language_dd == 'All':
                lang_chk = True
            else:
                lang_chk = False

            if Country_dd != 'All' and Country_dd in ITEM['_source']['country']:
                country_chk = True
            elif Country_dd == 'All':
                country_chk = True
            else:
                country_chk = False

            if listed_in_dd != 'All' and listed_in_dd in ITEM['_source']['listed_in']:
                genre_chk = True
            elif listed_in_dd == 'All':
                genre_chk = True
            else:
                genre_chk = False

            if year_chk and rating_chk and lang_chk and country_chk and genre_chk:
                object_list.append(ITEM['_source'])
        except:
            pass


    return render(request, 'search_results.html', {
        'object_list': sorted(object_list, key=lambda i: i[sort_key])
    })
