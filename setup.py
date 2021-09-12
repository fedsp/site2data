import sys,os
from pathlib import Path

working_directory = Path(os.getcwd())
sys.path.append(str(working_directory))
sys.path.append(str(working_directory.joinpath('./test')))
sys.path.append(str(working_directory.joinpath('./services')))
sys.path.append(str(working_directory.joinpath('./repositories')))
