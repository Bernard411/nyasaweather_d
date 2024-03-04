from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from . import models

import logging
import json
from datetime import datetime, timedelta
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .visualcrossing import VisualCrossingWeatherAPI
from core.key import api_key as visual_crossing_api_key
import requests
import math
import os

def home(request):
    location = models.Location.objects.all()
    disaster = models.Disaster.objects.all()[:6]
    messagez = models.Updates.objects.all()

    context = {
        'location': location,
        'disaster': disaster,
        'messagez': messagez
    }
    return render(request, 'landingpage.html', context)

def homez(request):
    location = models.Location.objects.all()
    disaster = models.Disaster.objects.all()[:6]
    messagez = models.Updates.objects.all()

    context = {
        'location': location,
        'disaster': disaster,
        'messagez': messagez
    }
    return render(request, 'landingpage2.html', context)

def index(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    return redirect('homepage_two')

logger = logging.getLogger(__name__)

def save_timeline_data_to_file(location, start_date, end_date):
    api_key = "922MWNKWR3G4MW2M7USGTL5JB"
    visual_crossing_api = VisualCrossingWeatherAPI(api_key)

    timeline_data = visual_crossing_api.get_timeline_data(location, start_date, end_date)

    output_folder = "core/output"
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, f"{location}_visual_crossing_detailed_timeline_data.json")

    with open(output_file_path, "w") as output_file:
        json.dump(timeline_data, output_file, indent=2)

    return output_file_path

def result(request):
    if request.method == "POST":
        openweathermap_api_key = '547afd6a9ad38bd23e255e28e1a2bf49'
        visual_crossing_api = VisualCrossingWeatherAPI(visual_crossing_api_key)

        city_name = request.POST["city"].lower()
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        try:
            visual_crossing_data = visual_crossing_api.get_timeline_data(city_name, start_date, end_date)

            visual_crossing_output = {
                "queryCost": visual_crossing_data.get("queryCost"),
                "latitude": visual_crossing_data.get("latitude"),
                "longitude": visual_crossing_data.get("longitude"),
                "resolvedAddress": visual_crossing_data.get("resolvedAddress"),
                "address": visual_crossing_data.get("address"),
                "timezone": visual_crossing_data.get("timezone"),
                "tzoffset": visual_crossing_data.get("tzoffset"),
                "description": visual_crossing_data.get("description"),
                "alerts": visual_crossing_data.get("alerts"),
                "stations": visual_crossing_data.get("stations"),
                "currentConditions": visual_crossing_data.get("currentConditions"),
                "source": visual_crossing_data.get("source"),
            }

            visual_crossing_output_file_path = "core/output/visual_crossing_detailed_timeline_data.json"

            with open(visual_crossing_output_file_path, "w") as output_file:
                json.dump(visual_crossing_data, output_file)

            visual_crossing_output["output_file_path"] = visual_crossing_output_file_path

            visual_crossing_context = {
                'simplified_output': visual_crossing_output,
            }

            openweathermap_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={openweathermap_api_key}"
            openweathermap_data = requests.get(openweathermap_url).json()

            try:
                openweathermap_temperatures = [
                    openweathermap_data["list"][i]["main"]["temp"] for i in range(1, 8)
                ]

                openweathermap_avg_temps = [
                    round((openweathermap_data["list"][i]["main"]["temp_min"] + openweathermap_data["list"][i]["main"]["temp_max"]) / 2 - 273.0) for i in range(1, 8)
                ]

                openweathermap_overall_avg_temp = round(sum(openweathermap_temperatures) / len(openweathermap_temperatures) - 273.0)
                avg_temp1 = round((openweathermap_data["list"][1]["main"]["temp_min"] + openweathermap_data["list"][1]["main"]["temp_max"]) / 2 - 273.0)
                avg_temp2 = round((openweathermap_data["list"][2]["main"]["temp_min"] + openweathermap_data["list"][2]["main"]["temp_max"]) / 2 - 273.0)
                avg_temp3 = round((openweathermap_data["list"][3]["main"]["temp_min"] + openweathermap_data["list"][3]["main"]["temp_max"]) / 2 - 273.0)
                avg_temp4 = round((openweathermap_data["list"][4]["main"]["temp_min"] + openweathermap_data["list"][4]["main"]["temp_max"]) / 2 - 273.0)
                avg_temp5 = round((openweathermap_data["list"][5]["main"]["temp_min"] + openweathermap_data["list"][5]["main"]["temp_max"]) / 2 - 273.0)
                avg_temp6 = round((openweathermap_data["list"][6]["main"]["temp_min"] + openweathermap_data["list"][6]["main"]["temp_max"]) / 2 - 273.0)
                avg_temp7 = round((openweathermap_data["list"][7]["main"]["temp_min"] + openweathermap_data["list"][7]["main"]["temp_max"]) / 2 - 273.0)

                output_file_path = save_timeline_data_to_file(city_name, start_date, end_date)

                openweathermap_context = {
                    "city_name": openweathermap_data["city"]["name"],
                    "city_country": openweathermap_data["city"]["country"],
                    "wind": openweathermap_data['list'][0]['wind']['speed'],
                    "degree": openweathermap_data['list'][0]['wind']['deg'],
                    "status": openweathermap_data['list'][0]['weather'][0]['description'],
                    "cloud": openweathermap_data['list'][0]['clouds']['all'],
                    'date': openweathermap_data['list'][0]["dt_txt"],
                    'date1': openweathermap_data['list'][1]["dt_txt"],
                    'date2': openweathermap_data['list'][2]["dt_txt"],
                    'date3': openweathermap_data['list'][3]["dt_txt"],
                    'date4': openweathermap_data['list'][4]["dt_txt"],
                    'date5': openweathermap_data['list'][5]["dt_txt"],
                    'date6': openweathermap_data['list'][6]["dt_txt"],
                    'date7': openweathermap_data['list'][7]["dt_txt"],
                    
                    "temp": round(openweathermap_data["list"][0]["main"]["temp"] - 273.0),
                    "temp_min1": math.floor(openweathermap_data["list"][1]["main"]["temp_min"] - 273.0),
                    "temp_max1": math.ceil(openweathermap_data["list"][1]["main"]["temp_max"] - 273.0),
                    "temp_min2": math.floor(openweathermap_data["list"][2]["main"]["temp_min"] - 273.0),
                    "temp_max2": math.ceil(openweathermap_data["list"][2]["main"]["temp_max"] - 273.0),
                    "temp_min3": math.floor(openweathermap_data["list"][3]["main"]["temp_min"] - 273.0),
                    "temp_max3": math.ceil(openweathermap_data["list"][3]["main"]["temp_max"] - 273.0),
                    "temp_min4": math.floor(openweathermap_data["list"][4]["main"]["temp_min"] - 273.0),
                    "temp_max4": math.ceil(openweathermap_data["list"][4]["main"]["temp_max"] - 273.0),
                    "temp_min5": math.floor(openweathermap_data["list"][5]["main"]["temp_min"] - 273.0),
                    "temp_max5": math.ceil(openweathermap_data["list"][5]["main"]["temp_max"] - 273.0),
                    "temp_min6": math.floor(openweathermap_data["list"][6]["main"]["temp_min"] - 273.0),
                    "temp_max6": math.ceil(openweathermap_data["list"][6]["main"]["temp_max"] - 273.0),
                    "temp_min7": math.floor(openweathermap_data["list"][7]["main"]["temp_min"] - 273.0),
                    "temp_max7": math.ceil(openweathermap_data["list"][7]["main"]["temp_max"] - 273.0),

                    "overall_avg_temp": openweathermap_overall_avg_temp,
                    "avg_temp1": avg_temp1,
                    "avg_temp2": avg_temp2,
                    "avg_temp3": avg_temp3,
                    "avg_temp4": avg_temp4,
                    "avg_temp5": avg_temp5,
                    "avg_temp6": avg_temp6,
                    "avg_temp7": avg_temp7,

                    "pressure": openweathermap_data["list"][0]["main"]["pressure"],
                    "humidity": openweathermap_data["list"][0]["main"]["humidity"],
                    "sea_level": openweathermap_data["list"][0]["main"]["sea_level"],
                    "weather": openweathermap_data["list"][1]["weather"][0]["main"],
                    "description": openweathermap_data["list"][1]["weather"][0]["description"],
                    "icon": openweathermap_data["list"][0]["weather"][0]["icon"],
                    "icons": [openweathermap_data["list"][i]["weather"][0]["icon"] for i in range(1, 22)],

                    'detailed_timeline_data_path': output_file_path,
                }

            except (KeyError, IndexError):
                openweathermap_context = {
                    "city_name": "Not Found, Check your spelling..."
                }

            return render(request, 'home.html', {**visual_crossing_context, **openweathermap_context})

        except requests.exceptions.HTTPError as errh:
            logger.error(f"Visual Crossing HTTP Error: {errh}")
            visual_crossing_context = {
                "city_name": f"Visual Crossing HTTP Error: {errh}"
            }
            return render(request, "home.html", visual_crossing_context)
        except requests.exceptions.ConnectionError as errc:
            logger.error(f"Visual Crossing Error Connecting: {errc}")
            visual_crossing_context = {
                "city_name": f"Visual Crossing Error Connecting: {errc}"
            }
            return render(request, "home.html", visual_crossing_context)
        except requests.exceptions.Timeout as errt:
            logger.error(f"Visual Crossing Timeout Error: {errt}")
            visual_crossing_context = {
                "city_name": f"Visual Crossing Timeout Error: {errt}"
            }
            return render(request, "home.html", visual_crossing_context)
        except requests.exceptions.RequestException as err:
            logger.error(f"Visual Crossing Request Exception: {err}")
            visual_crossing_context = {
                "city_name": f"Visual Crossing Request Exception: {err}"
            }
            return render(request, "home.html", visual_crossing_context)
    else:
        return redirect('homepage')
    
def save_timeline_data_to_file(location, start_date, end_date):
    # Use the same API key that is passed to the VisualCrossingWeatherAPI constructor
    api_key = "LZ8P3W65L7QQVAH3BL64DL8RH"
    visual_crossing_api = VisualCrossingWeatherAPI(api_key)

    # Get timeline weather data
    timeline_data = visual_crossing_api.get_timeline_data(location, start_date, end_date)

    # Define the output folder
    output_folder = "core/output"
    
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, f"{location}_visual_crossing_detailed_timeline_data.json")
    
    # Save detailed timeline data to the file
    with open(output_file_path, "w") as output_file:
        json.dump(timeline_data, output_file, indent=2)

    return output_file_path


def results(request):
    if request.method == "POST":
        # Replace with your OpenWeatherMap API key
        openweathermap_api_key = 'b0497bc522524401831134643231610'

        # Set up Visual Crossing Weather API
        visual_crossing_api = VisualCrossingWeatherAPI(visual_crossing_api_key)

        # Set parameters for weather data request
        city_name = request.POST["city"].lower()
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        try:
            # Get timeline weather data from Visual Crossing
            visual_crossing_data = visual_crossing_api.get_timeline_data(city_name, start_date, end_date)

            # Create simplified_output dictionary for Visual Crossing
            visual_crossing_output = {
                "queryCost": visual_crossing_data.get("queryCost"),
                "latitude": visual_crossing_data.get("latitude"),
                "longitude": visual_crossing_data.get("longitude"),
                "resolvedAddress": visual_crossing_data.get("resolvedAddress"),
                "address": visual_crossing_data.get("address"),
                "timezone": visual_crossing_data.get("timezone"),
                "tzoffset": visual_crossing_data.get("tzoffset"),
                "description": visual_crossing_data.get("description"),
                "alerts": visual_crossing_data.get("alerts"),
                "stations": visual_crossing_data.get("stations"),
                "currentConditions": visual_crossing_data.get("currentConditions"),
                "source": visual_crossing_data.get("source"),
            }

            #Save detailed timeline data to a file for Visual Crossing
            visual_crossing_output_file_path = "core/output/visual_crossing_detailed_timeline_data.json"

            with open(visual_crossing_output_file_path, "w") as output_file:
                json.dump(visual_crossing_data, output_file)

            # Add output file path to simplified_output for Visual Crossing
            visual_crossing_output["output_file_path"] = visual_crossing_output_file_path

            #Assuming len(weather_data) is the number of days for which you have weather data for Visual Crossing
            visual_crossing_context = {
                'simplified_output': visual_crossing_output,
                # 'detailed_timeline_data_path': visual_crossing_output_file_path,  # Add the path for download link
            }

            # Get weather data from OpenWeatherMap
            openweathermap_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={openweathermap_api_key}"
            openweathermap_data = requests.get(openweathermap_url).json()

            # Create context variables for OpenWeatherMap
            try:
                # Extracting temperatures for the next 7 days from OpenWeatherMap
                openweathermap_temperatures = [
                    openweathermap_data["list"][i]["main"]["temp"] for i in range(1, 8)
                    
                ]

                # Calculate average temperature for each day from OpenWeatherMap
                openweathermap_avg_temps = [
                    round((openweathermap_data["list"][i]["main"]["temp_min"] + openweathermap_data["list"][i]["main"]["temp_max"]) / 2 - 273.0) for i in range(1, 8)
                ]

                # Calculate overall average temperature for 7 days from OpenWeatherMap
                openweathermap_overall_avg_temp = round(sum(openweathermap_temperatures) / len(openweathermap_temperatures) - 273.0)
                avg_temp1 = round((openweathermap_data["list"][1]["main"]["temp_min"] + openweathermap_data["list"][1]["main"]["temp_max"]) / 2 - 273.0)
                avg_temp2 = round((openweathermap_data["list"][2]["main"]["temp_min"] + openweathermap_data["list"][2]["main"]["temp_max"]) / 2 - 273.0)
                avg_temp3 = round((openweathermap_data["list"][3]["main"]["temp_min"] + openweathermap_data["list"][3]["main"]["temp_max"]) / 2 - 273.0)
                avg_temp4 = round((openweathermap_data["list"][4]["main"]["temp_min"] + openweathermap_data["list"][4]["main"]["temp_max"]) / 2 - 273.0)
                avg_temp5 = round((openweathermap_data["list"][5]["main"]["temp_min"] + openweathermap_data["list"][5]["main"]["temp_max"]) / 2 - 273.0)
                avg_temp6 = round((openweathermap_data["list"][6]["main"]["temp_min"] + openweathermap_data["list"][6]["main"]["temp_max"]) / 2 - 273.0)
                avg_temp7 = round((openweathermap_data["list"][7]["main"]["temp_min"] + openweathermap_data["list"][7]["main"]["temp_max"]) / 2 - 273.0)


                # Save detailed timeline data to a file
                output_file_path = save_timeline_data_to_file(city_name, start_date, end_date)

                openweathermap_context = {
                    "city_name": openweathermap_data["city"]["name"],
                    "city_country": openweathermap_data["city"]["country"],
                    "wind": openweathermap_data['list'][0]['wind']['speed'],
                    "degree": openweathermap_data['list'][0]['wind']['deg'],
                    "status": openweathermap_data['list'][0]['weather'][0]['description'],
                    "cloud": openweathermap_data['list'][0]['clouds']['all'],
                    'date': openweathermap_data['list'][0]["dt_txt"],
                    'date1': openweathermap_data['list'][1]["dt_txt"],
                    'date2': openweathermap_data['list'][2]["dt_txt"],
                    'date3': openweathermap_data['list'][3]["dt_txt"],
                    'date4': openweathermap_data['list'][4]["dt_txt"],
                    'date5': openweathermap_data['list'][5]["dt_txt"],
                    'date6': openweathermap_data['list'][6]["dt_txt"],
                    'date7': openweathermap_data['list'][7]["dt_txt"],
                    
                    "temp": round(openweathermap_data["list"][0]["main"]["temp"] - 273.0),
                    "temp_min1": math.floor(openweathermap_data["list"][1]["main"]["temp_min"] - 273.0),
                    "temp_max1": math.ceil(openweathermap_data["list"][1]["main"]["temp_max"] - 273.0),
                    "temp_min2": math.floor(openweathermap_data["list"][2]["main"]["temp_min"] - 273.0),
                    "temp_max2": math.ceil(openweathermap_data["list"][2]["main"]["temp_max"] - 273.0),
                    "temp_min3": math.floor(openweathermap_data["list"][3]["main"]["temp_min"] - 273.0),
                    "temp_max3": math.ceil(openweathermap_data["list"][3]["main"]["temp_max"] - 273.0),
                    "temp_min4": math.floor(openweathermap_data["list"][4]["main"]["temp_min"] - 273.0),
                    "temp_max4": math.ceil(openweathermap_data["list"][4]["main"]["temp_max"] - 273.0),
                    "temp_min5": math.floor(openweathermap_data["list"][5]["main"]["temp_min"] - 273.0),
                    "temp_max5": math.ceil(openweathermap_data["list"][5]["main"]["temp_max"] - 273.0),
                    "temp_min6": math.floor(openweathermap_data["list"][6]["main"]["temp_min"] - 273.0),
                    "temp_max6": math.ceil(openweathermap_data["list"][6]["main"]["temp_max"] - 273.0),
                    "temp_min7": math.floor(openweathermap_data["list"][7]["main"]["temp_min"] - 273.0),
                    "temp_max7": math.ceil(openweathermap_data["list"][7]["main"]["temp_max"] - 273.0),

                    "overall_avg_temp": openweathermap_overall_avg_temp,
                    "avg_temp1": avg_temp1,
                    "avg_temp2": avg_temp2,
                    "avg_temp3": avg_temp3,
                    "avg_temp4": avg_temp4,
                    "avg_temp5": avg_temp5,
                    "avg_temp6": avg_temp6,
                    "avg_temp7": avg_temp7,

                    "pressure": openweathermap_data["list"][0]["main"]["pressure"],
                    "humidity": openweathermap_data["list"][0]["main"]["humidity"],
                    "sea_level": openweathermap_data["list"][0]["main"]["sea_level"],
                    "weather": openweathermap_data["list"][1]["weather"][0]["main"],
                    "description": openweathermap_data["list"][1]["weather"][0]["description"],
                    "icon": openweathermap_data["list"][0]["weather"][0]["icon"],
                    "icons": [openweathermap_data["list"][i]["weather"][0]["icon"] for i in range(1, 22)],

                    'detailed_timeline_data_path': output_file_path,
                }

            except (KeyError, IndexError):
                # Handle missing or unexpected data from OpenWeatherMap
                openweathermap_context = {
                    "city_name": "Not Found, Check your spelling..."
                }

            return render(request, 'rain.html', {**visual_crossing_context, **openweathermap_context})

        except requests.exceptions.HTTPError as errh:
            # Handle HTTP errors for Visual Crossing
            logger.error(f"Visual Crossing HTTP Error: {errh}")
            visual_crossing_context = {
                "city_name": f"Visual Crossing HTTP Error: {errh}"
            }
            return render(request, "rain.html", visual_crossing_context)
        except requests.exceptions.ConnectionError as errc:
            # Handle connection errors for Visual Crossing
            logger.error(f"Visual Crossing Error Connecting: {errc}")
            visual_crossing_context = {
                "city_name": f"Visual Crossing Error Connecting: {errc}"
            }
            return render(request, "rain.html", visual_crossing_context)
        except requests.exceptions.Timeout as errt:
            # Handle timeouts for Visual Crossing
            logger.error(f"Visual Crossing Timeout Error: {errt}")
            visual_crossing_context = {
                "city_name": f"Visual Crossing Timeout Error: {errt}"
            }
            return render(request, "rain.html", visual_crossing_context)
        except requests.exceptions.RequestException as err:
            # Handle other request exceptions for Visual Crossing
            logger.error(f"Visual Crossing Request Exception: {err}")
            visual_crossing_context = {
                "city_name": f"Visual Crossing Request Exception: {err}"
            }
            return render(request, "rain.html", visual_crossing_context)

    else:
        return redirect('home')

def view_disaster(request, pk):
    view_disaster = models.Disaster.objects.get(pk=pk)
    total_relief_aid_percentage = view_disaster.calculate_total_relief_aid_percentage()
    
    context = {
        'view_disaster': view_disaster,
        'total_relief_aid_percentage': total_relief_aid_percentage,
    }
    return render(request, 'data.html', context)




from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Disaster

def download_report(request, disaster_id):
    disaster = get_object_or_404(Disaster, id=disaster_id)

    report_content = f"Disaster Report - {disaster.location.name}-{disaster.location.name}\n\n{disaster.description}"

    response = HttpResponse(report_content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=disaster_report.txt'

    return response

from django.shortcuts import render, get_object_or_404
from .models import Disaster

def search_disaster(request):
    if request.method == 'POST':
        city_name = request.POST.get('city', '')
        try:
            disaster = Disaster.objects.get(location__name__iexact=city_name)
            return render(request, 'search_results.html', {'disaster': disaster})
        except Disaster.DoesNotExist:
            return render(request, 'search_results.html', {'error_message': 'Disaster not found.'})
    else:
        return render(request, 'search_form.html')

def rain(request):
    return render(request, 'rain.html')



from .forms import ProfilePictureForm, ProfileData, ProfileForm
from django.contrib.auth.models import User, Group

from django.contrib import messages


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models

@login_required
def profile(request, username):
    disaster = models.Disaster.objects.all()[:3]
    user = request.user  # Retrieve the authenticated user
    profile = get_object_or_404(models.Profile, user=user)
    return render(request, 'profile.html', {'user': user, 'profile': profile, 'disaster': disaster})



# Update Profile Picture
def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_page', username=request.user.username)
    else:
        form = ProfilePictureForm()

    return render(request, 'profile.html', {'form': form})
from django.contrib.auth.decorators import login_required


@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            
            profile.save()
            return redirect('homepage')  # Assuming you have a profile detail view
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'comp.html', {'form': form})

# Update Profile Data
def update_profile_data(request):
    if request.method == 'POST':
        form = ProfileData(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile data updated successfully.')
            return redirect('profile_page', username=request.user.username)
    else:
        form = ProfileData(instance=request.user.profile)

    return render(request, 'profile.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import RegistrationForm

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            # Authenticate the user
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            if new_user is not None:
                login(request, new_user)  # Log in the user
                return redirect('create_profile')  # Redirect to the home page after successful registration
            
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})



def community(request):
    disaster = models.Disaster.objects.all()[:6]
    categories = Category.objects.all()
    thread = Thread.objects.all()

    context = {
        
        'disaster': disaster,
        'categories': categories,
        'thread': thread,
       
    }
    return render(request, 'community.html', context)

def feedback(request, pk):
    return render(request, 'community.html')



# views.py

from django.http import JsonResponse
from .models import Post

def get_new_posts(request, thread_id):
    # Retrieve new posts for the specified thread (you can define your own logic)
    new_posts = Post.objects.filter(thread_id=thread_id, created_at__gt=request.GET.get('last_post_timestamp', ''))
    # Serialize new posts to JSON
    serialized_posts = [{'content': post.content, 'created_at': post.created_at} for post in new_posts]
    return JsonResponse(serialized_posts, safe=False)


from django.shortcuts import render
from .models import Category, Thread, Post


    

from django.shortcuts import get_object_or_404

def thread_detail(request, pk):
    disaster = models.Disaster.objects.all()[:6]
    categories = Category.objects.all()
    view_thread = models.Thread.objects.get(pk=pk)
    threads = Thread.objects.all()
    thread = get_object_or_404(Thread, pk=pk)
    posts = Post.objects.filter(thread=thread)
    post_count = models.Post.objects.count()

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user  # Set the author to the currently authenticated user
            post.thread = thread  # Set the thread to the current thread
            post.save()
            return redirect('thread_detail', pk=pk)  # Redirect to the thread detail page
    else:
        post_form = PostForm()
  

    context = {
        'disaster': disaster,
        'categories': categories,
        'view_thread' : view_thread,
        'threads': threads,
        'post_form': post_form,
        'posts':posts,
        'post_count': post_count
        
    }
    return render(request, 'inbox.html', context)


# Add more views for creating datas, posting replies, etc.

# views.py

from django.shortcuts import render, redirect
from .forms import PostForm


