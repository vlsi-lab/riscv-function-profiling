ROOT_DIR ?= $(realpath .)
BUILD_DIR ?= $(ROOT_DIR)/build/
TEST_DIR ?= $(ROOT_DIR)/cv32e40x
FG_DATA  ?= $(BUILD_DIR)flamegraph.data
PYTHON3 ?= python3
MAIN_ELF ?= $(TEST_DIR)/main.elf
WAVES	 ?= $(TEST_DIR)/waves.fst
SVG      ?= $(BUILD_DIR)flamegraph.svg


.PHONY: vendor-update
vendor-update:
	find sw/vendor -maxdepth 1 -type f -name "*.vendor.hjson" -exec python3 util/vendor.py -vU '{}' \;

$(FG_DATA): $(TEST_DIR)/config.wal $(MAIN_ELF) $(WAVES) $(BUILD_DIR)
	cd $(TEST_DIR) && $(PYTHON3) ../src/riscv-profile.py $(MAIN_ELF) $(WAVES) $(FG_DATA)

.PHONY: test
test: $(FG_DATA) $(SVG)

$(SVG): $(FG_DATA)
	# Generating SVG flamegraph...
	cd sw/vendor/FlameGraph && ./flamegraph.pl --flamechart $(FG_DATA) > $(SVG)
	# Changing SVG colormap...
	$(PYTHON3) src/colors.py $(SVG)

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)

%/:
	mkdir -p $@