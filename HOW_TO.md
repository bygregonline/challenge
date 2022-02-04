# Sumary
___

Date : 2022-02-03


* The application is fully containerized,
* Ready to be deployed
* just follow the steps in this document

---

***Features required and extra features***

* If something goes wrong the server always return 400 error with a friendly JSON message
* Almost 400 Lines of testing code was written to validate end-points
* Create Menu simple validation also convert valid string number to number and vice versa returns the a new UUID
* Tthe complete JSON schema has to be sent in the body to create a new menu
* GET menu by UUID returns JSON or 404 
* DELETE menu by UUID returns 200 or 404
* UPDATE menu by UUID accepts partial JSON Schema return the updated object
* CREATE ORDER 
	* The full JSON schema is validated before processing, even valid string numbers should be rejected, No extra parameters are allowed, also a non-positive number should be rejected on the first step.
	* Just in case two or more orders contain the same menu uuid it is reduced to a single order, before validation
	* Run database validation to validate if there is enough inventory to complete the order 
	* Validate payment vs order * quantity
	* New successful orders return a unique UUID 
	* You can get the order using the UUID ***Not in the original requirement***
	* ***TODO***. Write code documentation only if it is  demanded 
	* The order doesn't update the database. This option was programmed this way to be able to run stress tests against the container.




<br>
<br>
<br>
#### HOW TO
---

***only for macs users***

install json parser & beautifiers "only if you want"


```

brew install jsonpp
brew install jq


```

***run using dockers***

```

docker run -d -p 8000:8888  bygreg/deliverect:v1


```

---

<br>
<br>
### CRUD OPERATIONS
---

<br>

***Get all menus***<br>
method GET<br>
endpoint /api/v1/menu<br>
return ->200 code  <br>
returns JSON <br>

sample

```

curl   -v -H "Content-Type: application/json" http://localhost:8000/api/v1/menu/


```

<br>
***Get all menus formated json with colors***<br>
method GET<br>
endpoint /api/v1/menu<br>
return ->200 code  <br>
returns JSON <br>

sample

```

curl   -H "Content-Type: application/json" http://localhost:8000/api/v1/menu/ |jq


```

<br>
***GET all menus formated json***<br> 
method GET<br>
endpoint /api/v1/menu<br>
return ->200 code  <br>
returns JSON <br>

sample

```

curl   -H "Content-Type: application/json" http://localhost:8000/api/v1/menu/ |jsonpp


```

<br>
***GET single menu using UUID***<br>
method GET<br>
endpoint  api/v1/menu/<:uuid><br>
return ->200 code <br>
returns JSON <br>


sample

```

curl   -H "Content-Type: application/json" http://localhost:8000/api/v1/menu/74522465-5e05-4dd7-9673-17bd3a71d05c |jsonpp


```

<br>

***NEW menu***<br> 
method POST<br>
endpoint /api/v1/menu<br>
return code ->201 code | 400 <br>
returns JSON <br>


sample

```

curl -d '{   "price":12.34, "description":"some menu", "quantity":100}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/v1/menu |jsonpp


```

<br>

***UPDATE menu***<br> 
method PATCH <br>
endpoint /api/v1/menu<:uuid><br>
return code ->200 code | 404 | 400 <br>
returns JSON <br>


sample

```

curl -d '{   "price":12.34, "quantity":530}' -H "Content-Type: application/json" -X PATCH http://localhost:8000/api/v1/menu/133f1688-9a3b-4df8-96ce-bf90fcfd8c0f |jsonpp


```

<br>

***DELETE menu***<br> 
method DELETE<br>
endpoint /api/v1/menu<:uuid><br>
return code ->200 code | 404 | 400 <br>
returns JSON <br>


sample

```

curl   -X DELETE http://localhost:8000/api/v1/menu/133f1688-9a3b-4df8-96ce-bf90fcfd8c0f |jsonpp


```
<br>
<br>
### CREATE ORDERS

<br>

***CREATE Order***<br> 
method POST<br>
endpoint /api/v1/order<br>
return code ->200 code |  400 <br>
returns JSON <br>


sample

```

curl -d '{ "order": [ {"uuid": "ad1d401f-ce58-4106-b8ba-924adef436af", "quantity": 13 }], "info": {"note": "bla bla","payment": 187.2 }}' -H "Content-Type: application/json"  -X POST http://localhost:8000/api/v1/order |jsonpp


```
<br>


sample ***Invalid payment***

```

curl -d '{ "order": [ {"uuid": "ad1d401f-ce58-4106-b8ba-924adef436af", "quantity": 10 }], "info": {"note": "bla bla","payment": 7.2 }}' -H "Content-Type: application/json"  -X POST http://localhost:8000/api/v1/order |jsonpp

{
  "status": "error",
  "data": {
    "msg": "payment is not correct",
    "invalid": "144.0 != 7.2 "
  },
  "time": "2022-02-04 12:44:38.495071"
}


```

<br>


sample ***Invalid uuid***

```

curl -d '{ "order": [ {"uuid": "ad1d401f-ce58-4106-b8ba-024adef436af", "quantity": 10 }], "info": {"note": "bla bla","payment": 7.2 }}' -H "Content-Type: application/json"  -X POST http://localhost:8000/api/v1/order |jsonpp

{
  "status": "error",
  "data": {
    "msg": "uuid not found",
    "invalid": "{'ad1d401f-ce58-4106-b8ba-024adef436af'}"
  },
  "time": "2022-02-04 12:51:00.470250"
}


```

<br>


sample ***multimple orders same uuid***<br>
***Note*** Change UUID with the response UUID

```

curl -d '{ "order": [   {
            "uuid": "ad1d401f-ce58-4106-b8ba-924adef436af",
            "quantity": 4
            
        },
        {
          "uuid": "ad1d401f-ce58-4106-b8ba-924adef436af",
            "quantity": 1
        },
        
        {
          "uuid": "ad1d401f-ce58-4106-b8ba-924adef436af",
            "quantity": 4
        }], "info": {"note": "bla bla","payment": 129.6 }}' -H "Content-Type: application/json"  -X POST http://localhost:8000/api/v1/order |jsonpp


  "status": "success",
  "uuid": "f25a7094-a5ea-42d2-a9e2-81632a6f7c10",
  "time": "2022-02-04 12:54:48.648217"


curl  http://localhost:8000/api/v1/order/f25a7094-a5ea-42d2-a9e2-81632a6f7c10 |jsonpp

{
  "order": {
    "created_at": "2022-02-04T12:54:48.641261",
    "uuid": "f25a7094-a5ea-42d2-a9e2-81632a6f7c10",
    "amount": 129.6,
    "note": "bla bla",
    "items": [
      {
        "menu": "ad1d401f-ce58-4106-b8ba-924adef436af",
        "quantity": 9
      }
    ]
  }
}

```

<br>
***GET Order by UUID***<br> 
method GET<br>
endpoint /api/v1/order<:uuid><br>
return code ->200 code | 404 | 400 <br>
returns JSON <br>


sample

```

curl  http://localhost:8000/api/v1/order/9e475e2b-7d6d-4def-8e71-97f15db68927 |jsonpp


```


---

<br>
<br>
### EXTRA  END-POINTS
---

<br>
***GET server info***<br> 
method GET<br>
endpoint /api/v1/info<br>
return ->200 code  <br>
returns JSON <br>

sample

```

curl   -v -H "Content-Type: application/json" http://localhost:8000/api/v1/info |jsonpp


```

<br>
***GET server ps***<br> 
method GET<br>
endpoint /api/v1/ps<br>
return ->200 code  <br>
returns txt <br>

sample

```

curl   -H "Content-Type: application/json" http://localhost:8000/api/v1/ps


```


<br>
<br>
### Extra info


By the way, feel free to download all test-cases and run them by yourself with your postman app.<br>
Download the test cases from the following [Link](https://raw.githubusercontent.com/bygregonline/challenge/main/challenge.postman_collection.json) <br>
Import the test cases to your postman application <br>
File-Import-Load-File

```

wget https://raw.githubusercontent.com/bygregonline/challenge/main/challenge.postman_collection.json


```






