# Create a unity project from a project name

unity_5_3_6=/Applications/Unity5.3.6/Unity5.3.6.app/Contents/MacOS/Unity
unity=$unity_5_3_6

$unity -createProject $1 -batchmode -nographics -quit