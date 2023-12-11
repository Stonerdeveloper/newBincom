

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView
from .models import Image
from .forms import ImageForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views import View

class BaseView(View):
    def get(self, request, *args, **kwargs):
        # Add any additional context data if needed
        
        return redirect('image_list')
            # Add more variables as needed
        
        return render(request, 'base.html', context)

class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Store user data in the session
            request.session['registered_user'] = {
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password1'],  # Use the password1 field as it contains the hashed password
            }

            # Log in the user
            login(request, user)

            # Redirect to the image list page (adjust the URL as needed)
            return redirect('image_list')

        return render(request, self.template_name, {'form': form})


class ImageView(ListView):
    model = Image
    template_name = 'image_list.html'
    context_object_name = 'images'



def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Assign the authenticated user to the form instance
            form.instance.user = request.user

            if form.is_valid():
                form.save()
                return redirect('image_list')
        else:
            # Redirect to login page or handle the unauthenticated user case
            return redirect('custom_login')
    else:
        form = ImageForm()

    return render(request, 'upload_image.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        # Get user data from the session
        registered_user = request.session.get('registered_user')
        
        if registered_user:
            # Authenticate user using data from the registration form
            user = authenticate(request, username=registered_user['username'], password=registered_user['password'])
            
            # Check if authentication was successful
            if user is not None:
                # Log in the user
                login(request, user)
                
                # Redirect to the image list page (adjust the URL as needed)
                return redirect('image_list')
            else:
                messages.error(request, 'Invalid login credentials from registration.')
    
    # If the form is not submitted or authentication fails, create an empty form
    form = AuthenticationForm()
    
    # Render the login page with the form
    return render(request, 'registration/login.html', {'form': form})