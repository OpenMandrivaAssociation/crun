Name:		crun
Summary:	OCI Container Runtime fully written in C
Version:	0.13
Release:	1
Source0:	https://github.com/containers/crun/archive/%{version}/%{name}-%{version}.tar.gz
# Those are pulled in with "git submodule" in upstream git
Source1:	https://github.com/giuseppe/libocispec/archive/69a096a965ae47c5a83832b87e1d0a5178ca0b30.tar.gz
Source2:	https://github.com/opencontainers/image-spec/archive/79b036d80240ae530a8de15e1d21c7ab9292c693.tar.gz
Source3:	https://github.com/opencontainers/runtime-spec/archive/2086147713ebe64cd12681960914e81eadbbe1d9.tar.gz
Group:		Servers
License:	GPLv3+/LGPLv3+
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	make
BuildRequires:	pkgconfig(yajl)
BuildRequires:	pkgconfig(libseccomp)
BuildRequires:	pkgconfig(libselinux)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	gperf
# Let's turn crun into a drop-in replacement for runc
Obsoletes:	runc < 2:1.0.0-240
Provides:	runc = 2:1.0.0-240

%description
A fast and low-memory footprint OCI Container Runtime fully written in C.

crun conforms to the OCI Container Runtime specifications
(https://github.com/opencontainers/runtime-spec).

%prep
%autosetup -p1 -a 1
rmdir libocispec
mv libocispec-* libocispec
cd libocispec
rmdir image-spec runtime-spec
tar xf %{S:2}
tar xf %{S:3}
mv image-spec-* image-spec
mv runtime-spec-* runtime-spec
cd ..
autoreconf -fis
%configure
sed -i '/git-version.h/d' src/crun.c
sed -i -e 's,GIT_VERSION,"%{version}-%{release}",g' src/crun.c

%build
%make_build

%install
%make_install
# No point in shipping a static library if the headers
# aren't installed...
rm %{buildroot}%{_libdir}/*.a
ln -s crun %{buildroot}%{_bindir}/runc

%files
%{_bindir}/crun
%{_bindir}/runc
%{_mandir}/man1/crun.1*
