from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

from models import PointRequest, PointResponse, ErrorResponse
from geometry import check_point_in_area


app = FastAPI(
    title="EyeTracker Lab1 API",
    description="API для проверки попадания точки в заданную область",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/check-point")
async def check_point(
    x: int,
    y: float, 
    r: float
):
    try:
        request_data = PointRequest(x=x, y=y, r=r)
        
        is_hit, execution_time = check_point_in_area(
            request_data.x, 
            request_data.y, 
            request_data.r
        )
        
        return PointResponse(
            result=is_hit,
            time=execution_time,
            now=datetime.now()
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(reason=str(e)).dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(reason=f"Внутренняя ошибка сервера: {str(e)}").dict()
        )


@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now()}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
