sync:
	while sleep 1 ; do find . -name '*.*py' | entr -d rsync -avz --delete --prune-empty-dirs --include="*/" --include="*.*py" --exclude="*" ./ /Volumes/CIRCUITPY ; done

test:
	while sleep 1 ; do find . -name '*.py' | entr pytest ; done
