# create-hubspot-notes-from-transcriptions

A simple project that consists in get transcriptions and create hubspot notes from that

## Purpose

The purpose of this API is to take a raw text and transform it into a clearer text, 
using an AI text modifiyng tool, and then with this clearer text, create the hubspot notes.

## Usage

## Run locally:
To run locally follow this steps:

If it's the first execution:

* Create venv using this command: python -m venv .venv
* Active venv: source .venv/bin/active
* Install project libraries: pip install -r requirements.txt

If you already installed the libraries (from the second execution onwards):

* Active venv: source .venv/bin/active
* Run the API locally: uvicorn main:app --reload
