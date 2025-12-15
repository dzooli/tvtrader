#!/bin/bash
echo "Checking submodule branch status..."

git submodule foreach '
    BRANCH=$(git config -f $toplevel/.gitmodules submodule.$name.branch || echo main)
    CURRENT=$(git rev-parse --abbrev-ref HEAD)
    
    if [ "$CURRENT" = "HEAD" ]; then
        echo "⚠️  $name is in DETACHED HEAD state!"
        echo "   Run: cd $sm_path && git checkout $BRANCH"
    elif [ "$CURRENT" != "$BRANCH" ]; then
        echo "⚠️  $name is on wrong branch ($CURRENT, expected $BRANCH)"
    else
        echo "✅ $name is on correct branch ($CURRENT)"
    fi
'

