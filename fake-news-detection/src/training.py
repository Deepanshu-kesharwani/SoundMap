"""
Model Training Module for Fake News Detection
Implements multiple ML algorithms with hyperparameter tuning and evaluation
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import pickle
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class FakeNewsTrainer:
    """Class for training fake news detection models"""
    
    def __init__(self):
        """Initialize the trainer with default models"""
        self.models = {
            'logistic_regression': LogisticRegression(random_state=42),
            'svm': SVC(random_state=42, probability=True),
            'random_forest': RandomForestClassifier(random_state=42)
        }
        self.trained_models = {}
        self.best_params = {}
        self.evaluation_results = {}
    
    def train_model(self, 
                   model_name: str, 
                   X_train: np.ndarray, 
                   y_train: np.ndarray,
                   param_grid: Dict = None,
                   cv_folds: int = 5) -> None:
        """
        Train a specific model with optional hyperparameter tuning
        
        Args:
            model_name: Name of the model to train
            X_train: Training features
            y_train: Training labels
            param_grid: Parameters for grid search
            cv_folds: Number of cross-validation folds
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not available")
        
        model = self.models[model_name]
        
        if param_grid:
            print(f"Training {model_name} with hyperparameter tuning...")
            grid_search = GridSearchCV(
                model, 
                param_grid, 
                cv=cv_folds, 
                scoring='accuracy',
                n_jobs=-1,
                verbose=1
            )
            grid_search.fit(X_train, y_train)
            
            self.trained_models[model_name] = grid_search.best_estimator_
            self.best_params[model_name] = grid_search.best_params_
            
            print(f"Best parameters for {model_name}: {grid_search.best_params_}")
            print(f"Best cross-validation score: {grid_search.best_score_:.4f}")
        else:
            print(f"Training {model_name} with default parameters...")
            model.fit(X_train, y_train)
            self.trained_models[model_name] = model
    
    def train_all_models(self, 
                        X_train: np.ndarray, 
                        y_train: np.ndarray,
                        param_grids: Dict = None,
                        cv_folds: int = 5) -> None:
        """
        Train all available models
        
        Args:
            X_train: Training features
            y_train: Training labels
            param_grids: Dictionary of parameter grids for each model
            cv_folds: Number of cross-validation folds
        """
        for model_name in self.models.keys():
            param_grid = param_grids.get(model_name) if param_grids else None
            self.train_model(model_name, X_train, y_train, param_grid, cv_folds)
    
    def evaluate_model(self, 
                      model_name: str, 
                      X_test: np.ndarray, 
                      y_test: np.ndarray) -> Dict[str, float]:
        """
        Evaluate a trained model
        
        Args:
            model_name: Name of the model to evaluate
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary of evaluation metrics
        """
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} not trained")
        
        model = self.trained_models[model_name]
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred)
        }
        
        self.evaluation_results[model_name] = {
            'metrics': metrics,
            'predictions': y_pred,
            'probabilities': y_pred_proba,
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        return metrics
    
    def evaluate_all_models(self, 
                           X_test: np.ndarray, 
                           y_test: np.ndarray) -> pd.DataFrame:
        """
        Evaluate all trained models
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            DataFrame with evaluation results
        """
        results = []
        
        for model_name in self.trained_models.keys():
            metrics = self.evaluate_model(model_name, X_test, y_test)
            results.append({
                'Model': model_name,
                **metrics
            })
        
        return pd.DataFrame(results)
    
    def get_feature_importance(self, model_name: str, feature_names: list = None) -> pd.DataFrame:
        """
        Get feature importance for models that support it
        
        Args:
            model_name: Name of the model
            feature_names: List of feature names
            
        Returns:
            DataFrame with feature importance
        """
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} not trained")
        
        model = self.trained_models[model_name]
        
        if hasattr(model, 'feature_importances_'):
            # For tree-based models
            importance = model.feature_importances_
        elif hasattr(model, 'coef_'):
            # For linear models
            importance = np.abs(model.coef_[0])
        else:
            raise ValueError(f"Model {model_name} does not support feature importance")
        
        if feature_names is None:
            feature_names = [f'feature_{i}' for i in range(len(importance))]
        
        feature_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return feature_df
    
    def plot_feature_importance(self, model_name: str, feature_names: list = None, top_n: int = 20):
        """
        Plot feature importance
        
        Args:
            model_name: Name of the model
            feature_names: List of feature names
            top_n: Number of top features to display
        """
        try:
            feature_df = self.get_feature_importance(model_name, feature_names)
            
            plt.figure(figsize=(10, 8))
            top_features = feature_df.head(top_n)
            
            plt.barh(range(len(top_features)), top_features['importance'])
            plt.yticks(range(len(top_features)), top_features['feature'])
            plt.xlabel('Importance')
            plt.title(f'Top {top_n} Feature Importance - {model_name}')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            
            # Save plot
            os.makedirs('models/evaluation', exist_ok=True)
            plt.savefig(f'models/evaluation/{model_name}_feature_importance.png')
            plt.show()
            
        except ValueError as e:
            print(f"Cannot plot feature importance for {model_name}: {e}")
    
    def plot_confusion_matrix(self, model_name: str, y_test: np.ndarray):
        """
        Plot confusion matrix for a model
        
        Args:
            model_name: Name of the model
            y_test: Test labels
        """
        if model_name not in self.evaluation_results:
            raise ValueError(f"Model {model_name} not evaluated")
        
        cm = np.array(self.evaluation_results[model_name]['confusion_matrix'])
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Fake', 'Real'], 
                   yticklabels=['Fake', 'Real'])
        plt.title(f'Confusion Matrix - {model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        # Save plot
        os.makedirs('models/evaluation', exist_ok=True)
        plt.savefig(f'models/evaluation/{model_name}_confusion_matrix.png')
        plt.show()
    
    def cross_validate_model(self, 
                            model_name: str, 
                            X: np.ndarray, 
                            y: np.ndarray, 
                            cv_folds: int = 5) -> Dict[str, float]:
        """
        Perform cross-validation on a model
        
        Args:
            model_name: Name of the model
            X: Features
            y: Labels
            cv_folds: Number of cross-validation folds
            
        Returns:
            Dictionary with cross-validation results
        """
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} not trained")
        
        model = self.trained_models[model_name]
        
        cv_scores = cross_val_score(model, X, y, cv=cv_folds, scoring='accuracy')
        
        return {
            'mean_accuracy': cv_scores.mean(),
            'std_accuracy': cv_scores.std(),
            'scores': cv_scores.tolist()
        }
    
    def save_models(self, directory: str = 'models/trained_models') -> None:
        """
        Save all trained models to disk
        
        Args:
            directory: Directory to save models
        """
        os.makedirs(directory, exist_ok=True)
        
        for model_name, model in self.trained_models.items():
            filepath = os.path.join(directory, f'{model_name}.pkl')
            with open(filepath, 'wb') as f:
                pickle.dump(model, f)
            print(f"Saved {model_name} to {filepath}")
        
        # Save best parameters
        params_filepath = os.path.join(directory, 'best_parameters.json')
        with open(params_filepath, 'w') as f:
            json.dump(self.best_params, f, indent=2)
        
        # Save evaluation results
        eval_filepath = os.path.join(directory, 'evaluation_results.json')
        with open(eval_filepath, 'w') as f:
            # Convert numpy arrays to lists for JSON serialization
            json_results = {}
            for model_name, results in self.evaluation_results.items():
                json_results[model_name] = {
                    'metrics': results['metrics'],
                    'confusion_matrix': results['confusion_matrix'],
                    'classification_report': results['classification_report']
                }
            json.dump(json_results, f, indent=2)
    
    def load_models(self, directory: str = 'models/trained_models') -> None:
        """
        Load trained models from disk
        
        Args:
            directory: Directory containing saved models
        """
        for model_name in self.models.keys():
            filepath = os.path.join(directory, f'{model_name}.pkl')
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    self.trained_models[model_name] = pickle.load(f)
                print(f"Loaded {model_name} from {filepath}")
        
        # Load best parameters if available
        params_filepath = os.path.join(directory, 'best_parameters.json')
        if os.path.exists(params_filepath):
            with open(params_filepath, 'r') as f:
                self.best_params = json.load(f)

def get_default_param_grids() -> Dict[str, Dict]:
    """
    Get default parameter grids for hyperparameter tuning
    
    Returns:
        Dictionary of parameter grids
    """
    return {
        'logistic_regression': {
            'C': [0.1, 1, 10],
            'solver': ['liblinear', 'lbfgs'],
            'max_iter': [1000]
        },
        'svm': {
            'C': [0.1, 1, 10],
            'kernel': ['linear', 'rbf'],
            'gamma': ['scale', 'auto']
        },
        'random_forest': {
            'n_estimators': [100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5]
        }
    }

if __name__ == "__main__":
    # Demo training with sample data
    from preprocessing import prepare_sample_data, preprocess_dataset, split_data
    
    print("Preparing sample data...")
    df = prepare_sample_data()
    X, y = preprocess_dataset(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    print("Initializing trainer...")
    trainer = FakeNewsTrainer()
    
    print("Training models...")
    param_grids = get_default_param_grids()
    trainer.train_all_models(X_train, y_train, param_grids, cv_folds=3)
    
    print("Evaluating models...")
    results_df = trainer.evaluate_all_models(X_test, y_test)
    print("\nEvaluation Results:")
    print(results_df)
    
    print("Saving models...")
    trainer.save_models()
    
    print("Training completed successfully!")