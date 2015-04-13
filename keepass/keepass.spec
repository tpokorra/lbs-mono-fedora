Name:           keepass
Version:        2.27
Release:        1%{?dist}
Summary:        Password manager

License:        GPLv2+
URL:            http://keepass.info/

# Created with, e.g.:
# version=2.25 tmpdir=`mktemp -d` && cd $tmpdir && curl -LRO http://downloads.sourceforge.net/project/keepass/KeePass%202.x/$version/KeePass-$version-Source.zip && mkdir keepass-$version && unzip -d keepass-$version KeePass-$version-Source.zip && find keepass-$version -name "*dll" -delete && tar -cJf keepass-$version.tar.xz keepass-$version
Source0:        %{name}-%version.tar.xz

# Upstream does not include a .desktop file, etc..
Patch0:         keepass-desktop-integration.patch
Patch3:         keepass-appdata.patch

# Move XSL files to /usr/share/keepass:
Patch1:         keepass-fix-XSL-search-path.patch

# Locate locally-installed help files:
Patch2:         keepass-enable-local-help.patch

ExcludeArch:    armv7hl
BuildRequires:  mono-devel archmage desktop-file-utils python-devel
Requires:       xdotool xsel hicolor-icon-theme


# The debuginfo package would be empty if created.
%global debug_package %{nil}


%description
KeePass is a free open source password manager, which helps you to
remember your passwords in a secure way. You can put all your passwords in
one database, which is locked with one master key or a key file.  You
only have to remember one single master password or select the key file
to unlock the whole database.


%prep
%autosetup -p1


%build
( cd Build && sh PrepMonoDev.sh )
xbuild /target:KeePass /property:Configuration=Release
%{__python2} -c 'import archmod.CHM; archmod.CHM.CHMDir("Docs").process_templates("Docs/Chm")'


%install
install -d %{buildroot}/%{_prefix}/lib/%{name} %{buildroot}/%{_datadir}/%{name} %{buildroot}/%{_datadir}/%{name}/XSL %{buildroot}/%{_datadir}/applications %{buildroot}/%{_bindir} %{buildroot}/%{_datadir}/mime/packages %{buildroot}/%{_datadir}/icons/hicolor/256x256/apps %{buildroot}/%{_mandir}/man1 %{buildroot}/%{_docdir}/%{name} %{buildroot}/%{_datadir}/appdata
install -p -m 0644 Build/KeePass/Release/KeePass.exe Ext/KeePass.config.xml Ext/KeePass.exe.config %{buildroot}/%{_prefix}/lib/%{name}
install -p -m 0644 Ext/XSL/KDBX_DetailsFull.xsl Ext/XSL/KDBX_DetailsLite.xsl Ext/XSL/KDBX_PasswordsOnly.xsl Ext/XSL/KDBX_Styles.css Ext/XSL/KDBX_Tabular.xsl Ext/XSL/TableHeader.gif %{buildroot}/%{_datadir}/%{name}/XSL
install -p -m 0644 -T Ext/Icons/Finals/plockb.png %{buildroot}/%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
desktop-file-install --dir=%{buildroot}/%{_datadir}/applications dist/%{name}.desktop
install -p -m 0644 dist/%{name}.xml %{buildroot}/%{_datadir}/mime/packages
install -p -m 0644 dist/%{name}.1 %{buildroot}/%{_mandir}/man1
install -p -m 0644 dist/%{name}.appdata.xml %{buildroot}/%{_datadir}/appdata
install -p dist/%{name} %{buildroot}/%{_bindir}
sed 's/\r$//' Docs/History.txt > %{buildroot}/%{_docdir}/%{name}/History.txt
sed 's/\r$//' Docs/License.txt > %{buildroot}/%{_docdir}/%{name}/License.txt
cp -pr Docs/Chm %{buildroot}/%{_docdir}/%{name}/


%files
%dir %{_docdir}
%doc %{_docdir}/%{name}/History.txt
%doc %{_docdir}/%{name}/License.txt
%{_bindir}/%{name}
%{_prefix}/lib/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime
%{_datadir}/icons/hicolor/256x256/apps/keepass.png
%{_mandir}/man1/%{name}.1*
%{_datadir}/appdata/%{name}.appdata.xml


%post
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%package doc
Summary:        Documentation for the KeePass password manager
BuildArch: 	noarch

%description doc
Documentation for KeePass, a free open source password manager.

%files doc
%dir %{_docdir}
%doc %{_docdir}/%{name}/Chm/


%changelog
* Fri Jul 18 2014 Peter Oliver <rpm@mavit.org.uk> - 2.27-1
- Update to version 2.27.

* Fri Jul 18 2014 Peter Oliver <rpm@mavit.org.uk> - 2.26-10
- Add missing %u to Exec line in .desktop.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Peter Oliver <rpm@mavit.org.uk> - 2.26-7
- Mono crashes on ARM builders, so exclude that architecture.

* Thu May 22 2014 Peter Oliver <rpm@mavit.org.uk> - 2.26-6
- Depend on hicolor-icon-theme.
- The "%{__python2}" macro requires python-devel.

* Thu May 22 2014 Peter Oliver <rpm@mavit.org.uk> - 2.26-5
- Use "*" rather than ".gz" as the man page suffix, in case the
  compression format changes.
- Use "doc" rather than "-n %{name}-doc" in subpackages.
- Use "%{__python2}" macro.

* Sun May 18 2014 Peter Oliver <rpm@mavit.org.uk> - 2.26-4
- Install .desktop file via desktop-file-install.
- Don't recreate the build-root.
- Own documentation directory.
- Own icon and mime directories.
- Make the -doc subpackage noarch.
- Preserve timestamps when installing files.

* Sun Apr 20 2014 Peter Oliver <rpm@mavit.org.uk> - 2.26-3
- Reliable clipboard handling requires xsel.

* Sun Apr 20 2014 Peter Oliver <rpm@mavit.org.uk> - 2.26-2
- Build a documentation subpackage.
- For auto-type, xdotool is required.
- Include an AppData file.

* Fri Apr 18 2014 Peter Oliver <rpm@mavit.org.uk> - 2.26-1
- New package, based in part on the Debian package.
