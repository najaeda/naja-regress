include ../Makefile.inc

INPUTS = megaboom1.v megaboom2.v megaboom3.v data_2048x8.v btb_128x56.v ebtb_128x40.v meta_128x120.v array_256x128.v \
				 lb_32x128.v sdq_17x64.v dataArrayB_256x64.v tag_array_64x168.v tag_array_64x184.v \
				 l2_tlb_ram_0_512x46.v regfile_128x65.v regfile_128x64.v table_128x44.v mem_256x4.v \
				 table_256x48.v table_128x52.v
				 
INPUTS_DIR = $(foreach input,$(INPUTS),sources/$(input))
PARSE_INPUTS = $(foreach input,$(INPUTS_DIR),-i $(input))

all: megaboom_all_edited.v

megaboom_snl/snl.mf: $(INPUTS_DIR)
	export PYTHONPATH=${SET_PYTHONPATH}; \
	${PYTHON_ENV} ${NAJA_EDIT} -f verilog -t snl $(PARSE_INPUTS) -o megaboom_snl -p ${PRIMITIVES}/asap7_new.py

megaboom_all_edited.v: ${SCRIPTS}/pre_edit.py ${SCRIPTS}/post_edit.py megaboom_snl/snl.mf
	export PYTHONPATH=${SET_PYTHONPATH}; \
	export PRE_EDIT_BASE_NAME=megaboom_all_pre; \
	export POST_EDIT_BASE_NAME=megaboom_all_post; \
	${PYTHON_ENV} ${NAJA_EDIT} -f snl -t verilog -i megaboom_snl -o megaboom_all_edited.v -e ${SCRIPTS}/pre_edit.py -a all -z ${SCRIPTS}/post_edit.py 

clean:
	-rm -rf megaboom_snl
	-rm -rf __pycache__
	-rm *.stats

