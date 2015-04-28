%global         debug_package %{nil}
%global         upstream_name libgoogle-data-mono

Name:           gdata-sharp
Version:        1.4.0.2
Release:        14%{?dist}
Summary:        .NET library for the Google Data API

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://code.google.com/p/google-gdata/
Source0:        http://google-gdata.googlecode.com/files/%{upstream_name}-%{version}.tar.gz
# fixed in SVN:
# http://code.google.com/p/google-gdata/source/detail?spec=svn933&r=890
Patch0:         %{upstream_name}-1.4.0.2-pkgconfig.patch

BuildRequires:  mono-devel mono-nunit
#Requires:       

# Mono only available on these:
ExclusiveArch: %mono_arches

%description
The Google Data APIs (GData) provide a simple protocol for reading and
writing data on the web.

Each of the following Google services provides a Google data API:

    * Base
    * Blogger
    * Calendar
    * Spreadsheets
    * Google Apps Provisioning
    * Code Search
    * Notebook
    * Picasa Web Albums
    * Document Feed
    * Contacts
    * You Tube
    * Google Health 

The GData .NET Client Library provides a library and source code that
make it easy to access data through Google Data APIs.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{upstream_name}-%{version}
%patch0 -p1 -b .pkgconfig

%build
make %{?_smp_mflags} PREFIX=%{_prefix}

%check
# currently 98 tests out of 921 fail
# make test


%install
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix}

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%files
%defattr(-,root,root,-)
%doc LICENSE-2.0.txt RELEASE_NOTES.HTML
%{_prefix}/lib/mono/GData-Sharp
%{_prefix}/lib/mono/gac/Google.GData.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/gdata-sharp-*.pc


%changelog
* Tue Mar 24 2015 Than Ngo <than@redhat.com> - 1.4.0.2-14
- use %%mono_arches

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Brent Baude <baude@us.ibm.com> - 1.4.0.2-11
- Replacing ppc64 with pwoer64 macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 29 2011 Christian Krause <chkr@fedoraproject.org> - 1.4.0.2-6
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Fri Feb 25 2011 Dan Horák <dan[at]danny.cz> - 1.4.0.2-5
- updated the supported arch list

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 23 2009 Michel Salim <salimma@fedoraproject.org> - 1.4.0.2-3
- Replace %%define with %%global 

* Thu Sep  3 2009 Michel Salim <salimma@fedoraproject.org> - 1.4.0.2-2
- Build against latest mono-nunit

* Fri Aug 21 2009 Michel Salim <salimma@fedoraproject.org> - 1.4.0.2-1
- Initial Fedora package

