from auto_labeling_pipeline.labels import Labels
from auto_labeling_pipeline.mappings import MappingTemplate
from auto_labeling_pipeline.models import RequestModel
from auto_labeling_pipeline.postprocessing import BasePostProcessor


def pipeline(text: str,
             request_model: RequestModel,
             mapping_template: MappingTemplate,
             post_processing: BasePostProcessor) -> Labels:
    request = request_model.build()
    response = request.send(text)
    labels = mapping_template.render(response)
    labels = post_processing.transform(labels)
    return labels
