include ../Makefile.inc

all: swerv_wrapper_snl.v

swerv_wrapper/snl.mf: swerv_wrapper.v
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f verilog -t snl -i $< -o swerv_wrapper -p ${PRIMITIVES}/nangate45.py -e ${SCRIPTS}/pre_edit.py -a all -z ${SCRIPTS}/post_edit.py

swerv_wrapper_snl.v: swerv_wrapper/snl.mf
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f snl -t verilog -i swerv_wrapper -o swerv_wrapper_snl.v

clean:
	-rm -rf __pycache__ swerv_wrapper swerv_wrapper_snl.v swerv_wrapper_edited.v *.log *.stats 
