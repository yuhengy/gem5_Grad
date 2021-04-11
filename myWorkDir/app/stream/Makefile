CFLAGS = -O2 -static -I../../../include/ -L../../../util/m5/build/$(ISA)/out -DNTIMES=2 -DSTREAM_ARRAY_SIZE=5000

all: stream

stream: stream.c
	$(shell mkdir -p build)
	$(CC) $(CFLAGS) stream.c -lm5 -o build/stream

clean:
	rm -rf build
