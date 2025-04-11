from network_security.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score, precision_score, recall_score
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import sys

def get_classification_report(y_true, y_pred):
    try:
        f1_score_value = f1_score(y_true, y_pred)
        precision_score_value = precision_score(y_true, y_pred)
        recall_score_value = recall_score(y_true, y_pred)

        Classification_Metric = ClassificationMetricArtifact(
            f1_score = f1_score_value,
            precision_score = precision_score_value,
            recall_score = recall_score_value
        )

        return Classification_Metric
    except Exception as e:
        logging.error(f"Error occured in get_classification_report function {str(e)}")
        raise NetworkSecurityException(e, sys)