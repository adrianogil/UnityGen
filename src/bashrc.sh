alias gen-unity-project=${UNITY_GEN_PATH}'/src/unity_project_gen.sh'
alias gen-android-unity-plugin=${UNITY_GEN_PATH}'/src/unity_android_plugin_gen.sh'

_gen-unity-project()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts=$(python2 ${UNITY_GEN_PATH}/src/get_all_unity_versions.py)
    _script_folders=$opts

    if [[ ${cur} == * ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}
complete -F _gen-unity-project gen-unity-project

_mydirs()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="--save -s --open -o --remove -r --list -l --path -p"
    _script_folders=$(~/workspace/python/mydirs/src/mydirs.py --auto-list)

    if [[ "${prev}" == "--open" || "${prev}" == "-o" || "${prev}" == "--remove" || "${prev}" == "-r" || "${prev}" == "--path" || "${prev}" == "-p"  ]] ; then
        COMPREPLY=( $(compgen -W "${_script_folders}" -- ${cur}) )
        return 0
    fi

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}
complete -F _mydirs mydirs