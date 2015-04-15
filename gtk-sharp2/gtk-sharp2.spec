Name:           gtk-sharp2
Version:        2.12.11
Release:        12%{?dist}
Summary:        GTK+ and GNOME bindings for Mono

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.mono-project.com/GtkSharp
Source0:        http://origin-download.mono-project.com/sources/gtk-sharp212/gtk-sharp-%{version}.tar.bz2
Patch1:         gtk-sharp2-2.12.11-glib-include.patch

BuildRequires:  mono-devel gtk2-devel libglade2-devel monodoc
BuildRequires:  automake, libtool

# Mono only available on these:
ExclusiveArch: %ix86 x86_64 ppc %{power64} ia64 %{arm} sparcv9 alpha s390x

%description
This package provides a library that allows you to build
fully native graphical GNOME applications using Mono. Gtk#
is a binding to GTK+, the cross platform user interface
toolkit used in GNOME. It includes bindings for Gtk, Atk,
Pango, Gdk. 

%package gapi
Group:        Development/Languages
Summary:      Glib and GObject C source parser and C generator for the creation and maintenance of managed bindings for Mono and .NET
Requires:     perl-XML-LibXML-Common perl-XML-LibXML perl-XML-SAX

%description gapi
This package provides developer tools for the creation and
maintenance of managed bindings to native libraries which utilize
glib and GObject. Some examples of libraries currently bound using
the GAPI tools and found in Gtk# include Gtk, Atk, Pango, Gdk.

%package devel
Summary:      Files needed for developing with gtk-sharp2
Group:        Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package provides the necessary development libraries and headers
for writing gtk-sharp2 applications.

%package doc
Group:        Documentation
Summary:      Gtk# documentation
Requires:     %{name} = %{version}-%{release}
Requires:     monodoc

%description doc
This package provides the Gtk# documentation for monodoc.

%prep
%setup -q -n gtk-sharp-%{version}
%patch1 -p1 -b .glib-include

# Fix permissions of source files
find -name '*.c' -exec chmod a-x {} \;

%build
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
%configure
make

%install
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
make install DESTDIR=$RPM_BUILD_ROOT

#Remove libtool archive
%{__rm} $RPM_BUILD_ROOT%{_prefix}/%{_lib}/*.*a

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README
%{_libdir}/*.so
%dir %{_prefix}/lib/gtk-sharp-2.0
%{_prefix}/lib/mono/gac
%{_prefix}/lib/mono/gtk-sharp-2.0

%files gapi
%defattr(-,root,root,-)
%{_bindir}/gapi2-codegen
%{_bindir}/gapi2-fixup
%{_bindir}/gapi2-parser
%{_prefix}/lib/gtk-sharp-2.0/gapi_codegen.exe
%{_prefix}/lib/gtk-sharp-2.0/gapi-fixup.exe
%{_prefix}/lib/gtk-sharp-2.0/gapi-parser.exe
%{_prefix}/lib/gtk-sharp-2.0/gapi_pp.pl
%{_prefix}/lib/gtk-sharp-2.0/gapi2xml.pl
%{_datadir}/gapi-2.0
%{_libdir}/pkgconfig/gapi-2.0.pc

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*-sharp-2.0.pc
%{_libdir}/pkgconfig/gtk-dotnet-2.0.pc

%files doc
%defattr(-,root,root,-)
%{_prefix}/lib/monodoc/sources/*

%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Brent Baude <baude@us.ibm.com> - 2.12.11-10
- Changing ppc64 to power64 macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.12.11-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.12.11-4
- Rebuild for new libpng

* Sun Oct 23 2011 Christian Krause <chkr@fedoraproject.org> - 2.12.11-3
- Fix glib include

* Sun Oct 23 2011 Christian Krause <chkr@fedoraproject.org> - 2.12.11-2
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Sun Sep 04 2011 Christian Krause <chkr@fedoraproject.org> - 2.12.11-1
- Update to new upstream version

* Wed Jun 01 2011 Paul Whalen <paul.whalen@senecac.on.ca> - 2.12.10-8
- Updated to arm macro in ExclusiveArch

* Mon Mar 28 2011 Christian Krause <chkr@fedoraproject.org> - 2.12.10-7
- Minor spec file cleanup
- Rebuilt against mono 2.10

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Dan Horák <dan[at]danny.cz> - 2.12.10-5
- sync ExclusiveArch list with mono

* Thu Oct 28 2010 Christian Krause <chkr@fedoraproject.org> - 2.12.10-4
- Rebuild again to create correct requires/provides capabilities

* Sat Oct 09 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.12.10-4
- Rebuild for new mono
- Alter exported CAIRO_LIB to 2.0

* Mon Apr 05 2010 Christian Krause <chkr@fedoraproject.org> - 2.12.10-3
- Add missing BR monodoc

* Mon Apr 05 2010 Christian Krause <chkr@fedoraproject.org> - 2.12.10-2
- Fix monodoc integration (#550144)

* Fri Apr 02 2010 Christian Krause <chkr@fedoraproject.org> - 2.12.10-1
- Update to new upstream version
- Minor spec file cleanup

* Wed Sep 09 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.12.9-1
- Bump to newer version
- Fixed doc patch
- Spec file cleanup

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Xavier lamien <laxathom@fedoraproject.org> - 2.12.7-5
- Build ppc64.

* Tue May 12 2009 Karsten Hopp <karsten@redhat.com> 2.12.7-4.1
- mono is available on s390(x)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Dennis Gilmore <dennis@ausil.us> - 2.12.7-3
- build 32 bit sparc sparcv9

* Sat Dec 20 2008 Xavier lamien <lxtnow[at]gmail.com> - 2.12.7-2
- Rebuild.

* Fri Dec 12 2008 Xavier lamien <lxtnow[at]gmail.com> - 2.12.7-1
- Update release.

* Mon Dec 8 2008 Matthias Clasen <mclasen@redhat.com> - 2.12.5-2
- Rebuild to fix pkg-config autoprovides

* Sat Nov 08 2008 Xavier Lamien <lxtnow[at]gmail.com> - 2.12.5-1
- Update release.

* Wed Oct 22 2008 Xavier Lamien <lxtnow[at]gmail.com> - 2.12.4-1
- Update release.

* Thu Sep 18 2008 Nigel Jones <dev@nigelj.com> - 2.12.3-1
- New minor release (.3)

* Mon Jul 14 2008 Xavier Lamien <lxtnow[at]gmail.com> - 2.12.1-3
- Fix/Update libdir on GACUTIL & monodoc.

* Mon Jul 14 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 2.12.1-2
- Rebuild for fixed RPM for mono provides.

* Sun Jul 13 2008 Xavier Lamien <lxtnow[at]gmail.com> - 2.12.1-1
- Update release.

* Sat May 31 2008 Xavier Lamien <lxtnow[at]gmail.com> - 2.12.0-2
- Fixed monodoc libdir.

* Fri May 23 2008 Xavier Lamien <lxtnow[at]gmail.com> - 2.12.0-1
- Updated Release.

* Mon Mar 03 2008 Xavier Lamien <lxtnow[at]gmail.com> - 2.10.3-2
- Fixed Assembly_dir on Rawhide (bug #434286).

* Wed Feb 27 2008 Xavier Lamien <lxtnow[at]gmail.com> - 2.10.3-1
- Updated Release.
- Updated -libdir.patch against new release.

* Tue Jan 01 2008 Xavier Lamien <lxtnow[at]gmail.com> - 2.10.2-1
- Updated Release.
- Fixed lisence tag.
- Fixed source0 path.

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.10.0-6
- Rebuild for selinux ppc32 issue.

* Thu Jul 26 2007 Matthias Clasen  <mclasen@redhat.com> - 2.10.4-5
- Add alpha to ExclusiveArch (#246206)

* Tue Apr 17 2007 Alexander Larsson <alexl@redhat.com> 2.10.0-4
- Rebuild (#236295)

* Tue Sep 12 2006 Alexander Larsson <alexl@redhat.com> - 2.10.0-3
- Add -doc subpackage with the monodoc docs (#205561)

* Mon Sep 11 2006 Alexander Larsson <alexl@redhat.com> - 2.10.0-2
- Fix pc files for gapidir (#205979)

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.10.0-1.fc6
- Update to 2.10.0

* Fri Aug 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.0-2.fc6
- Fix pkgconfig requires

* Mon Aug 14 2006 Alexander Larsson <alexl@redhat.com> - 2.9.0-1
- update to 2.9.0, which splits out gnome stuff to gnome-sharp
- Split out devel package

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Jun  9 2006 Alexander Larsson <alexl@redhat.com> - 2.8.2-2
- Disable on s390* as mono doesn't build on s390 atm

* Fri Mar  3 2006 Christopher Aillon <caillon@redhat.com> - 2.8.2-1
- Update to 2.8.2 to fix an issue with marshalling on x86-64

* Fri Feb 10 2006 Christopher Aillon <caillon@redhat.com> - 2.8.1-1
- Update to 2.8.1

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.8.0-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Christopher Aillon <caillon@redhat.com> 2.8.0-1
- Update to 2.8.0

* Thu Jan 19 2006 Alexander Larsson <alexl@redhat.com> 2.4.0-3
- Mono now builds on s390x

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> - 2.4.0-2
- Fix vte build

* Tue Nov 15 2005 Alexander Larsson <alexl@redhat.com> - 2.4.0-1
- Initial version
