#
# spec file for PCL reference assemblies
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2014 Xamarin, Inc.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           referenceassemblies-pcl
Version:        2014.04.14
Release:        0
Url:            http://go-mono.org/
Source0:	http://download.mono-project.com/repo/debian/pool/main/r/%{name}/%{name}_%{version}.orig.tar.bz2
Source1:	EULA.rtf
Summary:        PCL reference assemblies for .NET
License:        EULA
Group:          Development/Libraries/Other
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
PCL Reference Assemblies are used for compiling code which
works on multiple .NET framework targets

%prep
%setup -c

%build
cp %{SOURCE1} .

%install
%{__mkdir_p} %{buildroot}%{_prefix}/lib/mono/xbuild-frameworks/.NETPortable/
cp -a */v4.0 %{buildroot}%{_prefix}/lib/mono/xbuild-frameworks/.NETPortable/
cp -a */v4.5 %{buildroot}%{_prefix}/lib/mono/xbuild-frameworks/.NETPortable/
cp -a */v4.6 %{buildroot}%{_prefix}/lib/mono/xbuild-frameworks/.NETPortable/

%files
%defattr(-, root, root)
%{_prefix}/lib/mono/xbuild-frameworks/.NETPortable
%doc EULA.rtf

%changelog

