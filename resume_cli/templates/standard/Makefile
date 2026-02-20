# Variables
MY_NAME = David_Reay_full
DATE    = $(shell date +%Y-%m-%d)
OUTPUT  = $(MY_NAME)_$(DATE).pdf

all:
	@echo "Building $(OUTPUT)..."
	@xelatex -jobname=$(MY_NAME)_$(DATE) resume.tex
	@echo "Done! Saved as $(OUTPUT)"

clean:
	rm -f *.aux *.log *.out *.pdf *.toc *.pre