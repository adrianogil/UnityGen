# Create a unity project from a project name

unity_5_5=/Applications/Unity5.5/Unity5.5.app/Contents/MacOS/Unity
unity_5_3_6=/Applications/Unity5.3.6/Unity5.3.6.app/Contents/MacOS/Unity
unity_5_3_5=/Applications/Unity5.3.5/Unity5.3.5.app/Contents/MacOS/Unity
unity=$unity_5_5

if [ -z "$1" ]
then
    repo='local'
else
    unity_version=$1
    unity='/Applications/Unity'$unity_version'/Unity'$unity_version'.app/Contents/MacOS/Unity'
fi

project_name=$2

$unity -createProject ${project_name} -batchmode -nographics -quit

assets_folder=${project_name}/Assets

# Create default folders
mkdir -p ${assets_folder}/Editor
mkdir -p ${assets_folder}/Materials
mkdir -p ${assets_folder}/Prefabs
mkdir -p ${assets_folder}/Resources
mkdir -p ${assets_folder}/Scenes
mkdir -p ${assets_folder}/Scripts
mkdir -p ${assets_folder}/Shaders
mkdir -p ${assets_folder}/Textures
