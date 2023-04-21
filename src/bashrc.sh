alias gen-android-unity-plugin=${UNITY_GEN_PATH}'/unity_android_plugin_gen.sh'

function gen-unity-project()
{
    # Create a unity project from a project name
    # Usage:
    # ./unity_project_gen.sh PROJECT_NAME
    # ./unity_project_gen.sh UNITY_VERSION PROJECT_NAME

    if [ -z "$2" ]
    then
        project_name=$1
        unity_version=$(ls ${UNITY_HUB_APPS_DIR} | default-fuzzy-finder)
    else
        unity_version=$1
        project_name=$2
    fi

    if [ -z "$UNITY_APPS_FOLDER" ]
    then
        unity_main_path=/Applications/
    else
        unity_main_path=${UNITY_APPS_FOLDER}
    fi

    unity_exe="${UNITY_HUB_APPS_DIR}/"${unity_version}"/Unity.app/Contents/MacOS/Unity"
    ${unity_exe} -createProject ${project_name} -batchmode -nographics -quit

    assets_folder=${project_name}/Assets

    # Create default folders
    echo "Generating default folder structure at Assets folder"
    mkdir -p ${assets_folder}/Editor
    mkdir -p ${assets_folder}/Materials
    mkdir -p ${assets_folder}/Prefabs
    mkdir -p ${assets_folder}/Resources
    mkdir -p ${assets_folder}/Scenes
    mkdir -p ${assets_folder}/Scripts
    mkdir -p ${assets_folder}/Shaders
    mkdir -p ${assets_folder}/Textures
}

_gen-unity-project()
{
    local cmd="${1##*/}"
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts=$(python2 ${UNITY_GEN_PATH}/get_all_unity_versions.py)
    _script_folders=$opts

    if [[ ${cur} == * ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}
complete -F _gen-unity-project gen-unity-project
