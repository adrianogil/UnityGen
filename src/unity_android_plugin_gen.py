import subprocess, sys, os

if len(sys.argv) < 2:
    exit()

current_unity_directory = sys.argv[1]

def get_project_settings(setting, label_size):
    get_settings_cmd = 'cat ' + current_unity_directory + '/ProjectSettings/ProjectSettings.asset | grep ' + setting
    settings_string = subprocess.check_output(get_settings_cmd, shell=True)
    settings_string = settings_string[label_size:-1]

    return settings_string

def get_android_targets():
    get_android_targets_cmd = 'android list targets | grep android-'
    android_targets = subprocess.check_output(get_android_targets_cmd, shell=True)
    android_targets = android_targets.split('\n')

    targets = {}

    for i in range(0, len(android_targets)-1):
        target = android_targets[i]
        for j in range(0, len(target)):
            if target[j:j+8] == 'android-':
                for d in range(4, len(target)):
                    if target[d] == ' ':
                        target_id = target[4:d]
                        print('Found android target ' + target[j+8:-1] + ' with id ' + target_id)
                        targets[target_id] = target[j+8:-1]
                        break
                break

    return targets

android_package = get_project_settings('bundleIdentifier', 20)
android_min_sdk = get_project_settings('AndroidMinSdkVersion:', 24)

print(android_package)
print(android_min_sdk)

path, filename = os.path.split(current_unity_directory)
unity_project_name = filename
android_project_name = unity_project_name + 'AndroidPlugin'

unity_project_path = current_unity_directory
android_project_path = unity_project_path + 'AndroidPlugin'

targets = get_android_targets()

if len(targets) <= 0:
    print('Error: no android target was found!')
    exit()

for android_id in targets:
    if targets[android_id] >= android_min_sdk:
        android_target_id = android_id

android_project_creation_cmd = 'android create project'+ \
                               ' --target ' + android_target_id + \
                               ' --name ' + android_project_name + \
                               ' --path ' + android_project_path + \
                               ' --activity MainActivity ' + \
                               ' --package ' + android_package + \
                               '-v'


android_project_creation_output = subprocess.check_output(android_project_creation_cmd, shell=True)
print(android_project_creation_output)
# --path <path-to-workspace>/CommandLineProject \
# --activity MainActivity \
# --package com.reversiblean.clproject \
# --gradle --gradle-version <android-gradle-plugin-version-no>