##uv : framework & 1) downlad MCP related software then 2) install uv : pip install uv

##Step 1: create default MCP code setup
uv init first_project_demo

##step 2: create ENV using uv and activate uv venv same as conda env
uv venv
.venv\Scripts\activate

##step3: add all required python library in requiremnets.txt file
uv add -r requirments.txt

##step 4: groq api key : https://console.groq.com/home

##step5: for testing : run the weather server by python, but we need to run weather_server by client python file only or use 3rd party server or DB or else
python weather_server.py


## run MCP client
python client.py

