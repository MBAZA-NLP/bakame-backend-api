FROM python:3.10.9

#create UI folder and set it as working folder
WORKDIR /UI

#Copy all files to the workdir
COPY . .

#install streamlit and dependencies
RUN pip install --no-cache-dir -r requirements.txt

#run the streamlit app
CMD [ "streamlit", "run", "main.py", "--server.port", "8501"]