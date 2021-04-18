MRSFAST_VERSION := "3.4.2"
BUILD_DATE := "$(shell date)"

CC = $(CCPRE)gcc
all: OPTIMIZE_FLAGS build
debug: DEBUG_FLAGS build
profile: PROFILE_FLAGS build
build: clean_executables SSE_FLAGS build/mrsFast snp_indexer clean_objects


LIBS=-lz -lm -lm5
CFLAGS=-fPIC -static -DMRSFAST_VERSION=\"$(MRSFAST_VERSION)\" -DBUILD_DATE=\"$(BUILD_DATE)\" -I../../../include/
LDFLAGS=-L../../../util/m5/build/$(ISA)/out -static

objects=baseFAST.o Sort.o MrsFAST.o Common.o CommandLineParser.o RefGenome.o HashTable.o Reads.o Output.o SNPReader.o

build/mrsFast: clean_executables $(objects)
	$(shell mkdir -p build)
ifeq ($(shell uname -s),Linux)
	$(CC) -w $(objects) -o $@ ${LDFLAGS} ${LIBS}
else
	$(CC) -Wl,-no_pie -fno-pic -w $(objects) -o $@ ${LDFLAGS} ${LIBS}
endif

snp_indexer: clean_executables SNPIndexer.o
	$(CC) SNPIndexer.o -o $@ ${LDFLAGS} ${LIBS}

clean_objects: build/mrsFast snp_indexer
	@rm -f $(objects)
	@rm -f SNPIndexer.o
	@rm -f HELPstub.c
	@rm -f HELPstub.o

clean:
	@rm -f $(objects)
	@rm -f SNPIndexer.o
	@rm -f HELPstub.c
	@rm -f HELPstub.o
	
clean_executables:
	@rm -f build/mrsFast
	@rm -f snp_indexer

DEBUG_FLAGS:
	$(eval CFLAGS = $(CFLAGS) -ggdb)
	$(eval LIBS = $(LIBS) -ggdb)

OPTIMIZE_FLAGS:
	$(eval CFLAGS = $(CFLAGS) -O2)

PROFILE_FLAGS:
		$(eval CFLAGS = $(CFLAGS) -pg -g)
	$(eval LIBS = $(LIBS) -pg -g)

SSE_FLAGS:
ifeq ($(shell uname -s),Linux)
ifeq ($(with-sse4),no)
		$(shell echo "-DSSE4=0")
else
        	$(eval CFLAGS = $(CFLAGS) \
        	$(shell gv=`$(CC) -dumpversion`; \
            	    sc=`grep -c "sse4" /proc/cpuinfo`; \
                	echo $$sc.$$gv | awk -F. '{if($$1>0 && $$2>=4 && $$3>=4) print "-DSSE4=1 -msse4.2"; else print "-DSSE4=0"}'))
endif
else
ifeq ($(with-sse4),no)
		$(shell echo "-DSSE4=0")
else
        $(eval CFLAGS = $(CFLAGS) \
        $(shell gv=`$(CC) -dumpversion`; \
                sc=`sysctl -n machdep.cpu.features | grep -c "SSE4"` ;\
                echo $$sc.$$gv | awk -F. '{if($$1>0 && $$2>=4 && $$3>=4) print "-DSSE4=1 -msse4.2"; else print "-DSSE4=0"}'))
endif
endif
