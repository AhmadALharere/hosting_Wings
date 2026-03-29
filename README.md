"# Wings_project" 

API Docs:

## Base URL:https://hosting-wings.onrender.com
## Authentication:
**Type**:JWT Authentication
**Header**(for authenticated endpoints): None
**Cookies**:[access_token , refresh_token]
---

## End Points:

### 1. Login

| Property           | Value                                         |
|--------------------|-----------------------------------------------|
| **URL**            | `/api/auth/user/login/`                       |
| **Method**         | `POST`                                        |
| **Authentication** | Not Required                                  |
| **Content-Type**   | `application/json`                            |
| **Description**    | `Log in with username or email and password.` |

#### Request Body

```json
either
{ "username": "newuser", "password": "srhjg" }
or
{ "email": "newuser@gmail.com", "password": "srhjg" }
```
#### Responses

| HTTP Status         |                    Body                            |
|---------------------|----------------------------------------------------|
| **200 OK**          | `{ "message": "Login successful"}`                 |
|---------------------|----------------------------------------------------|
| **400 Bad Request** | `{"error": "Invalid credentials"}`                 |
|---------------------|----------------------------------------------------|



### 2. Logout

| Property           | Value                                         |
|--------------------|-----------------------------------------------|
| **URL**            | `/api/auth/user/logout/`                      |
| **Method**         | `POST`                                        |
| **Authentication** | Required                                      |
| **Content-Type**   | null                                          |
| **Description**    | `Log out from current user`                   |

#### Request Body

null

#### Responses

| HTTP Status         | Body                                                                      |
|---------------------|---------------------------------------------------------------------------|
| **200 OK**          | `{"message": "Logged out successfully"}`                                  |
|---------------------|---------------------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`             |
|---------------------|---------------------------------------------------------------------------|


### 3. Registration

| Property           | Value                                         |
|--------------------|-----------------------------------------------|
| **URL**            | `/api/auth/user/register/`                    |
| **Method**         | `POST`                                        |
| **Authentication** | Not Required                                  |
| **Content-Type**   | `application/json`                            |
| **Description**    | signup                                        |

#### Request Body

```json
{"username": "newuser","email": "newuser@example.com","password1": "aeamlgng","password2": "aeamlgng",  "birth_date":"15/9/2003",
  "gender":"Male",
"phone_number":"+963111111111","image":<image>}
```
#### Responses

| HTTP Status         | Body                                                                      |
|---------------------|---------------------------------------------------------------------------|
| **200 OK**          | `{"message": "Sign up successful"}`                                       |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `{"username": ["A user with that username already exists."]}`             |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `{"email": ["Email is already in use."]}`                                 |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `["phone number is already in use."]`                                     |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `{"non_Failed_errors": ["The two password Faileds didn't match."]}`       |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `{"username": ["This Failed is required."]}`                              |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `{"email": ["This Failed is required."]}`                                 |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `{"password1": ["This Failed is required."]}`                             |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `{"password2": ["This Failed is required."]}`                             |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `{"gender": ["This Failed is required."]}`                                |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `{"birth_date": ["This Failed is required."]}`                            |
|---------------------|---------------------------------------------------------------------------|



### 4. Change Password

| Property           | Value                                                          |
|--------------------|----------------------------------------------------------------|
| **URL**            | `/auth/password/change/`                                       |
| **Method**         | `POST`                                                         |
| **Authentication** | Required                                                       |
| **Content-Type**   | `application/json`                                             |
| **Description**    | `change password for current user account and logging out`     |

#### Request Body

```json
{"old_password": "stlhks","new_password": "NewPassword","confirm_password": "NewPassword"}
```
#### Responses

| HTTP Status         | Body                                                                      |
|---------------------|---------------------------------------------------------------------------|
| **200 OK**          | `{"message": "Password changed successfully. Please login again."}`       |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `{"error": "Old password is incorrect"}`                                  |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `{"error": "All fields are required"}`                                    |
|---------------------|---------------------------------------------------------------------------|
| **400 Bad Request** | `{"error": "Passwords do not match"}`                                     |
|---------------------|---------------------------------------------------------------------------|


### 5. Refresh Tokens

| Property           | Value                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------|
| **URL**            | `/api/auth/user/refresh/`                                                                    |
| **Method**         | `POST`                                                                                       |
| **Authentication** | Required                                                                                     |
| **Content-Type**   | None                                                                                         |
| **Description**    | `refresh access_token using refresh_token if still valid, otherwise re-login  is required`   |

#### Request Body

null

#### Responses

| HTTP Status         | Body                                                                                      |
|---------------------|-------------------------------------------------------------------------------------------|
| **200 OK**          | `{"message": "Token refreshed"}`                                                          |
|---------------------|-------------------------------------------------------------------------------------------|
| **401 Unauthorized**| `{"error": "No refresh token"}`                                                           |
|---------------------|-------------------------------------------------------------------------------------------|
| **401 Unauthorized**| `{"error": "Invalid or expired refresh token"}`                                           |
|---------------------|-------------------------------------------------------------------------------------------|




### 6. Log in/sign up with Google

| Property           | Value                                                          |
|--------------------|----------------------------------------------------------------|
| **URL**            | `/api/auth/user/google/`                                       |
| **Method**         | `POST`                                                         |
| **Authentication** | Not Required                                                   |
| **Content-Type**   | `application/json`                                             |
| **Description**    | `Log in or Sign up for google accounts`                        |

#### Request Body

```json
{"access_token":"***.....","provider":"google"}
```
#### Responses

| HTTP Status         | Body                                                                                      |
|---------------------|-------------------------------------------------------------------------------------------|
| **200 OK**          | `{"message": "Login successful"}`                                                         |
|---------------------|-------------------------------------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Invalid Google access token."}`                                              |
|---------------------|-------------------------------------------------------------------------------------------|
| **400 Bad Request** | `{"non_Failed_errors": ["Incorrect input. access_token or code is required."]}`           |
|---------------------|-------------------------------------------------------------------------------------------|



### 7. Get profile

| Property           | Value                                                          |
|--------------------|----------------------------------------------------------------|
| **URL**            | `/api/auth/user/profile/`                                      |
| **Method**         | `GET`                                                          |
| **Authentication** | Required                                                       |
| **Content-Type**   | null                                                           |
| **Description**    | `get profile data for current user`                            |

#### Request Body


#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 1>`                                                     |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|



### 8. Edit proflie

| Property           | Value                                                                                                    |
|--------------------|----------------------------------------------------------------------------------------------------------|
| **URL**            | `/api/auth/user/profile/`                                                                                |
| **Method**         | `PATCH`                                                                                                  |
| **Authentication** | Required                                                                                                 |
| **Content-Type**   | `application/json`                                                                                       |
| **Description**    | `edit profile data for current user,this api did not save any change to username, email or phone_number `|

#### Request Body

```json
{"username": "ahmad","email": "ahmed@example.com","first_name": "أحمد","last_name": "الحريري","gender": "Male","birth_date":"2003-09-15","phone_number": "0954368434","image":<image>}
```

#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 1>`                                                     |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|



### 9. Flight List

| Property           | Value                                          |
|--------------------|------------------------------------------------|
| **URL**            | `/api/flights/`                                |
| **Method**         | `GET`                                          |
| **Authentication** | Required                                       |
| **Content-Type**   | None                                           |
| **Description**    | `get Flight List, support variant of options`  |

#### Request Body



#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 2>`                                                     |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|


#### options:


| key                                | type          | values                                                      |
|------------------------------------|---------------|-------------------------------------------------------------|
| type                               | filter        | ` LEAVING , COMING `                                        |
|------------------------------------|---------------|-------------------------------------------------------------|
| has_economy| filter                | filter        | ` <boolean value> `                                         |
|------------------------------------|---------------|-------------------------------------------------------------|
| has_premium_economy| filter        | filter        | ` <boolean value> `                                         |
|------------------------------------|---------------|-------------------------------------------------------------|
| has_business| filter               | filter        | ` <boolean value> `                                         |
|------------------------------------|---------------|-------------------------------------------------------------|
| has_first_class| filter            | filter        | ` <boolean value> `                                         |
|------------------------------------|---------------|-------------------------------------------------------------|
| scheduled_departure_minimum_date   | filter        | `<date value: yyyy-mm-dd>`                                  |
|------------------------------------|---------------|-------------------------------------------------------------|
| scheduled_departure_time_range_min | filter        | `<integer value>`                                           |
|------------------------------------|---------------|-------------------------------------------------------------|
| scheduled_departure_time_range_max | filter        | `<integer value>`                                           |
|------------------------------------|---------------|-------------------------------------------------------------|
| scheduled_arrival_maximum_date     | filter        | `<date value: yyyy-mm-dd>`                                  |
|------------------------------------|---------------|-------------------------------------------------------------|
| scheduled_arrival_time_range_max   | filter        | `<integer value>`                                           |
|------------------------------------|---------------|-------------------------------------------------------------|
| scheduled_arrival_time_range_min   | filter        | `<integer value>`                                           |
|------------------------------------|---------------|-------------------------------------------------------------|
| status                             | filter        | `scheduled , departed , delayed , arrived , cancelled `     |
|------------------------------------|---------------|-------------------------------------------------------------|
| counterpart                        | filter        | `<integer value:id> `                                       |
|------------------------------------|---------------|-------------------------------------------------------------|
| counterpart_airport                | filter        | `<integer value:id> `                                       |
|------------------------------------|---------------|-------------------------------------------------------------|
| page                               | paginator     | `<integer number>`                                          |
|------------------------------------|---------------|-------------------------------------------------------------|
| page_size                          | paginator     | `<integer number>`                                          |
|------------------------------------|---------------|-------------------------------------------------------------|
| ordering                           | order method  | ` counterpart , scheduled_departure , scheduled_arrival`    |
|------------------------------------|---------------|-------------------------------------------------------------|
| search                             | search        | `<string>`                                                  |
|------------------------------------|---------------|-------------------------------------------------------------|




### 10. Flight Details

| Property           | Value                                          |
|--------------------|------------------------------------------------|
| **URL**            | `/api/flights/<str:flight_number>`             |
| **Method**         | `GET`                                          |
| **Authentication** | Required                                       |
| **Content-Type**   | None                                           |
| **Description**    | `get Flight details`                           |

#### Request Body



#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 3>`                                                     |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|
| **404 Not Found**   | `{"detail": "No Flight matches the given query."}`             |
|---------------------|----------------------------------------------------------------|




### 11. Airport List

| Property           | Value                                          |
|--------------------|------------------------------------------------|
| **URL**            | `/api/flights/Airports/`                       |
| **Method**         | `GET`                                          |
| **Authentication** | Required                                       |
| **Content-Type**   | None                                           |
| **Description**    | `get Airports List, support variant of options`|

#### Request Body



#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 4>`                                                     |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|


#### options:


| key                                | type          | values                                                      |
|------------------------------------|---------------|-------------------------------------------------------------|
| destination                        | filter        | ` <integer value:id> `                                      |
|------------------------------------|---------------|-------------------------------------------------------------|
| min_rate                           | filter        | ` <float value:[0.0 , 5.0]> `                               |
|------------------------------------|---------------|-------------------------------------------------------------|
| max_rate                           | filter        | ` <float value:[0.0 , 5.0]> `                               |
|------------------------------------|---------------|-------------------------------------------------------------|
| page                               | paginator     | `<integer number>`                                          |
|------------------------------------|---------------|-------------------------------------------------------------|
| page_size                          | paginator     | `<integer number>`                                          |
|------------------------------------|---------------|-------------------------------------------------------------|
| ordering                           | order method  | ` name , rate , destination`                                |
|------------------------------------|---------------|-------------------------------------------------------------|
| search                             | search        | `<string>`                                                  |
|------------------------------------|---------------|-------------------------------------------------------------|


### 12. Destination List

| Property           | Value                                             |
|--------------------|---------------------------------------------------|
| **URL**            | `/api/flights/Destination/`                       |
| **Method**         | `GET`                                             |
| **Authentication** | Required                                          |
| **Content-Type**   | None                                              |
| **Description**    | `get Destination List, support variant of options`|

#### Request Body



#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 4>`                                                     |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|


#### options:


| key                                | type          | values                                                      |
|------------------------------------|---------------|-------------------------------------------------------------|
| country                            | filter        | ` <str value> `                                             |
|------------------------------------|---------------|-------------------------------------------------------------|
| min_static_rate                    | filter        | ` <float value:[0.0 , 5.0]> `                               |
|------------------------------------|---------------|-------------------------------------------------------------|
| max_static_rate                    | filter        | ` <float value:[0.0 , 5.0]> `                               |
|------------------------------------|---------------|-------------------------------------------------------------|
| min_avg_rate                       | filter        | ` <float value:[0.0 , 5.0]> `                               |
|------------------------------------|---------------|-------------------------------------------------------------|
| max_avg_rate                       | filter        | ` <float value:[0.0 , 5.0]> `                               |
|------------------------------------|---------------|-------------------------------------------------------------|
| is_top_destination                 | filter        | ` <boolean value> `                                         |
|------------------------------------|---------------|-------------------------------------------------------------|
| page                               | paginator     | `<integer number>`                                          |
|------------------------------------|---------------|-------------------------------------------------------------|
| page_size                          | paginator     | `<integer number>`                                          |
|------------------------------------|---------------|-------------------------------------------------------------|
| ordering                           | order method  | ` city , country , static_rate , avg_rate `                 |
|------------------------------------|---------------|-------------------------------------------------------------|
| search                             | search        | `<string>`                                                  |
|------------------------------------|---------------|-------------------------------------------------------------|



### 13. Top Destination List

| Property           | Value                                                            |
|--------------------|------------------------------------------------------------------|
| **URL**            | `/api/flights/Destination/top`                                   |
| **Method**         | `GET`                                                            |
| **Authentication** | Not Required                                                     |
| **Content-Type**   | None                                                             |
| **Description**    | `get top Destination List,without authentication for home screen`|

#### Request Body



#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 5>`                                                     |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|



### 14. Get Social Accounts

| Property           | Value                                 |
|--------------------|---------------------------------------|
| **URL**            | `/api/company/social/`                |
| **Method**         | `GET`                                 |
| **Authentication** | Not Required                          |
| **Content-Type**   | None                                  |
| **Description**    | `get social accounts for the company` |

#### Request Body



#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `[{"id": 1,"name": "Google","link": "example@gmail.com"},...]` |
|---------------------|----------------------------------------------------------------|



### 15. Get Careers List

| Property           | Value                                 |
|--------------------|---------------------------------------|
| **URL**            | `/api/company/careers/`               |
| **Method**         | `GET`                                 |
| **Authentication** | Not Required                          |
| **Content-Type**   | None                                  |
| **Description**    | `get Career list for this company `   |

#### Request Body


#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `< file 6 >`                                                   |
|---------------------|----------------------------------------------------------------|




### 16. Get Careers List

| Property           | Value                                 |
|--------------------|---------------------------------------|
| **URL**            | `/api/company/careers/<int:id>/`      |
| **Method**         | `GET`                                 |
| **Authentication** | Not Required                          |
| **Content-Type**   | None                                  |
| **Description**    | `get Career details for this company `|

#### Request Body



#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `< file 7 >`                                                   |
|---------------------|----------------------------------------------------------------|



### 17. submit on Career

| Property           | Value                                   |
|--------------------|-----------------------------------------|
| **URL**            | `/api/company/careers/<int:id>/submit/` |
| **Method**         | `POST`                                  |
| **Authentication** | Not Required                            |
| **Content-Type**   | `application/json`                      |
| **Description**    | `submit to a career `                   |

#### Request Body

```json
{ "full_name": "user", "email": "user@gmail.com","phone":"+963000000000","message": "text", "cv": "<file>" }
```

#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `< file 7 >`                                                   |
|---------------------|----------------------------------------------------------------|
| **400 Bad Requist** | `{"full_name": ["This field is required."],"email": ["This field is required."],"phone": ["This field is required."],"message": ["This field is required."]}`                  |
|---------------------|----------------------------------------------------------------|



### 18. Get article List

| Property           | Value                                 |
|--------------------|---------------------------------------|
| **URL**            | `/api/company/articles/`              |
| **Method**         | `GET`                                 |
| **Authentication** | Not Required                          |
| **Content-Type**   | None                                  |
| **Description**    | `get article list for company site`   |

#### Request Body



#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `< file 9 >`                                                   |
|---------------------|----------------------------------------------------------------|



### 19. Get investors List

| Property           | Value                                 |
|--------------------|---------------------------------------|
| **URL**            | `/api/company/investors/`             |
| **Method**         | `GET`                                 |
| **Authentication** | Not Required                          |
| **Content-Type**   | None                                  |
| **Description**    | `get investors list for company site` |

#### Request Body



#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `< file 10 >`                                                  |
|---------------------|----------------------------------------------------------------|



### 20. Get partners List

| Property           | Value                                 |
|--------------------|---------------------------------------|
| **URL**            | `/api/company/partners/`              |
| **Method**         | `GET`                                 |
| **Authentication** | Not Required                          |
| **Content-Type**   | None                                  |
| **Description**    | `get partners list for company site`  |

#### Request Body



#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `< file 11 >`                                                  |
|---------------------|----------------------------------------------------------------|


### 21. Booking List

| Property           | Value                                             |
|--------------------|---------------------------------------------------|
| **URL**            | `/api/service/booking/`                           |
| **Method**         | `GET`                                             |
| **Authentication** | Required                                          |
| **Content-Type**   | None                                              |
| **Description**    | `get Booking List for current user`               |

#### Request Body



#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 12>`                                                    |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|

### 22. Booking Details

| Property           | Value                                             |
|--------------------|---------------------------------------------------|
| **URL**            | `/api/service/booking/3/`                         |
| **Method**         | `GET`                                             |
| **Authentication** | Required                                          |
| **Content-Type**   | None                                              |
| **Description**    | `get Booking details for current user`            |

#### Request Body



#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 13>`                                                    |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|
| **404 Not Found**   | `{"detail": "No BookingFlight matches the given query."}`      |
|---------------------|----------------------------------------------------------------|



### 23. Edit Booking

| Property           | Value                                             |
|--------------------|---------------------------------------------------|
| **URL**            | `/api/service/booking/3/edit/`                    |
| **Method**         | `PUT`                                             |
| **Authentication** | Required                                          |
| **Content-Type**   | `application/json`                                |
| **Description**    | `get Booking details for current user`            |

#### Request Body

```json
{"flight_type":<"one_direction"|"two_direction">,"flight_go":<flight_id>,"flight_back":<flight_id>,"chears":<int>,"chear_type":<"Economy"|"Premium"|"Business"|"First">,"chears_checked_in_go":<int>,"chears_checked_in_back":<int>}
```

#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 14>`                                                    |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|
| **404 Not Found**   | `{"detail": "Booking not found."}`                             |
|---------------------|----------------------------------------------------------------|


### 24. Create Booking

| Property           | Value                                             |
|--------------------|---------------------------------------------------|
| **URL**            | `/api/service/booking/create/`                    |
| **Method**         | `POST`                                            |
| **Authentication** | Required                                          |
| **Content-Type**   | `application/json`                                |
| **Description**    | `Create Booking for current user`                 |

#### Request Body

```json
{"flight_type":<"one_direction"|"two_direction">,"flight_go":<flight_id>,"flight_back":<flight_id>,"chears":<int>,"chear_type":<"Economy"|"Premium"|"Business"|"First">,"chears_checked_in_go":<int>,"chears_checked_in_back":<int>}
```

#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 15>`                                                    |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|


### 25. Cancel Booking

| Property           | Value                                             |
|--------------------|---------------------------------------------------|
| **URL**            | `/api/service/booking/<int:id>/cancel/`           |
| **Method**         | `POST`                                            |
| **Authentication** | Required                                          |
| **Content-Type**   | None                                              |
| **Description**    | `Cancel Booking for current user`                 |

#### Request Body


#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `{"detail": "Booking cancelled and seats restored."}`          |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|
| **404 Not Found**   | `{"detail": "Booking not found."}`                             |
|---------------------|----------------------------------------------------------------|



### 26. Refund Booking

| Property           | Value                                             |
|--------------------|---------------------------------------------------|
| **URL**            | `/api/service/booking/<int:id>/refund/`           |
| **Method**         | `POST`                                            |
| **Authentication** | Required                                          |
| **Content-Type**   | None                                              |
| **Description**    | `Cancel Booking for current user`                 |

#### Request Body


#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `{"detail": "Refund issued successfully."}`                    |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|
| **404 Not Found**   | `{"detail": "Booking not found."}`                             |
|---------------------|----------------------------------------------------------------|



### 27. Special Assistance List 

| Property           | Value                                             |
|--------------------|---------------------------------------------------|
| **URL**            | `/api/service/assistance/`                        |
| **Method**         | `GET`                                             |
| **Authentication** | Not Required                                      |
| **Content-Type**   | None                                              |
| **Description**    | `get Special Assistance List`                     |

#### Request Body


#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 16>`                                                    |
|---------------------|----------------------------------------------------------------|



### 28. Special Assistance Details 

| Property           | Value                                             |
|--------------------|---------------------------------------------------|
| **URL**            | `/api/service/assistance/<int:id>/`               |
| **Method**         | `GET`                                             |
| **Authentication** | Not Required                                      |
| **Content-Type**   | None                                              |
| **Description**    | `get Special Assistance Details`                  |

#### Request Body


#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 17>`                                                    |
|---------------------|----------------------------------------------------------------|
| **404 Not Found**   | `{"detail": "No SpecialAssistance matches the given query."}`  |
|---------------------|----------------------------------------------------------------|




### 29. my Special Assistance List 

| Property           | Value                                                   |
|--------------------|---------------------------------------------------------|
| **URL**            | `/api/service/assistance/orders/`                       |
| **Method**         | `GET`                                                   |
| **Authentication** | Required                                                |
| **Content-Type**   | None                                                    |
| **Description**    | `get Special Assistance order history for current user` |

#### Request Body


#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 18>`                                                    |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|



### 30. my Special Assistance Details 

| Property           | Value                                                   |
|--------------------|---------------------------------------------------------|
| **URL**            | `/api/service/assistance/orders/<int:id>`               |
| **Method**         | `GET`                                                   |
| **Authentication** | Required                                                |
| **Content-Type**   | None                                                    |
| **Description**    | `get Special Assistance order details for current user` |

#### Request Body


#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `<file 19>`                                                    |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|



### 31. Order Special Assistance 

| Property           | Value                                                   |
|--------------------|---------------------------------------------------------|
| **URL**            | `/api/service/assistance/order/create/`                 |
| **Method**         | `POST`                                                  |
| **Authentication** | Required                                                |
| **Content-Type**   | `Application/Json`                                      |
| **Description**    | `Create Special Assistance order for current user`      |

#### Request Body
```json
{"flight":<int:id>,"special_assistance":<int:id>}
```

#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `{"detail": "Special assistance ordered successfully."}`       |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|
| **400 Bad Request** | `{"special_assistance": ["This field is required."]}`          |
|---------------------|----------------------------------------------------------------|


### 32. Cancel Ordering Special Assistance 

| Property           | Value                                                   |
|--------------------|---------------------------------------------------------|
| **URL**            | `/api/service/assistance/order/<int:id>/cancel/`        |
| **Method**         | `POST`                                                  |
| **Authentication** | Required                                                |
| **Content-Type**   | None                                                    |
| **Description**    | `Cancel Special Assistance order for current user`      |

#### Request Body


#### Responses

| HTTP Status         | Body                                                           |
|---------------------|----------------------------------------------------------------|
| **200 OK**          | `{"detail": "Special assistance order cancelled."}`            |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `{"detail": "Authentication credentials were not provided."}`  |
|---------------------|----------------------------------------------------------------|
| **401 Unauthorized**| `["Authentication failed. Please login again."]`               |
|---------------------|----------------------------------------------------------------|
| **400 Bad Request** | `{"special_assistance": ["This field is required."]}`          |
|---------------------|----------------------------------------------------------------|
| **404 Not Found**   | `{"detail": "Order not found."}`                               |
|---------------------|----------------------------------------------------------------|
