#
# Makefile for PhotoFilmStrip
#
include Makefile.rules


compile:
	python -c "import compileall, re;compileall.compile_dir('.', rx=re.compile('/[.]svn'), force=True, quiet=True)"
	python -OO -c "import compileall, re;compileall.compile_dir('.', rx=re.compile('/[.]svn'), force=True, quiet=True)"
	
	target=`echo $@`; \
	make -C po $$target

clean:
	if [ -e ./dist ] ; then rm -r ./dist ; fi
	find . -name "*.pyc" -exec rm {} ';'
	find . -name "*.pyo" -exec rm {} ';'
	
	target=`echo $@`; \
	make -C po $$target

	rm -f "$(displayname).pot"

install:
	$(mkdir) "$(DESTDIR)$(appdir)"
	cp -r "$(srcdir)/src/cli/" "$(DESTDIR)$(appdir)"
	cp -r "$(srcdir)/src/core/" "$(DESTDIR)$(appdir)"
	cp -r "$(srcdir)/src/gui/" "$(DESTDIR)$(appdir)"
	cp -r "$(srcdir)/src/lib/" "$(DESTDIR)$(appdir)"
	cp -r "$(srcdir)/src/res/" "$(DESTDIR)$(appdir)" 
	cp "$(srcdir)/src/$(appname)-cli.py" "$(DESTDIR)$(appdir)/"
	cp "$(srcdir)/src/$(appname)-gui.py" "$(DESTDIR)$(appdir)/"
	
	$(mkdir) "$(DESTDIR)$(desktopdir)"
	cp "$(srcdir)/build/$(appname).desktop" "$(DESTDIR)$(desktopdir)/"
	$(mkdir) "$(DESTDIR)$(pixmapdir)"
	cp "$(srcdir)/build/$(appname).xpm" "$(DESTDIR)$(pixmapdir)/"
	
	$(mkdir) "$(DESTDIR)$(bindir)"
	cp "$(srcdir)/build/$(appname)" "$(DESTDIR)$(bindir)/"
	cp "$(srcdir)/build/$(appname)-cli" "$(DESTDIR)$(bindir)/"
	
	target=`echo $@`; \
	make -C po $$target

uninstall:
	rm -Rf "$(DESTDIR)$(appdir)"
	rm -f "$(DESTDIR)$(desktopdir)/$(appname).desktop"
	rm -f "$(DESTDIR)$(pixmapdir)/$(appname).xpm"
	rm -f "$(DESTDIR)$(bindir)/$(appname)"
	rm -f "$(DESTDIR)$(bindir)/$(appname)-cli"
	
	target=`echo $@`; \
	make -C po $$target

pot:
	pygettext -o "$(displayname).pot" -v "$(srcdir)/src"


deb:
	appver=`echo $(appname)-$(VER)`; \
	releasedir=`echo release_\`date +"%Y_%m_%d"\``; \
	targetdir=`echo $$releasedir/$$appver`; \
	rm -rf $$releasedir; \
	$(mkdir) "$$targetdir"; \
	cp -R build/ "$$targetdir"; \
	cp -R po/ "$$targetdir"; \
	cp -R res/ "$$targetdir"; \
	cp -R src/ "$$targetdir"; \
	cp CHANGES "$$targetdir/"; \
	cp COPYING "$$targetdir/"; \
	cp Makefile "$$targetdir/"; \
	cp Makefile.rules "$$targetdir/"; \
	cp README "$$targetdir/"; \
	cp TODO "$$targetdir/"; \
	rm -rf `find $$targetdir -name .svn -type d`; \
	tar -C "$$releasedir" -czf "$$releasedir/$$appver.tar.gz" $$appver; \
	cd $$targetdir; \
	dh_make -e "jens@sg-dev.de" -c gpl -s -f "../$$appver.tar.gz"; \
	rm debian/*.ex; \
	rm debian/*.EX
