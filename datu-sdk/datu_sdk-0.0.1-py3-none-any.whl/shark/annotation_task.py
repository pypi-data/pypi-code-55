"""API for the AnnotationTask
"""

class AnnotationTask():
    """Scalabel Annotation Task.
    """

    def __init__(self, annotation_name: str):
        """Instantiate new annotation tasks.
        """
        self.annotation_name = annotation_name

    def summarize(self) -> str:
        """Summarizing the object.
        """
        return self.annotation_name
