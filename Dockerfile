FROM python:3.8

WORKDIR /app
EXPOSE 8080

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Run the application on port 8080
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0", "--"]
