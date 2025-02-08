from fastapi import FastAPI, HTTPException
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from sqlalchemy import exc
from src.inventory_module import ItemsController, ItemScheme
from fastapi.encoders import jsonable_encoder
import uvicorn
from src.kafka_driver import kafkaProducer,kafkaConsumer
from datetime import datetime
import json


app = FastAPI()

items_controler = ItemsController() 

kafka_producer = kafkaProducer(["item_created", "item_updated"]) 

kafka_consumer = kafkaConsumer(["item_created", "item_updated"])




####################################################
################ RESPONSE GENERETOR ################
####################################################



def create_response(success: bool, status_code: int, message: str, data):
    """
    ### Build response format
    #### Return: 
    ```
    Response format (dict)
    ```

    """
    
    return {
            "time": datetime.now().isoformat(),
            "success": success,
            "status_code": status_code,
            "message": message,
            "data": data
        }


 


####################################################
###################### ROUTES ######################
####################################################





@app.get("/items/{item_id}")
def get_item(item_id: int):
    """ 
    ## Retrieve a specific item by its ID from the database.
    
    #### Args:
    ```
    id (int): The unique identifier of the item.
    ```

    #### Return: 
    A single item.
    """

    # GET ITEM DATA
    item_data = items_controler.get_item(item_id)
    
    # CHECK STATUS   
    status = True if item_data != None else False  

    # BUILD RESPONSE
    res = create_response(
        success=status,
        status_code= 200 if status else 404,
        message="Ok" if status else "Item not found.",
        data= jsonable_encoder(item_data) if status else None
        )
    
    return JSONResponse(content=res, status_code=res["status_code"])
    





@app.get("/items")
def get_items():
    """
    ## Get all items.

    #### Returns:
    A list of items stored in the database.
    """

    # GET ITEMS DATA
    all_items = items_controler.get_all_items()

    # CHECK STATUS 
    status = True if all_items != None else False
    
    # BUILD RESPONSE
    res = create_response(
        success = status,
        status_code = 200 if status else 503,
        message =  "Ok" if status else "Database issue.",
        data = jsonable_encoder(all_items) if status else None
        )
    
    return JSONResponse(content=res, status_code=res["status_code"])



@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """ 
    ## Delete item by ID.
        
    #### Args:
    ```
    id (int): The unique identifier of the item.
    ```

    #### Return:
    The deleted item.
    """

    # TRY TO DELETE
    status = items_controler.delete_item(item_id)
    
    # IF ITEM NOT FOUND
    if status == None:
    
        # BUILD RESPONSE
        res = create_response(
            success = False,
            status_code = 404,
            message = "Item not found.",
            data = None
            )
        
    # IF ITEM DELETED
    else:

        # BUILD RESPONSE
        res = create_response(
            success = True,
            status_code = 200,
            message = "The item was deleted successfully.",
            data = jsonable_encoder(status)
            )
        
    return JSONResponse(content=res, status_code=res["status_code"])




@app.post("/items")
def create_item(item: ItemScheme):
    """ 
    ## Create a new item.
 
    #### Return: 
    The created item with its assigned ID.
    """

    # TRY TO ADD NE ITEM
    item_data = items_controler.create_item(**item.model_dump())
    
    # CHECK STATUS   
    status = True if item_data != None else False  

    # BUILD RESPONSE
    res = create_response(
        success = status,
        status_code = 201 if status else 500,
message = "The item was created successfully." if status else "Database issue.",
        data = jsonable_encoder(item_data) if status else None
        )
   

    if status:
        kafka_producer.send_msg("item_created", msg=json.dumps(res))
    
    return JSONResponse(content=res, status_code=res["status_code"])



@app.put("/items/{item_id}")
def update_item(item_id,item: ItemScheme):
    """ 
    ## Update an existing item in the database.
   
    #### Return: 
    The updated item data.
    """
    
    # TRY TO UPDATE
    status = items_controler.update_item(item_id=item_id,item=item)
    
    # IF ITEM NOT FOUND
    if status == None:
    
        # BUILD RESPONSE
        res = create_response(
            success = False,
            status_code = 404,
            message = "Item not found.",
            data = None
            )
        
    # IF ITEM UPDATE
    else:

        # BUILD RESPONSE
        res = create_response(
            success = True,
            status_code = 200,
            message = "The item was updated successfully.",
            data = jsonable_encoder(status)
            )
       
        kafka_producer.send_msg("item_updated", msg=json.dumps(res))

    return JSONResponse(content=res, status_code=res["status_code"])







####################################################
################## ERROR HANDLING ##################
####################################################


class DatabaseExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except exc.SQLAlchemyError:
            return JSONResponse(status_code=503, content={"detail": "Database unavailable"})

app.add_middleware(DatabaseExceptionMiddleware)




class CustomExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return create_response(success=False, status_code=exc.status_code, message=exc.detail, data=None)
        except Exception:
            return create_response(success=False, status_code=500, message="Internal Server Error", data=None)

app.add_middleware(CustomExceptionMiddleware)








if __name__ == "__main__":
    kafka_consumer.get_msgs()
    uvicorn.run(app, host="0.0.0.0", port=8000)