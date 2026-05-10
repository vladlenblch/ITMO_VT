#!/bin/bash
export SVN_EDITOR="'/usr/bin/nano' -w"

if [ ! -d "./commits" ]; then
    echo "Папка commits не найдена!"
    exit 1
fi

unzip_commit() {
    local rev=$1
    local zip_path="../commits/${rev}.zip"

    if [ ! -f "$zip_path" ]; then
        echo "Файл $zip_path не найден!"
        exit 1
    fi

    find . -maxdepth 1 ! -name '.svn' ! -name '.' -exec rm -rf {} +
    unzip -qo "$zip_path" -d .

    svn add --force . >/dev/null 2>&1 || true
    svn status | grep '^\!' | sed 's/^! *//' | xargs -I% svn rm "%" 2>/dev/null || true
}

rm -rf OPI_Lab2_svn red blue low_red

REPO="$PWD/OPI_Lab2_svn"
svnadmin create "$REPO"
REPO_URL="file://$REPO"

svn mkdir -m "add trunk and branches" "$REPO_URL/trunk" "$REPO_URL/branches"

svn co "$REPO_URL/trunk" red

cd red
unzip_commit "commit0"
svn commit -m "r0" --username "Egor Shubin"
cd ..

# r1
svn copy "$REPO_URL/trunk" "$REPO_URL/branches/blue" -m "r1"
svn co "$REPO_URL/branches/blue" blue
cd blue
unzip_commit "commit1"
svn commit -m "r1" --username "Vlad Larionov"
cd ..

# r2, r3
cd red
svn up
unzip_commit "commit2"
svn commit -m "r2" --username "Egor Shubin"
unzip_commit "commit3"
svn commit -m "r3" --username "Egor Shubin"
cd ..

# r4
svn copy "$REPO_URL/trunk" "$REPO_URL/branches/low_red" -m "create low_red (r4)" --username "Egor Shubin"
svn co "$REPO_URL/branches/low_red" low_red

cd low_red
unzip_commit "commit4"
svn commit -m "r4" --username "Egor Shubin"
cd ..

# r5 
cd blue
unzip_commit "commit5"
svn commit -m "r5" --username "Vlad Larionov"
cd ..

# r6, 7, 8
cd low_red
svn up
unzip_commit "commit6"
svn commit -m "r6" --username "Egor Shubin"
unzip_commit "commit7"
svn commit -m "r7" --username "Egor Shubin"
unzip_commit "commit8"
svn commit -m "r8" --username "Egor Shubin"
cd ..

# r9, 10, 11
cd blue
svn up
svn merge ^/branches/low_red
svn resolve --accept working -R .
unzip_commit "commit9"
svn commit -m "r9" --username "Vlad Larionov"
unzip_commit "commit10"
svn commit -m "r10" --username "Vlad Larionov"
unzip_commit "commit11"
svn commit -m "r11" --username "Vlad Larionov"
cd ..

# r12, 13, 14
cd red
svn up
unzip_commit "commit12"
svn commit -m "r12" --username "Egor Shubin"
svn merge ^/branches/blue
svn resolve --accept working -R .

unzip_commit "commit13"
svn commit -m "r13k" --username "Egor Shubin"
unzip_commit "commit14"
svn commit -m "r14" --username "Egor Shubin"
cd ..

svn log "$REPO_URL/trunk"