# create-hubspot-notes-from-transcriptions

A simple project that consists in get transcriptions and create hubspot notes from that

## Purpose

The purpose of this API is to take a raw text and transform it into a clearer text, 
using an AI text modifiyng tool, and then with this clearer text, create the hubspot notes.

## Important notices:

* AI Commit Review (Study Mode): The OPENAI API is not free, you have to buy credits in the OPENAI platform to use this githubaction. See: https://github.com/gabriel-valenga/ai-commit-revisor-for-study for more.

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


## Using AI Commit Review (Study Mode): 
Add [ai-commit-review-study] to commit messages in commit that you want to be reviewed.
For more details see: https://github.com/gabriel-valenga/ai-commit-revisor-for-study#how-it-works

