"""
Divergence domain adaptation methods.
==========================================

This example illustrates the DeepCoral method from [1]
on a simple image classification task.

.. [1]  Baochen Sun and Kate Saenko. Deep coral:
        Correlation alignment for deep domain
        adaptation. In ECCV Workshops, 2016.

"""
# Author: Théo Gnassounou
#
# License: BSD 3-Clause
# sphinx_gallery_thumbnail_number = 4

# %%
from skorch import NeuralNetClassifier
from torch import nn

from skada.datasets import load_mnist_usps
from skada.deep import DeepCoral
from skada.deep.modules import MNISTtoUSPSNet

# %%
# Load the image datasets
# ----------------------------------------------------------------------------

dataset = load_mnist_usps(n_classes=2, n_samples=0.5, return_dataset=True)
X, y, sample_domain = dataset.pack(
    as_sources=["mnist"], as_targets=["usps"], mask_target_labels=True
)
X_test, y_test, sample_domain_test = dataset.pack(
    as_sources=[], as_targets=["usps"], mask_target_labels=False
)

# %%
# Train a classic model
# ----------------------------------------------------------------------------
model = NeuralNetClassifier(
    MNISTtoUSPSNet(),
    criterion=nn.CrossEntropyLoss(),
    batch_size=128,
    max_epochs=5,
    train_split=False,
    lr=1e-2,
)
model.fit(X[sample_domain > 0], y[sample_domain > 0])
model.score(X_test, y=y_test)

# %%
# Train a DeepCoral model
# ----------------------------------------------------------------------------
model = DeepCoral(
    MNISTtoUSPSNet(),
    layer_name="fc1",
    batch_size=128,
    max_epochs=5,
    train_split=False,
    reg=1,
    lr=1e-2,
)
model.fit(X, y, sample_domain=sample_domain)
model.score(X_test, y_test, sample_domain=sample_domain_test)
