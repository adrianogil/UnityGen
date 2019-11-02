import os

unity_versions = ''

unity_main_path = '/Applications/'

if os.environ["UNITY_APPS_FOLDER"] is not None:
    unity_main_path = os.environ["UNITY_APPS_FOLDER"]

# Get all version of Unity already installed
files = [f for f in os.listdir(unity_main_path)]
for f in files:
    for i in xrange(0, len(f)-5):
        if f[i:i+5] == 'Unity':
            unity_versions = unity_versions + f[i+5:] + ' '
print(unity_versions)

