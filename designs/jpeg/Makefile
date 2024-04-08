include ../Makefile.inc

all: parse_snl parse_snl_flat 

jpeg_snl/snl.mf: jpeg.v
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f verilog -t snl -i $< -o jpeg_snl -p ${ASAP7_PRIMITIVES}

jpeg_flat_snl/snl.mf: jpeg_flat.v
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f verilog -t snl -i $< -o jpeg_flat_snl -p ${ASAP7_PRIMITIVES}

parse_snl: jpeg_snl/snl.mf
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f snl -i jpeg_snl

parse_snl_flat: jpeg_flat_snl/snl.mf
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f snl -i jpeg_flat_snl

clean:
	-rm -rf jpeg_snl jpeg_flat_snl 
