from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "56a553d3-5dac-44ed-a287-9de81af2c3d1"
FLOW_ID = "b063b304-55a5-4f56-8a69-d24e2429c071"
APPLICATION_TOKEN = "AstraCS:HONnmIdkcIcBFaQZUmTtaUnc:5fd64877ee59298cd0557c1348226de69f3d6256ff3f0c2b03418a0fc011e38d"
ENDPOINT = "spyandgrow"


class RunFlowRequest(BaseModel):
    message: str
    output_type: str = "chat"
    input_type: str = "chat"


@app.get("/")
def setup():
    return {"result" : True}

@app.post("/run-flow")
async def run_flow(request: RunFlowRequest):
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": request.message,
        "output_type": request.output_type,
        "input_type": request.input_type,
    }
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        output = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
        return output
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


# Example usage: Run the server and make a POST request to http://localhost:8000/run-flow
# with a JSON payload like {"message": "slashritesh"}
