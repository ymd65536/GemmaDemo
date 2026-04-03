## Overview

This repository contains a simple Python client for sending a prompt to the Ollama-compatible generate endpoint exposed through the Cloud Run service `gemmademo`.

## Setup

Install the Google Cloud CLI if `gcloud` is not available.

```bash
curl -sSL https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

Authenticate with Google Cloud.

```bash
gcloud auth login
gcloud auth application-default login
```

Set the active Google Cloud project.

```bash
gcloud config set project PROJECT_ID
```

You can confirm the current project with:

```bash
gcloud config list --format='value(core.project)'
```

## Set Region

```bash
gcloud config set run/region europe-west1
```

## Start the proxy

Expose the Cloud Run service locally on port 9090.

```bash
gcloud run services proxy gemmademo --port=9090
```

After this starts successfully, the local endpoint below becomes available.

```text
http://localhost:9090/api/generate
```

## Call the endpoint with curl

```bash
curl http://localhost:9090/api/generate -d '{
	"model": "gemma3:4b",
	"prompt": "Why is the sky blue?"
}'
```

The response is streamed line by line.

## Call the endpoint with Python

Run the included script.

```bash
python3 generate_stream.py
```

You can also pass a custom prompt, model, or endpoint URL.

```bash
python3 generate_stream.py "Why is the sky blue?" --model gemma3:4b --url http://localhost:9090/api/generate
```
