from typing import Dict, List, Optional

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline


class SentimentClassifier:
    def __init__(
            self,
            classifier_model: Optional[str] = None,
            multi_class: Optional[bool] = True,
    ):
        # Model names: joeddav/xlm-roberta-large-xnli, facebook/bart-large-mnli

        self.analyzer = SentimentIntensityAnalyzer()
        self.multi_class = multi_class
        if classifier_model is not None:
            self.classifier = pipeline("zero-shot-classification", model=classifier_model)

    def init_classifier_model(self, classifier_model: str):
        if self.classifier is not None:
            raise AttributeError("Classifier already initialized")

        self.classifier = pipeline("zero-shot-classification", model=classifier_model)

    def get_sentiment_score(self, text: str) -> float:
        scores = self.analyzer.polarity_scores(text)
        return scores["compound"]

    def classify_text(self, text: str, labels: List[str]) -> Dict[str, float]:
        if self.classifier is None:
            raise AttributeError("Classifier not initialized")

        scores_data = self.classifier(text, labels, multi_class=self.multi_class)

        score_dict = {label: score for label, score in zip(scores_data["labels"], scores_data["scores"])}
        return dict(sorted(score_dict.items(), key=lambda x: x[1], reverse=True))
