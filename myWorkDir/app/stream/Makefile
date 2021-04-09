CFLAGS = -O2 -static -DNTIMES=2 -DSTREAM_ARRAY_SIZE=5000

all: stream

stream: stream.c
	$(shell mkdir -p build)
	$(CC) $(CFLAGS) stream.c -o build/stream

clean:
	rm -rf build
