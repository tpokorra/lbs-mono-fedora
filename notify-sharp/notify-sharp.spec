%define svndate 20100411
%define debug_package %{nil}
%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif

Name:           notify-sharp
Version:        0.4.0
Release:        0.25.%{svndate}svn%{?dist}
Summary:        A C# implementation for Desktop Notifications

Group:          System Environment/Libraries
License:        MIT
URL:            http://trac.galago-project.org/wiki/DesktopNotifications
#svn checkout, revision 3032. To reproduce tarball:
#svn co -r 3032  http://svn.galago-project.org/trunk/notify-sharp notify-sharp-20100411 && tar -cvjf notify-sharp-20100411.tar.bz2 notify-sharp-20100411
Source0:        %{name}-%{svndate}.tar.bz2
#use dbus-sharp instead of deprecated ndesk-dbus
#patch is a modifed version of https://build.opensuse.org/package/view_file?file=notify-sharp-use-dbus-sharp.patch&package=notify-sharp&project=Mono%3ACleanup
Patch0:         notify-sharp-0.4.0-use-dbus-sharp.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mono-devel, gtk-sharp2-devel, gnome-sharp-devel, dbus-sharp-glib-devel
BuildRequires:  autoconf, automake, libtool

BuildRequires:  monodoc-devel
# Mono only available on these:
ExclusiveArch: %{mono_arches}

%description
notify-sharp is a C# client implementation for Desktop Notifications,
i.e. notification-daemon. It is inspired by the libnotify API.

Desktop Notifications provide a standard way of doing passive pop-up
notifications on the Linux desktop. These are designed to notify the
user of something without interrupting their work with a dialog box
that they must close. Passive popups can automatically disappear after
a short period of time.

%package devel
Summary:        Development files for notify-sharp
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development files for notify-sharp

%package doc
Summary:        Documentation files for notify-sharp
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
Requires:       monodoc

%description doc
Documentation files for notify-sharp

%prep
%setup -qn %{name}-%{svndate}
%patch0 -p1 -b .use_dbus_sharp

%build
sed -i "s#gmcs#mcs#g" configure.ac
autoreconf --install
%configure --libdir=%{_prefix}/lib
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig/*.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING NEWS README AUTHORS
%{_prefix}/lib/mono/gac/notify-sharp/
%{_prefix}/lib/mono/notify-sharp/

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/notify-sharp.pc

%files doc
%defattr(-,root,root,-)
%{_prefix}/lib/monodoc/sources/*

%changelog
* Mon Apr 20 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 0.4.0-0.25.20100411svn
- Define mono_arches for epel6

* Mon Apr 20 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 0.4.0-0.24.20100411svn
- Build for mono 4

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-0.23.20100411svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-0.22.20100411svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-0.21.20100411svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-0.20.20100411svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-0.19.20100411svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Christian Krause <chkr@fedoraproject.org> - 0.4.0-0.18.20100411svn
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)
- Use dbus-sharp instead of deprecated ndesk-dbus

* Wed May 09 2012 Karsten Hopp <karsten@redhat.com> 0.4.0-0.17.20100411svn
- fix PPC filelist

* Wed May 02 2012 Dennis Gilmore <dennis@ausil.us> - 0.4.0-0.16.20100411svn
- make the location for docs match whats in the mono package
- use the mono_arches macro for ExclusiveArch

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-0.15.20100411svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-0.14.20100411svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 07 2011 Dan Horák <dan[at]danny.cz> - 0.4.0-0.13.20100411svn
- updated the supported arch list

* Thu Oct 28 2010 Christian Krause <chkr@fedoraproject.org> - 0.4.0-0.12.20100411svn
- Rebuilt against Mono 2.8

* Sun Apr 11 2010 Christian Krause <chkr@fedoraproject.org> - 0.4.0-0.11.20100411svn
- Update to latest snapshot
- Fix minor directory ownership issue (BZ 512564)

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 0.4.0-0.10.20080912svn
- Switch to ExcludeArch sparc64 has no mono

* Thu Aug 20 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.4.0-0.9.20080912svn.1
- Rebuild to pick up ppc64 builds

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-0.8.20080912svn.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Karsten Hopp <karsten@redhat.com> 0.4.0-0.7.20080912svn.1
- mono is available on s390x

* Fri May 29 2009 Xavier Lamien <laxathom@fedoraproject.org> - 0.4.0-0.7.20080912svn
- Build arch ppc64.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-0.6.20080912svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 9 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org - 0.4.0-0.5.20080912svn
- Fix doc package dependencies.

* Wed Sep 24 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org - 0.4.0-0.4.20080912svn
- Replace with simple sed line in spec
- Build documentation, add monodoc dependencies.

* Wed Sep 24 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org - 0.4.0-0.3.20080912svn
- Add patch to fix libdir on all arches.

* Mon Sep 22 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org - 0.4.0-0.2.20080912svn
- Update changelog
- Fix whitespace issues

* Fri Sep 12 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org - 0.4.0-0.1.20080912svn
- Redid svn checkout and tarball creation process
- Added autoreconfig shebang + autotools deps

* Sat May 31 2008 Nigel Jones <dev@nigelj.com> - 0.4.0-0.1.20080531svn
- Initial RPM based on David Nielsen's work on fedorapeople.org
