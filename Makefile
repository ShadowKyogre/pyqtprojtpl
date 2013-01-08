ifeq ("$(APPNAME)","")
$(error What the fuck are you doing, please give your project an APPNAME!)
endif

ifeq ("$(DESTDIR)","")
$(error What the fuck are you doing, please put your project somewhere!)
endif

all: prepare setup.py $(APPNAME)lib $(APPNAME).desktop README.md

prepare:
	mkdir -p $(DESTDIR)

README.md:
	m4 -D_APPNAME_=$(APPNAME) $@.in >$(DESTDIR)/$@

setup.py:
	m4 -D_APPNAME_=$(APPNAME) -D_APPNAME_lib=$(APPNAME)lib $@.in >$(DESTDIR)/$@

$(APPNAME)lib:
	mkdir -p $(DESTDIR)/$@
	m4 -D_APPNAME_=$(APPNAME) appcode/__init__.py.in >$(DESTDIR)/$@/__init__.py
	m4 -D_APPNAME_Config=$(APPNAME)Config -D_APPNAME_=$(APPNAME) appcode/gui.py.in >$(DESTDIR)/$@/gui.py
	m4 -D_APPNAME_Config=$(APPNAME)Config appcode/guiconfig.py.in >$(DESTDIR)/$@/guiconfig.py
	m4 -D_APPNAME_=$(APPNAME) appcode/core.py.in >$(DESTDIR)/$@/core.py

$(APPNAME).desktop:
	m4 -D_APPNAME_=$(APPNAME) _APPNAME_.desktop.in >$(DESTDIR)/$@


