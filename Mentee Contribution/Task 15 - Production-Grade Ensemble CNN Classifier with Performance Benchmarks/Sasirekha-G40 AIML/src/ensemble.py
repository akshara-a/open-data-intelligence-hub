import numpy as np

def majority_vote(probabilities):
    predictions = np.stack([p.argmax(axis=1) for p in probabilities])
    return np.apply_along_axis(
        lambda votes: np.bincount(votes, minlength=probabilities[0].shape[1]).argmax(),
        axis=0,
        arr=predictions,
    )

def soft_vote(probabilities):
    averaged = np.mean(np.stack(probabilities, axis=0), axis=0)
    return averaged.argmax(axis=1), averaged

def weighted_soft_vote(probabilities, weights):
    weights = np.asarray(weights, dtype=np.float64)
    weights = weights / weights.sum()
    averaged = sum(w * p for w, p in zip(weights, probabilities))
    return averaged.argmax(axis=1), averaged

def disagreement_rate(probabilities):
    labels = np.stack([p.argmax(axis=1) for p in probabilities])
    all_agree = np.all(labels == labels[0], axis=0)
    return float(1.0 - np.mean(all_agree))
