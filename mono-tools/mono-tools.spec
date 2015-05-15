%define debug_package %{nil}

Summary: A collection of tools for mono applications
Name: mono-tools
Version: 3.10
Release: 1%{?dist}
License: MIT
Group: Development/Tools
Source0: http://download.mono-project.com/sources/mono-tools/%{name}-%{version}.tar.gz
Patch0: mono-tools-3.10-webdoc.patch
URL: http://www.mono-project.com/Main_Page
BuildRequires:  mono-data, mono-devel >= 4.0, gtk-sharp2-gapi, pkgconfig mono-nunit
BuildRequires: gnome-sharp-devel, gettext-devel
BuildRequires: gtk-sharp2-devel autoconf automake libtool mono-nunit-devel
BuildRequires: hunspell-devel desktop-file-utils gnome-desktop-sharp-devel
BuildRequires: mono-data-oracle monodoc-devel mono-web-devel
BuildRequires: webkit-sharp-devel desktop-file-utils
BuildRequires: libgdiplus-devel
Requires: mono-core >= 4.0 links monodoc
Requires: mono(webkit-sharp)

# Mono only available on these:
ExclusiveArch: %ix86 x86_64 ppc ppc64 ia64 %{arm} sparcv9 alpha s390x

%description
Monotools are a number of tools for mono such as allowing monodoc to be run
independantly of monodevelop

%package devel
Summary: .pc file for mono-tools
Group: Development/Languages
Requires: %{name} = %{version}-%{release} pkgconfig

%description devel
Development file for mono-tools

%package monodoc
Summary: Monodoc documentation
Group: Documentation
Requires: %{name} = %{version}-%{release} monodoc

%description monodoc
Documentation for monotools for use with monodoc

%package gendarme
Summary: Inspect your .NET and Mono assemblies
Requires: %{name} = %{version}-%{release}

%description gendarme
Inspect your .NET and Mono assemblies.

%package ilcontrast
Summary: Assembly Comparison Tool
Requires: %{name} = %{version}-%{release}

%description ilcontrast
Identify differences in the API exposed by mono library assemblies.

%prep
%setup -q
%patch0 -p1
chmod 644 COPYING

find . -name "Makefile.in" -print -exec sed -i "s#GMCS#MCS#g" {} \;

%build
%configure --libdir=%{_prefix}/lib
make 
# no smp flags - breaks the build

%install
make DESTDIR=%{buildroot} install

desktop-file-install \
%if 0%{?fedora} && 0%{?fedora} < 19
        --vendor fedora \
%endif
        --dir %{buildroot}%{_datadir}/applications \
        --add-category Development \
        --delete-original \
        %{buildroot}%{_datadir}/applications/ilcontrast.desktop

desktop-file-install \
%if 0%{?fedora} && 0%{?fedora} < 19
        --vendor fedora \
%endif
        --dir %{buildroot}%{_datadir}/applications \
        --add-category Development \
        --delete-original \
        %{buildroot}%{_datadir}/applications/monodoc.desktop

mkdir -p %{buildroot}%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv %{buildroot}%{_prefix}/lib/pkgconfig/*.pc %{buildroot}%{_libdir}/pkgconfig/

%find_lang %{name}

%post
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%postun
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%files -f %{name}.lang
%defattr(-, root, root,-)
%doc COPYING AUTHORS ChangeLog README
%{_bindir}/create-native-map
%{_bindir}/gasnview
%{_bindir}/monodoc
%{_bindir}/mprof*
%{_bindir}/gsharp
%{_bindir}/gd2i
%{_bindir}/mperfmon
%{_bindir}/gui-compare
%{_bindir}/emveepee
%{_bindir}/minvoke
%{_prefix}/lib/gsharp/gsharp.exe*
%{_prefix}/lib/create-native-map
%{_prefix}/lib/mperfmon/*
%dir %{_prefix}/lib/gui-compare
%{_prefix}/lib/gui-compare/gui-compare.exe*
%{_prefix}/lib/mono/1.0/gasnview.exe
%{_prefix}/lib/monodoc/WebKitHtmlRender.dll
%{_prefix}/lib/monodoc/browser.exe
%{_prefix}/lib/minvoke/minvoke.exe
%dir %{_prefix}/lib/minvoke
%dir %{_prefix}/lib/mono-tools
%{_prefix}/lib/mono-tools/mprof*
%{_prefix}/lib/mono-tools/Mono.Profiler.Widgets*
%{_prefix}/lib/mono-tools/emveepee.exe*
%{_mandir}/man1/mprof*
%{_mandir}/man1/create-native-map.1.gz
%{_datadir}/pixmaps/ilcontrast.png
%{_datadir}/pixmaps/monodoc.png
%{_datadir}/applications/gsharp.desktop
%{_datadir}/applications/monodoc.desktop
%{_prefix}/lib/monodoc/MonoWebBrowserHtmlRender.dll
%{_mandir}/man1/mperfmon*
%{_mandir}/man1/gd2i*
%{_datadir}/icons/hicolor/

%files gendarme
%{_bindir}/gendarme*
%{_datadir}/applications/gendarme-wizard.desktop
%{_datadir}/pixmaps/gendarme.svg
%{_mandir}/man1/gendarme*
%{_prefix}/lib/gendarme/*.dll
%{_prefix}/lib/gendarme/*.exe
%{_prefix}/lib/gendarme/*.xml

%files ilcontrast
%{_datadir}/applications/ilcontrast.desktop
%{_bindir}/ilcontrast
%dir %{_prefix}/lib/ilcontrast
%{_prefix}/lib/ilcontrast/ilcontrast.exe

%files devel
%defattr(-, root, root,-)
%{_libdir}/pkgconfig/*.pc

%files monodoc
%defattr(-,root,root,-)
%{_prefix}/lib/monodoc/sources/Gendarme*
%{_prefix}/lib/monodoc/sources/gendarme*
%dir %{_prefix}/lib/monodoc/web
%{_prefix}/lib/monodoc/web/*
%{_mandir}/man5/gendarme*

%changelog
* Fri May 15 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 3.10-1
- upgrade to mono-tools 3.10, build with Mono4

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 24 2014 Richard Hughes <richard@hughsie.com> - 2.10-11
- Split out gendarme and ilcontrast as subpackages so the different applications
  are visible in gnome-software.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 2.10-8
- Remove --vendor from desktop-file-install for F19+

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 23 2011 Christian Krause <chkr@fedoraproject.org> - 2.10-4
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Sat Apr 30 2011 Christian Krause <chkr@fedoraproject.org> - 2.10-3
- Rebuilt against mono 2.10.2

* Tue Apr 26 2011 Dan Horák <dan[at]danny.cz> - 2.10-2
- updated the supported arch list

* Tue Mar 29 2011 Christian Krause <chkr@fedoraproject.org> - 2.10-1
- Update to 2.10
- Disable GeckoHtmlRenderer
- Minor spec file cleanup

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Christian Krause <chkr@fedoraproject.org> - 2.8-4
- Don't build gtkhtml renderer since gtkhtml-sharp is not
  available anymore (BZ 660867).

* Wed Dec 22 2010 Paul <paul@all-the-johnsons.co.uk> - 2.8-3
- rebuilt

* Wed Dec 22 2010  Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.8-2
- Rebuild

* Sun Oct 03 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.8-1
- Bump to 2.8 preview 8
- Remove BR mono-jscript

* Wed Jun 23 2010 Christian Krause <chkr@fedoraproject.org> - 2.6.2-1
- Bump to the 2.6.2 release
- Cleanup spec file

* Wed Dec 23 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.6.1-1
- Bump to the 2.6.1 release
- Removed webkit patch

* Thu Nov 26 2009 Christian Krause <chkr@fedoraproject.org> - 2.6-3
- Fix monodoc crash when using WebKit html renderer (BZ 538555)

* Thu Nov 26 2009 Christian Krause <chkr@fedoraproject.org> - 2.6-2
- Restore version 2.6
- Re-apply Dennis Gilmore's sparc64 changes

* Sun Oct 04 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6-1
- Bump to 2.6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Christian Krause <chkr@fedoraproject.org> - 2.4.2-4
- Add version to requirement of gtkhtml-sharp to distinguish between
gtk-sharp and gnome-desktop-sharp

* Sat Jul 11 2009 Christian Krause <chkr@fedoraproject.org> - 2.4.2-3
- Add mono(webkit-sharp) as run-time requirement since it is needed by the
webkit engine of monodoc (BZ 478650)
- More minor spec file beautifications to fix rpmlint warnings

* Sat Jul 11 2009 Christian Krause <chkr@fedoraproject.org> - 2.4.2-2
- Add BR webkit-sharp-devel to build the webkit engine for monodoc (BZ 478650)
- Add mono(gtkhtml-sharp) as run-time requirement since it is needed by the
gtkhtml engine of monodoc (BZ 478650)
- Minor spec file beautification to fix some rpmlint warnings

* Tue Jun 09 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.4.2-1
- Bump to 2.4.2 preview 1
- Add support for ppc and ppc64

* Mon Apr 06 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.4-8.1
- remove ppc

* Thu Mar 26 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.4-8
- Full 2.4 release

* Wed Mar 18 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.4-7.RC3
- bump to RC3

* Thu Mar 12 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.4-6.RC2
- bump to RC2
- Add BR mono-web-devel

* Fri Feb 27 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.4-5.RC1
- bump to RC1
- Fix libdir problem for monodoc

* Fri Feb 20 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.4-4.20092002svn127416
- update from svn
- tagged as preview 3 release

* Tue Feb 10 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.4-3.20091002svn126075
- update from svn

* Mon Feb 02 2009  Paul F. Johnson <paul@all-the-johnsons.co.uk> -.2.4-3.20090202svn125131
- update from svn
- retagged for pre-release 1
- removed guicompare.dlls

* Sat Jan 24 2009  Paul F. Johnson <paul@all-the-johnsons.co.uk> -.2.4-2.20090124svn124416
- update from svn
- altered BRs and Rs to use mono-2.4

* Fri Jan 16 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.4-1.20091601svn123182
- Move to 2.4 svn branch

* Sun Jan 11 2009  Paul F. Johnson <paul@all-the-johnsons.co.uk> -.2.2-10.RC2.20090111svn122974
- update from svn
- bump to RC2

* Sun Jan 04 2009  Paul F. Johnson <paul@all-the-johnsons.co.uk> -.2.2-9.RC1.20090104svn122377
- update from svn

* Tue Dec 30 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> -.2.2-9.RC1.20081230svn122166
- update from svn

* Wed Dec 24 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> -.2.2-9.RC1.20081224svn122098
- Bump to RC1 svn branch

* Fri Dec 19 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.2-8.pre3.20081219svn121827
- Update from svn
- Re-enable ppc build

* Mon Dec 15 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.2-3.pre3.20081215svn121681
- Bump to preview 3
- Updated to svn

* Mon Dec 15 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.2-7.pre2.20081215svn121502
- Updated to svn

* Sat Dec 06 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.2-6.pre2
- Bump to preview 2
- use sed to remove the patches

* Sat Nov 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.2-5.pre1.1
- Dropped the last patch and sedded it instead

* Sat Nov 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.2-5.pre1
- More patches. Crumbs - why can't these guys just use $(libdir)?

* Sat Nov 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.2-4.pre1
- More patches

* Sat Nov 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.2-3.pre1
- actually apply the configure patch helps...

* Wed Nov 26 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.2-2.pre1
- added configure patch

* Thu Nov 20 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.2-1.pre1
- bump to 2.2 preview 1
- fix patch files
- branch off monodoc documentation

* Fri Oct 03 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.0-7
- bump to rc3

* Wed Oct 01 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.0-6
- bump to rc3

* Tue Sep 09 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.0-5
- bump to 2.0 RC 1
- spec file chanages

* Fri Aug 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.0-4
- additional BRs included

* Thu Aug 28 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0-3
- include unowned directories

* Fri Aug 15 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-2
- reworked the patchfiles
- removed monodir (not used)
- spec file fix

* Sun Aug 03 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-1
- bump to 2.0 preview 1
- spec file fixes

* Tue Jul 08 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-4
- added br gnome-desktop-sharp
- fix for archs

* Mon Jul 07 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-3.1
- rebuild

* Tue Jun 03 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-3
- added BR desktop-file-utils

* Tue May 06 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-2.1
- rebuild

* Wed Apr 30 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-2
- added hunspell-devel

* Mon Apr 21 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-1
- bump

* Mon Jan 14 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-3
- spec file fixes
- excludearch ppc64

* Fri Jan 04 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-2
- license fix

* Fri Jan 04 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-1
- bump
- spec file fixes
- removed support for under FC7

* Fri Feb 23 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.3-2
- fix for mock

* Thu Feb 15 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.3-1
- bump
- a couple of small spec file fixes
- disabled installing the gnunit apps as theyre broken currently

* Sun Jan 28 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.1-4
- added gettext-devel for findlangs to work

* Thu Jan 18 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.1-3
- added gecko-sharp2-devel and gnome-sharp-devel 

* Fri Dec 01 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.1-2
- various spec file changes
- rename spec and package to be mono-tools

* Sat Nov 25 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.1-1
- bump
- added addition files and devel subpackage

* Sat Oct 14 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.17-1
- bump

* Thu Sep 07 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.11-1
- Initial import, debug and the likes

