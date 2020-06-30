sync:
	while sleep 1 ; do find . -name '*.py' | entr -d rsync -avz --prune-empty-dirs --include="*/" --include="*.py" --exclude="*" ./ /Volumes/CIRCUITPY ; done
