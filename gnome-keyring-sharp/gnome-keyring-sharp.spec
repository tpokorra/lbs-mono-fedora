%if 0%{?rhel}%{?el6}%{?el7}
%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif
# see https://fedorahosted.org/fpc/ticket/395
%define _monodir %{_prefix}/lib/mono
%define _monogacdir %{_monodir}/gac
%endif

%global svn_rev 133722
%global debug_package %{nil}

Name:           gnome-keyring-sharp
Version:        1.0.1
Release:        0.19.%{svn_rev}svn%{?dist}
Summary:        Mono implementation of GNOME Keyring

Group:          System Environment/Libraries
License:        MIT
URL:            http://www.mono-project.com/Libraries#Gnome-KeyRing-Sharp
# Tarfile created from svn snapshot
# svn co -r %{svn-rev} \
#   svn://anonsvn.mono-project.com/source/trunk/gnome-keyring-sharp \
#   gnome-keyring-sharp-%{version}
# tar cjf gnome-keyring-sharp-%{version}-r%{svn_rev}.tar.bz2 --exclude=.svn \
#   gnome-keyring-sharp-%{version}
Source0:        gnome-keyring-sharp-%{version}-r%{svn_rev}.tar.bz2
# Patch to directly p/invoke libgnome-keyring instead of using
# deprecated socket interface taken from upstream bug report:
# https://bugzilla.novell.com/show_bug.cgi?id=589166
Patch1:         gnome-keyring-sharp-1.0.1-new-api.diff
Patch2:         gnome-keyring-sharp-1.0.1-monodoc-dir.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Mono only available on these:
ExclusiveArch:  %mono_arches

BuildRequires:  autoconf automake libtool
BuildRequires:  mono-devel ndesk-dbus-devel monodoc
BuildRequires:  gtk-sharp2-devel libgnome-keyring-devel

%description
gnome-keyring-sharp is a fully managed implementation of libgnome-keyring.

When the gnome-keyring-daemon is running, you can use this to retrive/store
confidential information such as passwords, notes or network services user
information.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files
for developing applications that use %{name}.

%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
Requires:       monodoc

%description    doc
The %{name}-doc package contains documentation
for %{name}.


%prep
%setup -q
%patch1 -p0 -F 2 -b .new-api
%patch2 -p1 -b .monodoc-dir
sed -i "s#gmcs#mcs#g" configure.ac

%build
autoreconf -f -i
%configure --disable-static
make
# sharing violation when doing parallel build
#%{?_smp_mflags}


%install
%make_install
strip $RPM_BUILD_ROOT%{_libdir}/libgnome-keyring-sharp-glue.so
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_monodir}/gnome-keyring-sharp-1.0
%{_monogacdir}/Gnome.Keyring
%{_libdir}/libgnome-keyring-sharp-glue.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}-1.0.pc

%files doc
%defattr(-,root,root,-)
%{_prefix}/lib/monodoc/sources/Gnome.Keyring.*


%changelog
* Tue May 12 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 1.0.1-0.19.133722svn
- Build for Mono 4
- Use mono macros

* Tue Mar 24 2015 Than Ngo <than@redhat.com> - 1.0.1-0.18.133722svn
- use %%mono_arches

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.17.133722svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.16.133722svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Brent Baude <baude@us.ibm.com> - 1.0.1-0.15.133722svn
- Changed ppc64 to power64 macro

* Sat May 24 2014 Brent Baude <baude@us.ibm.com>
- rebuilt

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.13.133722svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.12.133722svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.11.133722svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.10.133722svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 31 2011 Christian Krause <chkr@fedoraproject.org> - 1.0.1-0.9.133722svn
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Fri Feb 25 2011 Dan Horák <dan[at]danny.cz> - 1.0.1-0.8.133722svn
- updated the supported arch list

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.7.133722svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 27 2010 Christian Krause <chkr@fedoraproject.org> - 1.0.1-0.6.133722svn
- Add patch to directly p/invoke libgnome-keyring instead of using
  deprecated socket interface (BZ 595457)

* Thu Aug 20 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.1-0.5.133722svn%{?dist}
- Rebuild for ppc64 since previous build was obsoleted.

* Thu Aug 20 2009 Michel Salim <salimma@fedoraproject.org> - 1.0.1-0.4.133722svn%{?dist}
- Update to r133722
- Disable building on sparc64

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.3.115768svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 01 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.0.1-0.3.115768svn
- Build arch ppc64.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-0.2.115768svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 29 2009 Michel Salim <salimma@fedoraproject.org> - 1.0.1-0.1.115768svn%{?dist}
- Update to r115768

* Mon Jul 14 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.0.0-0.2.87622svn%{?dist}
- Disable creation of -debuginfo subpackage

* Sun Jul  6 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.0.0-0.1.87622svn%{?dist}
- Initial package
