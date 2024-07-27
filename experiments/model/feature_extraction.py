# Feature Extractor for Observations


from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from gymnasium import spaces

import torch as th
from torch import nn


class MixtureOfExperts(nn.Module):

    ''' Mixture of Experts Layer for PyTorch '''
    ''' Uses Soft Attention to Weight the Output of Multiple Experts '''
    ''' Each Expert is a Neural Network Module '''

    def __init__(self, n_experts, expert_module, input_dim, output_dim, hidden_dim, dropout=0.0):

        self.n_experts = n_experts
        self.experts = nn.ModuleList([expert_module(input_dim, output_dim, hidden_dim, dropout) for _ in range(n_experts)])
        self.attention = nn.Linear(input_dim, n_experts)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        pass

class CustomFeatureExtractor(BaseFeaturesExtractor):

    """
    Combined features extractor for Dict observation spaces.
    Builds a features extractor for each key of the space. Input from each space is fed through
    a seperate submodule then the output features are concatenated.

    :param observation_space: (gym.Space)

    """

    def __init__(self, observation_space: spaces.Dict):

        super().__init__(observation_space, features_dim=1)

        # CNN for Image Observation from Emulator
        cnn_output_dim = 256
        n_input_channels = observation_space['screen'].shape[0]

        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 64, kernel_size=8, stride=4, padding=(2,0)),
            nn.ReLU(),
            nn.AdaptiveMaxPool2d(output_size=(9, 9)),
            nn.Conv2d(32*2, 64*2, kernel_size=4, stride=2, padding=2),
            nn.ReLU(),
            nn.Conv2d(64*2, 64*2, kernel_size=3, stride=1, padding=0),
            nn.ReLU(),
            nn.Flatten(),
        )

        # Compute the shape by doing one forward pass

        with th.no_grad():
            n_flatten = self.cnn(th.as_tensor(observation_space['screen'].sample()[None]).float()).shape[1]
        
        self.cnn_linear = nn.Sequential(
            nn.Linear(n_flatten, cnn_output_dim),
            nn.ReLU(),
        )

        # Embedding of minimap_object physics
        minimap_object_output_dim = 8 
        self.minimap_object_embedding = nn.Embedding(256, minimap_object_output_dim, padding_idx=0)
        n_input_channels = minimap_object_output_dim + observation_space['minimap_info'].shape[2]

        self.minimap_cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 32*2, kernel_size=4, stride=2, padding=0),
            nn.ReLU(),
            nn.AdaptiveMaxPool2d(output_size=(3, 3)),
            nn.Conv2d(32*2, 64*2, kernel_size=2, stride=2, padding=0),
            nn.ReLU(),
            nn.Conv2d(64*2, 128*2*2, kernel_size=1, stride=1, padding=0),
            nn.ReLU(),
            nn.Flatten(),
        )

        n_flatten = 128*2*2

        self.minimap_cnn_linear = nn.Sequential(nn.Linear(n_flatten, 256), nn.ReLU())

        entity_output_dim = 8
        self.entity_type_embedding = nn.Embedding(256, entity_output_dim, padding_idx=0) # 256 - > (16,8) entity types
        self.entity_relu = nn.Sequential(
            nn.Linear(12, 32),
            nn.ReLU(),
            nn.Linear(32,32),
            nn.ReLU(),
            nn.Flatten(),
        )

        self._features_dim = 256 + 256 + 512 + 89

    def forward(self, observations) -> th.Tensor:
        
        # Extract image features
        image_features = self.cnn(observations['screen'].float())
        image_features = self.cnn_linear(image_features)

        # Extract Object Minimap features - This is a matrix of object ints in the game
        minimap_physics = observations['minimap_object'].to(th.int) # 7,7
        embedded_minimap_physics = self.minimap_object_embedding(minimap_physics) # 7,7,8
        embedded_minimap_physics = embedded_minimap_physics.permute(0, 3, 1, 2) #8,7,7
        
        # This is Additional Minimap Information 
        minimap_info = observations['minimap_info']  # (10, 7, 7)
        minimap_info = minimap_info.permute(0, 3, 1, 2)       
        minimap = th.cat([minimap_info, embedded_minimap_physics], dim=1)

        # Put it through a CNN after combining
        minimap_features = self.minimap_cnn(minimap)
        minimap_features = self.minimap_cnn_linear(minimap_features)

        # Extract Entity Features 
        entity_type = observations["entity_type"].to(th.int) # (16,)
        embedded_entity_type = self.entity_type_embedding(entity_type) # (16, 8)

        entity_info = observations["entity_info"] # (16, 4)
        entity = th.cat([embedded_entity_type,entity_info], dim=-1) # (16, 12)
        entity_features = self.entity_relu(entity)
    
        vector = observations['vector'] # (89,)

        return th.cat((image_features,minimap_features, entity_features, vector), dim=-1) #