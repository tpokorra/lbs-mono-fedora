%global debug_package %{nil}
%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif

Name:           bareftp
Version:        0.3.9
Release:        9%{?dist}
Summary:        File transfer client supporting the FTP, FTP over SSL/TLS (FTPS) and SSH

Group:          Applications/Internet

#  <spot> cassmodiah: okay, so the code from SharpSSH and JSch is BSD, the Banshee
#  bits are MIT, the Classpath bits are GPLv2+ with exceptions
#  <spot> cassmodiah: if you combine all of that with GPLv2 only code, you end up
#  with GPLv2 with exceptions
#  <spot> cassmodiah: feel free to put that in comments above the License tag to
#  explain it. :)

License:        GPLv2 with exceptions
URL:            http://www.bareftp.org/
Source0:        http://www.bareftp.org/release/%{name}-%{version}.tar.gz

BuildRequires:  gnome-sharp-devel
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  perl(XML::Parser)
BuildRequires:  gnome-desktop-sharp-devel
BuildRequires:  gtk-sharp2-gapi
BuildRequires:  gtk-sharp2-devel
BuildRequires:  mono-devel
BuildRequires:  gnome-keyring-sharp-devel

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

ExclusiveArch: %{mono_arches}


%description
bareFTP is a file transfer client supporting the FTP, FTP over SSL/TLS (FTPS)
and SSH File Transfer Protocol (SFTP). It is written in C#, targeting the Mono
framework and the GNOME desktop environment. bareFTP is free and open source
software released under the terms of the GPL license.

%prep
%setup -q

# Fixes for build with Mono 4
sed -i "s#gmcs#mcs#g" configure
sed -i "s#gmcs#mcs#g" configure.ac
sed -i "s#mono/2.0#mono/4.5#g" configure

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"


for file in $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop
do
   desktop-file-validate $file
done

find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%postun
update-desktop-database &> /dev/null ||:

if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
        gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING CREDITS README
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/bareFTP.Common.Utils.dll
%{_libdir}/%{name}/bareFTP.Connection.dll
%{_libdir}/%{name}/bareFTP.Gui.Dialog.dll
%{_libdir}/%{name}/bareFTP.Gui.FileManager.dll
%{_libdir}/%{name}/bareFTP.Gui.Preferences.dll
%{_libdir}/%{name}/bareFTP.Gui.ProgressMonitor.dll
%{_libdir}/%{name}/bareFTP.Gui.dll
%{_libdir}/%{name}/bareFTP.Preferences.dll
%{_libdir}/%{name}/bareFTP.Protocol.Ftp.dll
%{_libdir}/%{name}/bareFTP.Protocol.Sftp.dll
%{_libdir}/%{name}/bareFTP.Protocol.dll
%{_libdir}/%{name}/bareFTP.SftpPty.dll
%{_libdir}/%{name}/libsftppty.so
%{_libdir}/%{name}/bareftp.exe
%{_bindir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/bareftp*

%changelog
* Tue May 12 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 0.3.9-9
- Build with mono 4
- Declare mono_arches for EPEL6

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 21 2011 Dan Horák <dan[at]danny.cz> - 0.3.9-2
- updated supported arch list

* Sat Sep 24 2011 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.3.9-1
- New release.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.3.7-1
- new version 0.3.7

* Wed Oct 27 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.3.6-1
- New version 0.3.6
- Build against mono-2.8

* Mon Apr 19 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.3.2-1
- New Version 0.3.2

* Mon Jan 25 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.3.1-1
- New Version 0.3.1

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 0.2.3-4
- Exclude sparc64 no mono available

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 27 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.2.3-2
- fix buildrequires

* Sat Jun 27 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.2.3-1
- new version 0.2.3

* Sat May 30 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.2.2-3
- enable ppc64 build

* Sat Apr 11 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.2.2-2
- fix from rhbz #495001 Comment #1 From  Simon Wesp (cassmodiah@fedoraproject.org)
- include ExclusiveArch, disable creation of debuginfo package

* Wed Apr 08 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.2.2-1
- Initial RPM release
