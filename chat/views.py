import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import Word


def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context={}
    return render(request, "chat/chatPage.html", context)

def get_word_data(request):
    words = Word.objects.all()
    serialized_data = [{'Words': word.words, 'Difficulty': word.difficulty, 'Score': word.score} for word in words]
    
    output=get_word_list(serialized_data,4,5,3,2,1)
    return JsonResponse(output, safe=False)

def get_word_list(
    word_dataset, num_very_easy, num_easy, num_moderate, num_difficult, num_challenging
):
    selected_words = []
    n = random.randint(2, 70)
    
    # Shuffle the serialized data to randomize word selection
    random.shuffle(word_dataset)
    
    for row in word_dataset:
        word = row["Words"]
        difficulty = row["Difficulty"]
        score = row["Score"]

        if difficulty == "Very Easy" and num_very_easy > 0:
            selected_words.append((word, score))
            num_very_easy -= 1
        elif difficulty == "Easy" and num_easy > 0:
            selected_words.append((word, score))
            num_easy -= 1
        elif difficulty == "Moderate" and num_moderate > 0:
            selected_words.append((word, score))
            num_moderate -= 1
        elif difficulty == "Challenging" and num_challenging > 0:
            selected_words.append((word, score))
            num_challenging -= 1
        elif difficulty == "Difficult" and num_difficult > 0:
            selected_words.append((word, score))
            num_difficult -= 1

        # Check if we have selected the desired number of words from each category
        if (
            num_very_easy == 0
            and num_easy == 0
            and num_moderate == 0
            and num_difficult == 0
            and num_challenging == 0
        ):
            break
    
    return selected_words
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')  # Redirect to a success page, change 'home' to your desired URL name.
        else:
            return render(request,'chat/register.html',{'error':'Registration failed. Please correct the errors below.'})

    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or do something else
                return redirect('/')  # Replace 'home' with your desired URL name
    else:
        form = AuthenticationForm()
    
    return render(request, 'chat/LoginPage.html')