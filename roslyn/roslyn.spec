Name:           roslyn
Version:        1.3.0
Release:        1%{?dist}
Summary:        The .NET Compiler Platform ("Roslyn") provides open-source C# and Visual Basic compilers with rich code analysis APIs.

Group:          Development/Languages
License:        Apache 2.0
URL:            https://github.com/dotnet/roslyn
Source0:        https://github.com/dotnet/roslyn/archive/version-%{version}.tar.gz
Source1:        roslyn.build
BuildRequires:  nant
BuildRequires:  dotnet-corefx # for System.Collections.Immutable

%description
The .NET Compiler Platform ("Roslyn") provides open-source C# and Visual Basic compilers with rich code analysis APIs.

%prep
%setup -q -n %{name}-version-%{version}
cp %{SOURCE1} .

%build

# disable some visualbasic projects
sed -i 's#.*909B656F-6095-4AC2-A5AB-C3F032315C45.*##g' CrossPlatform.sln #VisualBasicErrorFactsGenerator.vbproj
sed -i 's#.*6AA96934-D6B7-4CC8-990D-DB6B9DD56E34.*##g' CrossPlatform.sln #VisualBasicSyntaxGenerator.vbproj

nant generateProjectFiles
xbuild CrossPlatform.sln
#error : PCL Reference Assemblies not installed

%install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
# TODO license or copyright

%changelog
* Mon Nov 21 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 1.0.0-1
- initial package
