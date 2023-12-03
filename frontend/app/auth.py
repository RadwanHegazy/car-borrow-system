from django.shortcuts import render, redirect
from frontend.settings import URL
import requests


def is_auth (token) : 
    url = URL + 'user/info/'

    headers = {'Authorization':f'token {token}'}
    
    req = requests.get(url,headers=headers)

    is_logged = req.status_code == 200 

    
    if is_logged == False : 
        return False
    else : 
        context =  req.json()
        
        url = URL + 'session/get/'
        req = requests.get(url,headers=headers)
        context['sessions'] = req.json()

        return context



def login (request) : 

    context = {}
    if request.method == "POST" : 
        phone = request.POST['phone']
        password = request.POST['password']

        url = URL + 'user/login/'

        content = {
            'phone' : f'+2{phone}',
            'password' : password
        }

        req = requests.post(url,data=content)

        if req.status_code == 400 : 
            context['errors'] = req.json()['errors']

        elif req.status_code == 200 : 
            token = req.json()['token']
            repsonse = redirect('driver')

            repsonse.set_cookie('user', token)
            
            return repsonse

    return render(request,'login.html',context)

def register (request) : 

    context = {}
    if request.method == "POST" : 

        data = dict(request.POST)
        data.pop('csrfmiddlewaretoken')
        
        


        # edit phone
        phone = f'+2' + data['phone'][0]
        data['phone'][0] = phone

        filterd_data = {}
        for key, val in data.items() :
            filterd_data[key] = val[0]

        
        images = {}
        if 'image' in request.FILES :
            image = request.FILES['image']
            images['image'] = image
        else : 
            if 'image' in filterd_data :
                filterd_data.pop('image')
            
        req = requests.post(
            url = URL + 'user/register/',
            data=filterd_data,files=images
        )

        status = (req.status_code == 200)
        
        if status : 
            token = req.json()['token']
            response = redirect('driver')
            response.set_cookie('user',token)
            return response
        else : 
            context['error'] = 'البيانات غير صحيحة'
        

    return render(request,'register.html',context)


def logout (request) : 

    response = redirect('home')

    if 'user' in request.COOKIES : 
        response.delete_cookie('user')
    
    return response