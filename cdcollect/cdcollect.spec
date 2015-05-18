%global debug_package %{nil}

%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif

Name:		cdcollect
Version:	0.6.0
Release:	22%{?dist}
Summary:	Simple CD/DVD catalog for GNOME

Group:		Applications/Productivity
License:	GPLv2+
URL:		http://cdcollect.sourceforge.net
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:		cdcollect-libdir.patch
Patch1:		cdcollect-0.6.0.patch
Patch2:		cdcollect-0.6.0-sqlite.patch

BuildRequires:	mono-devel >= 1.1.17, gtk-sharp2-devel >= 2.8.0, gnome-sharp-devel
BuildRequires:	glib2-devel, sqlite-devel >= 3.3.5, mono-data-sqlite, gettext
BuildRequires:	perl(XML::Parser), desktop-file-utils

Requires:	mono-core >= 1.1.17, gtk-sharp2 >= 2.8.0, gnome-sharp
Requires:	sqlite >= 3.3.5, mono-data-sqlite

Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):GConf2

ExclusiveArch: %{mono_arches}

%description
CDCollect is a simple CD/DVD catalog for GNOME written in C# using Mono
and GTK#. All data are stored in a sqlite database.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .sqlite

%build
%configure --disable-schemas-install
make %{?_smp_mflags}

%install
%make_install

desktop-file-install --remove-category="Application" \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	$RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%pre
if [ "$1" -gt 1 ]; then
	export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
	gconftool-2 --makefile-uninstall-rule \
		%{_sysconfdir}/gconf/schemas/%{name}.schemas >/dev/null || :
fi

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
	%{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :

%preun
if [ "$1" -eq 0 ]; then
	export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
	gconftool-2 --makefile-uninstall-rule \
		%{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
fi


%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog README TODO 
%config(noreplace) %{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
* Mon May 18 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 0.6.0-22
- Rebuild for mono 4
- Use mono macros

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 01 2013 Dan Horák <dan[at]danny.cz> - 0.6.0-18
- rebuild for aarch64 (#925136)

* Fri Feb 15 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.0-17
- disable debuginfo generation since this is a mono app

* Thu Feb 14 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.0-16
- remove vendor tag from desktop file. https://fedorahosted.org/fpc/ticket/247
- clean up spec to follow current guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan  1 2011 Dan Horák <dan[at]danny.cz> 0.6.0-11
- updated the supported arch list
- switch to Mono.Data.Sqlite bindings

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 0.6.0-10
- ExcludeArch sparc64  no mono there

* Wed Sep 23 2009 Dan Horak <dan[at]danny.cz> 0.6.0-9
- drop ExcludeArch for ppc64

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.6.0-6
- rebuild for new gnome-sharp

* Thu Feb 14 2008 Dan Horak <dan[at]danny.cz> 0.6.0-5
- rebuild for gcc 4.3

* Wed Sep 26 2007 Dan Horak <dan[at]danny.cz> 0.6.0-4
- set ExcludeArch: ppc64 as Mono doesn't exist there

* Wed Sep 26 2007 Dan Horak <dan[at]danny.cz> 0.6.0-3
- fixed URLs
- removed unneeded BR: pkgconfig

* Mon Sep 24 2007 Dan Horak <dan[at]danny.cz> 0.6.0-2
- update license tag
- fix desktop file installation

* Tue Jul 17 2007 Dan Horak <dan[at]danny.cz> 0.6.0-1
- initial version
