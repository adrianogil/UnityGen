current_unity_directory=${PWD}

python ${UNITY_GEN_PATH}/src/unity_android_plugin_gen.py ${current_unity_directory}

# android_plugin_project=CommandLineProject

# android create project --target <target-id> --name ${android_plugin_project} \
# --path <path-to-workspace>/CommandLineProject \
# --activity MainActivity \
# --package com.reversiblean.clproject \
# --gradle --gradle-version <android-gradle-plugin-version-no>