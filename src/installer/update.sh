#!/bin/bash

# Define o caminho do arquivo a ser pesquisado
file_path="../locales/en/LC_MESSAGES/stop-smoke.po"

# Usa o comando grep para procurar a linha desejada e, em seguida, usa o comando sed para extrair o valor
version=$(grep "Project-Id-Version:" "$file_path" | sed 's/[^0-9\.]*//g' | tr -d '\n')

# Exibe o valor da versão no console
echo "Versão: $version"



# Update version in .iss file in MyAppVersion variable
#sed -i "s/MyAppVersion*/MyAppVersion $VERSION/g" stop-smoke.iss

#ISCC.exe stop-smoke.iss