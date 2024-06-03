from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from ..forms import CustomLoginForm
from connections import universitydb, users

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        identificacion = request.POST.get('identificacion')
        password = request.POST.get('password')
        user = authenticate(request, identificacion=identificacion, password=password)

        if user is not None:
            login(request, user, backend='users.backends.CustomUserBackend')

            with universitydb.cursor() as cursor:
                cursor.execute('SELECT nombres, apellidos, tipo_empleado, email FROM  eventos.empleados WHERE identificacion = %s', [identificacion])
                user_university_db = cursor.fetchall()
                cursor.close()

                if len(user_university_db)==1:  
                    user_university_db = user_university_db[0]

                    user_mongo_db = users.find_one({'identificacion': identificacion})

                    if (user_mongo_db["nombres"] != user_university_db[0]):
                        users.update_one({'identificacion': identificacion}, {'$set': {'nombres': user_university_db[0]}})

                    if (user_mongo_db["apellidos"] != user_university_db[1]):
                        users.update_one({'identificacion': identificacion}, {'$set': {'apellidos': user_university_db[1]}})

                    if (user_mongo_db["tipo_relacion"] != user_university_db[2]):
                        users.update_one({'identificacion': identificacion}, {'$set': {'tipo_relacion': user_university_db[2]}})

                    if (user_mongo_db["email"] != user_university_db[3]):
                        users.update_one({'identificacion': identificacion}, {'$set': {'email': user_university_db[3]}})

            return redirect('home')
        else:
            msg = "Identificación o contraseña no validas"
            form = CustomLoginForm(request.POST)
            return render(request, 'users/login.html', {'form': form, 'msg': msg})
    else:
        form = CustomLoginForm()
        return render(request, 'users/login.html', {'form': form})
