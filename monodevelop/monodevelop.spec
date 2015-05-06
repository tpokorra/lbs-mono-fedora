%global debug_package %{nil}
%define tarballversion 5.9.0.431

Name:           monodevelop
Version:        5.9
Release:        1%{?dist}
Summary:        A full-featured IDE for Mono and Gtk#

Group:          Development/Tools
License:        GPLv2+
URL:            http://monodevelop.com/
Source0:        http://download.mono-project.com/sources/monodevelop/monodevelop-%{tarballversion}.tar.bz2
Patch0:         monodevelop-avoidgiterrors.patch
Patch1:         monodevelop-downgrade_to_mvc3.patch
Patch2:         monodevelop-nunit-unbundle.patch
BuildRequires:  mono-devel >= 4.0.0
BuildRequires:  mono-addins-devel >= 0.6
BuildRequires:  nunit-devel >= 2.6.3
BuildRequires:  nunit25-devel
BuildRequires:  monodoc-devel
BuildRequires:  gnome-desktop-sharp-devel
BuildRequires:  desktop-file-utils intltool
BuildRequires:  nuget dos2unix
Requires:       mono-core >= 3.0.4
Requires:       mono-addins >= 0.6
# Using system nunit, but dependency not automatically picked up by RPM
Requires:       mono(nunit.core)
Requires:       mono(nunit.framework)
Requires:       mono-locale-extras
Requires:       gnome-desktop-sharp
Requires:       subversion monodoc
Requires:       hicolor-icon-theme shared-mime-info
Requires:       gtk-sharp2-devel

# Mono only available on these:
ExclusiveArch: %ix86 x86_64 ppc ppc64 ia64 %{arm} sparcv9 alpha s390x

%description
This package provides MonoDevelop, a full-featured IDE for Mono with
syntax coloring, code completion, debugging, project management and
support for C sharp, Visual Basic.NET, Java, Boo, Nemerle and MSIL.


%package        devel
Summary:        Development files for monodevelop
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
 
%description devel
Development files for %{name}.


%prep
%setup -qn %{name}-%{version}

%patch0 -p1
%patch1 -p1
dos2unix external/nrefactory/ICSharpCode.NRefactory.Tests/ICSharpCode.NRefactory.Tests.csproj
%patch2 -p1

# Delete shipped *.dll files
find -name '*.dll' -exec rm -f {} \;

#Fixes for Mono 4
sed -i "s#gmcs#mcs#g" configure
sed -i "s#gmcs#mcs#g" configure.in
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

%build
%configure --enable-git --disable-update-mimedb --disable-update-desktopdb

make %{?_smp_mflags}

%check
make check

%install
%make_install

desktop-file-install \
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications \
                     --delete-original \
  $RPM_BUILD_ROOT%{_datadir}/applications/monodevelop.desktop

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/m*
%{_prefix}/lib/monodevelop
%{_mandir}/man1/m*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/mime/packages/monodevelop.xml

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/monodevelop*.pc

%changelog
* Mon May 04 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 5.9-1
- Update to 5.9

* Tue Apr 28 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 5.7.0.660-2
- require mono-locale-extras to avoid Encoding errors

* Tue Apr 14 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 5.7.0.660-1
- Build latest release 5.7

* Fri Jan 09 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 5.8-2
- Add mozroots intented fix nuget restore

* Thu Jan 08 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 5.8-1
- Update to 5.8 from jenkins

* Fri Oct 10 2014 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 5.5-1
- Update to 5.5.0.227

* Mon Jun 23 2014 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 5.0.1-1
- Update to 5.0.1

* Tue Jan 28 2014 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 4.2.2-1
- Update to 4.2.2

* Sat Aug 03 2013 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 4.2-1
- Update to upstream

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Christian Krause <chkr@fedoraproject.org> - 2.8.8.4-1
- Update to 2.8.8.4

* Wed Jan 04 2012 Christian Krause <chkr@fedoraproject.org> - 2.8.5-1
- Update to 2.8.5

* Tue Oct 25 2011 Christian Krause <chkr@fedoraproject.org> - 2.8.1-2
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Sun Oct 16 2011 Christian Krause <chkr@fedoraproject.org> - 2.8.1-1
- Update to 2.8.1

* Tue Sep 13 2011 Christian Krause <chkr@fedoraproject.org> - 2.6-2
- Obsolete deprecated plugins

* Sun Sep 11 2011 Christian Krause <chkr@fedoraproject.org> - 2.6-1
- Update to 2.6
- Drop upstreamed patches
- Update unbundle-nunit patch
- Delete shipped *.dll files in %%prep
- Add x86_64 build fix

* Wed May 04 2011 Christian Krause <chkr@fedoraproject.org> - 2.4.2-4
- fix startup issue with newer GTK+ (BZ #679373) by adding
  3 upstream patches

* Tue Apr 19 2011 Dan Horák <dan[at]danny.cz> - 2.4.2-3
- updated the supported arch list

* Mon Apr 04 2011 Christian Krause <chkr@fedoraproject.org> - 2.4.2-2
- Minor spec file cleanup
- Fix usage of scriptlets

* Wed Mar 30 2011 Christian Krause <chkr@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2
- Don't unbundle Mono.Cecil for now due to incompatible API changes

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jun 19 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-0
- Bump to 2.4 release

* Mon May 31 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.3.1-2
- Build against mono-addins-0.5

* Fri May 28 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.3.1-1
- Bump to 2.4 beta 2
- Fix mono.cecil patches - it's gone strange...

* Fri May 07 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.3-1
- Bump to 2.4 beta 1
- Updated rmcecildeps patch

* Sun Apr 18 2010 Christian Krause <chkr@fedoraproject.org> - 2.2.2-2
- Fix monodevelop and mdtool wrapper scripts for x86_64

* Fri Mar 19 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2.2-1
- Bump to 2.2.2 bug fix release

* Thu Feb 18 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2.1-2
- Fixes for 64 bit as MD likes setting paths internally (thanks Chris for the fix)
- Fixed my name in the changelog!

* Thu Feb 04 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2.1-1
- Bump to new 2.2.1 release

* Sat Dec 26 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-2
- Patch monodevelop.pc file for more monocecil fixes

* Tue Dec 22 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-1
- Bump to 2.2 release
- Fix unbundle-cecil patch
- Copy system mono-cecil to build/bin

* Mon Oct 19 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.1.1-1
- Bump to 2.2 beta 2

* Wed Sep 30 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.1.0-3
- Fix for lib64

* Mon Sep 21 2009 Michel Salim <salimma@fedoraproject.org> - 2.1.0-2
- Properly disable bundled Mono.Cecil and NUnit
- Readjust launcher script (bz #523695)
- Remove unnecessary dependencies
- Clean up spec file

* Wed Sep 09 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.1.0-1
- Bump to 2.2 beta 1
- Fixed cecil patch
- Drop desktop patch

* Tue Jun 23 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.0-3
- Fix mdtool libdir issue
- Add additional arcs

* Mon Apr 27 2009 Christopher Aillon <caillon@redhat.com> - 2.0-2
- Rebuild against newer gecko

* Thu Mar 26 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-1
- Full 2.0 release

* Tue Mar 10 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.3-1.beta2
- Move back to tarballs
- Bump to beta2

* Fri Feb 27 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.2-2.beta1.20092202svn127584
- Added desktop file patch

* Sun Feb 22 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.2-1.beta1.20092202svn127584
- Update from svn
- Fix the month on the changelog
- renamed use-system-cecil patch to removed-contrib

* Tue Feb 10 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.2-beta1.20091003svn126521
- Update from svn
- retagged as beta 1
- ensure being built against mono-2.4 and mono-addins-0.4

* Tue Feb 03 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.2-pre1.20090203svn125551
- Update from svn

* Thu Jan 29 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.2-pre1.20090129svn124664
- Update from svn

* Sat Jan 24 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.2-pre1.20090124svn124411
- Update from svn

* Fri Jan 16 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.2-pre1.20090116svn123651
- Update from svn
- Altered nunit patch

* Sat Jan 10 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.2-pre1.200900109svn122940
- Update from svn

* Sun Jan 04 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.2-pre1.200900104svn122336
- Update from svn
- Reversioned as 1.9.1 is out there already

* Tue Dec 30 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.1-7.pre1.20081230svn122192
- Update from svn

* Wed Dec 24 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.1-7.pre1.20081224svn122090
- Update from svn

* Fri Dec 19 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.1-7.pre1.20081219svn121787
- Update from svn

* Thu Dec 18 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.1-6.pre1.20081217svn121699
- Actually use the svn version!

* Wed Dec 17 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.1-5.pre1.20081217svn121653
- Update

* Tue Dec 16 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.1-4.pre1.20081216svn121578
- Update

* Sat Nov 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.1-3.pre1
- missed a libdir...

* Sat Nov 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.1-2.pre1
- remove libdir patch, now using sed

* Sun Nov 23 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.1-1.pre1
- Update to 1.9.1 preview 1
- Removed R mono-basic and vala

* Sat Oct 18 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-7
- Fix dependancies of R (BZ 467544)

* Tue Sep 09 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-6
- Added patch to build against 2.0 RC 1
- rebuild against 2.0 RC 1

* Mon Aug 25 2008 Michel Salim <salimma@fedoraproject.org> - 1.9-5
- Use system-provided nunit

* Sat Aug 23 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.9-4
- Clean up build dependencies: database support now a separate package
- Clean up spec file and patches

* Fri Aug 08 2008 David Nielsen <gnomeuser@gmail.com> - 1.9-3
- rebase configure patch for fuzz
- file list fix up

* Thu Jul 10 2008 David Nielsen <gnomeuser@gmail.com> 1.9-2
- numerical compare for fedora version test, fixes compile on f10

* Mon Jul 07 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-1
- bump to latest beta for md2
- fixes to patch files for mono.cecil
- fix the archs to be mono package happy
- spec file fixes

* Tue May 06 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.0-6
- added br mono-tools
- removed prepackaged mime

* Thu May 01 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.0-5.1
- attempt a fix for a text editor to work
- rebuild

* Wed Apr 30 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.0-4
- mdtool fix

* Wed Apr 30 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.0-3
- remove BR ikvm-devel

* Fri Apr 25 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.0-2
- add in gtksourceview2 support

* Mon Apr 21 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.0-1
- bump to release

* Mon Apr 21 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.19-7
- remove ppc specific stuff
- enabled gnomeplatform and c and c++ projects
- add BR monobasic
- remove the debug package

* Sat Apr 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.19-6
- disable Requires on ikvm, since ikvm doesn't build from source at the moment

* Fri Apr 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.19-5
- ExcludeArch ppc (no mono-nunit22, due to no nant, means no ppc)

* Fri Apr 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.19-4
- buildrequires mono-core for gacutil

* Fri Apr 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.19-3
- use system Mono.Cecil
- use copies of built from source nunit22 rather than bundling (upstream should really uncouple this)

* Thu Feb 21 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.19-2
- added BR update-desktop-database

* Thu Feb 21 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.19-1
- bump to preview 1

* Fri Jan 04 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.18.1-1
- bump

* Wed Dec 19 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.18-1
- fix for BR boo where boo is not supported
- bump to MD0.18

* Tue Nov 13 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.17-4
- added R mono-data-sqlite

* Sun Nov 11 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.17-3
- excludearch ppc64

* Sun Nov 11 2007 David Nielsen <david@lovesunix.net> - 0.17-2
- Remove support for Fedora < 5
- rediff config patch

* Thu Nov  8 2007 David Nielsen <david@lovesunix.net> - 0.17-1
- Update to MonoDevelop Beta 2

* Wed Oct 17 2007 David Nielsen <david@lovesunix.net> - 0.16
- Update to MonoDevelop Beta 1

* Sat Aug 11 2007 David Nielsen <david@lovesunix.net> - 0.15
- bump to 0.15

* Thu Mar 08 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.13.1-1
- bugfixes to the source

* Fri Feb 23 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.13-1
- bump to new version

* Wed Dec 20 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.12-9
- disables version control
- requires gnome-sharp
- enable nemerle added
- enabled aspnet and aspnetedit (rawhide only - requires jscall-sharp)
- added R firefox > 1.99

* Wed Nov 01 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.12-7
- Added R gtk-sharp2-gapi

* Fri Oct 27 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.12-6
- fixed url
- added R apr-devel

* Wed Sep 27 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.12-5
- pkgconfig fix 

* Mon Sep 25 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.12-4
- added R mono-nunit

* Mon Sep 18 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.12-3
- rebuild to make use of the new boo

* Thu Sep 07 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.12-2
- minor spec file fixes

* Wed Sep 06 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.12-1
- Bump to new version
- Include the patches for all users
- Fixed so it uses ?fedora (silly me!)
- Added BR mono-nunit-devel (FC6)

* Mon Sep 04 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-21
- Revert 64 bit clean for FC-5 and still follow FC guidelines

* Sun Sep 03 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-20
- Added gtk sharp fix
- Added conditional so it builds for FC5

* Sun Aug 27 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-17
- 64 bit goodness restored

* Fri Aug 04 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-16
- fixed ownership problem in spec file
- added comment about the libdir hack

* Wed Aug 02 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-15
- removed R which, added R mono-nunit
- changed R bytefx-data-mysq to msql
- altered update-mime-info and added update-desktop-database
- added R pkgconfig to devel
- added comment as to why smp_flags are not used on the build

* Sat Jul 29 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-14
- Added additional Rs
- minor specfile tweaks

* Sun Jul 23 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-12
- fixed which problem
- fixes the libdir issue for 64 bit

* Sun Jul 09 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-11
- minor spec files changes to satisfy rpmlint
- added BR ikvm-devel

* Sun Jul 09 2006 John Mahowald  <jpmahowald@gmail.com> - 0.11-10
- libdir fixes
- BR mono-data-sqlite

* Sun Jul 09 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-9
- removed noarch
- added a couple of patches from the new nant package
- fixes for new mono guidelines

* Wed Jun 14 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-8
- Removed libdir hack
- Added BR pkgconfig
- Added R monodoc
- Altered configure line to satisfy the parts required

* Mon Jun 05 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-7
- Added additional fix for 64 bit systems

* Sun Jun 04 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-6
- Minor mod to the BR
- Fixed the desktop-file-install problem

* Sat Jun 03 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-5
- Removed duplicate desktop file

* Sat Jun 03 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-4
- Removed R filesystem
- Simplified mime-applications
- Added scriptlets to handle mime info
- Corrected handling of desktop icon
- Removed INSTALL file

* Sat Jun 03 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-3
- Added BR shared-mime-info
- Added R filesystem
- Made all of the bindir and datadir ownerships explicit

* Wed May 31 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-2
- Added devel
- Added fix for 64 bit systems

* Sun May 07 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.11-1
- bump to new version
- added exclude archs for x86_64 and ia64 due to build problems

* Wed Apr 26 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.10-8
- removed smp_flags
- added boo and ikvm support

* Sun Apr 23 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.10-7
- removed static usrlib
- added export macros to fix the x86_64 problem
- disabled boo

* Wed Apr 19 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.10-6
- spec file version correctly bumped
- small spec file fixed
- enable-boo and enable-java added to the %%configure line

* Tue Apr 18 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.10-5
- libdir now usr-lib irrespective of hardware built on

* Mon Apr 17 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.10-4
- Altered install script somewhat
- Changed the path for the monodevelop libdir to be FE compliant
- Fixed source and URL

* Sat Apr 15 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.10-3
- Add in boo and mono-debugger
- fixed a couple of minor spec file bugs
- fixed MonoDevelop.Core not being found in the addins

* Wed Apr 5 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.10-2
- Additional buildreqs and two typo fixed - thanks to Angel Marin again

* Wed Apr 5 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.10-1
- Bump to new version
- mods to spec file for new version

* Wed Apr 5 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.9-3
- minor tweaks
- fixed a couple of typos - thanks to Angel Marin for spotting them

* Wed Jan 25 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.9-2
- added deps for ikvm and bytefx-data-mysql
- removed language support for the moment

* Mon Jan 23 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.9-1
- Initial import

