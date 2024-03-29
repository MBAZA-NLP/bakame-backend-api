FROM python:3.10.9

#Create and make the API folder the working directory
WORKDIR /usr/src/app

#Create tts cache
RUN mkdir cache
RUN mkdir cache/tts 

#copy the requirments
COPY requirements.txt .

#upgrade pip
RUN pip install --no-cache-dir --upgrade pip

#Install all the dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy all the files
COPY . . 

#Expose the port
EXPOSE 8000

#Run the app
CMD ["uvicorn", "main:api", "--host=0.0.0.0", "--port=8000"]

