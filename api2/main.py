import json
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field , ValidationError
from typing import Optional
# import model.prediction as pp
import pandas as pd
import pickle
import pandas as pd



app = FastAPI()


properties =  [
        {
            "area": 1450,
            "property_type": "house",
            "rooms_number": 4,
            "zip_code": 0,
            "land_area": 0,
            "garden": 'true',
            "garden_area": 0,
            "equipped_kitchen": 'true',
            "full_address": "string",
            "swimming_pool": 'true',
            "furnished": 'true',
            "open_fire": 'true',
            "terrace": 'true',
            "terrace_area": 0,
            "facades_number": 0,
            "building_state": "string"
        }
    ]

class Data(BaseModel):
    area: int
    property_type: str 
    rooms_number: int
    zip_code: int 
    land_area: Optional[int] 
    garden: Optional[bool] = None
    garden_area: Optional[int] = None
    equipped_kitchen: Optional[bool] = None
    full_address: Optional[str] = None
    swimming_pool: Optional[bool] = None
    furnished: Optional[bool] = None
    open_fire: Optional[bool] = None
    terrace: Optional[bool] = None
    terrace_area: Optional[int] = None
    facades_number: Optional[int] = None
    building_state: Optional[str] = None



@app.get("/")
async def root():
    return {"message": "alive"}



@app.post("/prediction/")
async def post_data(data: Data = Body(embed=True)):
    if data.area  == 0:
        raise HTTPException(status_code = 422, detail = "Area of the property")      
    if data.zip_code  == 0:
        raise HTTPException(status_code = 422, detail = "zip-code of the property") 
    if data.rooms_number  == 0:
        raise HTTPException(status_code = 422, detail = "number of rooms")
    
    df = pd.DataFrame.from_dict([data.dict()])
    pred = pp.prediction(df)
    print(pred)
    prediction_dict = {"Prediction" : pred[0]}
    print(data.dict())
    return prediction_dict


@app.post("/properties")
async def validate_property(property: Data):
    properties.append(property)
    with open('properties.json', 'w') as f:
        json.dump(properties, f)
    return {"message": "Property added"}


@app.get("/allproperties")
async def root():
    return {"prop": properties}

@app.get("/info")
async def info():
    return """
    Send a POST request to /predict with the following data in JSON format:

    {
        "data": {
            "area": int,
            "property-type": "APARTMENT" | "HOUSE" | "OTHERS",
            "rooms-number": int,
            "zip-code": int,
            "land-area": Optional[int],
            "garden": Optional[bool],
            "garden-area": Optional[int],
            "equipped-kitchen": Optional[bool],
            "full-address": Optional[str],
            "swimming-pool": Optional[bool],
            "furnished": Optional[bool],
            "open-fire": Optional[bool],
            "terrace": Optional[bool],
            "terrace-area": Optional[int],
            "facades-number": Optional[int],
            "building-state": Optional[
                "NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"
            ]
        }
    }
    """
    
    
    
    
    
    
    
    
    
    
    

# def validate_property(property: Property):
#     required_attributes = ["area", "property_type", "rooms_number", "zip_code"]
#     for attr in required_attributes:
#         if not hasattr(property, attr):
#             raise ValueError(f"Property is missing required attribute '{attr}'")
#         return property


# print(properties)
# df = pd.DataFrame(properties)
# print(df)

# # Fill missing values with a specified value
# df_filled = df.fillna(value=0)













