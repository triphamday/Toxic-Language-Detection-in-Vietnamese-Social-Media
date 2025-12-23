from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)


def error(labels, predictions, num_labels=2):
    acc = accuracy_score(labels, predictions)
    if num_labels == 2:
        f1 = f1_score(labels, predictions)
        precision = precision_score(labels, predictions, zero_division=0)
        recall = recall_score(labels, predictions, zero_division=0)
    else:
        f1 = f1_score(labels, predictions, average="macro")
        precision = precision_score(labels, predictions, average="macro", zero_division=0)
        recall = recall_score(labels, predictions, average="macro", zero_division=0)
    
    return acc, f1, precision, recall
