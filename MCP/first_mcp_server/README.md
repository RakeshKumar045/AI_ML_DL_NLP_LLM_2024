##uv : framework & 1) downlad MCP related software then 2) install uv : pip install uv

##Step 1: create default MCP code setup
uv init first_project_demo

##step 2: create ENV using uv and activate uv venv same as conda env
uv venv
.venv\Scripts\activate

##step3: add all required python library in requiremnets.txt file
uv add -r requirements.txt

##step 4 create api key: groq api key : https://console.groq.com/home

##step 5:  server must be running and server should be up
### run  python server : python weather_server.py


##step6: for testing : run the weather_server.py by python, but we need to run weather_server by client python file only or use 3rd party server or DB or else
python weather_server.py


##step 7: run the local or run our application or script : means run the MCP client
## run MCP client
python client.py

