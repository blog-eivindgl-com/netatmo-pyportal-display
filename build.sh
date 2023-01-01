if [[ ! -e ./build ]]; then
    mkdir ./build
fi
 
cp ./src/code.py ./build/

#
for file in ./src/*.py
do
    if [ "$file" == "code.py" || "$file" == "secrets.py" ]; then
        continue
    fi
    ./mpycross -o ./build/ ./src/$file
done

