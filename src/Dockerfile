FROM mcr.microsoft.com/azure-functions/python:4.13.0-python3.9

ENV AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY src/requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

ENV AzureWebJobsSecretStorageType=Files

COPY  src/ /home/site/wwwroot 