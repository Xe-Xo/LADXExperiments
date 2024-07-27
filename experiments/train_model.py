from model.models import train_model, train_from_existing_model, train_jax_model

# Overide the default training hyper params here with a dictionary
# You can also update the reward scalling and other env params
# Base tuning hyper params are in model/models.py
# Base reward and env params are in gym_env/link_awake_env.py

import torch
# get warnings on my system without this
# feel free to remove on your machine
torch.backends.cudnn.benchmark = True


# Example of training a model from scratch
train_model()

# Example of training a model from an existing model
#train_from_existing_model("ba221132//2")

# Example of using jax instead
##TODO: This doesnt work yet
#train_jax_model()
