ROOT_DIR ?= $(realpath .)
BUILD_DIR ?= $(ROOT_DIR)/build/
TEST_DIR ?= $(ROOT_DIR)/cv32e40x
FG_DATA  ?= $(BUILD_DIR)flamegraph.data
PYTHON3 ?= python3
MAIN_ELF ?= $(TEST_DIR)/main.elf
WAVES	 ?= $(TEST_DIR)/waves.fst
SVG      ?= $(BUILD_DIR)flamegraph.svg
CFG_DATA ?= $(TEST_DIR)/config.wal
ARGS	 ?= --elf $(MAIN_ELF) --fst $(WAVES) --cfg $(CFG_DATA)


.PHONY: vendor-update
vendor-update:
	find sw/vendor -maxdepth 1 -type f -name "*.vendor.hjson" -exec python3 util/vendor.py -vU '{}' \;

$(FG_DATA): $(TEST_DIR)/config.wal $(MAIN_ELF) $(WAVES) $(CFG_DATA) $(BUILD_DIR)
	$(PYTHON3) src/rv_profile.py $(ARGS)

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