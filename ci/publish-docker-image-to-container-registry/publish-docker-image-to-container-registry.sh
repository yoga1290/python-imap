# Required env var:
##########################
# GIT_REPOSITORY_NAME
# DOCKER_FILE
# GITHUB_REPOSITORY_OWNER
# ACCESS_TOKEN (w/ package ghcr.io access)
##########################

#####################################
# Generating Image Tag
#####################################

# https://www.cyberciti.biz/faq/linux-unix-shell-programming-converting-lowercase-uppercase/
REPO=$(echo "${GIT_REPOSITORY_NAME}" | tr '[:upper:]' '[:lower:]')

IMAGE_NAME=$( echo "${REPO}" | sed -e "s/.*\///g" )
# TAG=$(date +%y.%m).$(git tag -l | wc -l)
TAG=$(date +%y.%m)
DOCKER_TAG="$IMAGE_NAME:$TAG"
#####################################################################################

# see https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#pushing-container-images
# DOCKER_IMAGE="ghcr.io/${GITHUB_REPOSITORY_OWNER}/${GIT_REPOSITORY_NAME}/${DOCKER_TAG}"
DOCKER_IMAGE="ghcr.io/${GITHUB_REPOSITORY_OWNER}/${DOCKER_TAG}"

echo "========================"
echo "BUILDING ${DOCKER_IMAGE}"
echo "========================"
docker build -t "${DOCKER_IMAGE}" -f ${DOCKER_FILE} .

echo "================================================="
echo "LOGGING IN TO GITHUB CONTAINER REGISTRY (GHCR.IO)"
echo "================================================="
echo "${ACCESS_TOKEN}" | docker login ghcr.io -u "${GITHUB_REPOSITORY_OWNER}" --password-stdin

echo "===================================================================="
echo "PUSHING DOCKER IMAGE ${DOCKER_IMAGE} TO CONTAINER REGISTRY (GHCR.IO)"
echo "===================================================================="
docker push "${DOCKER_IMAGE}"