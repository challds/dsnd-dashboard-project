import pickle
from pathlib import Path

# create a project root path
project_root = Path(__file__).parents[1]
# create a path for the model
model_path = project_root / 'assets' / 'model.pkl'

def load_model():

    with model_path.open('rb') as file:
        model = pickle.load(file)

    return model