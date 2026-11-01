# Interview Preparation: Automated Casting Defect Detection

Realistic questions and concise answers, specific to this project.

---

**1. Why did you use a CNN for this problem?**
CNNs learn spatial visual patterns (edges, textures, shapes) directly
from raw pixels through convolutional filters, which is exactly what's
needed to detect visual defects like cracks or rough surfaces in
casting images, without hand-engineering features.

**2. Why is this framed as binary classification instead of multi-class?**
The business requirement was only to decide pass/fail -- whether a
defect is present -- not to identify the defect type or location, so a
single 0/1 output matches the actual decision the factory needs.

**3. Why sigmoid on the output layer?**
Sigmoid squashes the output to a single value between 0 and 1, which
can be directly interpreted as the probability that the image belongs
to the "defective" class -- the natural choice for binary
classification.

**4. Why binary cross-entropy as the loss function?**
Binary cross-entropy is the standard loss for two-class problems with
a sigmoid output; it directly penalizes the model based on how far its
predicted probability is from the true 0/1 label.

**5. Why Adam as the optimizer?**
Adam adapts the learning rate per parameter and combines momentum with
RMSProp-style scaling, which generally converges quickly and reliably
on image tasks without extensive manual learning-rate tuning.

**6. Why resize images to 224x224?**
Neural networks require a fixed input shape for every image in a
batch; 224x224 is a common, well-supported size that balances enough
visual detail against computation cost.

**7. Why use data augmentation?**
It exposes the model to realistic variations (slight rotation, zoom,
flip, lighting change) so it learns that a defect is still a defect
under minor viewpoint/lighting differences, improving generalization
to new camera captures.

**8. Why apply augmentation only to training data?**
Validation and test data must represent real, unseen conditions as
they would actually appear in production; augmenting them would give
an artificially easier or harder evaluation and distort the measured
performance.

**9. What is overfitting, and how would you recognize it here?**
Overfitting is when the model memorizes training data patterns
(including noise) rather than learning generalizable features. It
shows up as training accuracy continuing to rise while validation
accuracy stalls or falls, and validation loss starts increasing.

**10. Why did you use Dropout?**
Dropout randomly disables a fraction of neurons during training,
preventing the network from relying too heavily on specific neurons
and reducing overfitting.

**11. Why use early stopping?**
It halts training once validation loss stops improving for a set
number of epochs, preventing the model from continuing to overfit and
saving unnecessary compute time.

**12. Why report precision in addition to accuracy?**
Precision tells you, among items predicted defective, how many
actually were -- important because low precision means good products
get unnecessarily pulled for manual review.

**13. Why is recall especially important in this project?**
Recall measures how many actual defects the model catches. In quality
control, missing a real defect (a false negative) is usually far more
costly than a false alarm, since a defective product could reach the
customer.

**14. Why do false negatives matter more than false positives here?**
A false negative lets a defective product pass inspection undetected,
which can lead to returns, safety issues, or reputational damage. A
false positive only causes an unnecessary manual re-check.

**15. What is threshold tuning, and why did you implement it?**
The default 0.5 cutoff on the predicted probability isn't necessarily
optimal for every business context. Lowering the threshold generally
increases recall (catches more defects) at the cost of more false
positives. We evaluated multiple thresholds so the business can choose
based on the acceptable trade-off.

**16. Why not rely on accuracy alone to judge the model?**
Accuracy can be misleading, especially with any class imbalance --a
model that always predicts "non-defective" could still score high
accuracy while missing every real defect. Precision, recall, and the
confusion matrix give a fuller picture.

**17. Why keep the test set completely separate from training/validation?**
The test set estimates how the model will perform on genuinely unseen
data. If test images leak into training or validation, the reported
performance would be overly optimistic and unreliable in production.

**18. Why save only the "best" model instead of the final epoch's model?**
`ModelCheckpoint` with `save_best_only=True` keeps the version with the
lowest validation loss, which is often not the very last epoch,
especially since training may continue past the point of best
generalization before early stopping triggers.

**19. Why did you choose Gradio for the dashboard?**
Gradio provides a fast way to build an interactive web UI for image
upload and prediction with minimal code, and its Blocks API supports a
clean, structured layout suitable for a demo or portfolio project.

**20. How would you deploy this system in production?**
Package the trained model behind an inference service (e.g. a REST API
or embedded on-device with TensorFlow Lite), connect it to the factory
camera pipeline, log predictions and outcomes for monitoring, and route
flagged items to a human review queue.

**21. How would you improve this model further?**
Options include transfer learning with MobileNetV2/EfficientNet,
batch normalization, class weighting if the dataset is imbalanced,
Grad-CAM for explainability, and collecting more diverse production
images over time.

**22. What happens if factory lighting conditions change?**
Performance could degrade because the model has only seen the lighting
conditions present in the training images (domain shift). Mitigations
include augmenting for lighting variation, periodically retraining on
new production images, and monitoring live performance.

**23. What happens if a new, previously unseen defect type appears?**
The model may fail to detect it reliably, since it can only recognize
patterns present in its training data. This is a key limitation of any
supervised model and argues for ongoing monitoring and periodic
retraining as new defect examples are collected.

**24. How would you monitor this model after deployment?**
Track prediction distributions and confidence over time, sample and
manually review flagged and unflagged items periodically, watch for
drift in defect rates, and retrain when performance on newly labeled
production data degrades.

**25. How would you reduce false negatives specifically?**
Lower the decision threshold (accepting more false positives in
exchange), increase recall-focused regularization/training emphasis,
collect more defective-class training examples, and add human review
as a safety net for borderline-probability predictions.
