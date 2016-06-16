%global debug_package %{nil}
%global monodir %{_prefix}/lib
%global bootstrap 1

Summary: NAnt is a build tool for Mono and .NET
Name: nant
Version: 0.92
Release: 2%{?dist}
Epoch: 1
Source0: http://downloads.sourceforge.net/nant/%{name}-%{version}-src.tar.gz
Patch1: nant-0.92-no_ndoc.patch
Patch2: nant-0.92-system_nunit.patch
Patch3: nant-0.90-no_sharpcvslib.patch
Patch4: nant-0.90-system_sharpziplib.patch
Patch5: nant-0.92-system_log4net.patch
Patch7: nant-fixmono42_scripttask.patch
License: GPLv2+
Group: Development/Tools
Url: http://nant.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: mono-devel
BuildRequires: mono-nunit-devel
%if 0%{bootstrap}
# Nothing here if we're bootstrapping
%else
BuildRequires: log4net-devel
%endif
# Mono only available on these:
ExclusiveArch: %ix86 x86_64 ppc %{power64} ia64 sparcv9 alpha s390x 

%if 0%{bootstrap}
# In bootstrap mode, filter requires of the prebuilt DLLs. Some of these
# require older mono runtime, creating broken rpm deps.
%filter_requires_in %{_prefix}/lib/NAnt/
# Also filter provides of the prebuilt DLLs
%filter_provides_in %{_prefix}/lib/NAnt/
%filter_setup
%endif

%description
NAnt is a free .NET build tool. In theory it is kind of like make
without make's wrinkles. In practice it's a lot like Ant.

%package docs
Summary:	Documentation package for nant
Group:	Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description docs
Documentation for nant

%package devel
Summary:	Development file for nant
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Development file for %{name}

%prep
%setup -q -n %{name}-%{version}

# install to libdir instead of datadir
sed -i -e "/property name=\"install\.share\"/ s/'share'/'lib'/" NAnt.build
sed -i -e "s,/share/,/lib/," etc/nant.pc.in

%if 0%{bootstrap}
# do nothing
%else

# Remove NDoc support
%patch1 -p1 -b .no_ndoc
rm src/NAnt.DotNet/Tasks/NDocTask.cs
find lib -name 'NDoc*.dll' | xargs rm

# Remove NUnit1 support and fix build with system NUnit.
# Based on Debian's 004-nant-nunit_2.4.dpatch
%patch2 -p1 -b .system_nunit
find lib -iname 'nunit*' | xargs rm
%endif

# Remove SharpCvsLib support
%patch3 -p1 -b .no_sharpcvslib
find lib -name "*SharpCvsLib*.dll" | xargs rm
find lib -name "scvs.exe" | xargs rm

# Use system SharpZipLib which is older than the one bundled with nant
# https://bugzilla.novell.com/show_bug.cgi?id=426065
%patch4 -p1 -F 3 -b .system_sharpziplib
find lib -name "*SharpZipLib*.dll" | xargs rm

find . -type d|xargs chmod 755
find . -type f|xargs chmod 644
sed -i 's/\r//' doc/license.html
sed -i 's/\r//' COPYING.txt
sed -i 's/\r//' README.txt
sed -i 's/\r//' doc/releasenotes.html

# Clean out the prebuilt files (unless we're bootstrapping)
# If we're not bootstrapping, leave the files alone:
%if 0%{bootstrap}
echo "BOOTSTRAP BUILD"
%else
echo "NORMAL BUILD, NUKING PREBUILT BUNDLED DLL FILES"
rm -rf lib/*
%endif

# Use system log4net, unless we're bootstrapping.
%if 0%{bootstrap}
# do nothing
%else
%patch5 -p1 -b .system_log4net
%endif

%patch7 -p1

#Fixes for Mono 4
sed -i "s#gmcs#mcs#g" Makefile
sed -i "s#TARGET=mono-2.0#TARGET=mono-4.0#g" Makefile
sed -i "s#mono/4.0#mono/4.5#g" src/NAnt.Console/App.config
sed -i "s#dmcs#mcs#g" src/NAnt.Console/App.config
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

%build
make

%install
rm -rf %{buildroot}
make install prefix=%{_prefix} DESTDIR=%{buildroot}
find examples -name \*.dll -o -name \*.exe|xargs rm -f
rm -rf %{buildroot}%{_datadir}/NAnt/doc
rm -rf %{buildroot}%{_prefix}/lib/doc/NAnt

# Flush out the binary bits that we used to build, unless we're bootstrapping.
%if 0%{bootstrap}
# Do nothing
%else
rm -rf %{buildroot}%{_prefix}/lib/NAnt/bin/lib
rm -rf %{buildroot}%{_prefix}/lib/NAnt/bin/log4net.dll
%endif

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.txt doc/*.html COPYING.txt
%{_bindir}/nant
%{monodir}/NAnt/

%files docs
%defattr(-,root,root,-)
%doc examples/* doc/help/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/nant.pc

%changelog
* Thu Jun 16 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> 0.92-2
- add a fix for scripttask, https://github.com/nant/nant/issues/161

* Fri May 15 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> 0.92-1
- upgrade to NAnt 0.92, build for Mono 4

* Tue Oct 14 2014 Karsten Hopp <karsten@redhat.com> 0.90-17
- change exclusivearch from ppc64 to power64 macro to include ppc64le

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.90-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun  9 2014 Tom Callaway <spot@fedoraproject.org> - 1:0.90-15
- rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.90-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 17 2014 Kalev Lember <kalevlember@gmail.com> - 1:0.90-13
- Drop scrollkeeper handling

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.90-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.90-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.90-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.90-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 20 2011 Christian Krause <chkr@fedoraproject.org> - 1:0.90-8
- Unbootstrap

* Sun Nov 20 2011 Christian Krause <chkr@fedoraproject.org> - 1:0.90-7
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Tue Apr 19 2011 Dan Horák <dan[at]danny.cz> - 1:0.90-6
- updated the supported arch list

* Sat Apr 09 2011 Kalev Lember <kalev@smartlink.ee> - 1:0.90-5
- Unbootstrap

* Fri Apr 08 2011 Kalev Lember <kalev@smartlink.ee> - 1:0.90-4
- Fixed build in bootstrap mode
- Added a patch to build without NDoc
- Added a patch to build with system mono-nunit instead of the bundled copy and
  removed support for mono-nunit22
- Build without SourceControl support to avoid SharpCvsLib dep
- Patch to build with system SharpZipLib
- Build with system log4net if we aren't bootstrapping

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.90-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 26 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1:0.90-2.1
- Fix bootstrap makefile

* Mon Oct 25 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1:0.90-2
- More build path fixes

* Mon Oct 25 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1:0.90-1.1
- Correct build paths

* Thu Oct 14 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1:0.90-1
- Bump to 0.90
- Replace patch 2, fix other patches
- Fix mono-1.0 bits
- Add devel subpackage

* Thu Feb 11 2010 Karsten Hopp <karsten@redhat.com> 1:0.85-34
- enable builds on s390(x)

* Tue Dec  1 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1:0.85-33
- disable bootstrap

* Tue Dec  1 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1:0.85-32.1
- bootstrap again

* Thu Oct 29 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.85-31
- rebuild because mono-ndoc "cleverly" encodes its build date into its ABI ver

* Fri Jul 31 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.85-30
- clarify comments on bootstrapping

* Thu Jul 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.85-29
- unbootstrap

* Thu Jul 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.85-28.1
- bootstrap to get mono-ndoc rebuilt

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.85-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar  3 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.85-27
- unbootstrap

* Mon Mar  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.85-26.2
- fix BR to be wrapped by bootstrap

* Mon Mar  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.85-26.1
- bootstrap... again. *sigh*

* Mon Mar  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.85-26
- disable bootstrap

* Mon Mar  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.85-25.1
- proper conditionals for bootstrapping

* Mon Mar  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.85-24.1
- bootstrap hack (to recover from mass rebuild)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.85-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.85-23
- undo bootstrapping hack
- readd BR mono-sharpcvslib-devel (yes, it is circular, mono is a mess)

* Tue Dec 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.85-22.1
- bootstrapping hack
- don't monkey with patches, bad form

* Thu Dec 18 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 1:0.85-22
- rebuild
- removed BR mono-sharpcvslib-devel (circular dep with mono-sharpcvslib)

* Fri Jun 06 2008 Caolán McNamara <caolanm@redhat.com> - 1:0.85-21
- rebuild for dependancies

* Thu Apr 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.85-20
- don't use prebuilt binary bits

* Mon Apr  7 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1:0.85-19
- Downgrade to 0.85 because of issues with boo package as discussed on
  bug #435898).  add Epoch: 1 :(
- Add nant-0.85-api.patch from David Nielsen to enable build on F-9

* Thu Mar 06 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.86-5
- bump to beta 1

* Mon Nov 12 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.85-17
- removed excludearch in favour of exclusivearch

* Mon Nov 12 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.85.15
- removed fc5 and fc6 support
- fixed small errors in the code base

* Sun Dec 17 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.85-11
- No longer the RC release

* Sat Sep 16 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.85-10
- more hacks and slashes...

* Sat Sep 16 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.85-9
- more 64bit fixes

* Sat Sep 16 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.85-8
- scrollkeeper fixes

* Wed Sep 06 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.85-7
- FC5 and FC6 fixes (libdir)

* Wed Jul 19 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.85-6
- Security fix to spec file
- Other spec file fixes

* Sun Jul 09 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.85-5
- fixes to EOLs
- added R scrollkeeper
- changed group

* Sat Jul 08 2006 John Mahowald  <jpmahowald@gmail.com> - 0.85-4
- libdir fix

* Wed Jun 07 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.85-rc4-3
- Added docs package
- Added post and postun for docs
- Removed debuginfo package (empty)

* Sat Jun 03 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.85-rc4-1
- Initial import for FC Extras

