all: docDist
docDist: docDist.cpp
	$(shell mkdir -p build)
	$(CCPRE)g++ -static -I../../../include/ -L../../../util/m5/build/$(ISA)/out docDist.cpp -lm5 -o build/docDist

