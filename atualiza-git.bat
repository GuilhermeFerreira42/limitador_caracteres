@echo off

:: Altere para o diretorio onde o script esta localizado
cd /d %~dp0

:menu
cls
echo Diretorio atual: %cd%
echo =====================================
echo     GIT AUTOMATION MENU
echo =====================================
echo 1. Verificar status do repositorio
echo 2. Adicionar todas as alteracoes
echo 3. Fazer commit
echo 4. Fazer push para o GitHub
echo 5. Fazer pull do repositorio
echo 6. Mostrar log de commits
echo 7. Mostrar comandos basicos do Git
echo 8. Sair
echo =====================================
set /p escolha="Escolha uma opcao: "

if %escolha%==1 goto status
if %escolha%==2 goto add
if %escolha%==3 goto commit
if %escolha%==4 goto push
if %escolha%==5 goto pull
if %escolha%==6 goto log
if %escolha%==7 goto comandos
if %escolha%==8 goto fim
goto menu

:status
echo Diretorio atual: %cd%
echo Verificando o status do repositorio...
git status
pause
goto menu

:add
echo Diretorio atual: %cd%
echo Adicionando todas as alteracoes...
git add .
pause
goto menu

:commit
set /p comentario="Digite o comentario do commit: "
echo Diretorio atual: %cd%
git commit -m "%comentario%"
pause
goto menu

:push
echo Diretorio atual: %cd%
echo Fazendo push para o GitHub...
git push
pause
goto menu

:pull
echo Diretorio atual: %cd%
echo Fazendo pull do repositorio...
git pull
pause
goto menu

:log
echo Diretorio atual: %cd%
echo Exibindo o historico de commits...
git log
pause
goto menu

:comandos
cls
echo =====================================
echo     COMANDOS BASICOS DO GIT
echo =====================================
echo git init: Inicializa um novo repositorio Git
echo git status: Mostra o estado do repositorio
echo git commit -m "mensagem": Faz um commit
echo git push: Envia commits para o remoto
echo git pull: Baixa atualizacoes e mescla
echo git fetch: Baixa atualizacoes sem mesclar
echo git merge: Mescla uma branch
echo git branch: Lista as branches locais
echo git reset: Desfaz alteracoes
echo git log: Exibe o historico de commits
echo =====================================
echo 1. Voltar ao menu principal
echo =====================================
set /p voltar="Escolha uma opcao: "

if %voltar%==1 goto menu
goto comandos

:fim
echo Saindo...
pause
