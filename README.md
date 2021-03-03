# Machine Learning in Production: a Single Entry Point for Every Model

This project uses Google Cloud Functions and Google Cloud AI to push models in production.

One entry for every request: **interface**.

2 possible pipelines:
- custom model hosted on Google Cloud AI, will do the equivalent of a model.predict() on scikit-learn
- more complex pipeline with preprocessing and postprocessing; the example given allows to detect a particular sequence in an image given with the use of Google Vision and use a succession of three Google Functions: document_preprocessing, google_ocr and document_postprocessing.

Responses are sent to a chosen webhook url.

## Installation


## Usage

### Custom Model

```bash
curl 
```

### OCR

```bash
curl -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer aaaa0000' --data '{"instances": [{"urls": ["https://my_image.jpg"], "doc_id": 123}]}' 'https://europe-west1-project-name.cloudfunctions.net/interface_opensource?model=document_preprocessing_opensource&url=my_url'
```

Response example:
```JSON
{
  "predictions": [
    {
      "has_first_name": 0,
      "doc_id": 123
    }
  ]
}
```

## License







