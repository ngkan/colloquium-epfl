UV ?= uv
SHOWCASE := output/epfl-math-showcase.html
STARTER := output/epfl-starter.html
PCP := output/epfl-pcp-showcase.html

.PHONY: install build export starter export-starter pcp export-pcp serve test clean
install:
	$(UV) sync --locked
build:
	$(UV) run --locked epfl-slides examples/showcase.md -o $(SHOWCASE)
export:
	$(UV) run --locked epfl-slides examples/showcase.md -o $(SHOWCASE) --pdf
starter:
	$(UV) run --locked epfl-slides examples/starter.md -o $(STARTER)
export-starter:
	$(UV) run --locked epfl-slides examples/starter.md -o $(STARTER) --pdf
pcp:
	$(UV) run --locked epfl-slides examples/pcp-showcase.md -o $(PCP)
export-pcp:
	$(UV) run --locked epfl-slides examples/pcp-showcase.md -o $(PCP) --pdf
serve: build
	$(UV) run --locked python -m http.server 8091 --bind 127.0.0.1 --directory output
test:
	$(UV) run --locked python -m unittest discover -s tests -v
clean:
	rm -f output/epfl-math-showcase.html output/epfl-math-showcase.pdf $(STARTER) output/epfl-starter.pdf $(PCP) output/epfl-pcp-showcase.pdf
