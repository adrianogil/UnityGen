# unity_android_plugin_gen
import subprocess, sys, os

if len(sys.argv) < 2:
    exit()

current_unity_directory = sys.argv[1]

def get_project_settings(setting, label_size):
    get_settings_cmd = 'cat ' + current_unity_directory + '/ProjectSettings/ProjectSettings.asset | grep ' + setting

    settings_string = ""

    try:
        settings_string = subprocess.check_output(get_settings_cmd, shell=True)
    except:
        if settings_string == "":
            return ""
    if settings_string == "":
        return ""
    settings_string = settings_string[label_size:-1]

    return settings_string

def get_android_targets():
    get_android_targets_cmd = 'android list target | grep android-'
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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

android_package = get_project_settings('bundleIdentifier', 20)
if android_package == "":
    android_package = get_project_settings('Android:', 12)
android_min_sdk = get_project_settings('AndroidMinSdkVersion:', 24)

android_min_sdk = int(android_min_sdk)

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
    if is_number(android_id):
        if int(targets[android_id]) >= android_min_sdk:
            android_target_id = android_id

android_project_creation_cmd = 'android create lib-project'+ \
                               ' --target ' + android_target_id + \
                               ' --name ' + android_project_name + \
                               ' --path ' + android_project_path + \
                               ' --package ' + android_package + \
                               ' --gradle --gradle-version 3.3'


android_project_creation_output = subprocess.check_output(android_project_creation_cmd, shell=True)
print(android_project_creation_output)

gradle_path = android_project_path + '/build.gradle'

with open(gradle_path, 'r') as f:
    gradle_lines = f.readlines()

new_gradle_lines = []

already_added_gradle_lines = False

for l in gradle_lines:
    if not already_added_gradle_lines and 'android {' in l:
        new_gradle_lines.append(l)
        new_gradle_lines.append("\n")
        new_gradle_lines.append("\tdef KEY_PATH = '';\n")
        new_gradle_lines.append("\tdef AAR_PATH = '';\n")
        new_gradle_lines.append("\n")
        new_gradle_lines.append("\tif (System.getProperty('os.name').contains('Windows')) {\n")
        new_gradle_lines.append("\t\tKEY_PATH = '' + rootDir + '\\\\key\\\\';\n")
        new_gradle_lines.append("\t\tAAR_PATH = '' + rootDir + '\\\\..\\\\" + unity_project_name + "\\\\Assets\\\\Plugins\\\\Android\\\\';\n")
        new_gradle_lines.append("\t} else {\n")
        new_gradle_lines.append("\t\tKEY_PATH = '' + rootDir + '/key/';\n")
        new_gradle_lines.append("\t\tAAR_PATH = '' + rootDir + '/../" + unity_project_name + "/Assets/Plugins/Android/';\n")
        new_gradle_lines.append("\t}\n");
        new_gradle_lines.append("\n")
        new_gradle_lines.append("\tlintOptions {\n");
        new_gradle_lines.append("\t\tabortOnError false\n");
        new_gradle_lines.append("\t}\n");
        new_gradle_lines.append("\n");
        new_gradle_lines.append("\tassembleRelease.doLast {\n");
        new_gradle_lines.append("\t\tcopy {\n");
        new_gradle_lines.append("\t\t\tfrom('build/outputs/aar') {\n");
        new_gradle_lines.append("\t\t\t\tinclude '*.jar'\n");
        new_gradle_lines.append("\t\t\t}\n");
        new_gradle_lines.append("\t\tinto AAR_PATH\n");
        new_gradle_lines.append("\t\t}\n");
        new_gradle_lines.append("\t}\n");
        new_gradle_lines.append("\n");

        already_added_gradle_lines = True
    elif 'runProguard' in l:
        new_gradle_lines.append(l.replace('runProguard', 'minifyEnabled'))
    else:
        new_gradle_lines.append(l)

with open(gradle_path, 'w') as f:
    for l in new_gradle_lines:
        f.write(l)

# try:
#     build_cmd = 'cd ' + android_project_path + ' && ./gradlew tasks'
#     build_output = subprocess.check_output(build_cmd, shell=True)
# except:
#     print('')

gradle_properties_path = android_project_path + '/gradle/wrapper/gradle-wrapper.properties'

with open(gradle_properties_path, 'r') as f:
    gradle_lines = f.readlines()

new_gradle_lines = []

for l in gradle_lines:
    if 'distributionUrl' in l:
        new_gradle_lines.append('distributionUrl=http\\://services.gradle.org/distributions/gradle-2.2-all.zip\n')
    else:
        new_gradle_lines.append(l)

with open(gradle_properties_path, 'w') as f:
    for l in new_gradle_lines:
        f.write(l)

build_cmd = 'cd ' + android_project_path + ' && gradle wrapper && ./gradlew build'

build_output = subprocess.check_output(build_cmd, shell=True)
print(build_output)



# def KEY_PATH = '';
# def AAR_PATH = '';

# if (System.getProperty('os.name').contains('Windows')) {
#     KEY_PATH = '' + rootDir + '\\key\\';
#     AAR_PATH = '' + rootDir + '\\..\\PROJECT\\Assets\\Plugins\\Android\\';
# } else {
#     KEY_PATH = '' + rootDir + '/key/';
#     AAR_PATH = '' + rootDir + '/../PROJECT/Assets/Plugins/Android/';
# }
# android {
#     lintOptions {
#         abortOnError false
#     }
# }

# assembleRelease.doLast {
#    copy {
#       from('build/outputs/aar') {
#         include '*-release.aar'
#       }
#       into AAR_PATH
#    }
# }

# --path <path-to-workspace>/CommandLineProject \
# --activity MainActivity \
# --package com.reversiblean.clproject \
# --gradle --gradle-version <android-gradle-plugin-version-no>