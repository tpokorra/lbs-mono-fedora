%define debug_package %{nil}

Name:    taglib-sharp
Version: 2.0.3.7
Release: 12%{?dist}
Summary: Provides tag reading and writing for Banshee and other Mono apps

Group:   System Environment/Libraries
License: LGPLv2+
URL:     http://download.banshee-project.org/taglib-sharp/
Source0: http://download.banshee-project.org/taglib-sharp/%{version}/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Mono only available on these:
ExclusiveArch: %{mono_arches}

BuildRequires: mono-devel, monodoc-devel, gnome-sharp-devel

%description
TagLib# is a FREE and Open Source library for the .NET 2.0 and Mono frameworks 
which will let you tag your software with as much or as little detail as you 
like without slowing you down. It supports a large variety of movie and music 
formats which abstract away the work, handling all the different cases, so all 
you have to do is access file.Tag.Title, file.Tag.Lyrics, or my personal 
favorite file.Tag.Pictures. But don't think all this abstraction is gonna keep 
you from tagging's greatest gems. You can still get to a specific tag type's 
features with just a few lines of code. 

%package devel
Summary: Provides tag reading and writing for Banshee and other Mono apps
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Development files for taglib-sharp.

%prep
%setup -q

%build
# Docs are broken.
%configure --disable-docs
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p %{buildroot}%{_libdir}/pkgconfig
mv %{buildroot}%{_datadir}/pkgconfig/*.pc %{buildroot}%{_libdir}/pkgconfig/

%files
%defattr(-,root,root,-)
%doc COPYING
%{_prefix}/lib/mono/gac/*/
%{_prefix}/lib/mono/taglib-sharp/

%files devel
%defattr(-,root,root,-)
# %%doc %{_libdir}/monodoc/sources/taglib-sharp-docs*
%{_libdir}/pkgconfig/taglib-sharp.pc

%changelog
* Thu Nov 27 2014 Dan Horák <dan[at]danny.cz> - 2.0.3.7-12
- switch to mono_arches

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Brent Baude <baude@us.ibm.com> - 2.0.3.7-9
- Changing ppc64 arch to power64 macro

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 29 2011 Christian Krause <chkr@fedoraproject.org> - 2.0.3.7-4
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Mon Mar 21 2011 Dan Horák <dan[at]danny.cz> - 2.0.3.7-3
- updated the supported arch list

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar 24 2010 Christian Krause <chkr@fedoraproject.org> - 2.0.3.7-1
- Update to 2.0.3.7

* Sun Feb 28 2010 Christian Krause <chkr@fedoraproject.org> - 2.0.3.6-2
- Fix compilation on x86_64

* Sat Feb 27 2010 Christian Krause <chkr@fedoraproject.org> - 2.0.3.6-1
- Update to 2.0.3.6

* Thu Feb 18 2010 Karsten Hopp <karsten@redhat.com> 2.0.3.2-5.1
- enable s390, s390x where we have mono now

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 2.0.3.2-5
- switch sparc to sparcv9

* Thu Aug 20 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.3.2-4
- Build for ppc64

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Xavier Lamien <laxathom@fedoraproject.org> - 2.0.3.2-3
- Build arches ppc.

* Wed Feb 25 2009 David Nielsen <dnielsen@fedoraproject.org> - 2.0.3.2-2
- fix pkgconfig file

* Tue Feb 24 2009 David Nielsen <dnielsen@fedoraproject.org> - 2.0.3.2-1
- Update to 2.0.3.2
- The Banshee project has now taking over upstream responsibilities
- Remove patches
- Enable threaded build in accordance to Fedora guidelines

* Mon Feb 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.3.0-8
- disable doc generation

* Mon Nov 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.3.0-7
- apply mimetypes fix recommended by banshee upstream

* Thu Jun 5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.3.0-6
- fix docs generation

* Thu Jun 5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.3.0-5
- Rebuild against new mono bits

* Sat Apr 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.3.0-4
- don't need to specify pkgconfig as a BR, it gets pulled in

* Sat Apr 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.3.0-3
- BR: monodoc-devel

* Sat Apr 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.3.0-2
- just fix noInjectMenuItem

* Sat Apr 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.3.0-1
- initial package
