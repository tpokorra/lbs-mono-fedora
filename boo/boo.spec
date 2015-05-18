%define debug_package %{nil}
%if 0%{?rhel}%{?el7}
# see https://fedorahosted.org/fpc/ticket/395
%global _monodir %{_prefix}/lib/mono
%global _monogacdir %{_monodir}/gac
%endif

Summary: An OO statically typed language for CLI
Name: boo
Version: 0.9.4.9
Release: 12%{?dist}
License: MIT
Group: Development/Languages
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://boo.codehaus.org
Source0: http://dist.codehaus.org/boo/distributions/%{name}-%{version}-src.tar.bz2
Patch0: boo-pkgconfig_path_fix.patch
Patch1: boo-gtksourceview.patch
Patch2: boo-removeprebuild.patch
BuildRequires: mono-devel, gtksourceview2-devel, shared-mime-info, pkgconfig, nant
# Mono only available on these:
ExclusiveArch: %mono_arches
# Nant needs to be built for %%{arm}

%description
Boo is a new object oriented statically typed programming language for the 
Common Language Infrastructure with a python inspired syntax and a special 
focus on language and compiler extensibility.

%package devel
Summary: Development files for boo
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files for boo

%prep
%setup -q
%patch0 -p1 -b .pc-original
%patch1 -p1 -b .sourceview
%patch2 -p1

# Get rid of prebuilt dll files
rm -rf bin/*.dll bin/pt/*.dll

%build
nant -D:install.prefix=%{_prefix} -D:install.libdir=%{_monodir}

%install
rm -rf %{buildroot}
nant -f:default.build install -D:install.buildroot=%{buildroot} -D:install.prefix=%{buildroot}%{_prefix} -D:install.share=%{buildroot}%{_datadir} -D:install.libdir=%{buildroot}%{_monodir} -D:install.bindir=%{buildroot}%{_bindir} -D:fakeroot.sharedmime=%{buildroot}%{_datadir}/.. -D:fakeroot.gsv=%{buildroot}%{_prefix}

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%clean
rm -rf %{buildroot}

%post
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi

%posttrans
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files 
%defattr(-,root,root,-)
%doc license.txt notice.txt readme.txt docs/BooManifesto.sxw
%{_monodir}/boo*/
%exclude %{_monodir}/Boo.NAnt.Tasks.dll
%dir %{_monodir}/boo
%{_monodir}/boo/*.dll
%{_monogacdir}/Boo*/
%{_bindir}/boo*
%exclude %{_datadir}/gtksourceview-1.0/language-specs/boo.lang
%{_datadir}/mime/packages/boo*
%{_datadir}/mime-info/boo*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/boo.pc
%{_monodir}/boo/Boo.NAnt.Tasks.dll

%changelog
* Mon May 18 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 0.9.4.9-12
- Rebuild for mono 4
- Use mono macros

* Mon Sep 08 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.4.9-11
- update mime scriptlet

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 08 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 0.9.4.9-9
- Remove %%arm from ExclusiveArch for lack of nant (#1106011)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Christian Krause <chkr@fedoraproject.org> - 0.9.4.9-3
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Tue Apr 19 2011 Dan Horák <dan[at]danny.cz> - 0.9.4.9-2
- updated the supported arch list

* Fri Feb 18 2011 Paul Lange <palango@gmx.de> - 0.9.4.9-1
- update to 0.9.4

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3.3457-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 14 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.9.3.3457-1
- Update to newest version
- Alter BR nant to BR nant-devel

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 0.9.2.3383-3
- ExcludeArch sparc64

* Tue Oct 06 2009 Paul Lange <palango@gmx.de> - 0.9.2.3383-2
- Move Boo.NAnt.Tasks.dll to boo-devel

* Wed Sep 16 2009 Paul Lange <palango@gmx.de> - 0.9.2.3383-1
- Update to boo 0.9.2
- remove libdir patch

* Fri Aug 28 2009 Paul Lange <palango@gmx.de> - 0.9.1.3287-3
- Fix executable paths

* Thu Aug 27 2009 Michel Salim <salimma@fedoraproject.org> - 0.9.1.3287-2
- Fix libdir in boo.pc to use %{_libdir}
- Summary no longer repeats package name

* Sun Aug 02 2009 Paul Lange <palango@gmx.de> - 0.9.1.3287-1
- Update to boo 0.9.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1.2865-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.8.1.2865-7
- Include missing directory entries (#473630).

* Mon Apr 20 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0.8.1.2865-6
- Fix FTBFS: added boo-mono.patch

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1.2865-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Apr 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.1.2865-4
- get rid of prebuilt binary files

* Tue Mar  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.8.1.2865-3
- Rebuild for new nant (causes broken deps)

* Sat Feb 23 2008 David Nielsen <gnomeuser@gmail.com> - 0.8.1-2865-2
- Nope, ppc still broken (#434631)

* Sat Feb 23 2008 David Nielsen <gnomeuser@gmail.com> - 0.8.1-2865-1
- Bump to 0.8.1
- Exclude Visual Studio Environment buildtarget
- Reenable ppc

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.8.0.2730-9
- Autorebuild for GCC 4.3

* Thu Jan 03 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.8.0-2730-7
- spec fix

* Wed Dec 19 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.8.0-2730-6
- remove ppc build
- fix libdir problem for pc file

* Sun Dec 16 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.8.0-2730-5
- reenable ppc

* Thu Nov 22 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.8.0-2730-4
- fixes to patches for corrected libdirs

* Sat Nov 17 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.8.0-2730-3
- Added exclusivearch

* Sun Nov 11 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.8.0-2730-2
- large bump
- removed fc5 and fc6 bit6
- removed MS update builds from default build
- fixed problem with the boo.pc file

* Sun Feb 18 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6-2237-13
- fix for correct libdir in bin scripts

* Wed Dec 20 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6-2237-11
- fix for correct libdir

* Thu Sep 14 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6.2237-9
- rebuild

* Mon Aug 07 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6.2237-8
- adds conditional for boo.lang - not required in FC6

* Wed Jul 26 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6.2237-7
- claims ownership of monodir-boo now

* Tue Jul 25 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6.2237-6
- replaced monodir for libdir in devel
- fixed tab-spaces problem
- removed rm rf from the prep step
- added update-mime-database

* Sun Jul 23 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6.2237-5
- removed nodebug
- removed redefine of libdir
- removed buildarch
- added BR nant

* Sat Jun 17 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6.2237-3
- removed exclusivearch
- changed BR
- removed R
- altered nant to /usr/bin/nant

* Thu Jun 08 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6.2237-1
- Spec file fixes
- Fix for gtksourceview-1.0 langspecs
- Added fixed libdir
- rebuild for mono 1.1.15

* Thu Jun 08 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.6.2237-1
- Bump to 0.7.6-2237
- Added R nant
- Multiple fixes to the install as it uses nant rather than make install
- Removed some bits from the files section as they're no longer in boo

* Wed May 31 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.5.2013-7
- Added devel files
- Added doc to files section instead of adding the files manually
- Added fix for x86_64

* Mon May 08 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.5.2013-6
- Altered again for mock and x86_64

* Fri Apr 28 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.5.2003-5
- added shared mime to satisfy mock

* Sat Apr 22 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.5.2003-4
- Removal of the always usr-lib, but now use the system used in f-spot
- include archs mono is available on
- added requires: mono-core, gtksourceview
- changed BR to include gtksourceview-sharp
- removes the conflict in the language-specs with gtksourceview package

* Tue Apr 18 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.5.2003-3
- Spec file tweaks
- libdir is now usr-lib irrespective of hardware built on
- Added docs to package

* Mon Apr 17 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.5.2003-2
- Small fix to the spec file

* Sat Apr 15 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7.5.2003-1
- Initial import and debug for FE (spec file based on the mono project one)
