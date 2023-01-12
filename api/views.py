import requests
from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json




@api_view()
def country_info (request, pk):
  #if request.method == 'GET': 
   URL = "https://en.wikipedia.org/wiki/"
   URL+=pk
   r = requests.get(URL)
   soup = BeautifulSoup(r.content, 'html5lib') 
   #print(soup.prettify())
   #print(r.content)
   table = soup.find('table')
  
   data=table.find_all('td')
   tr=table.find_all('tr')
   quote = {}

   quote['flag_link']=""
   for i in data:
      if(quote['flag_link'] is not ""):
         break
      if i.a:
        quote['flag_link'] = i.a['href']
      
   
   for i in tr:
    q=i.find('th')
    if(q):
      if 'Capital' in str(q.text) :
        td=i.find('td')
        lst=td.find_all('li')
     
        if not lst:
         quote['capital']=td.a['title']
        else:
          quote['capital']=[]
          for j in lst:
           if(j.a.text):
              quote['capital'].append(j.a.text)

      if 'largest city' in str(q.text).lower():
        td=i.find('td')  
        lst=td.find_all('li')
       
        if not lst:
         quote['largest_city']=td.a['title']
        else:
          quote['largest_city']=[]
          for j in lst:
           if(j.a.text):
              quote['largest_city'].append(j.a.text)
      
      if 'Official languages' in str(q.text):
      
        td=i.find('td') 
        #print(td) 
        lst=td.find_all('li')
        #print(lst)
        if not lst:
         quote['official_languages']=td.a['title']
         
        else:
          quote['official_languages']=[]
          for j in lst:
           if(j.a.has_attr('title')):
            quote['official_languages'].append(j.a['title'])


   f=1
   cnt=0
   for i in tr:
    cnt+=1
    q=i.find('th')
    if(q):
      if f==1 and q.text[2:] == 'Total' :
        td=i.find('td')
        quote['area_total'] = td.text
        f=0
        
      if q.text[2:] == '2022 estimate':
        td=i.find('td')
        quote['Population'] = td.text
        
   
   for i in tr:
    q=i.find('th')
    if(q):
      if q.text[2:] == 'Total' :
        td=i.find('td')
        quote['GDP_nominal'] = td.text
        

   return JsonResponse(quote, status=200)
   
      
