from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings

# Step 1: Redirect user to Google's OAuth page
def google_login(request):
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    
    # Redirect user to Google's OAuth URL
    return redirect(f"{google_auth_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}")

# Step 2: Handle the callback from Google
def google_callback(request):
    if "error" in request.GET:
        return JsonResponse({"error": request.GET["error"]}, status=400)

    code = request.GET.get("code")

    # Exchange the authorization code for an access token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data)
    token_info = response.json()

    # Fetch user info
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {token_info['access_token']}"}
    user_info_response = requests.get(user_info_url, headers=headers)

    return JsonResponse(user_info_response.json())  # Return user details
