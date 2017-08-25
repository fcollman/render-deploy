import os

for dirpath, dirnames, filenames in os.walk('.'):
    requirement_files = [f for f in filenames if f.endswith('requirements.txt')]
    for filename in requirement_files:
        fullfile = os.path.join(dirpath,filename)
        os.system('pip install -r %s'%fullfile)
