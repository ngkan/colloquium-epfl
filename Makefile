UV ?= uv
SHOWCASE := output/epfl-math-showcase.html
STARTER := output/epfl-starter.html

.PHONY: install build export starter serve test clean
install:
	$(UV) sync --locked
build:
	$(UV) run --locked epfl-slides examples/showcase.md -o $(SHOWCASE)
export:
	$(UV) run --locked epfl-slides examples/showcase.md -o $(SHOWCASE) --pdf
starter:
	$(UV) run --locked epfl-slides examples/starter.md -o $(STARTER)
serve: build
	$(UV) run --locked python -m http.server 8091 --bind 127.0.0.1 --directory output
test:
	$(UV) run --locked python -m unittest discover -s tests -v
clean:
	rm -f output/epfl-math-showcase.html output/epfl-math-showcase.pdf output/epfl-starter.html
