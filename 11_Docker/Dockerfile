# base image
FROM python:3.12

# working directory
WORKDIR /app

# copy command
COPY . /app

# run command
RUN pip install -r requirements.txt

# port expose
# generally flask run at port 5000
EXPOSE 5000 

# command to run on container start
CMD ["python", "./app.py"]



# docker build -t username/image_name .