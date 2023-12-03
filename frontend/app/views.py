from django.shortcuts import render, HttpResponse, redirect
from frontend.settings import URL
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .auth import is_auth




@csrf_exempt
def home (request) : 
    

    req = requests.get(URL)
    sessions = req.json()
    
    if 'user' in request.COOKIES : 
        user_token = request.COOKIES['user']
        
        if is_auth(user_token):
            return redirect('driver')

    if 'from' or 'to' in request.GET :
        from_place = request.GET.get('from','')
        to_place = request.GET.get('to','') 

        if from_place or to_place :
            req = requests.get(
                url = URL + f'?form={from_place}&to={to_place}'
            )
            try : 
                sessions = [i[0] for i in req.json()]
            except KeyError : 
                sessions = req.json()
    
    context = {'sessions' : sessions}

    
    if request.method == "POST" : 
        data = str(request.POST['main_data']).split('@')
        customer, session = data[0], data[1]

        ticket_req = requests.post(
            url = URL + f"customer/create/{session}/",
            data={'customer_name':customer}
        )

        status = (ticket_req.status_code == 200)

        if status :
            ticket = URL + ticket_req.json()['ticket'] 
            context['ticket'] = ticket
        else : 
            context['error'] = 'توجد مشكلة في حجز التذكرة'
        
    
    return render(request,'index.html',context)

@csrf_exempt
def driver (request) : 

    context = {}

    if 'user' in request.COOKIES :

        token = request.COOKIES['user']
        user = is_auth(token)
        if user == False:
            return redirect('login')
        
        if 'session' in request.GET  : 
        
            
            session = request.GET['session']

            headers = {'Authorization':f'token {request.COOKIES["user"]}'}
            if session == 'create' : 
                url = URL + 'session/create/'
            elif session == 'close' : 
                url = URL + 'session/close/'
                

            req = requests.post(url,headers=headers)


            return redirect('driver')

        if request.method == "POST" :
            customer_uuid = request.POST['customer']
            url = URL + 'customer/check/ticket/' + customer_uuid
            headers = {'Authorization':f'token {token}'}

            req = requests.post(
                url = url,
                headers = headers
            )

            is_valid = (req.status_code == 200)

            if is_valid :
                context['count'] = req.json()['count']
                context['msg'] = 'المستخدم موجود'
            else :
                context['msg'] = 'المستخدم ليس موجود'

          
            

        return render(request,'driver.html',context)
    else : 
        return redirect('login')



def userinfo (request) : 
    
    context = {}

    if 'user' in request.COOKIES : 
        user_token = request.COOKIES['user']
        user = is_auth(user_token)
        
        
        if user : 
            
            context = {
                'user' : user,
            }

    return context





