#!/usr/bin/env bash

action() {
    local base="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    local py_version="$( python -c "import sys; print('{}.{}'.format(*sys.version_info))" )"


    #
    # setup env
    #

    # Python >= 2.7 is required
    if [ "$py_version" = "2.6" ]; then
        2>&1 echo "Python >= 2.7 is required (try a lxplus7 machine)"
        return "1"
    fi

    export WLCG_EXAMPLE_BASE="$base"
    export WLCG_EXAMPLE_STORE="$WLCG_EXAMPLE_BASE/tmp/data"
    export WLCG_EXAMPLE_SOFTWARE="$WLCG_EXAMPLE_BASE/tmp/software"
    export LAW_HOME="$WLCG_EXAMPLE_BASE/.law"
    export LAW_CONFIG_FILE="$WLCG_EXAMPLE_BASE/law.cfg"
    export LAW_JOB_FILE_DIR="$WLCG_EXAMPLE_BASE/tmp/jobs"

    # check if we're on lxplus
    [[ "$( hostname )" = lxplus*.cern.ch ]] && WLCG_EXAMPLE_ON_LXPLUS="1" || WLCG_EXAMPLE_ON_LXPLUS="0"
    export WLCG_EXAMPLE_ON_LXPLUS

    # infer the grid user name from the local lxplus user if not already set
    # complain in case we're not on lxplus
    if [ -z "$WLCG_EXAMPLE_GRID_USER" ]; then
        if [ "$WLCG_EXAMPLE_ON_LXPLUS" = "1" ]; then
            export WLCG_EXAMPLE_GRID_USER="$( whoami )"
            echo "using lxplus user name '$WLCG_EXAMPLE_GRID_USER' as grid user name"
        else
            2>&1 echo "WARNING: this example is designed to run on lxplus, please export the WLCG_EXAMPLE_GRID_USER variable manually and source this file again"
            return "1"
        fi
    fi


    #
    # minimal software stack
    #

    _pip_install() {
        pip install --ignore-installed --no-cache-dir --prefix "$WLCG_EXAMPLE_SOFTWARE" "$@"
    }

    _addpy() {
        [ ! -z "$1" ] && export PYTHONPATH="$1:$PYTHONPATH"
    }

    _addbin() {
        [ ! -z "$1" ] && export PATH="$1:$PATH"
    }

    # update paths
    _addbin "$WLCG_EXAMPLE_SOFTWARE/bin"
    _addpy "$WLCG_EXAMPLE_SOFTWARE/lib/python$py_version/site-packages"
    _addpy "$WLCG_EXAMPLE_BASE"

    # setup external software once
    if [ ! -d "$WLCG_EXAMPLE_SOFTWARE" ]; then
        echo "installing software stack at $WLCG_EXAMPLE_SOFTWARE"
        mkdir -p "$WLCG_EXAMPLE_SOFTWARE"
        echo ""

        _pip_install six
        _pip_install git+https://github.com/spotify/luigi.git
        LAW_INSTALL_CUSTOM_SCRIPT="1" _pip_install --no-dependencies git+https://github.com/riga/law.git
    fi

    # initially source the law bash completion
    source "$( law completion )"
}
action
