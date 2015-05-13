#
# spec file for package log4net (Version 1.2.13)
#
# Please submit bugfixes or comments via http://bugzilla.redhat.com

Name:	 	log4net
BuildRequires:	mono-data-sqlite
BuildRequires:	mono-devel
BuildRequires:	unzip
BuildRequires:	nant
URL:		http://logging.apache.org/log4net/
License:	ASL 2.0
Group:		System Environment/Libraries
Version:	1.2.13
Release:	3%{?dist}
Summary:	A .NET framework for logging
Source:		http://mirror.reverse.net/pub/apache/logging/log4net/source/log4net-1.2.13-src.zip
Patch0:		log4net-1.2.13-mono-2.0.patch
# Mono only available on these:
ExclusiveArch: %ix86 x86_64 %{power64} ia64 sparcv9 alpha s390x
# Someone needs to build nant for %{arm}

# %define debug_package %{nil}
# This is a mono package

%description
log4net is a tool to help the programmer output log statements to a
variety of output targets. log4net is a port of the excellent log4j
framework to the .NET runtime

%package devel
Summary:	A .NET framework for logging
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
log4net is a tool to help the programmer output log statements to a
variety of output targets. log4net is a port of the excellent log4j
framework to the .NET runtime

%prep
%setup -q
%patch0 -p1 -b .mono-2.0
%{__sed} -i 's/\r//' NOTICE
%{__sed} -i 's/\r//' README.txt
%{__sed} -i 's/\r//' LICENSE
# Remove prebuilt dll files
rm -rf bin/

%build
# Use system mono.snk key
rm -rf log4net.snk
ln -s /etc/pki/mono/mono.snk log4net.snk
# ASF recommend using nant to build log4net
nant -buildfile:log4net.build compile-all

%install
%{__rm} -rf $RPM_BUILD_ROOT

# install pkgconfig file
cat > %{name}.pc <<EOF
Name: log4net
Description: log4net - .Net logging framework
Version: %{version}
Libs: -r:%{_prefix}/lib/mono/log4net/log4net.dll
EOF

%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
cp %{name}.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
%{__mkdir_p} $RPM_BUILD_ROOT/%{_prefix}/lib/mono/gac/
echo $PWD
gacutil -i bin/mono/2.0/release/log4net.dll -f -package log4net -root ${RPM_BUILD_ROOT}/%{_prefix}/lib

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_prefix}/lib/mono/gac/log4net
%{_prefix}/lib/mono/log4net
%doc LICENSE NOTICE README.txt

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/log4net.pc


%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun  2 2014 Tom Callaway <spot@fedoraproject.org> - 1.2.13-1
- update to 1.2.13

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 20 2011 Christian Krause <chkr@fedoraproject.org> - 1.2.10-17
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Tue Apr 19 2011 Dan Horák <dan[at]danny.cz> - 1.2.10-16
- updated the supported arch list

* Fri Apr 08 2011 Kalev Lember <kalev@smartlink.ee> - 1.2.10-15
- Fixed build with mono 2.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 30 2010 Dan Horák <dan[at]danny.cz> - 1.2.10-13
- bump NVR

* Tue Dec  1 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2.10-10
- use system mono.snk key instead of generating our own on each build

* Sun Nov 29 2009 Christopher Brown <snecklifter@gmail.com> - 1.2.10-9
- Fix pkg-config file location

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 1.2.10-8
- Exclude sparc64  no mono

* Thu Jul 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2.10-7
- rebuild to get nant cooking again

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Apr 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2.10-4
- excludearch ppc (nant doesn't work on ppc)
- delete bundled binary bits

* Mon Feb 25 2008 Christopher Brown <snecklifter@gmail.com> - 1.2.10-3
- Bump for upgrade path now nant is in rawhide

* Wed Feb 20 2008 Christopher Brown <snecklifter@gmail.com> - 1.2.10-1
- Add excludearch for ppc64
- File ownership cleanup

* Fri Sep  7 2007 Christopher Brown <snecklifter@gmail.com> - 1.2.10-1
- switch to nant for build

* Mon Sep  3 2007 Christopher Brown <snecklifter@gmail.com> - 1.2.9-70.1
- initial cleanup for Fedora

* Thu Mar 29 2007 rguenther@suse.de
- add unzip BuildRequires
* Mon May 22 2006 jhargadon@novell.com
- fix for bug 148685 This was a remotely triggerable vulnerability
  issue where the syslog() function from glibc was used incorrectly.
* Wed Apr 26 2006 wberrier@suse.de
- Change to noarch package, remove unnecessary deps
* Sat Feb 25 2006 aj@suse.de
- Do not build as root
- Reduce BuildRequires.
* Tue Feb  7 2006 ro@suse.de
- drop self obsoletes
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jan 12 2006 ro@suse.de
- modified neededforbuild (use mono-devel-packages)
* Mon Nov 28 2005 cgaisford@novell.com
- Initial package creation
