# Simple ML Deployment Framework

## Purpose and Philosophy

The purpose of this project is to create a simple reusable and customizable framework to easily deploy machine learning models in production on Google Cloud.

In order to call the different models more easily, we use one single entry for every request: it is the Google Cloud Function called interface.

Depending on the model you call, that function will do one of the following:
directly respond with the prediction of your model 
call another Google Cloud Function containing custom code (for example for preprocessing and postprocessing purposes). The final response will be sent to a chosen webhook url.

## First Case: Simple Pipeline

Let’s look at the first case. It’s the easiest one: all you have to do is hosting a model on Google Cloud AI. The name of that model is then a parameter of the request you make to the interface function, and the interface function takes care of the rest: calling the model on Google Cloud AI and answering your requests with the results. This is a synchronous process, and you will receive the answer immediately.

NB: If you’re familiar with scikit-learn, it’s doing the equivalent of a model.predict().
See Google documentation: https://cloud.google.com/ai-platform/prediction/docs/deploying-models

The example given in this repository is a DummyClassifier (https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html).

## Second Case: Complex Pipeline

The second case allows for more complex pipelines. The example given in this repository allows for the extraction of email addresses from a list of documents (including images), represented by their urls. 
An email address for the purpose of this demonstration will be defined as “having an @ and a . placed as follow: test@test.test”. No further verification about whether or not the email actually exists has been implemented. If that’s something you need, you could easily add such a verification to the postprocessing function.

The pipeline we chose to set up here consists in three separate Google Cloud Functions after the interface one:
document_preprocessing: it stores each document in the list on Google Cloud Storage. It is required to use Google Vision, which serves as an Optical Character Recognition (OCR) tool and will extract plain text from the documents.
google_ocr: for each document in the list, it will extract the plain text. It uses Google Vision.
document_postprocessing: extracts email addresses from the plain texts and sends the answer to a webhook url.

These three functions are triggered with Google Pub Sub. Once you’ve sent your request, everything happens within the Google Cloud Project you’ve set up, and you don’t need further authentication to use Google Cloud components.

This example is meant to show you how to use Google Cloud Functions for more complex machine learning pipelines. There are as many other possibilities as there are user cases.

## Quick Start

### Deploy the interface

* Step 1: Fork the github repository on your account
* Step 2: Create a google cloud account
* Step 3: Connect github to your google cloud account and activate cloudbuild
Go on this page and follow the steps on the screencast.
https://console.cloud.google.com/cloud-build/triggers

![connect-github](https://user-images.githubusercontent.com/58165523/114436916-3336ee80-9bc6-11eb-83dc-3c4a0c5b4396.gif)

* Step 4: Click on run and wait for the deploy ! 🎉

You’re all set. The public interface is deployed. You should be able to see the Google Cloud Functions on the following page: https://console.cloud.google.com/functions/list.

If you want to have different environments, you can copy the cloudbuild file and create a new pipeline

### Deploy your first model

dummy_classifier

### Set the environment variables

You’ll need to set up the following environment variables.
Go on this page: https://console.cloud.google.com/functions/list.
Click on the interface function, click on modify and enter environment variable below in the runtime section.
Then, you need to deploy again your function.

`AUTH_TOKEN: aaaa0000`
 
## Usage

Custom Model

```bash
curl 'https://your-url.cloudfunctions.net/interface_opensource?model=dummy_classifier' \
  -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer aaaa0000' \
  --data '{"instances": [1,1,1,1]}'
```
 
Email Detection with use of an OCR
We use the asynchronous model document_preprocessing_opensource.

```bash
curl 'https://your-url.cloudfunctions.net/interface_opensource?model=document_preprocessing_opensource&url=my_webhook_url' \
  -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer aaaa0000' \
  --data '{"instances": [{"urls": ["https://my_image.jpg"], "doc_id": 123}]}' 
```

Response example:

```bash
{
  "predictions": [
    {
      "has_first_name": 0,
      "doc_id": 123
    }
  ]
}
```


## How It Works

This project uses several elements of Google Cloud:
* Simple models such as pickle exports of scikit-learn models can be deployed on Google AI Platform (https://cloud.google.com/ai-platform/prediction/docs/deploying-models)
* More complex models needing preprocessing or post processing can also be deploy on Google AI platform using the “custom prediction routines” feature (https://cloud.google.com/ai-platform/prediction/docs/custom-prediction-routines)
* Even more complex models can be deployed in Google Cloud Functions (https://cloud.google.com/functions/docs/quickstarts)
* The public interface for accessing the different models is based on a Google Cloud Function named interface in the /interface/main.py file
* Asynchronous models can use Google Cloud Pub/Sub to send information to other Google Cloud Functions (https://cloud.google.com/pubsub/docs/overview). An example is available on the repository.
* If your model uses files you can also use Google Cloud Storage (https://cloud.google.com/storage/docs/introduction). An example is available on the repository.
* Finally, we use Google Cloud Build to automate the deployment of the models and associated Google Cloud Functions (https://cloud.google.com/build/docs/quickstart-build)

## License

Copyright (c) 2021 Flatlooker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
