from app.controller import app
from app.config import HOST, PORT
import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)