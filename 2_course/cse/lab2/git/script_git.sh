#!/bin/bash
set -e

if [ -d "./commits" ]; then
    ZIP_DIR=$(realpath "./commits")
else
    echo "Папка 'commits' не найдена!"
    exit 1
fi

unzip_commit() {
    local rev=$1
    local zip_path="$ZIP_DIR/$rev.zip"
        
    if [ ! -f "$zip_path" ]; then
        echo " Файл $zip_path не найден!"
        exit 1
    fi

    find . -maxdepth 1 ! -name '.git' ! -name '.' -exec rm -rf {} +
    unzip -qo "$zip_path" -d .
    git add .
}

resolve_conflicts() {
    echo "Конфликт"
    git status

    echo "Исправьте конфликты вручную"
    echo "После этого выполните:"
    echo "  git add ."
    echo "  git commit"

    while true; do
        read -p "Нажмите ENTER для проверки..."

        if git diff --name-only --diff-filter=U | grep -q .; then
            echo "Конфликты всё ещё есть!"
        else
            echo "Конфликты решены"
            break
        fi
    done
}

rm -rf OPI_Lab2_Git
mkdir OPI_Lab2_Git
cd OPI_Lab2_Git
git init
git config user.name "Egor Shubin"
unzip_commit "commit0"
git commit -m "r0" 
unzip_commit "commit1"
git commit -m "r1"

git config user.name "Vlad Larionov"
git switch -c dev/branch_blue
unzip_commit "commit2" 
git commit -m "r2"
unzip_commit "commit3"
git commit -m "r3" 

git config user.name "Egor Shubin"
git switch master
unzip_commit "commit4"
git commit -m "r4"
git switch -c dev/branch_red
unzip_commit "commit5"
git commit -m "r5"

git config user.name "Vlad Larionov"
git switch dev/branch_blue
unzip_commit "commit6"
git commit -m "r6" 

git config user.name "Egor Shubin"
git switch dev/branch_red
unzip_commit "commit7"
git commit -m "r7"

git config user.name "Vlad Larionov"
git switch dev/branch_blue
unzip_commit "commit8"
git commit -m "r8"

git merge dev/branch_red --no-ff -m "merge with red-branch" || resolve_conflicts

unzip_commit "commit9"
git commit -m "r9" 
unzip_commit "commit10"
git commit -m "r10" 
unzip_commit "commit11"
git commit -m "r11"
unzip_commit "commit12"
git commit -m "r12"
unzip_commit "commit13"
git commit -m "r13"

git config user.name "Egor Shubin"
git switch master
unzip_commit "commit14"
git commit -m "r14"

git merge dev/branch_red --no-ff -m "merge with red-branch" || resolve_conflicts

git log --graph --oneline --decorate --all