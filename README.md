# LAST MILE DELIVERY 🚚
---

## Pre-requistes
<br>

1. Python **3.7** >
2. Pip3 
3. Google Maps API Key

---

## Setup

<br>

Cloning the repositry
<br>

```
git clone https://github.com/kshitijdhara/last-mile-delivery.git
```
<br>

Adding the **Config** Files
> 1. Create a Firebase project and add the app to your project 
> 2. Copy the config json and paste it in a file named config.py in directory /app/config.py
> 3. Create a JSON key for the firebase admin serice account from the GCP Console of your Firebase project
> 4. Download the JSON key
> 5. Rename the JSON Key File as firestore_config.json
> 6. Move firestore_config.json in the directory /app/firestore_config.json 

<br>

Installing the dependencies

```
pip install -r requirements.txt
```
<br>

Running the **Server**

```
python application.py
```
<br>

To check if application is running open http://localhost:8080
> response should be
> "Last Mile delivery server is running" 
