# Auto labeling pipeline

Auto labeling pipeline helps doccano to annotate a document automatically. This package is intended to be used from the inside of doccano. You shouldn't use this package directly.

## Installation

To install auto-labeling-pipeline, simply run:

```bash
pip install auto-labeling-pipeline
```

## How to contribute

You can contribute this project by adding new templates as follows:

1. Add a new request model class to [models.py](https://github.com/doccano/auto-labeling-pipeline/blob/master/auto_labeling_pipeline/models.py).
2. Add a new template(Jinja2 format) to [templates/](https://github.com/doccano/auto-labeling-pipeline/tree/master/auto_labeling_pipeline/templates) directory.
3. Add a new template class to [mappings.py](https://github.com/doccano/auto-labeling-pipeline/blob/master/auto_labeling_pipeline/mappings.py).
4. Add a new option to [menu.py](https://github.com/doccano/auto-labeling-pipeline/blob/master/auto_labeling_pipeline/menu.py).
5. Testing.

## License

[MIT](https://github.com/doccano/auto-labeling-pipeline/blob/master/LICENSE)
