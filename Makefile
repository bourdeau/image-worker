PREFIX ?= /usr/local
BINDIR ?= $(DESTDIR)$(PREFIX)/bin
MANDIR ?= $(DESTDIR)$(PREFIX)/share/man/man1
DOCDIR ?= $(DESTDIR)$(PREFIX)/share/doc/worker

.PHONY: all install uninstall

all:

install:
	install -m755 -d $(BINDIR)
	install -m755 -d $(MANDIR)
	install -m755 -d $(DOCDIR)
	cp worker.py image-worker
	install -m755 image-worker $(BINDIR)
	install -m644 README.md $(DOCDIR)
	rm image-worker

uninstall:
	rm -f $(BINDIR)/image-worker
	rm -rf $(DOCDIR)
