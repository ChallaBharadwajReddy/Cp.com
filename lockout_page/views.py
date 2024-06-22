from django.shortcuts import render,HttpResponse,redirect
import requests
from django.http import JsonResponse
import random
from django.contrib.auth.models import User
from .models import mini_lockout,ForcesId
from django.db.models import Q
from django.utils import timezone
# Create your views here.
k=0
def lockout(request,pk):

   dual = mini_lockout.objects.get(id=pk)

   if dual.status == "Prepared":

      url="https://codeforces.com/api/problemset.problems"
      response = requests.get(url)
      data = response.json()
      if data["status"]=="OK":
         questions=data["result"]["problems"]

      handel1=ForcesId.objects.get(player=dual.player1)
      handel2=ForcesId.objects.get(player=dual.player2)

      id1=handel1.handel
      id2=handel2.handel
   
      url1="https://codeforces.com/api/user.status?handle="+id1
      responce= requests.get(url1)
      datauser1= responce.json()

      url2="https://codeforces.com/api/user.status?handle="+id2
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
      v800=[]
      v1200=[]
      v1400=[]
      for question in questions:
         if "rating" in question:
            if question["rating"] == 800 :
               v800.append(question)
            if question["rating"] == 1200:
               v1200.append(question)
            if question["rating"] == 1400:
               v1400.append(question)

      while selected == 0:
         a=random.randint(0,len(v800)-1)
         cid=str(v800[a]["contestId"])
         ind=str(v800[a]["index"])
         problem=cid+"_"+ind
         if problem not in dictusers or dictusers[problem]!="SOLVED":
            v800[a]["claim"] = "NONE"
            v800[a]["ind"] = selected
            selected_questions.append(v800[a])
            selected+=1
      while selected == 1:
         a=random.randint(0,len(v1200)-1)
         cid=str(v1200[a]["contestId"])
         ind=str(v1200[a]["index"])
         problem=cid+"_"+ind
         if problem not in dictusers or dictusers[problem]!="SOLVED":
            v1200[a]["claim"] = "NONE"
            v1200[a]["ind"] = selected
            selected_questions.append(v1200[a])
            selected+=1
      while selected == 2:
         a=random.randint(0,len(v1400)-1)
         cid=str(v1400[a]["contestId"])
         ind=str(v1400[a]["index"])
         problem=cid+"_"+ind
         if problem not in dictusers or dictusers[problem]!="SOLVED":
            v1400[a]["claim"] = "NONE"
            v1400[a]["ind"] = selected
            selected_questions.append(v1400[a])
            selected+=1
         
      dual.question1=repr(selected_questions[0])
      dual.question2=repr(selected_questions[1])
      dual.question3=repr(selected_questions[2])
      dual.status = "Running"
      dual.start_time=timezone.now()
      dual.save()
      context={"selprobs":selected_questions,"ContestId":pk,"k":0,"stat":"Running","Rtime":300,"usr":request.user.username}
      return render(request,"lockout_page/questions_page.html",context) 
   else:
      
      present_time=timezone.now()
      dur=present_time-dual.start_time
      dur=(dur.seconds)

      selected_questions=[]
      selected_questions.append(eval(dual.question1))
      selected_questions.append(eval(dual.question2))
      selected_questions.append(eval(dual.question3))

      if dur>=300 :
         dual.status="end"
         dual.save()
         ps1=0
         ps2=0
         for question in selected_questions:
            if question["claim"] != "NONE":
               if question["claim"] == dual.player1.username :
                  ps1+=1
               else:
                  ps2+=1
         winner = "draw"
         if ps1>ps2:
            winner = dual.player1.username
         elif ps2>ps1:
            winner = dual.player2.username
            
         context={"selprobs":selected_questions,"ContestId":pk,"k":0,"stat":"end","Rtime":0,"winner":winner,"usr":request.user.username}
         return render(request,"lockout_page/questions_page.html",context)
      

      Rtime=300-dur
      temp=0
      context={"selprobs":selected_questions,"ContestId":pk,"k":temp,"stat":"Running","Rtime":Rtime,"usr":request.user.username}   
      if request.method == "POST":
         ind = request.POST.get("probInd")
         ind=int(ind)
         if selected_questions[ind]["claim"] == "NONE":
            print(ind)
            use=request.user
            handel1=ForcesId.objects.get(player=use)
            id1=handel1.handel
            url1="https://codeforces.com/api/user.status?handle="+id1
            responce= requests.get(url1)
            datauser1= responce.json()
            temp=0
            if datauser1["status"]=="OK":
               if datauser1["result"][0]["verdict"] == 'OK' :
                  if datauser1["result"][0]["problem"]["contestId"] == selected_questions[ind]["contestId"] and datauser1["result"][0]["problem"]["index"] == selected_questions[ind]["index"]:
                     selected_questions[ind]["claim"] = request.user.username
                     dual.question1=selected_questions[0]
                     dual.question2=selected_questions[1]
                     dual.question3=selected_questions[2]
                     dual.save()
                     temp=(ind+1)*10+1
               
                     context={"selprobs":selected_questions,"ContestId":pk,"k":temp,"stat":"Running","Rtime":Rtime,"usr":request.user.username}      
                     return render(request,"lockout_page/questions_page.html",context)



      context={"selprobs":selected_questions,"ContestId":pk,"k":0,"stat":"Running","Rtime":Rtime,"usr":request.user.username}
      return render(request,"lockout_page/questions_page.html",context)


def MakeaMatch(request):
   random_user = User.objects.get(username="--1")
   try:
      already = mini_lockout.objects.get(Q((Q(player1 = request.user) & ~Q(player2 = random_user) ) | Q(Q(player2 = request.user) & ~Q(player1 = random_user))) & ~Q(status="end"))
      return redirect('contest',pk=already.id)
   except:
      try:
         available = mini_lockout.objects.get(Q(player1 = request.user) & ~Q(status="end"))
         pk=available.id
         print(available.player1.username)
         context={"ContestId":pk}
         return render(request,"lockout_page/waiting.html",context)
      except:
         try:
            available = mini_lockout.objects.get(player2 = random_user)
            available.player2 = request.user
            available.save()

            return redirect('contest',pk=available.id)
         except:
            new = mini_lockout(player1=request.user , player2 = random_user)
            new.save()
            pk = new.id
   context={"ContestId":pk}
   return render(request,"lockout_page/waiting.html",context)

def Worker(request):
   return HttpResponse(request,"lockout_page/timerworker.js")