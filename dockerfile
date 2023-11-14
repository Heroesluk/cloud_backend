FROM python:3.9-slim

# Copy local code to the container image.
ENV APP_HOME=/app
ENV FLASK_APP=main.py

WORKDIR $APP_HOME
COPY README.md requirements.txt main.py upload.html ./
COPY tests ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
# Run the web service on container startup.
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]