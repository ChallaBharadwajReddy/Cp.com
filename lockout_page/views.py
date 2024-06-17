from django.shortcuts import render,HttpResponse,redirect
import requests
from django.http import JsonResponse
import random
from django.contrib.auth.models import User
from .models import mini_lockout
from django.db.models import Q
from django.utils import timezone
# Create your views here.
def lockout(request,pk):

   dual = mini_lockout.objects.get(id=pk)

   if dual.status == "Prepared":

      url="https://codeforces.com/api/problemset.problems"
      response = requests.get(url)
      data = response.json()
      if data["status"]=="OK":
         questions=data["result"]["problems"]
   
      url1="https://codeforces.com/api/user.status?handle=ChallaBharadwajReddy"
      responce= requests.get(url1)
      datauser1= responce.json()

      url2="https://codeforces.com/api/user.status?handle=RajaVamshiNath"
      responce= requests.get(url2)
      datauser2= responce.json()
   
      dictusers=dict()

      if(datauser1["status"]=="OK"):
         for sub in datauser1["result"]:
            if sub["verdict"]=='OK':
               cid=str(sub["problem"]["contestId"])
               ind=str(sub["problem"]["index"])
               problem=cid+"_"+ind
               dictusers[problem]="SOLVED"

      if(datauser2["status"]=="OK"):
         for sub in datauser2["result"]:
            if sub["verdict"]=='OK':
               cid=str(sub["problem"]["contestId"])
               ind=str(sub["problem"]["index"])
               problem=cid+"_"+ind
               dictusers[problem]="SOLVED"

      qlen=len(questions)
      selected=0
      selected_questions=[]

      while selected<3:
         a=random.randint(100,qlen-100)

         if questions[a]["rating"]>1600:
            continue

         cid=str(questions[a]["contestId"])
         ind=str(questions[a]["index"])

         problem=cid+"_"+ind
         if problem not in dictusers or dictusers[problem]!="SOLVED":
            selected_questions.append(questions[a])
            selected+=1
         
      dual.question1=repr(selected_questions[0])
      dual.question2=repr(selected_questions[1])
      dual.question3=repr(selected_questions[2])
      dual.status = "Running"
      dual.start_time=timezone.now()
      dual.save()
      context={"selprobs":selected_questions}
      return render(request,"lockout_page/questions_page.html",context) 
   else:
      selected_questions=[]
      selected_questions.append(eval(dual.question1))
      selected_questions.append(eval(dual.question2))
      selected_questions.append(eval(dual.question3))
      context={"selprobs":selected_questions}   
      return render(request,"lockout_page/questions_page.html",context)


def MakeaMatch(request):
   random_user = User.objects.get(username="--1")
   try:
      already = mini_lockout.objects.get(Q(Q(player1 = request.user) & ~Q(player2 = random_user) ) | Q(Q(player2 = request.user) & ~Q(player1 = random_user)))
      return redirect('contest',pk=already.id)
   except:
      try:
         available = mini_lockout.objects.get(player1 = request.user)
         print(available.player1.username)
      except:
         try:
            available = mini_lockout.objects.get(player2 = random_user)
            available.player2 = request.user
            available.save()

            return redirect('contest',pk=available.id)
         except:
            new = mini_lockout(player1=request.user , player2 = random_user)
            new.save()
   return HttpResponse("making a match")