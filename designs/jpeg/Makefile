include ../Makefile.inc

all: jpeg_hier_edited.v jpeg_flat_edited.v

jpeg_snl/snl.mf: jpeg.v
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f verilog -t snl -i $< -o jpeg_snl -p ${PRIMITIVES}/asap7.py

jpeg_flat_snl/snl.mf: jpeg_flat.v
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f verilog -t snl -i $< -o jpeg_flat_snl -p ${PRIMITIVES}/asap7.py

jpeg_hier_edited.v: jpeg_snl/snl.mf
	export PYTHONPATH=${SET_PYTHONPATH}; \
	export PRE_EDIT_BASE_NAME=pre_hier; \
	export POST_EDIT_BASE_NAME=post_hier; \
	${PYTHON_ENV} ${NAJA_EDIT} -f snl -t verilog -i jpeg_snl -o jpeg_hier_edited.v -e ${SCRIPTS}/pre_edit.py -a dle -z ${SCRIPTS}/post_edit.py 

jpeg_flat_edited.v: jpeg_flat_snl/snl.mf
	export PYTHONPATH=${SET_PYTHONPATH}; \
	export PRE_EDIT_BASE_NAME=pre_flat; \
	export POST_EDIT_BASE_NAME=post_flat; \
	${PYTHON_ENV} ${NAJA_EDIT} -f snl -t verilog -i jpeg_flat_snl -o jpeg_flat_edited.v -e ${SCRIPTS}/pre_edit.py -a dle -z ${SCRIPTS}/post_edit.py 

clean:
	-rm -rf jpeg_snl jpeg_flat_snl *.log *.stats *_edited.v
