#!/bin/bash
# script to automatically generate the sphinx_nbexamples api documentation using
# sphinx-apidoc and sed
sphinx-apidoc -f -M -e  -T -o api ../model_organization/
# replace chapter title in model_organization.rst
sed -i '' -e 1,1s/.*/'API Reference'/ api/model_organization.rst
sed -i '' -e 2,2s/.*/'============='/ api/model_organization.rst
