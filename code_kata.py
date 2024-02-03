

User 
name: String, surname: String, email: String, password: String, type: String

Student extends User 
Educator extends User

Team 
id: int, name: String, numMembers: int

Tournament
id: int, name: String, description: String, submissionDeadline: Date, endingDate: Date

Battle 
id: int, name: String, registrationDeadline: Date, sumbissionDeadline: Date, maxTeamStudents: int, minTeamStudents: int


Battle->Tournament (belongs to: one-to-many)
Team->Battle (joins: one-to-many)
Educator->Tournament (manages: many-to-many)
Educator->Battle (manages:many-to-one)
Student->Tournament (subscribes: many-to-many)
Student->Team (takes part in: many-to-many)


--MODELS
from django.db import models
from django.contrib.auth.models import User

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    submission_deadline = models.DateField()
    ending_date = models.DateField()

class Battle(models.Model):
    name = models.CharField(max_length=100)
    registration_deadline = models.DateField()
    submission_deadline = models.DateField()
    max_team_students = models.IntegerField()
    min_team_students = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

class Team(models.Model):
    name = models.CharField(max_length=100)
    num_members = models.IntegerField()
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)

class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tournaments = models.ManyToManyField(Tournament, related_name='students')
    teams = models.ManyToManyField(Team, related_name='students')

class Educator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tournaments = models.ManyToManyField(Tournament, related_name='educators')
    battles_managed = models.ManyToManyField(Battle, related_name='educators')
---------- STEP DA FARE--------------------------
Create Views:
Define views in the views.py file inside your app directory (CKBApp in your case). Views handle HTTP requests and return responses. Create views to handle the functionality described in your application.
python
Copy code
# CKBApp/views.py
from django.shortcuts import render
from .models import Tournament, Battle, Team, Badge, Score

def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'CKBApp/tournament_list.html', {'tournaments': tournaments})

# Create other views for battles, teams, badges, etc.
Create Templates:
Create HTML templates inside the templates directory within your app directory. These templates will be used to render the views.

scss
Copy code
CKBApp/
├── templates/
│   └── CKBApp/
│       ├── tournament_list.html
│       ├── battle_list.html
│       └── ... (other templates)
Example tournament_list.html:

html
Copy code
<!DOCTYPE html>
<html>
<head>
    <title>Tournament List</title>
</head>
<body>
    <h1>Tournaments</h1>
    <ul>
        {% for tournament in tournaments %}
            <li>{{ tournament.name }}</li>
        {% endfor %}
    </ul>
</body>
</html>
Define URLs:
Set up URL patterns in the urls.py file inside your app directory. This file will define the routes for your views.

python
Copy code
# CKBApp/urls.py
from django.urls import path
from .views import tournament_list

urlpatterns = [
    path('tournaments/', tournament_list, name='tournament-list'),
    # Add other URL patterns for battles, teams, badges, etc.
]
Include URLs in Project's urls.py:
Include the URLs of your app in the project's urls.py. Open the urls.py file in your Django project directory and add the following:

python
Copy code
# CKBProject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckb/', include('CKBApp.urls')),
    # ... other paths ...
]
Replace 'ckb/' with the desired path for your app.

Configure Django Admin:
Register your models in the admin.py file inside your app directory to make them visible and manageable in the Django Admin interface.

python
Copy code
# CKBApp/admin.py
from django.contrib import admin
from .models import Tournament, Battle, Team, Badge, Score

admin.site.register(Tournament)
admin.site.register(Battle)
admin.site.register(Team)
admin.site.register(Badge)
admin.site.register(Score)
Run the Development Server:
Start the development server to test your application:

bash
Copy code
python manage.py runserver
Visit http://localhost:8000/ckb/tournaments/ in your browser to see the output of your tournament_list view.

These steps provide a basic setup for your Django application. You can continue to expand and customize your application based on your specific requirements. If you encounter any issues or have further questions, feel free to ask!

---REGISTRATION--
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration</title>
    <link rel="stylesheet" href="RegistrationStyle.css"> <!-- Link to your stylesheet, if any -->
</head>

<body>
    <form name="registrationForm" method="post" action="process_registration.php">
        <div class="formCo">
            <h2>Registration</h2>
            <label for="firstName">First Name:</label>
            <input type="text" id="firstName" name="firstName" required>

            <label for="lastName">Last Name:</label>
            <input type="text" id="lastName" name="lastName" required>

            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>

            <label for="userType">Select User Type:</label>
            <select id="userType" name="userType" required>
                <option value="" disabled selected>Select user type</option>
                <option value="student">Student</option>
                <option value="educator">Educator</option>
            </select>

            <input type="submit" value="Register">
        </div>
    </form>
</body>
</html>

---REGFORM
{% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration</title>
    <link rel="stylesheet" href="{% static 'CKBApp/css/RegistrationStyle.css' %}">
</head>
<body>
    <form name="registrationForm" method="post" action="{% url 'registration-page' %}">
        {% csrf_token %}
        <div class="formCo">
            <h2>Registration</h2>
            {{ form.as_p }}
            <input type="submit" value="Register">
        </div>
    </form>
</body>
</html>


---PAGINA EDUCATORE---
Prima schermata: Managing Tournaments con sotto i tornei  + 
sezioni con i bottoni e pagine a parte. 
Interfaccia 1: Create Tournament quando clicco il bottone
Interfaccia 2:Evaluate Work quando clicco il bottone (OK: Già a parte)
Interfaccia 3: Available tournaments status quando clicco il bottone
Interfaccia 4: Student Profile quando clicco il bottone (OK: Già a parte)

REMINDER
grant permission: se vogliamo mettere un messaggio--->Non penso
che segnala che sono già stati garantiti i permessi
badges: li dobbiamo mettere statici?---> si li lasciamo così
tasto per andare indietro alla pagina precedente e/o alla homepage---> FATTO
creatore del team da settare a unique?
le deadline della battaglia devono essere dopo quelle del torneo---> FATTO
la pagina di battle details dell'educatore deve essere diversa perche
	non ci deve stare il battle score ??????
ti puoi iscrivere al torneo o alla battaglia sono se le deadline non sono passate---> FATTO da testare
impostare nel form della valutazione un max di 100 per lo score---> FATTO da testare

MANCA
la pagina di battle details dell'educatore deve essere diversa perche
	non ci deve stare il battle score ??????
code kata
repository github
manual evaluation


<!--<td>{{ student.tournaments.through.objects.get(student=student, tournament=tournament).score }}</td>-->

   creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)