import sys,os
from pathlib import Path
import json

working_directory = Path(os.getcwd())
sys.path.append(str(working_directory))
sys.path.append(str(working_directory.joinpath('./test')))
sys.path.append(str(working_directory.joinpath('./services')))
sys.path.append(str(working_directory.joinpath('./repositories')))

with open('./settings.json') as settings_file:
    settings = json.load(settings_file)
 