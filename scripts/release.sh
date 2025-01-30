#!/usr/bin/env bash
export MLFLOW_OIDC_AUTH_VERSION=${1:-3.0.0.dev0}
#export MLFLOW_OIDC_AUTH_VERSION=${1:-0.0.0.dev0}
pushd web-ui &&\
yarn install &&\
yarn release &&\
popd &&\
python -m build