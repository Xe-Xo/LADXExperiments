import pygame
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.ppo import PPO

class PygameViewer(BaseCallback): 

    ''' Callback that opens a pygame window to display the images of the environment'''

    def __init__(self, width,height):
        super().__init__()

        # Size of the PyGame Window
        # and Initialize Pygame

        self.width = width * 144
        self.height = height * 160
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.width+4*144, self.height))
        self.font = pygame.font.SysFont('Arial', 16)
    
    def _draw_screen(self):

        # Draw the Screen with the Images from the Environment

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
        self.screen.fill((0,0,0))
        for i, v in enumerate(self.image_order):
            r = i % 4
            c = i // 4
            
            
            surf = pygame.surfarray.make_surface(self.last_image[v])
            surf = pygame.transform.flip(surf, False, True)
            surf = pygame.transform.rotate(surf, 270)


            self.screen.blit(surf, (r * 144,c * 160))

        rescaled = pygame.transform.scale(pygame.transform.rotate(pygame.transform.flip(pygame.surfarray.make_surface(self.other_image),False,True),270), (4*144,4*160))
        self.screen.blit(rescaled, (4*144,0))
        steps = self.font.render(f"Total Steps: {self.total_steps}", True, (255,255,255), (0,0,0))
        self.screen.blit(steps, (4*144,0))

        pygame.display.flip()

    def _on_step(self):

        # On Step, Get the Images from each of the Environments

        self.total_steps = self.model.num_timesteps

        if self.total_steps % 64 != 0:
            return True
        

        
        num_envs = min(self.training_env.num_envs,16)

        self.last_reward = self.training_env.unwrapped.env_method('last_step_reward', indices=list(range(num_envs)))

        self.last_image = self.training_env.unwrapped.env_method('get_image', **{
            'include_seen': True,
            'include_reward': True,
        }, indices=list(range(num_envs)))

        # reorder last_image according to the order of the max last reward

        self.image_order = sorted(range(len(self.last_reward)), key=lambda k: self.last_reward[k], reverse=True)
        #self.image_order = self.image_order[:16]

        self.other_image = self.training_env.unwrapped.env_method('get_image', **{
            'include_seen': True,
            'include_reward': True,
            'include_entities': True
        }, indices=[self.image_order[0]])[0]


        self._draw_screen()

        return True


        
