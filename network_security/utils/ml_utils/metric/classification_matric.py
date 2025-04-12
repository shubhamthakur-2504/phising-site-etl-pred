from network_security.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV
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
    
def evaluate_model(x_train, y_train, x_test, y_test, models, prams):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = prams[list(models.keys())[i]]

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(x_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            y_train_pred = model.predict(x_train)

            y_test_pred = model.predict(x_test)

            train_model_metric = get_classification_report(y_true=y_train, y_pred=y_train_pred)

            test_model_metric = get_classification_report(y_true=y_test, y_pred=y_test_pred)

            report[list(models.keys())[i]] = test_model_metric

        return report

    except Exception as e:
        logging.error(f"Error occured in evaluate_model function {str(e)}")
        raise NetworkSecurityException(e, sys)