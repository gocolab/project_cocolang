# github oauth : https://youtu.be/Pm938UxLEwQ?si=waW2OkK5Dp6texol

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import httpx
import uvicorn

app = FastAPI()

# Replace with your GitHub client ID and secret
github_client_id = "your_github_client_id"
github_client_secret = "your_github_client_secret"

@app.get("/github/login")
def github_login():
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={github_client_id}")

@app.get("/github/callback")
async def github_callback(code: str):
    params = {
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'code': code
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post('https://github.com/login/oauth/access_token', params=params, headers={'Accept': 'application/json'})
    
    access_token = response.json().get("access_token")
    if access_token:
        async with httpx.AsyncClient() as client:
            headers = {'Authorization': f'Bearer {access_token}'}
            user_response = await client.get('https://api.github.com/user', headers=headers)
        return user_response.json()
    else:
        return {"error": "Failed to obtain access token"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)