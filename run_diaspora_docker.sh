#!/usr/bin/env bash
set -e

if [ -z "${DSE_TUNNEL_PATH}" ]; then
  echo "Tunnel path is not set"
  exit 1
fi

DIR="$(dirname "${DSE_TUNNEL_PATH}")"
if [ ! -d "${DIR}" ]; then
  echo "The directory '${DIR}' does not exist."
  exit 1
fi

FILE="$(basename "${DSE_TUNNEL_PATH}")"

exec docker run \
  --cpus=1 \
  -v "${DIR}":/var/run/dse \
  --env "DSE_TUNNEL_PATH=/var/run/dse/$FILE" \
  --rm \
  diaspora-dse "$@"

