from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

from ..forms import CustomUserCreationForm as UserCreationForm
from ..forms import UserCreationForm_FirstStage

from university.models import Empleados
from ..models import AuthenticationCodes, User

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return signup_first_stage(request)
    
def signup_first_stage(request):
    if request.method == 'POST':
        identificacion = request.POST.get('identificacion')
        email = request.POST.get('email')
        
        try:
            empleado = Empleados.objects.get(identificacion=identificacion)

            #TODO
            if empleado.email == email:
                # TODO: Generar codigo
                codigo = "123456"
                # Guardar codigo en la DB
                auth_code = AuthenticationCodes(identificacion=identificacion, email=email, codigo=codigo)
                auth_code.save()

                # TODO: Enviar codigo por email
                # return
                # new_request = HttpRequest()
                return signup_employee_stage(request, identificacion)

            #TODO cambiar al form y la vista que le corresponda
            else:
                error = "La identificacion o el email no coinciden"
                return render(request, 'users/signup.html', {'error': error})
            
        except ObjectDoesNotExist:
            #TODO: aqui iria el caso de que no pertenesca a la DB de universidad
            pass

        # acaba de enviar la id y el email
        # !saber si este usuario esta en la base
        # buscar por id, si esta, buscar si el email coincide
        # si coincide, crear un temporal codigo, guardarlo temporalmente en la DB (mirar como hacer este codigo temporal) y enviarlo por email
    else:
        form = UserCreationForm_FirstStage()
        return render(request, 'users/signup.html', {'code_sended': False, 'form': form})
    
def signup_employee_stage(request, identificacion):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')

        try:
            auth_code = AuthenticationCodes.objects.filter(identificacion=identificacion, codigo=codigo)

            auth_code.delete()

            # TODO: Dejar que el usuario decida su username y password
            user = User(
                identificacion=identificacion,
                tipo_relacion='profesor',
                nombre_usuario='nombre_usuario',
                email='email@example.com',
                first_name='First',
                last_name='Last',
                ciudad=123,
                is_superuser=False
            )
            user.set_password('password')
            user.save()

            return redirect('home')
        
        except ObjectDoesNotExist:
            error = "El codigo no coincide"
            return render(request, 'users/signup.html', {'error': error})
                

        pass
    else:
        form = UserCreationForm_FirstStage()
        return render(request, 'users/signup.html', {'code_sended': True, 'form': form})