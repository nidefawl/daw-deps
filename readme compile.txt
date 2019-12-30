OSX:
python ../daw-deps/build.py ./build ./install -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_OSX_DEPLOYMENT_TARGET=10.12
WIN:
python ../daw-deps/build.py ./build ./install -DCMAKE_EXPORT_COMPILE_COMMANDS=ON 

cmake .. -G "MinGW Makefiles" -DCMAKE_CXX_FLAGS=--target=x86_64-pc-windows-gnu -DCMAKE_C_FLAGS=--target=x86_64-pc-windows-gnu