from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

from config import Config as cfg
from api.database.schemas.TradeDesk import TradeDesk, get_sql
from api.database.execute_query import execute_query

API_KEY = "1234567asdfgh"
API_KEY_NAME = "access_token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)

app = FastAPI()


async def get_api_key(
    api_key_query: str = Security(api_key_query)):
    if api_key_query == API_KEY:
        return api_key_query
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


@app.get(f'{cfg.REST_URL_PREFIX}/query')
async def query(account_id: str, response_model=TradeDesk):

    sql = get_sql(account_id)
    data = execute_query(sql)

    return data


@app.get('/documentation', tags=["documentation"])
async def get_documentation(api_key: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(openapi_url='/openapi.json', title="docs")
    return response


@app.get('/openapi.json', tags=["documentation"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
    )
    return response
