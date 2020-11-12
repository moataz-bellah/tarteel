from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import pyrebase
import uuid
from django.urls import reverse
config = {
     "apiKey": "AIzaSyCsiqPJQiJdcuKgEbWMEFYJc4ve6HiWKsA",
     "authDomain": "tarteel-acbd9.firebaseapp.com",
     "databaseURL": "https://tarteel-acbd9.firebaseio.com",
     "projectId": "tarteel-acbd9",
     "storageBucket": "tarteel-acbd9.appspot.com",
     "messagingSenderId": "1069308251512",
     "appId": "1:1069308251512:web:5186b355f3ddff1bfd0c8d",
     "measurementId": "G-59STGM53NK"
   }
firebase      = pyrebase.initialize_app(config)
auth          = firebase.auth()
storage       = firebase.storage()
imgName = "Capture.PNG"
path_on_cloud = f"images/{imgName}"
path_local    = "Capture.PNG"
cred = credentials.Certificate('./Tarteel-acbd9-firebase-adminsdk-c85l4-bc6b481b91.json')
default_app   = firebase_admin.initialize_app(cred)

# add course
# requests from students page
# requests from teacher page
# Login Page
# Registration Page
# Dashboard Page
# Home Page
def dashboard(request):
    return render(request,"admin2/dashboard.html",{})
def returnDataAsDict(doc):
    data = [i.to_dict() for i in doc]
    return data
def returnDataIds(doc):
    dataIds = {i.id:i.to_dict() for i in doc}
    return dataIds
def addCourse(request):
    db = firestore.client()
    if request.method == 'POST':
        course_name = request.POST['name']
        data = {"course_name":course_name,'course_students':[],'course_supervisors':[],'course_teachers':[],"course_price":int(request.POST["price"])}
        db.collection(u'courses').document(course_name).set(data)
        return HttpResponseRedirect("/dash/courses_list")
    return render(request,'admin2/add_course.html')

def coursesList(request):
    db = firestore.client()
    doc = db.collection(u'courses').stream()
    dataIds = returnDataIds(doc)
    data = [dataIds[j] for j in dataIds]
    print(dataIds)
    print('the idss  ',data)
    return render(request,'admin2/courses_list.html',{'doc':zip(data,dataIds)})
def deleteCourse(request,course_name):
    db = firestore.client()
    db.collection(u'courses').document(course_name).delete()
    doc = db.collection(u'courses').stream()
    dataIds = returnDataIds(doc)
    data = [dataIds[j] for j in dataIds]
    return render(request,"admin2/courses_list.html",{"doc":zip(data,dataIds)})
def updateCourse(request,course_id):
    db = firestore.client()
    doc = db.collection(u'courses').document(course_id)
    msg = ""
    if request.method == 'POST':
        doc.update({u"course_name":request.POST["name"]})
        msg = "Update Done"
    return render(request,'admin2/update_course.html',{'msg':msg})
def viewCourseTeachers(request):
    return render()
def registration(request):
    db = firestore.client()
    if request.method == 'POST':
        messages = []
        email      = request.POST['email']
        password   = request.POST['password']
        first_name = request.POST['fname']
        last_name  = request.POST['lname']
        phone      = request.POST['phone']
        username   = request.POST['username']
        user_type  = request.POST['user_type']
        userCheck = db.collection(u'profiles').document(email)
        if userCheck:
            messages.append("This email is already exists")
        if len(password) < 6:
            messages.append("password must be more than 6 character")
        try:
            user = auth.create_user_with_email_and_password(email, password)
            uid  = user['localId']
            data = {
                'user_email':email,'user_first_name':first_name,'user_last_name':last_name,
                'user_phone':phone,'username':username,'is_active':False,'user_courses':[],
                'user_id':uid,'user_type':user_type
            }
            db.collection(u'profiles').document(email).set(data)
            return HttpResponse("<h1>Done</h1>")
        except:
            #essage = "This email is already exists"
            return render(request,'admin2/registration.html',{'messages':messages})
    return render(request,'admin2/registration.html',{})
def signinAdmin(request):
    db = firestore.client()
    messages = ""
    if request.method == 'POST':
        email    = request.POST['email']
        password = request.POST['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            request.session["user_id"] = user["localId"]
            request.session["email"] = user["email"]
            doc = db.collection(u"profiles").document(email).get().to_dict()
            if doc["user_type"] == "admin":
                request.session["user_type"] = "admin"
            return HttpResponseRedirect("/dash/courses_list")
        except:
            messages = "Email or password is wrong"
    return render(request,'signin.html',{"message":messages})
def signin(request):
    db = firestore.client()
    messages = ""
    docs = db.collection(u"courses").stream()
    data = [i.to_dict() for i in docs]
    if request.method == 'POST':    
        email = request.POST["email"]
        password = request.POST['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            request.session["user_id"] = user["localId"]
            request.session["email"] = user["email"]
            doc = db.collection(u"profiles").document(email).get().to_dict()
            if doc["user_type"] == "student":
                request.session["user_type"] = "student"
                request.session["username"] = doc["username"]
            homePage(request)
        except:
            messages = "Email or password is wrong"
    return HttpResponseRedirect("/dash/home")
def logout(request):
      db = firestore.client()
      #auth.signOut()
      docs = db.collection(u"courses").stream()
      data = [i.to_dict() for i in docs]
      del request.session['user_id']
      del request.session["email"]
      del request.session["user_type"]
      del request.session["username"]
      return HttpResponseRedirect("/dash/home")
def register(request,reg_course,course_price):
    db = firestore.client()
    docs = db.collection(u"courses").stream()
    data2 = [i.to_dict() for i in docs]
    user_data = db.collection(u"profiles").document(request.session["email"]).get().to_dict()
    ID = uuid.uuid4()
    print(request.session["user_type"])
    #if request.method == "POST":
    reg_email      = user_data["user_email"]
    reg_first_name = user_data["user_first_name"]
    reg_last_name  = user_data["user_last_name"]
    reg_phone      = user_data["user_phone"]
    reg_type       = user_data["user_type"]
    user_id        = user_data["user_id"]
    #reg_course     = request.POST.get("course_name")
    #course_price   = request.POST.get("course_price")
    data = {
            "is_paid":False,"reg_course":reg_course,"reg_email":reg_email,"reg_first_name":reg_first_name,
            "reg_last_name":reg_last_name,"reg_phone":reg_phone,"reg_type":reg_type,"reg_username":user_data["username"],
            "user_id":user_id,'reg_id':str(ID),"course_price":int(course_price)
    }
    db.collection(u"registrations").document(str(ID)).set(data)
    return HttpResponseRedirect("/dash/home")
    #return redirect(reverse('dashboard:home', kwargs={"data": data2}))
    #return render(request,"admin2/signin_salon.html",{"data":data})
def coursesRequests(request):
    db = firestore.client()
    docs = db.collection(u"registrations").stream()
    data = [i.to_dict() for i in docs]
    return render(request,"admin2/courses_requests.html",{"doc":data})
def payTheCourse(request,reg_id):
    db = firestore.client()
    doc = db.collection(u"registrations").document(reg_id)
    doc.update({
        'is_paid':True
    })
    course = db.collection(u"courses").document(doc.get().to_dict()["reg_course"])
    coureStudents = course.get().to_dict()["course_students"]
    coureStudents.append(doc.get().to_dict()["reg_username"])
    course.update({
    u"course_students":coureStudents
    })
    studentdData = db.collection(u"profiles").document(doc.get().to_dict()["reg_email"])
    data = studentdData.get().to_dict()["user_courses"]
    data.append(doc.get().to_dict()["reg_course"])
    studentdData.update({
        u"user_courses":data,"is_active":True
    })
    docs = db.collection(u"registrations").stream()
    data = [i.to_dict() for i in docs]
    return render(request,"admin2/courses_requests.html",{"doc":data})
def deleteTheRequest(request,req_id):
    
    db = firestore.client()
    db.collection(u"registrations").document(req_id).delete()
    docs = db.collection(u"registrations").stream()
    data = [i.to_dict() for i in docs]
    return render(request,"admin2/courses_requests.html",{"doc":data})
def teachersRequests(request):
    db = firestore.client()
    docs = db.collection(u"profiles").where(u"user_type",u"==","teacher").stream()
    data = [i.to_dict() for i in docs]
    return render(request,"admin2/teachers_requests.html",{"doc":data})
def acceptTeacher(request,user_email):
    db = firestore.client()
    doc = db.collection(u"profiles").document(user_email)
    doc.update({
        u"is_active":True
    })
    data = db.collection(u"profiles").document(user_email).get().to_dict()
    data2 = {
        "teacher_email":data["user_email"],"teacher_first_name":data["user_first_name"],
        "teacher_id":data["user_id"],"teacher_last_name":data["user_last_name"],"teacher_phone":data["user_phone"],
        "teacher_salary":0,"teacher_username":data["username"],"teacher_courses":[]
    }
    db.collection(u"teachers").document(user_email).set(data2)
    docs = db.collection(u"profiles").where(u"user_type",u"==","teacher").stream()
    data = [i.to_dict() for i in docs]
    return render(request,"admin2/teachers_requests.html",{"doc":data})
# def deleteTeacher(request,user_email):
#     from firebase_admin import auth
#     from firebase_admin import exceptions
#     db = firestore.client()
#     userData = auth.get_user_by_email(user_email)
#     doc = db.collection(u"profiles").document(user_email).get().to_dict()["user_id"]
#     db.collection(u"profiles").document(user_email).delete()
#     auth.delete_user(userData.uid)
#     docs = db.collection(u"profiles").where(u"user_type",u"==","teacher").stream()
#     data = [i.to_dict() for i in docs]
#     return render(request,"admin2/teachers_requests.html",{"doc":data})

def studentsList(request):
    db = firestore.client()
    docs = db.collection(u"profiles").where(u"is_active",u"==",True).where(u"user_type",u"==","student").stream()
    data = [i.to_dict() for i in docs]
    print(data)
    return render(request,"admin2/students_list.html",{"doc":data})
def deleteStudent(request,user_email):
    from firebase_admin import auth
    from firebase_admin import exceptions
    db = firestore.client()
    userData = auth.get_user_by_email(user_email)
    doc = db.collection(u"profiles").document(user_email).get().to_dict()["user_id"]
    db.collection(u"profiles").document(user_email).delete()
    auth.delete_user(userData.uid)
    docs = db.collection(u"profiles").where(u"is_active",u"==",True).where(u"user_type",u"==","student").stream()
    data = [i.to_dict() for i in docs]
    return render(request,"admin2/teachers_requests.html",{"doc":data})
def teachersList(request):
    db = firestore.client()
    docs = db.collection(u"teachers").stream()
    data = [i.to_dict() for i in docs]
    return render(request,"admin2/teachers_list.html",{"doc":data})
def addcourseForTeacher(request,teacher_email):
    db = firestore.client()
    if request.method == "POST":
        doc = db.collection(u"teachers").document(teacher_email)
        teacher_courses = db.collection(u"teachers").document(teacher_email).get().to_dict()["teacher_courses"]
        course = db.collection(u"courses").document(request.POST["course_name"])
        coureTeachers = course.get().to_dict()["course_teachers"]
        coureTeachers.append(doc.get().to_dict()["teacher_username"])
        course.update({
        u"course_teachers":coureTeachers
        })
        if teacher_courses == None:
            teacher_courses = [request.POST["course_name"]]
        else:
            teacher_courses.append(request.POST["course_name"])
        doc.update({
        u"teacher_courses":teacher_courses
        })
        docs = db.collection("teachers").stream()
        data = [i.to_dict() for i in docs]
        return render(request,"admin2/teachers_list.html",{"doc":data})
    docs = db.collection("courses").stream()
    data = [i.to_dict() for i in docs]
    return render(request,"admin2/add_course_for_teacher.html",{"doc":data})
def deleteTeacher(request,teacher_email):
    #from firebase_admin import auth
    #from firebase_admin import exceptions
    db = firestore.client()
    #userData = auth.get_user_by_email(teacher_email)
    doc = db.collection(u"teachers").document(teacher_email).get().to_dict()["teacher_id"]
    #auth.delete_user(userData.uid)
    db.collection(u"teachers").document(teacher_email).delete()
    docs = db.collection(u"teachers").stream()
    data = [i.to_dict() for i in docs]
    return render(request,"admin2/teachers_list.html",{"doc":data})
# def addSupervisour(request):
#     db = firestore.client()
#     return render(request,"admin2/add_super.html",{})
def updateTeacher(request,teacher_email):
    db = firestore.client()
    doc = db.collection(u"teachers").document(teacher_email).get().to_dict()
    doc2 = db.collection(u"teachers").document(teacher_email)
    if request.method == "POST":
        first_name = request.POST["fname"]
        last_name  = request.POST["lname"]
        phone = request.POST["phone"]
        salary = int(request.POST["salary"])
        doc2.update({u"teacher_first_name":first_name,
                    u"teacher_last_name":last_name,u"teacher_phone":phone,u"teacher_salary":salary})
        docs = db.collection(u"teachers").stream()
        data = [i.to_dict() for i in docs]
        return redirect("dashboard:teachers_list")    
    return render(request,"admin2/update_teacher.html",{"data":doc})
def courseStudents(request,course_name):
    db = firestore.client()
    doc = db.collection(u"courses").document(course_name).get().to_dict()["course_students"]
    return render(request,"admin2/course_students.html",{"doc":doc})
def courseTeachers(request,course_name):
    db = firestore.client()
    doc = db.collection(u"courses").document(course_name).get().to_dict()["course_teachers"]
    return render(request,"admin2/course_teachers.html",{"doc":doc})

def deleteCourseForTeacher(request,teacher_email,course_name):
    db = firestore.client()
    doc = db.collection(u"teachers").document(teacher_email).get().to_dict()["teacher_courses"]
    index = doc.index(course_name)
    d = doc.pop(index)
    db.collection(u"teachers").document(teacher_email).update({
        u"teacher_courses":doc
    })
    return redirect("dashboard:teachers_list")
#client Side
def homePage(request):
    db = firestore.client()
    docs = db.collection(u"courses").stream()
    data = [i.to_dict() for i in docs]
    return render(request,"admin2/index.html",{"data":data})
def addSupervisor(request):
    db = firestore.client()
    messages = []
    if request.method == "POST":
        first_name = request.POST["fname"]
        last_name  = request.POST["lname"]
        email      = request.POST["email"]
        phone      = request.POST["phone"]
        username   = request.POST["username"]
        password   = request.POST["password"]
        userCheck = db.collection(u'profiles').document(email)
        if userCheck:
            messages.append("This email is already exists")
        if len(password) < 6:
            messages.append("password must be more than 6 character")
        try:
            user = auth.create_user_with_email_and_password(email, password)
            uid  = user['localId']
            data = {
            "is_active":True,"user_courses":[],"user_email":email,"user_first_name":first_name,
            "user_last_name":last_name,"user_phone":phone,"user_type":"supervisor","username":username,"user_id":uid}   
            db.collection(u'profiles').document(email).set(data)
            return HttpResponseRedirect("/dash/supervisors_list")
        except:
            #essage = "This email is already exists"
            return render(request,'admin2/add_supervisor.html',{'messages':messages})
    return render(request,"admin2/add_supervisor.html",{'messages':messages})
def supervisorsList(request):
    db = firestore.client()
    docs = db.collection(u"profiles").where(u"user_type",u"==","supervisor").stream()
    data = [i.to_dict() for i in docs]
    return render(request,"admin2/supervisors_list.html",{"data":data})
def addSupervisorForCourse(request,course_name):
    db = firestore.client()
    docs = db.collection(u"profiles").where(u"user_type",u"==","supervisor").stream()
    data = [i.to_dict() for i in docs]
    if request.method == "POST":
        supervisor = request.POST["super"]
        course = db.collection(u"courses").document(course_name)
        supervisorArray  = course.get().to_dict()["course_supervisors"]   
        supervisorArray.append(supervisor)
        supervisorCourses = db.collection(u"profiles").document(supervisor).get().to_dict()["user_courses"]
        supervisorCourses.append(course_name)
        course.update({
            u"course_supervisors":supervisorArray
        })
        db.collection(u"profiles").document(supervisor).update({
            u"user_courses":supervisorCourses
        })
        return HttpResponseRedirect("/dash/courses_list")
    return render(request,"admin2/add_supervisor_for_course.html",{"data":data})
def deleteSupervior(request,super_email):
    db = firestore.client()
    #userData = auth.get_user_by_email(super_email)
    doc = db.collection(u"profiles").document(super_email).get().to_dict()["user_id"]
    db.collection(u"profiles").document(super_email).delete()
    #auth.delete_user(userData.uid)
    docs = db.collection(u"profiles").where(u"is_active",u"==",True).where(u"user_type",u"==","student").stream()
    data = [i.to_dict() for i in docs]
    return HttpResponseRedirect("/dash/supervisors_list")
# update,delete superbisor
def updateSupervisor(request,super_email):
    db = firestore.client()
    doc = db.collection(u"profiles").document(super_email).get().to_dict()
    doc2 = db.collection(u"profiles").document(super_email)
    if request.method == "POST":
        first_name = request.POST["fname"]
        last_name  = request.POST["lname"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        username = request.POST["username"]
        #salary = int(request.POST["salary"])
        doc2.update({u"user_first_name":first_name,
                    u"user_last_name":last_name,u"user_phone":phone,u"user_email":email,"username":username})
        docs = db.collection(u"profiles").stream()
        data = [i.to_dict() for i in docs]
        return HttpResponseRedirect("/dash/supervisors_list")
    return render(request,"admin2/update_supervisor.html",{})
