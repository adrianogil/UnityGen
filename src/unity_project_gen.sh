# Create a unity project from a project name
# Usage:
# ./unity_project_gen.sh PROJECT_NAME
# ./unity_project_gen.sh UNITY_VERSION PROJECT_NAME

if [ -z "$2" ]
then
    project_name=$1
    unity_version='5.6.0.11b'
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

unity="${unity_main_path}/Unity"${unity_version}"/Unity"${unity_version}".app/Contents/MacOS/Unity"

$unity -createProject ${project_name} -batchmode -nographics -quit

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

