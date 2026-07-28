# Container image for the Azure Functions variant.
# Build from the repo root so the shared `app` package is in context:
#   docker build -f functionapp/Dockerfile -t embr-easyauth-func .

FROM mcr.microsoft.com/azure-functions/python:4-python3.12

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY functionapp/requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY functionapp/ /home/site/wwwroot/
# Shared code: the same FastAPI app the embr deployment runs.
COPY app/ /home/site/wwwroot/app/
