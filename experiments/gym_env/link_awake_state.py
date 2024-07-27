
import pickle


class LinkAwakeningData():

    ''' Saves the data of the environment to be able to restore it later '''

    def __init__(self, env, name, type="found"):
        self.total_steps = env.total_steps # This is for tracking only. Not inputted into the environment so not to run into max steps
        self.seen_pos = env.seen_pos.copy()
        self.seen_map = env.seen_map.copy()
        self.seen_entities = env.seen_entities.copy()
        self.seen_objects = env.seen_objects.copy()
        self.saved_pos_count = env.saved_pos_count
        self.saved_map_count = env.saved_map_count
        self.saved_entities_count = env.saved_entities_count
        self.saved_objects_count = env.saved_objects_count
        self.object_info_history = env.object_info_history
        self.name = name
        self.type = type
        self.save(env,f'experiments//checkpoints//{self.type}//{self.name}')
        env.save_image(f"experiments//checkpoints//{self.type}//{self.name}", )

    def load_env(self, env):
        env.seen_pos = self.seen_pos.copy()
        env.seen_map = self.seen_map.copy()
        env.seen_entities = self.seen_entities.copy()
        env.seen_objects = self.seen_objects.copy()
        env.saved_entities_count = self.saved_entities_count
        env.saved_objects_count = self.saved_objects_count
        env.saved_pos_count = self.saved_pos_count
        env.saved_map_count = self.saved_map_count
        env.object_info_history = self.object_info_history
        env.checkpoint_loaded = True
        env.checkpoint = (self.type, self.name)

    def __repr__(self):
        return f"{self.name} - {self.total_steps} steps"
    
    def save(self, env, path):
        self.save_state(env,path)
        self.save_data(path)

    def save_state(self,env, path):
        with open(path + '.state', "wb") as f:
            env.pyboy.save_state(f)
    
    def save_data(self, path):
        with open(path + '.lad', "wb") as f:
            pickle.dump(self, f)

    def load(env, name, type="found"):
        path = f'experiments//checkpoints//{type}//{name}'
        try:
            with open(path + '.state', "rb") as f:
                env.pyboy.load_state(f)
            with open(path + '.lad', "rb") as f:
                data = pickle.load(f)
                data.load_env(env)

            #cx, cy, cz, _ = tuple(name.split("_"))
            #assert env.get_map_pos() == (int(cx),int(cy),int(cz))
        except FileNotFoundError as e:
            raise e
        

            
  
