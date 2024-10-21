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
echo 5. Sair
echo =====================================
set /p escolha="Escolha uma opcao: "

if %escolha%==1 goto status
if %escolha%==2 goto add
if %escolha%==3 goto commit
if %escolha%==4 goto push
if %escolha%==5 goto fim
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

:fim
echo Saindo...
pause