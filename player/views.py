from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json,requests,os
from bs4 import BeautifulSoup
from django.core.files.storage import FileSystemStorage
from .models import *

links = ['http://192.168.0.11/frnds/','http://dl5.upfdl.com/files/Serial/','http://dl8.heyserver.in/film/','http://79.127.126.110/Serial/','http://dl8.heyserver.in/serial/','http://dl8.heyserver.in/ali/','http://dl8.heyserver.in/trailer/']
CONST = 0
LINK_TO_INDEX = links[0]
con = LINK_TO_INDEX
videoformats = ['mp4','m4v','mkv','webm','mov','avi','wmv','mpg','flv','3gp','m4a','3gpp','mka']

	
def generic(request):
    BASE = LINK_TO_INDEX
    curr = ''
    if 'url' not in request.GET:
        geturl = BASE
    else:
        curr = request.GET['url']
        geturl = BASE+curr

    for one in geturl:
        if '.'+one in curr:
            name = ''
            nextvid = ''
            if 'name' in request.GET:
                name = request.GET['name']
            if 'next' in request.GET:
                nextvid = request.GET['next']
            data = {'url':geturl, "title":name, "next":nextvid}
            return render(request,'player/playvid.html',data)
    page = requests.get(geturl)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    anchors = soup.find_all('a')
    if len(anchors) < 2:
        return HttpResponse("Not found")
    arr = []
    # for link in anchors:
    #     if link.string == '../' or '.srt' in link.get('href'):
    #         continue
        
    #     arr.append({'name':link.string[:-1],'link':'/?url='+curr+link.get('href')+'&name='+link.string[:-1]})
    for i in range(len(anchors)):
        link = anchors[i]
        if link.string == '../' or '.srt' in link.get('href'):
            continue
        nextvid= ''
        if i + 1 == len(anchors):
            pass
        else:
            nextvid = '/?url='+curr + anchors[i+1].get('href')
        arr.append({'name':link.string[:-1],'link':'/?url='+curr+link.get('href')+'&name='+link.string[:-1]})


    data = {'series':arr}
    return render(request,'player/list.html',data)

