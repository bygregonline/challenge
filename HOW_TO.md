<h1>How to run</h1>
___

run using docker
brew install jsonpp
brew install jq


```
docker run -p 8888:8888  bygreg/deliverect:v1
```

---

<br>
<br>
***CRUD OPERATIONS***
---

<br>

***Get menus***

return -> 200 code

```

curl   -v -H "Content-Type: application/json" http://localhost:8000/api/v1/menu/


```


<br>
Get all menus formated json with colors <br>
return ->200 code 

```

curl   -H "Content-Type: application/json" http://localhost:8000/api/v1/menu/ |jq


```

<br>
Get all menus formated json<br> 
return ->200 code 

```

curl   -H "Content-Type: application/json" http://localhost:8000/api/v1/menu/ |jsonpp


```

<br>
Get single menu using uuid<br>
method POST<br>
endpoint /api/v1/menu
http://localhost:8000/api/v1/menu/uuid<br>
return ->200 code <br>
sample


```

curl   -H "Content-Type: application/json" http://localhost:8000/api/v1/menu/74522465-5e05-4dd7-9673-17bd3a71d05c |jsonpp


```
<br>


***Create new menu***

Get single menu using uuid<br>
http://localhost:8000/api/v1/menu/uuid<br>
method POST
endpoint /api/v1/menu
return ->201 code or 400 <br>
sample
http://127.0.0.1:8000/api/v1/menu/

