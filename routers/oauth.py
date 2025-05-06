from os import getenv

from authlib.integrations.starlette_client import (  # pyright: ignore[reportMissingTypeStubs]
  OAuth,
  OAuthError,
)
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from starlette.config import Config

GOOGLE_CLIENT_ID = getenv('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = getenv('GOOGLE_CLIENT_SECRET', '')

config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
_ = oauth.register( # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
  name='google',
  server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
  client_kwargs={'scope': 'openid email profile'}
)

router = APIRouter(prefix="/oauth", tags=["oauth"])

@router.post('/login')
async def login(request: Request) -> Response:
  redirect_uri = request.url_for('auth')  # This creates the url for the /auth endpoint
  return await oauth.google.authorize_redirect(request, redirect_uri) # pyright: ignore[reportOptionalMemberAccess, reportUnknownMemberType, reportUnknownVariableType]

@router.post('/auth')
async def auth(request: Request) -> Response:
  try:
    access_token = await oauth.google.authorize_access_token(request) # pyright: ignore[reportOptionalMemberAccess, reportUnknownMemberType, reportUnknownVariableType]
  except OAuthError:
    return RedirectResponse(url='/')
  user_data = await oauth.google.parse_id_token(request, access_token) # pyright: ignore[reportOptionalMemberAccess, reportUnknownMemberType, reportUnknownVariableType]
  request.session['user'] = dict(user_data) # pyright: ignore[reportUnknownArgumentType]
  return RedirectResponse(url='/')
