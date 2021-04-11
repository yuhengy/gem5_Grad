all: hello
hello: hello.cpp
	$(shell mkdir -p build)
	$(CC) -static -I../../../include/ -L../../../util/m5/build/$(ISA)/out hello.cpp -lm5 -o build/hello

