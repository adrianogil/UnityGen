alias gen-unity-project=${UNITY_GEN_PATH}'/unity_project_gen.sh'
alias gen-android-unity-plugin=${UNITY_GEN_PATH}'/unity_android_plugin_gen.sh'

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