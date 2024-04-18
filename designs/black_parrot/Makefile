include ../Makefile.inc

all: black_parrot_edited.v black_parrot_snl.v

black_parrot_snl/snl.mf: black_parrot.v
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f verilog -t snl -i $< -o black_parrot_snl -p ${NANGATE45_PRIMITIVES}

black_parrot_snl.v: black_parrot_snl/snl.mf
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f snl -t verilog -i black_parrot_snl -o black_parrot_snl.v

black_parrot_edited.v: pre_edit.py post_edit.py black_parrot_snl/snl.mf
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f snl -t verilog -i black_parrot_snl -o black_parrot_edited.v -e pre_edit.py -z post_edit.py 

clean:
	-rm -rf black_parrot_snl black_parrot_snl.v black_parrot_edited.v 
