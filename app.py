'''
This script is the main entry point for the FastAPI application. It defines the API endpoints and the logic for the p-value calculation from employee table data.

Author: Sana Iqbal
For: Syndio Take Home Assignment
'''
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import JSONResponse
import os
from config import *
from pvalues import *
from utils import *
logger = setup_logging( script_name=os.path.basename(__file__))
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/")
def home_screen():
    return {
        "message": "Welcome to the Employee Compensation Analysis API",
        "endpoints": {
            "/pvalue": "Get the p-value for the specified department"
        }
    }

@app.get("/pvalue")
def get_pvalue(department: Optional[str] = Query(None, description="The department name")):
    PV_FEATURE = "protected_class"
    try:
        pvalue = calculate_pvalue(department, pv_feature=PV_FEATURE)
        if not isinstance(pvalue, float):
            raise ValueError("P-value must be a float")
        if pvalue is None:
            raise HTTPException(status_code=404, detail="No data found for the specified department")
        response = {"pvalue": pvalue}
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except ValueError as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Bad Request{e}")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error:{e}")


if __name__ == "__main__":
    import uvicorn
    #look for the environment variable PORT, if it does not exist, default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
