MONCTL := fl-monitor-ctl monitor.conf
LOG_HOME := ./log

ifdef REPORT_HOME
	REPORT = $(REPORT_HOME)
else
	REPORT = ./report
endif

ifdef URL
# FunkLoad options
	FLOPS = -u $(URL) $(EXT)
else
	FLOPS = $(EXT)
endif

all: test

# testing
test: start
	fl-run-test test_restapp.py -dv $(FLOPS)

# benching
bench: start
	@$(MONCTL) restart
	-taskset -c 0 fl-run-bench -c 1:2:3:4:5:6:8:10:16 -D 4 -f --simple-fetch test_restapp.py restapp.test_restapp $(FLOPS)
	@$(MONCTL) stop
	-fl-build-report $(LOG_HOME)/restapp-bench.xml --html -o $(REPORT)

# monitor ctl
start:
	 -mkdir -p $(REPORT) $(LOG_HOME)

start_monitor:
	$(MONCTL) start

stop_monitor:
	-$(MONCTL) stop

restart_monitor:
	$(MONCTL) restart

clean:
	-find . "(" -name "*~" -or  -name ".#*" ")" -print0 | xargs -0 rm -f
