
from django.urls import path
from django.contrib.auth import views as auth_views
from dashboard import views
app_name = "dashboard"

urlpatterns = [
    path('add_course/',views.addCourse, name = 'add_course'),
    path('courses_list/',views.coursesList,name = 'courses_list'),
    path('update_course/<str:course_id>/',views.updateCourse,name = 'update_course'),
    path('reg/',views.registration,name='reg'),
    path('signin_admin/',views.signinAdmin,name= 'signin_admin'),
    path("reg_course/<str:reg_course>/<str:course_price>/",views.register,name = "reg_course"),
    path('courses_requests/',views.coursesRequests,name = "courses_requests"),
    path('pay_course/<str:reg_id>/',views.payTheCourse,name = "pay_course"),
    path('delete_req/<str:req_id>/',views.deleteTheRequest,name = "delete_req"),
    path("teachers_requests/",views.teachersRequests,name = "teachers_requests"),
    path("accept/<str:user_email>/",views.acceptTeacher,name = "accept"),
    # path("delete_teacher/<str:user_email>/",views.deleteTeacher,name = "delete_teacher"),
    path("students_list/",views.studentsList,name = "students_list"),
    path("delete_student/<str:user_email>/",views.deleteStudent,name = "delete_student"),
    path("teachers_list/",views.teachersList,name = "teachers_list"),
    path("add_course_for_teacher/<str:teacher_email>/",views.addcourseForTeacher,name = "add_course_for_teacher"),
    path("course_students/<str:course_name>/",views.courseStudents,name = "course_students"),
    path("course_teachers/<str:course_name>/",views.courseTeachers,name = "course_teachers"),
    path("dashboard/",views.dashboard,name = "dashboard"),
    path("delete_course/<str:course_name>/",views.deleteCourse,name = "delete_course"),
    path("delete_teacher/<str:teacher_email>/",views.deleteTeacher,name="delete_teacher"),
    path("update_teacher/<str:teacher_email>/",views.updateTeacher,name="update_teacher"),
    path("delete_course_for_teacher/<str:teacher_email>/<str:course_name>/",views.deleteCourseForTeacher,name = "delete_course_for_teacher"),
    #path("add_super/",views.addSupervisour,name = "add_super"),
    path("home/",views.homePage,name = "home"),
    path("signin/",views.signin,name = "signin"),
    path("logout/",views.logout,name="logout"),
    path("add_super/",views.addSupervisor,name = "add_super"),
    path("supervisors_list/",views.supervisorsList,name = "supervisors_list"),
    path("add_supervisor_for_course/<str:course_name>/",views.addSupervisorForCourse,name = "add_supervisor_for_course"),
    path("delete_super/<str:super_email>/",views.deleteSupervior,name = "delete_super"),
    path("update_super/<str:super_email>/",views.updateSupervisor,name = "update_super"),
]
