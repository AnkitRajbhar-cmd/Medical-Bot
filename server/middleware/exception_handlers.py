from fastapi.responses import JSONResponse
import traceback

async def catch_exception_middleware(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print("\n🔥 REAL ERROR START 🔥")
        traceback.print_exc()
        print("🔥 REAL ERROR END 🔥\n")

        return JSONResponse(
            content={
                "error": str(e),
                "type": type(e).__name__
            },
            status_code=500
        )