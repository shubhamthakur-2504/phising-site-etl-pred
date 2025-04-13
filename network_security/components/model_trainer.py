import os
import sys
from network_security.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.utils.utils import save_object, load_object , load_numpy_array_data
from network_security.utils.ml_utils.metric.classification_matric import get_classification_report, evaluate_model
from network_security.utils.ml_utils.model.estimator import NetworkSecurityModel
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
import mlflow
import dagshub
dagshub.init(repo_owner='shubhamthakur-2504', repo_name='phising-site-etl-pred', mlflow=True)

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            logging.error(f"Error occured in ModelTrainer class constructor {str(e)}")
            raise NetworkSecurityException(e, sys)
        
    def track_mlflow(self, model_name, classification_report,model):
        with mlflow.start_run(run_name=model_name):
            f1_score = classification_report.f1_score
            precision_score = classification_report.precision_score
            recall_score = classification_report.recall_score
            mlflow.set_tag("model_name", model_name)
            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.sklearn.log_model(model, "model")
        
    def train_model(self, x_train, y_train, x_test, y_test):
        models = {
            "Logistic Regression": LogisticRegression(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Random Forest": RandomForestClassifier(verbose=1),
            "KNN": KNeighborsClassifier(),
            "AdaBoost": AdaBoostClassifier()
        }
        params = {
            "Logistic Regression": {
                'penalty': ['l1', 'l2'],
                'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
                'solver': ['lbfgs', 'liblinear', 'saga'],
            },
            "Decision Tree": {
                'criterion': ['gini', 'entropy', 'log_loss'],
                'splitter': ['best', 'random'],
                'max_features': [None, 'sqrt', 'log2'],
            },
            "Gradient Boosting": {
                'learning_rate': [0.1, 0.01, 0.05],
                'subsample': [0.6, 0.7, 0.9],
                'loss': ['deviance', 'exponential'],
                'criterion': ['friedman_mse', 'mae'],
                'max_features': [None, 'sqrt', 'log2'],
                'n_estimators': [8, 16, 32, 64, 128, 256],
            },
            "Random Forest": {
                'criterion': ['gini', 'entropy', 'log_loss'],
                'max_features': [None, 'sqrt', 'log2'],
                'n_estimators': [8, 16, 32, 64, 128, 256],
                'n_jobs': [-1]
            },
            "KNN": {
                'n_neighbors': [3, 5, 7, 9, 11],
                'weights': ['uniform', 'distance'],
                'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                'n_jobs': [-1]
            },
            "AdaBoost": {
                'n_estimators': [8, 16, 32, 64, 128, 256],
                'learning_rate': [0.1, 0.01, 0.05]
            }
        }

        models_report = evaluate_model(x_train, y_train, x_test, y_test, models, params)

        best_model_score = max(report.f1_score for report in models_report.values())
        logging.info(f"Best Model Score: {best_model_score}")

        best_model_name = next(name for name, report in models_report.items() if report.f1_score == best_model_score)
        logging.info(f"Best Model Name: {best_model_name}")

        best_model = models[best_model_name]  # Selecting the best model

        y_train_pred = best_model.predict(x_train)
        train_metric = get_classification_report(y_true=y_train, y_pred=y_train_pred)
        # track the Mlflow
        self.track_mlflow(model_name=best_model_name,classification_report=train_metric,model=best_model)

        y_test_pred = best_model.predict(x_test)
        test_metric = get_classification_report(y_true=y_test, y_pred=y_test_pred)
        # track the Mlflow
        self.track_mlflow(model_name=best_model_name,classification_report=test_metric,model=best_model)

        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        Network_Security_Model = NetworkSecurityModel(model=best_model, preprocessor=preprocessor)
        save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=Network_Security_Model)
        save_object(file_path=r"final_model/model.pkl",obj=best_model)

        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact= train_metric,
            test_metric_artifact= test_metric
        )
        logging.info("Model trainer artifact created")
        return model_trainer_artifact


    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path =self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(file_path=train_file_path)
            test_arr = load_numpy_array_data(file_path=test_file_path)

            x_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            x_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            model_trainer_artifact =self.train_model(x_train, y_train, x_test, y_test)
            return model_trainer_artifact
            
        except Exception as e:
            logging.error(f"Error occured in initiate_model_trainer function {str(e)}")
            raise NetworkSecurityException(e, sys)