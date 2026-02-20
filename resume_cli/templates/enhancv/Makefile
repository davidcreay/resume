# templates/enhancv/Makefile
MY_NAME = David_Reay
DATE    = $(shell date +%Y-%m-%d)

all: resume letter

resume:
	@echo "Compiling Resume PDF..."
	xelatex -jobname=$(MY_NAME)_CV_$(DATE) resume.tex

letter:
	@if [ -f cover_letter.tex ]; then \
		echo "Compiling Cover Letter PDF..."; \
		xelatex -jobname=$(MY_NAME)_Cover_Letter_$(DATE) cover_letter.tex; \
	fi

clean:
	rm -f *.aux *.log *.out *.pdf