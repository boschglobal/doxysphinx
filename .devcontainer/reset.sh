#! /usr/bin/env bash

# Script to remove the devcontainer and all caches to simulate clean checkout (or a fresh startover)
# Use it at your own risk!!

# some color definitions
C_GRAY="\e[90m"
C_LGRAY="\e[37m"
C_CYAN="\e[36m"
C_LGREEN="\e[92m"
C_RESET="\e[0m"

debug() {
 echo -e "$C_GRAY$1$C_RESET"
}

info() {
 echo -e "$C_LGREEN$1$C_RESET"
}

CWD=$(pwd)
WS_ROOT=$CWD
DIR_NAME=$(basename $CWD)
if [ "$DIR_NAME" = ".devcontainer" ]; then
    debug "script is called from .devcontainer directory... adjusting paths..."
    WS_ROOT=$(cd $CWD/..; pwd)
fi
IMAGE_NAME=$(basename $WS_ROOT)
debug "Current directory is $C_LGRAY$CWD"
debug "Workspace root directory is $C_LGRAY$WS_ROOT"
debug "Image name equals the workspace name: $C_LGRAY$IMAGE_NAME"

echo ""
info "getting containers of $C_CYAN$IMAGE_NAME$C_LGREEN and removing them.."
docker ps -a | grep "$IMAGE_NAME" | awk '{print $1}' | xargs -r docker rm -f
info "getting container images of $C_CYAN$IMAGE_NAME$C_LGREEN and removing them..."
docker images -a | grep "$IMAGE_NAME" | awk '{print $3}' | xargs -r docker rmi
info "cleaning all cached images, layers etc that aren't in use... (docker system prune)"
docker system prune -f

# remove cache and venv directories
info "clearing cache ($C_CYAN$WS_ROOT/.cache)$C_LGREEN directory..."
rm -rf $WS_ROOT/.cache
info "clearing local ($C_CYAN$WS_ROOT/.venv)$C_LGREEN directory..."
rm -rf $WS_ROOT/.venv
echo ""
info "Done everything cleaned up."
