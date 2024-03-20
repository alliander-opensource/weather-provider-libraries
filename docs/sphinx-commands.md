# How to update the Sphinx documentation

The following two commands can be used to update the Sphinx documentation that is also used to construct the GitHub 
Pages for this project.

1. The command to update the Sphinx module information:<br>
`sphinx-apidoc -o ./docs/sphinx-docs/ ./src/weather_provider_libraries/`

2. Rebuild the Sphinx documentation with the current module information.<br>
`sphinx-build  ./docs/sphinx-docs/ _build`