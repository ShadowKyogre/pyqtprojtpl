ifeq ("$(APPNAME)","")
$(error What the fuck are you doing, please give your project an APPNAME!)
endif

ifeq ("$(DESTDIR)","")
$(error What the fuck are you doing, please put your project somewhere!)
endif

all: prepare setup.py __init__.py gui.py guiconfig.py core.py $(APPNAME).desktop README.md

prepare:
	mkdir -p $(DESTDIR)
	cp COPYTING $(DESTDIR)

README.md: prepare
	m4 -D_APPNAME_=$(APPNAME) $@.in >$(DESTDIR)/$@

setup.py: prepare
	m4 -D_APPNAME_=$(APPNAME) -D_APPNAME_lib=$(APPNAME)lib $@.in >$(DESTDIR)/$@

$(APPNAME)lib: prepare
	mkdir -p $(DESTDIR)/$@

__init__.py: $(APPNAME)lib
	m4 -D_APPNAME_=$(APPNAME) appcode/__init__.py.in >$(DESTDIR)/$(APPNAME)lib/$@

gui.py: $(APPNAME)lib
	m4 -D_APPNAME_Config=$(APPNAME)Config -D_APPNAME_=$(APPNAME) appcode/gui.py.in >$(DESTDIR)/$(APPNAME)lib/$@

guiconfig.py: $(APPNAME)lib
	m4 -D_APPNAME_Config=$(APPNAME)Config appcode/guiconfig.py.in >$(DESTDIR)/$(APPNAME)lib/$@

core.py: $(APPNAME)lib
	m4 -D_APPNAME_=$(APPNAME) appcode/core.py.in >$(DESTDIR)/$(APPNAME)lib/$@

$(APPNAME).desktop: prepare
	m4 -D_APPNAME_=$(APPNAME) _APPNAME_.desktop.in >$(DESTDIR)/$(APPNAME)lib/$@


