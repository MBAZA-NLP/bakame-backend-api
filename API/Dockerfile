FROM python:3.10.9

WORKDIR /API

#Copy all the files
COPY . . 

#Install all the dependencies
RUN pip install -r requirements.txt

#install the package using apt with packages.txt file
RUN apt-get update && cat packages.txt | xargs apt-get install -y

#Expose the port
EXPOSE 5000

#Run the app
CMD ["uvicorn", "app:app", "--port", "5000"]

