include ../Makefile.inc

INPUTS = megaboom1.v megaboom2.v megaboom3.v data_2048x8.v btb_128x56.v ebtb_128x40.v meta_128x120.v array_256x128.v \
				 lb_32x128.v sdq_17x64.v dataArrayB_256x64.v tag_array_64x168.v tag_array_64x184.v \
				 l2_tlb_ram_0_512x46.v regfile_128x65.v regfile_128x64.v table_128x44.v mem_256x4.v \
				 table_256x48.v table_128x52.v
				 
INPUTS_DIR = $(foreach input,$(INPUTS),sources/$(input))
PARSE_INPUTS = $(foreach input,$(INPUTS_DIR),-i $(input))

all: parse_snl

megaboom_snl/snl.mf: $(INPUTS_DIR)
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f verilog -t snl $(PARSE_INPUTS) -o megaboom_snl -p ${ASAP7_PRIMITIVES}

parse_snl: megaboom_snl/snl.mf
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f snl -i megaboom_snl -a dle -e ${SCRIPTS}/pre_edit.py -z ${SCRIPTS}/post_edit.py

clean:
	-rm -rf megaboom_snl
	-rm -rf __pycache__
	-rm *.stats

